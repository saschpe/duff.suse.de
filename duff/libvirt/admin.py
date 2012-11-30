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

from django.contrib import admin

from models import Allocation, Domain, Interface, Network, Service


class AllocationInline(admin.TabularInline):
    model = Allocation
    extra = 0


class InterfaceInline(admin.TabularInline):
    model = Interface
    extra = 0


class AllocationAdmin(admin.ModelAdmin):
    list_display = ("domain", "service", "running")
    list_filter = ("domain", "service", "running")
    search_fields = ("domain.name", "service.name")


class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "state", "max_memory", "memory", "vcpus", "cpu_time")
    list_filter = ("state", "vcpus")
    search_fields = ("name", "state")
    inlines = (AllocationInline, InterfaceInline)


class InterfaceAdmin(admin.ModelAdmin):
    list_display = ("domain", "network", "mac_address", "ip_address")
    list_filter = ("domain", "network")
    search_fields = ("domain.name", "network.name", "mac_address", "ip_address")


class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "bridge_name", "forward_mode", "domain_name", "active", "persistent") 
    list_filter = ("forward_mode", "domain_name", "active", "persistent")
    search_fields = ("name", "bridge_name", "domain_name")
    inlines = (InterfaceInline,)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "port", "protocol")
    list_filter = ("port", "protocol")
    search_fields = ("name", "description")
    inlines = (AllocationInline,)


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Service, ServiceAdmin)
