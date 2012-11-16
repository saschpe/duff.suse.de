# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Domain, Interface, Network


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


admin.site.register(Domain, DomainAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
