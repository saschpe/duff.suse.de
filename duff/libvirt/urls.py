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

from django.conf.urls import patterns, include, url


urlpatterns = patterns("duff.libvirt.views",
    url(r"^$", "index", name="index"),
    #url(r"^domains/$", "domain_index", name="domain-index"),
    #url(r"^domains/(?P<name>\w+)/$", "domain_show", name="domain-show"),
)
