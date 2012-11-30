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

from django.shortcuts import render_to_response

from duff.libvirt.models import Domain, Network


def index(request):
    domains = Domain.objects.all().prefetch_related("allocation_set")
    networks = Network.objects.all()
    return render_to_response("virt/index.html", {"domains": domains, "networks": networks})
