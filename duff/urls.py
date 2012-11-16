# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", "duff.views.index", name="index"),
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls)),
    #url(r"^iptables/", include("duff.iptables.urls"),
    url(r"^libvirt/", include("duff.libvirt.urls")),
    #url(r"^services/", include("duff.services.urls"),
)
