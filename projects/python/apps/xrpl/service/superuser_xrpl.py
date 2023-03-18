import json
from binascii import hexlify

import ipfsApi
import xrpl
from django.conf import settings
from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.models import AccountNFTs, NFTokenCreateOffer, NFTBuyOffers, NFTokenAcceptOffer, \
    NFTokenMint, NFTokenMintFlag, Subscribe, StreamParameter, Payment
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.utils import xrp_to_drops
from xrpl.wallet import generate_faucet_wallet, Wallet

from apps.libs.encryption.keys import generate_keys
from apps.xrpl.dataclass.account import Account


class SuperUserXrplService:
    def __init__(self):
        self.JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.WEBSOCKET_URL = "wss://s.altnet.rippletest.net:51233"
        self.client = JsonRpcClient(self.JSON_RPC_URL)
        self.ipfs_client = ipfsApi.Client(settings.IPFS_HOST, settings.IPFS_PORT)

    def get_superuser_waller(self) -> Wallet:
        seed = settings.WALLET_CREDS["seed"]
        return Wallet(seed=seed, sequence=0)

    def get_superuser_address(self):
        return settings.WALLET_CREDS["classic_address"]

    def process_token_offer(self, message):
        owner_address = self.get_superuser_address()
        if message.get("transaction", {}).get("Owner") == owner_address:
            print(message)

    def listen_nft_offers(self):
        account = self.get_superuser_waller()
        response = self.client.request(
            AccountNFTs(account=self.get_superuser_address())
        )

        if response.status[0:7] == "success":
            nft_list = response.result['account_nfts']

            # Only append the NFTs' NFT ID onto the nft_keylets list, other fields aren't needed
            nft_keylets = []
            for x in nft_list:
                nft_keylets.append(x['NFTokenID'])

            # Query through the NFTs' buy Offers
            # For each NFT owned by the account (on nft_keylets), go through all their respective buy Offerss
            for nft in nft_keylets:
                response = self.client.request(
                    NFTBuyOffers(
                        nft_id=nft
                    )
                )

                offer_objects = response.result
                if 'error' not in offer_objects:
                    for offer_object in offer_objects.get("offers"):
                        self.accept_nft(offer_object)
                        print(f"\n Offer {offer_object['nft_offer_index']} was accepted")
                else:
                    print(f"\nNFT {nft} does not have any buy offers...")

        else:
            print(f"Account {account} does not own any NFTs!")
        # issuer_wallet = self.get_superuser_waller()
        # response = self.client.request(
        #     AccountNFTs(account=issuer_wallet)
        # )

    def listen_new_transaction(self):
        issuer_wallet = self.get_superuser_waller()
        req = Subscribe(streams=[StreamParameter.TRANSACTIONS], accounts=[self.get_superuser_address()])
        with WebsocketClient(self.WEBSOCKET_URL) as client:
            client.send(req)
            # inside the context the client is open
            for message in client:
                print(message)
                if message.get("engine_result") == "tecUNFUNDED_OFFER":
                    self.process_token_offer(message)

                # if message.get("transaction", {}).get("Destination", "") == issuer_wallet.classic_address:
                #     yield message

    def accept_nft(self, offer):
        accept_sell_offer_tx = NFTokenAcceptOffer(
            account=offer["owner"],
            nftoken_buy_offer=offer["nft_offer_index"]
        )
        accept_sell_offer_tx_signed = safe_sign_and_autofill_transaction(transaction=accept_sell_offer_tx,
                                                                         wallet=self.get_superuser_waller(),
                                                                         client=self.client)
        accept_sell_offer_tx_signed = send_reliable_submission(transaction=accept_sell_offer_tx_signed,
                                                               client=self.client)
        accept_sell_offer_tx_result = accept_sell_offer_tx_signed.result

        return accept_sell_offer_tx_result

    def generate_subscriptions(self):
        issuer_wallet = self.get_superuser_waller()

        print(f"\nIssuer Account: {issuer_wallet.classic_address}")

        # ipfs_address = self.ipfs_client.add_str(json.dumps({
        #     "public_key": public_key,
        # }))

        # uri = xrpl.utils.str_to_hex(f"ipfs://{ipfs_address}")
        mint_tx = NFTokenMint(
            account=issuer_wallet.classic_address,
            nftoken_taxon=1,
            flags=NFTokenMintFlag.TF_TRANSFERABLE,
            # uri=uri,
        )

        # Sign mint_tx using the issuer account
        mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet,
                                                            client=self.client)
        mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=self.client)
        mint_tx_result = mint_tx_signed.result

        print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
        print(f"     Tx response: {mint_tx_result}")

    # def send_payment

    def create_subscription(self, buyer_addr: str, amount: int = 10000000):

        # self.generate_subscriptions(public_key)
        issuer_wallet = self.get_superuser_waller()

        issuerAddr = issuer_wallet.classic_address

        get_account_nfts = AccountNFTs(
            account=issuerAddr
        )

        response = self.client.request(get_account_nfts)
        response = response.result['account_nfts'][0]

        # Put up a buy offer for the NFT on the open market
        buy_offer_amount = str(amount)
        print(f"Buying NFT {response['NFTokenID']} for {int(buy_offer_amount) / 1000000} XRP ")
        buy_tx = NFTokenCreateOffer(
            account=buyer_addr,
            owner=issuerAddr,
            nftoken_id=response['NFTokenID'],
            amount=buy_offer_amount,  # 10 XRP in drops, 1 XRP = 1,000,000 drops
        )

        # Sign buy_tx using the issuer account
        buy_tx_signed = safe_sign_and_autofill_transaction(transaction=buy_tx, wallet=buyer_wallet, client=self.client)
        buy_tx_signed = send_reliable_submission(transaction=buy_tx_signed, client=self.client)
        buy_tx_result = buy_tx_signed.result

        print(f"\n  NFTokenCreateOffer tx result: {buy_tx_result['meta']['TransactionResult']}")
        print(f"                   Tx response: {buy_tx_result}")

        # Index through the tx's metadata and check the changes that occurred on the ledger (AffectedNodes)
        for node in buy_tx_result['meta']['AffectedNodes']:
            if "CreatedNode" in list(node.keys())[0] and "NFTokenOffer" in node['CreatedNode']['LedgerEntryType']:
                print(f"\n - Buy Offer metadata:"
                      f"\n        NFT ID: {node['CreatedNode']['NewFields']['NFTokenID']}"
                      f"\n Sell Offer ID: {node['CreatedNode']['LedgerIndex']}"
                      f"\n  Offer amount: {node['CreatedNode']['NewFields']['Amount']} drops"
                      f"\n   Offer owner: {node['CreatedNode']['NewFields']['Owner']}"
                      f"\n  Raw metadata: {node}")

        # Query buy offers for the NFT
        response_offers = self.client.request(
            NFTBuyOffers(nft_id=response['NFTokenID'])
        )

        offer_objects = response_offers.result
        first_offer_object = offer_objects['offers'][0]

        offer_int = 1
        print(f"\n - Existing Buy Offers for NFT {response['NFTokenID']}:")
        for offer in offer_objects['offers']:
            print(f"\n{offer_int}. Buy Offer metadata:"
                  f"\n        NFT ID: {offer_objects['nft_id']}"
                  f"\n Sell Offer ID: {offer['nft_offer_index']}"
                  f"\n  Offer amount: {offer['amount']} drops"
                  f"\n   Offer owner: {offer['owner']}"
                  f"\n  Raw metadata: {offer}")
            offer_int += 1

        accept_sell_offer_tx = NFTokenAcceptOffer(
            account=issuerAddr,
            nftoken_buy_offer=first_offer_object["nft_offer_index"]
        )

        accept_sell_offer_tx_signed = safe_sign_and_autofill_transaction(transaction=accept_sell_offer_tx,
                                                                         wallet=issuer_wallet,
                                                                         client=self.client)
        accept_sell_offer_tx_signed = send_reliable_submission(transaction=accept_sell_offer_tx_signed,
                                                               client=self.client)
        accept_sell_offer_tx_result = accept_sell_offer_tx_signed.result

        return accept_sell_offer_tx_result


super_user_xrpl_service = SuperUserXrplService()
