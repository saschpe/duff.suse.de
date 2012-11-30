# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Allocation, Domain, Interface, Network, Service


class AllocationAdmin(admin.ModelAdmin):
    list_display = ("domain", "service", "running")
    list_filter = ("domain", "service", "running")
    search_fields = ("domain.name", "service.name")


class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "state", "max_memory", "memory", "vcpus", "cpu_time")
    list_filter = ("state", "vcpus")
    search_fields = ("name", "state")


class InterfaceAdmin(admin.ModelAdmin):
    list_display = ("domain", "network", "mac_address", "ip_address")
    list_filter = ("domain", "network")
    search_fields = ("domain.name", "network.name", "mac_address", "ip_address")


class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "bridge_name", "forward_mode", "domain_name", "active", "persistent") 
    list_filter = ("forward_mode", "domain_name", "active", "persistent")
    search_fields = ("name", "bridge_name", "domain_name")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "port", "protocol")
    list_filter = ("port", "protocol")
    search_fields = ("name", "description")


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Service, ServiceAdmin)
