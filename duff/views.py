# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

#from duff.iptables.models import Chain, Rule, Table
from duff.libvirt.models import Domain, Interface, Network
#from duff.services.models import Allocation, Service


def index(request):
    domains = Domain.objects.all()
    networks = Network.objects.all()
    return render_to_response("index.html", {"domains": domains, "networks": networks})
