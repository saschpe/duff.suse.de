from django.shortcuts import render_to_response

from duff.virtual.models import Domain


def index(request):
    domains = Domain.objects.all()
    return render_to_response("index.html", {"domains": domains})
