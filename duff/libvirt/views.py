# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from models import Domain, Interface, Network


# def index(request):
#     domains = Domain.objects.all()
#     return render_to_response("index.html", {"domains": domains})
