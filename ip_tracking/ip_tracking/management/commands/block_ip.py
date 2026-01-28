from django.core.management.base import BaseCommand
from ip_tracking.models import BlockIP


class Command(BaseCommand):
    help = "Block an IP address."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str)

    def handle(self, *args, **options):
        ip_address = options['ip_address']

        obj, created = BlockIP.objects.get_or_create(
            ip_address=ip_address
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"IP {ip_address} has been blocked.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"IP {ip_address} is already blocked.")
            )
