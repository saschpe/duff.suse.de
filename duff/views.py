# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from duff.libvirt.models import Domain, Interface, Network


def index(request):
    domains = Domain.objects.all().prefetch_related("allocation_set")
    #interfaces = Interface.objects.all()
    networks = Network.objects.all()
    return render_to_response("virt/index.html", {"domains": domains, "networks": networks})
