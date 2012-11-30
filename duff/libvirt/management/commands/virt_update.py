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

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
import libvirt

from ...models import Domain, Network


class Command(BaseCommand):
    args="<connection_uri>"
    help="Update libvirt domains (virtual machines)"

    def handle(self, *args, **options):
        if len(args) is 1:
            uri = args[0]
        else:
            uri = "qemu:///system"

        conn = libvirt.openReadOnly(uri)
        Domain.objects.update_or_create_all_from_libvirt(conn)
        Network.objects.update_or_create_all_from_libvirt(conn)
        conn.close()
