import logging

import libvirt

from django.core.exceptions import ValidationError
from django.db import models


class Service(models.Model):
    """User-visible (web) service.
    """
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name


class DomainManager(models.Manager):
    """Custom libvirt domain model manager.
    """
    def create_from_domain_info(self, domain_name, domain_info, domain_id=None):
        domain = Domain(name=domain_name)
        domain.update(domain_info, domain_id)
        return domain

    def update_or_create_from_domain_info(self, domain_name, domain_info, domain_id=None):
        try:
            domain = Domain.objects.get(name=domain_name)
            domain.update(domain_info, domain_id)
        except Domain.DoesNotExist:
            domain = self.create_from_domain_info(domain_name, domain_info, domain_id)
        return domain

    def update_or_create_all_from_libvirt(self, hypervisor="qemu:///system"):
        conn = libvirt.open(hypervisor)

        # Iterate over active domains:
        for domain_id in conn.listDomainsID():
            domain = conn.lookupByID(domain_id)
            domain_info = domain.info()
            self.update_or_create_from_domain_info(domain.name(), domain_info, domain_id=domain_id)

        # Iterate over defined domains:
        for domain_name in conn.listDefinedDomains():
            domain = conn.lookupByName(domain_name)
            domain_info = domain.info()
            self.update_or_create_from_domain_info(domain_name, domain_info)

        conn.close()


class Domain(models.Model):
    """Libvirt-managed domain (virtual machine).
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
    vcpus = models.PositiveIntegerField(default=1, verbose_name="Virtual CPUs", help_text="Should not exceed physical CPUs")
    cpu_time = models.BigIntegerField(default=0, verbose_name="CPU time")
    #ip_address = models.IPAddressField(blank=True, null=True)
    services = models.ManyToManyField(Service, through="Allocation")

    objects = DomainManager()

    class Meta:
        ordering = ("id", "name",)

    def clean(self):
        if self.memory > self.max_memory:
            raise ValidationError("Domain memory must be not be greater than max_memory.")
        if self.cpu_time < 0:
            raise ValidationError("Negative CPU time is not possible!")

    def update(self, domain_info, domain_id=None, save=True):
        if domain_id:
            self.id = domain_id
        self.state = domain_info[0]
        self.max_memory = domain_info[1]
        self.memory = domain_info[2]
        self.vcpus = domain_info[3]
        self.cpu_time = domain_info[4]
        #logging.debug("Update", domain_info, domain_id)
        if save:
            self.save()

    def __unicode__(self):
        return self.name


class Allocation(models.Model):
    """Many-to-many relation between domains (virtual machines) and services.
    """
    OFFLINE = 0
    ONLINE = 1

    STATE_CHOICES = (
        (OFFLINE, "Offline"),
        (ONLINE, "Online"),
    )

    domain = models.ForeignKey(Domain)
    service = models.ForeignKey(Service)
    port = models.PositiveIntegerField(primary_key=True)
    state = models.CharField(choices=STATE_CHOICES, default=OFFLINE, max_length=16)

    class Meta:
        ordering = ("port",)

    def __unicode__(self):
        return self.port
