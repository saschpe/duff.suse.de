# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models

#from duff.libvirt.models import Domain


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
    port = models.PositiveIntegerField()
    protocol = models.PositiveIntegerField(choices=PROTOCOL_CHOICES, default=HTTP)

    class Meta:
        ordering = ("port", "name")

    def __unicode__(self):
        return self.name


class Allocation(models.Model):
    """Many-to-many relation between domains (virtual machines) and services.
    """
    #domain = models.ForeignKey(Domain)
    service = models.ForeignKey(Service)
    running = models.BooleanField(default=False)

   #class Meta:
   #    ordering = ("domain", "service")

    def __unicode__(self):
        return self.port
