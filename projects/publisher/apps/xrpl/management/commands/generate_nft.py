import base64
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from xrpl.models import NFTokenMint, NFTokenMintFlag, AccountNFTs
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission

from apps.xrpl.service.xrpl import xrpl_service


class Command(BaseCommand):
    help = 'Generate nft'

    def add_arguments(self, parser):
        parser.add_argument('total_nfts', type=int)
        parser.add_argument('account_base64_data', type=str)

    def handle(self, total_nfts, *args, **options):

        xrpl_service.generate_subscriptions(total_nfts)
