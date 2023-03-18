from django.core.management.base import BaseCommand

from apps.xrpl.service.superuser_xrpl import super_user_xrpl_service


class Command(BaseCommand):
    help = 'Listen xrp'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for message in super_user_xrpl_service.listen_new_transaction():
            print(message)
