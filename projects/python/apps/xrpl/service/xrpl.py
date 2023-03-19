import json
from binascii import hexlify

import base58
import ipfsApi
import requests
import xrpl
from django.conf import settings
from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.models import AccountNFTs, NFTokenCreateOffer, NFTBuyOffers, NFTokenAcceptOffer, \
    NFTokenMint, NFTokenMintFlag, Subscribe, StreamParameter, Payment, NFTokenCreateOfferFlag, NFTSellOffers
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.utils import xrp_to_drops
from xrpl.wallet import generate_faucet_wallet, Wallet

from apps.libs.encryption.keys import generate_keys
from apps.xrpl.dataclass.account import Account
from apps.xrpl.service import REQUEST_SUBSCRIPTION_DROPS, USER_SUBSCRIPTION_DROPS
from apps.xrpl.service.superuser_xrpl import super_user_xrpl_service
from apps.xrpl.service.test import test_image


class XrplService:
    def __init__(self):
        self.JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.WEBSOCKET_URL = "wss://s.altnet.rippletest.net:51233"
        self.client = JsonRpcClient(self.JSON_RPC_URL)
        self.ipfs_url = f"http://{settings.IPFS_HOST}:{settings.IPFS_PORT}"
        self.ipfs_client = ipfsApi.Client(settings.IPFS_HOST, settings.IPFS_PORT)

    def create_wallet(self) -> Account:
        w: xrpl.wallet.Wallet = generate_faucet_wallet(self.client, debug=True)
        return Account(w.public_key, w.private_key, w.classic_address, w.seed)

    def get_superuser_address(self):
        return settings.WALLET_CREDS["classic_address"]

    def send_payment(self, account: Account, amount: int):
        issuerWallet = account.get_wallet()
        my_payment = Payment(
            account=issuerWallet.classic_address,
            amount=xrp_to_drops(amount),
            destination=self.get_superuser_address(),
        )

        print("Payment object:", my_payment)

        # Sign transaction -------------------------------------------------------------
        signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
            my_payment, account.get_wallet(), self.client)
        max_ledger = signed_tx.last_ledger_sequence
        tx_id = signed_tx.get_hash()
        print("Signed transaction:", signed_tx)
        print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_tx.fee), "XRP")
        print("Transaction expires after ledger:", max_ledger)
        print("Identifying hash:", tx_id)

        # Submit transaction -----------------------------------------------------------
        tx_response = xrpl.transaction.send_reliable_submission(signed_tx, self.client)
        return tx_response

        # # Wait for validation ----------------------------------------------------------
        # # send_reliable_submission() handles this automatically, but it can take 4-7s.
        #
        # # Check transaction results ----------------------------------------------------
        # import json
        # print(json.dumps(tx_response.result, indent=4, sort_keys=True))
        # print(f"Explorer link: https://testnet.xrpl.org/transactions/{tx_id}")
        # metadata = tx_response.result.get("meta", {})
        # if metadata.get("TransactionResult"):
        #     print("Result code:", metadata["TransactionResult"])
        # if metadata.get("delivered_amount"):
        #     print("XRP delivered:", xrpl.utils.drops_to_xrp(
        #         metadata["delivered_amount"]))

    def create_subscription(self, account: Account):
        issuerAddr = self.get_superuser_address()
        buyer_wallet = account.get_wallet()
        buyerAddr = buyer_wallet.classic_address
        get_account_nfts = AccountNFTs(
            account=self.get_superuser_address()
        )

        response = self.client.request(get_account_nfts)
        response = response.result['account_nfts'][0]

        nfTokeID = response['NFTokenID']
        buy_tx = NFTokenCreateOffer(
            account=buyerAddr,
            owner=issuerAddr,
            nftoken_id=nfTokeID,
            amount=str(USER_SUBSCRIPTION_DROPS),  # 10 XRP in drops, 1 XRP = 1,000,000 drops
        )

        # Sign buy_tx using the issuer account
        buy_tx_signed = safe_sign_and_autofill_transaction(transaction=buy_tx, wallet=buyer_wallet, client=self.client)
        buy_tx_signed = send_reliable_submission(transaction=buy_tx_signed, client=self.client)
        buy_tx_result = buy_tx_signed.result

        return {}
        #
        # return super_user_xrpl_service.accept_nft(issuerAddr, response['NFTokenID'])

    def get_subscriptions(self, account: Account):
        issuerAddr = account.get_wallet().classic_address
        get_account_nfts = self.client.request(AccountNFTs(account=issuerAddr, limit=100))
        return get_account_nfts.result['account_nfts']

    def read_nft_content(self, nft):
        uri = nft.get('URI')
        if uri:
            uri = bytes.fromhex(nft.get("URI")).decode('utf-8')
            h = uri.split("//")[1]

            import requests

            params = {
                'arg': h,
            }

            response = requests.post(f'{self.ipfs_url}/api/v0/get', params=params, timeout=10)
            if response.status_code != 200:
                return None
            try:
                text = response.text[response.text.index("{"):response.text.rindex("}") + 1]

                data = json.loads(text)
            except:
                return None

            # data = {
            #     "title": "Test",
            #     "description": "Test",
            #     "content": test_image,
            # }
            data["hash"] = h
            data["token"] = nft

            return data

        return None

    def get_nfts(self, address):
        get_account_nfts = AccountNFTs(
            account=address
        )

        response = self.client.request(get_account_nfts)
        response = response.result['account_nfts']
        return response

    def purchase_article(self, account: Account, original_nft_id):
        # Get issuer wallet and address
        issuer_wallet = super_user_xrpl_service.get_superuser_waller()
        issuerAddr = issuer_wallet.classic_address

        # Put original nft_id on ipfs
        ipfs_address = self.ipfs_client.add_str(json.dumps({
            "original_nft_id": original_nft_id
        }))
        uri = xrpl.utils.str_to_hex(f"ipfs://{ipfs_address}")

        # mint
        mint_tx = NFTokenMint(
            account=issuerAddr,
            nftoken_taxon=1,
            flags=NFTokenMintFlag.TF_TRANSFERABLE,
            uri=uri,
        )

        # Sign mint_tx using the issuer account
        mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet,
                                                            client=xrpl_service.client)
        mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=xrpl_service.client)
        mint_tx_result = mint_tx_signed.result
        if not mint_tx_result:
            raise Exception("NFT not mint")

        buyer_wallet = account.get_wallet()
        buyerAddr = buyer_wallet.classic_address

        response = [x for x in self.get_nfts(issuer_wallet.classic_address) if
                    x.get("URI", "") == mint_tx_signed.result.get("URI") and x.get(
                        'Issuer') == issuer_wallet.classic_address][0]

        nfTokeID = response['NFTokenID']
        buy_tx = NFTokenCreateOffer(
            account=buyerAddr,
            owner=issuerAddr,
            nftoken_id=nfTokeID,
            amount=str(1000),  # 10 XRP in drops, 1 XRP = 1,000,000 drops
        )

        # Sign buy_tx using the issuer account
        buy_tx_signed = safe_sign_and_autofill_transaction(transaction=buy_tx, wallet=buyer_wallet, client=self.client)
        buy_tx_signed = send_reliable_submission(transaction=buy_tx_signed, client=self.client)
        buy_tx_result = buy_tx_signed.result



        # accept offer

        # Query buy offers for the NFT
        response_offers = self.client.request(
            NFTBuyOffers(nft_id=response['NFTokenID'])
        )
        first_offer_object = response_offers.result["offers"][0]

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



        # print(nft_id)
        return accept_sell_offer_tx_result

    def upload_content(self, account: Account, content):
        ipfs_address = self.ipfs_client.add_str(content)
        issuer_wallet = account.get_wallet()

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

        return mint_tx_result


xrpl_service = XrplService()
