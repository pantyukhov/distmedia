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
from apps.xrpl.service import REQUEST_SUBSCRIPTION_DROPS, USER_SUBSCRIPTION_DROPS
from apps.xrpl.service.superuser_xrpl import super_user_xrpl_service


class XrplService:
    def __init__(self):
        self.JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.WEBSOCKET_URL = "wss://s.altnet.rippletest.net:51233"
        self.client = JsonRpcClient(self.JSON_RPC_URL)
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

        return super_user_xrpl_service.accept_nft(issuerAddr, response['NFTokenID'])

    def get_subscriptions(self, account: Account):
        issuerAddr = account.get_wallet().classic_address
        get_account_nfts = self.client.request(AccountNFTs(account=issuerAddr))
        return get_account_nfts.result['account_nfts']


xrpl_service = XrplService()
