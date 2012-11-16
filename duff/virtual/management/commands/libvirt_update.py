from django.core.management.base import BaseCommand, CommandError

from ...models import Domain


class Command(BaseCommand):
    help="Update libvirt domains (virtual machines)"

    def handle(self, *args, **options):
        conn = libvirt.openReadOnly(hypervisor)
        Domain.objects.update_or_create_all_from_libvirt(conn)
        Network.objects.update_or_create_all_from_libvirt(conn)
        conn.close()
        Domain.objects.update_or_create_all_from_libvirt()
