# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Allocation, Service


class AllocationAdmin(admin.ModelAdmin):
    list_display = ("domain", "service", "port", "state")
    list_filter = ("domain", "service", "state")
    search_fields = ("domain.name", "service.name", "port")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Service, ServiceAdmin)

