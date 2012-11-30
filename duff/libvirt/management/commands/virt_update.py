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
