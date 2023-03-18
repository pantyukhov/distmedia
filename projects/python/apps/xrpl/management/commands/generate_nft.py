from django.core.management.base import BaseCommand

from apps.xrpl.service.superuser_xrpl import super_user_xrpl_service
from apps.xrpl.service.xrpl import xrpl_service


class Command(BaseCommand):
    help = 'Generate nft'

    def add_arguments(self, parser):
        parser.add_argument('total_nfts', type=int)

    def handle(self, total_nfts, *args, **options):
        for i in range(0, total_nfts):
            super_user_xrpl_service.generate_subscriptions()
