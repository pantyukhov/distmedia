import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet

from apps.xrpl.dataclass.account import Account


class XrplService:
    def __init__(self):
        JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.client = JsonRpcClient(JSON_RPC_URL)

    def create_wallet(self) -> Account:
        wallet: xrpl.wallet.Wallet = generate_faucet_wallet(self.client, debug=True)

        return Account(wallet.public_key, wallet.private_key, wallet.classic_address)


xrpl_service = XrplService()
