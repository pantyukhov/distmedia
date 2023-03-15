import json
from binascii import hexlify

import ipfsApi
import xrpl
from django.conf import settings
from xrpl.clients import JsonRpcClient
from xrpl.models import AccountNFTs, NFTokenCreateOffer, NFTBuyOffers, NFTokenAcceptOffer, \
    NFTokenMint, NFTokenMintFlag
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.wallet import generate_faucet_wallet, Wallet

from apps.libs.encryption.keys import generate_keys
from apps.xrpl.dataclass.account import Account


class XrplService:
    def __init__(self):
        JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.client = JsonRpcClient(JSON_RPC_URL)
        self.ipfs_client = ipfsApi.Client(settings.IPFS_HOST, settings.IPFS_PORT)

    def create_wallet(self) -> Account:
        w: xrpl.wallet.Wallet = generate_faucet_wallet(self.client, debug=True)
        return Account(w.public_key, w.private_key, w.classic_address, w.seed)

    def get_superuser_waller(self) -> Wallet:
        seed = settings.WALLET_CREDS["seed"]
        return Wallet(seed=seed, sequence=0)

    def generate_subscriptions(self, public_key):
        issuer_wallet = self.get_superuser_waller()

        print(f"\nIssuer Account: {issuer_wallet.classic_address}")

        ipfs_address = self.ipfs_client.add_str(json.dumps({
            "public_key": public_key,
        }))

        uri = xrpl.utils.str_to_hex(f"ipfs://{ipfs_address}")
        mint_tx = NFTokenMint(
            account=issuer_wallet.classic_address,
            nftoken_taxon=1,
            flags=NFTokenMintFlag.TF_TRANSFERABLE,
            uri=uri,
        )

        # Sign mint_tx using the issuer account
        mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet,
                                                            client=xrpl_service.client)
        mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=xrpl_service.client)
        mint_tx_result = mint_tx_signed.result

        print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
        print(f"     Tx response: {mint_tx_result}")

        for node in mint_tx_result['meta']['AffectedNodes']:
            if "CreatedNode" in list(node.keys())[0]:
                print(f"\n - NFT metadata:"
                      f"\n        NFT ID: {node['CreatedNode']['NewFields']['NFTokens'][0]['NFToken']['NFTokenID']}"
                      f"\n  Raw metadata: {node}")

    def get_subscriptions(self, account: Account):
        issuerAddr = account.get_wallet().classic_address
        get_account_nfts = self.client.request(AccountNFTs(account=issuerAddr))
        return get_account_nfts.result['account_nfts']

    def create_subscription(self, account: Account, public_key: str, amount: int = 10000000):

        self.generate_subscriptions(public_key)
        issuer_wallet = self.get_superuser_waller()

        issuerAddr = issuer_wallet.classic_address

        buyer_wallet = account.get_wallet()
        buyerAddr = buyer_wallet.classic_address

        get_account_nfts = AccountNFTs(
            account=issuerAddr
        )

        response = self.client.request(get_account_nfts)
        response = response.result['account_nfts'][0]

        # Put up a buy offer for the NFT on the open market
        buy_offer_amount = str(amount)
        print(f"Buying NFT {response['NFTokenID']} for {int(buy_offer_amount) / 1000000} XRP ")
        buy_tx = NFTokenCreateOffer(
            account=buyerAddr,
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


xrpl_service = XrplService()
