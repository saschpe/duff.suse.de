from django.contrib import admin

from models import Allocation, Domain, Service


class AllocationAdmin(admin.ModelAdmin):
    list_display = ("domain", "service", "port", "state")
    list_filter = ("domain", "service", "state")
    search_fields = ("domain.name", "service.name", "port")


class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "state", "max_memory", "memory", "vcpus", "cpu_time")
    list_filter = ("state", "vcpus")
    search_fields = ("name", "state")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Service, ServiceAdmin)
