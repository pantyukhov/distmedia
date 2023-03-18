from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Article publisher'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
