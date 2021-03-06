# Copyright 2012 Sascha Peilicke <saschpe@gmx.de>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import re
import socket
import subprocess
import urllib2

from django.core.exceptions import ValidationError
from django.db import models
from lxml import etree


class DomainManager(models.Manager):
    """Custom Domain model manager.
    """
    def create_from_vir_domain(self, vir_domain):
        domain = Domain()
        domain.update(vir_domain)
        if domain.state is Domain.RUNNING:
            Interface.objects.update_all_for_domain_from_vir_domain(domain, vir_domain)
            Allocation.objects.update_all_from_domain(domain)
        return domain

    def update_or_create_from_vir_domain(self, vir_domain):
        try:
            domain = Domain.objects.get(name=vir_domain.name())
            domain.update(vir_domain)
            if domain.state is Domain.RUNNING:
                Interface.objects.update_all_for_domain_from_vir_domain(domain, vir_domain)
                Allocation.objects.update_all_from_domain(domain)
        except Domain.DoesNotExist:
            domain = self.create_from_vir_domain(vir_domain)
        return domain

    def update_or_create_all_from_libvirt(self, libvirt_connection):
        # Iterate over active domains:
        for domain_id in libvirt_connection.listDomainsID():
            vir_domain = libvirt_connection.lookupByID(domain_id)
            self.update_or_create_from_vir_domain(vir_domain)
        # Iterate over defined domains:
        for domain_name in libvirt_connection.listDefinedDomains():
            vir_domain = libvirt_connection.lookupByName(domain_name)
            self.update_or_create_from_vir_domain(vir_domain)


class Domain(models.Model):
    """Virtual machine (libvirt domain).
    """
    NOSTATE = 0 
    RUNNING = 1
    BLOCKED = 2
    PAUSED = 3
    SHUTDOWN = 4
    SHUTOFF = 5
    CRASHED = 6
    PMSUSPENDED = 7

    STATE_CHOICES = (
        (NOSTATE, "No State"),
        (RUNNING, "Running"),
        (BLOCKED, "Blocked"),
        (PAUSED, "Paused"),
        (SHUTDOWN, "Shut Down"),
        (SHUTOFF, "Shut Off"),
        (CRASHED, "Crahed"),
        (PMSUSPENDED, "PM Suspended"),
    )

    name = models.CharField(max_length=64, primary_key=True)
    id = models.PositiveIntegerField(null=True, unique=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=NOSTATE)
    max_memory = models.PositiveIntegerField(default=2097152)
    memory = models.PositiveIntegerField(default=2097152)
    vcpus = models.PositiveIntegerField(default=1, verbose_name="virtual CPUs", help_text="Should not exceed physical CPUs")
    cpu_time = models.BigIntegerField(default=0, verbose_name="CPU time")
    network_set = models.ManyToManyField("Network", through="Interface")
    service_set = models.ManyToManyField("Service", through="Allocation")

    objects = DomainManager()

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.memory > self.max_memory:
            raise ValidationError("Domain memory must be not be greater than max_memory.")
        if self.cpu_time < 0:
            raise ValidationError("Negative CPU time is not possible!")

    def update(self, vir_domain, save=True):
        self.name = vir_domain.name()
        if vir_domain.ID() is not -1:
            self.id = vir_domain.ID()
        else:
            self.id = None
        domain_info = vir_domain.info()
        self.state = domain_info[0]
        self.max_memory = domain_info[1]
        self.memory = domain_info[2]
        self.vcpus = domain_info[3]
        self.cpu_time = domain_info[4]
        if save:
            self.save()


class InterfaceManager(models.Manager):
    """Custom Interface model manager.
    """
    def update_all_for_domain_from_vir_domain(self, domain, vir_domain):
        # Parse network interfaces from XML description
        domain.interface_set.all().delete()
        xml = etree.fromstring(vir_domain.XMLDesc(0))
        for xml_if in xml.findall("devices/interface[@type='network']"):
            mac_address = xml_if.find("mac").attrib["address"].lower().strip()
            network_name = xml_if.find("source").attrib["network"].lower().strip()
            # Make sure there's a suitable Network instance available:
            network = Network.objects.get_or_create(name=network_name)[0]

            # libvirt provides no means to lookup domain ip addresses, thus:
            # Check /etc/hosts:
            ip_address = None
            try:
                ping_output = subprocess.check_output(["ping", "-c1", domain.name])
                try:
                    ip_address = re.search("\(((\d+\.){3}\d+)\)", ping_output).groups()[0]
                except AttributeError:
                    pass
            except subprocess.CalledProcessError: 
                # Try arp cache:
                arp_output = subprocess.check_output(["arp", "-n"])
                for line in arp_output.split("\n")[1:]:
                    try:
                        ip, mac = re.match("([\d\.]+)\s+\w+\s+([\d:]+)", line).groups()
                        if mac is mac_address:
                            ip_address = ip # Found it!
                            break
                    except AttributeError:
                        pass
            Interface.objects.create(domain=domain, network=network,
                                     mac_address=mac_address, ip_address=ip_address)


class Interface(models.Model):
    """Network interface, also a many-to-many relation between domains and networks.
    """
    domain = models.ForeignKey("Domain")
    network = models.ForeignKey("Network")
    mac_address = models.CharField(max_length=17, verbose_name="MAC Address")
    ip_address = models.IPAddressField(blank=True, null=True, verbose_name="IP Address")

    objects = InterfaceManager()

    class Meta:
      ordering = ("domain", "mac_address")

    def __unicode__(self):
        return self.mac_address


class NetworkManager(models.Manager):
    """Custom Network model manager.
    """
    def create_from_vir_network(self, vir_network):
        network = Network()
        network.update(vir_network)
        return network

    def update_or_create_from_vir_network(self, vir_network):
        try:
            network = Network.objects.get(name=vir_network.name())
            network.update(vir_network)
        except Network.DoesNotExist:
            network = self.create_from_vir_network(vir_network)
        return network

    def update_or_create_all_from_libvirt(self, libvirt_connection):
        # Iterate over active networks:
        for network_name in libvirt_connection.listNetworks():
            vir_network = libvirt_connection.networkLookupByName(network_name)
            self.update_or_create_from_vir_network(vir_network)
        # Iterate over defined networks:
        for network_name in libvirt_connection.listDefinedNetworks():
            vir_network = libvirt_connection.networkLookupByName(network_name)
            self.update_or_create_from_vir_network(vir_network)


class Network(models.Model):
    """Virtual network.
    """
    name = models.CharField(max_length=32, primary_key=True)
    bridge_name = models.CharField(default="virbr0", max_length=16)
    forward_mode = models.CharField(default="nat", max_length=32)
    domain_name = models.CharField(max_length=256)
    active = models.BooleanField(default=False)
    persistent = models.BooleanField(default=False)

    objects = NetworkManager()

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    def update(self, vir_network, save=True):
        self.name = vir_network.name()
        self.bridge_name = vir_network.bridgeName()
        xml = etree.fromstring(vir_network.XMLDesc(0))
        if xml.find("forward") is not None:
            self.forward_mode = xml.find("forward").attrib["mode"]
        else:
            self.forward_mode = ""
        if xml.find("domain") is not None:  # <domain name=""> is optional
            self.domain_name = xml.find("domain").attrib["name"]
        else:
            self.domain_name = ""
        self.active = vir_network.isActive()
        self.persistent = vir_network.isPersistent()
        if save:
            self.save()
        

class Service(models.Model):
    """Web service provided by virtual machine (libvirt domain).
    """
    HTTP = 0
    HTTPS = 1

    PROTOCOL_CHOICES = (
        (HTTP, "HTTP"),
        (HTTPS, "HTTPS"),
      )

    name = models.CharField(max_length=128)
    description = models.TextField()
    port = models.PositiveIntegerField(verbose_name="Default Port")
    protocol = models.PositiveIntegerField(choices=PROTOCOL_CHOICES, default=HTTP)

    class Meta:
        ordering = ("port", "name")

    def __unicode__(self):
        return self.name


class AllocationManager(models.Manager):
    """Custom Allocation model manager.
    """
    def update_all_from_domain(self, domain):
        for allocation in domain.allocation_set.all():
            allocation.update()


class Allocation(models.Model):
    """Many-to-many relation between domains (virtual machines) and services.
    """
    domain = models.ForeignKey(Domain)
    service = models.ForeignKey(Service)
    running = models.BooleanField(default=False)

    objects = AllocationManager()

    class Meta:
        ordering = ("domain", "service")

    def __unicode__(self):
        return u"{0} {1}".format(self.domain, self.service)

    def url(self):
        protocol = self.service.get_protocol_display().lower()
        ip_address = self.domain.interface_set.all()[0].ip_address
        return u"{0}://{1}:{2}/".format(protocol,
                                        ip_address,
                                        self.service.port)

    def external_url(self):
        protocol = self.service.get_protocol_display().lower()
        #TODO: Parse iptables and find out host port forwarding
        forwarding_port = 8080
        return u"{0}://{1}:{2}/".format(protocol, socket.getfqdn(), forwarding_port)

    def update(self, save=True):
        try:
            response = urllib2.urlopen(self.url())
            self.running = response.getcode() is 200
        except (urllib2.HTTPError, urllib2.URLError):
            self.running = False
        if save:
            self.save()
