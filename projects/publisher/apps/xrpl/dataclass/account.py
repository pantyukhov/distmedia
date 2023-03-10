from dataclasses import dataclass
from typing import Optional

from xrpl.wallet import Wallet


@dataclass
class Account:
    public_key: Optional[str]
    private_key: Optional[str]
    classic_address: Optional[str]
    seed: Optional[str]

    def __init__(self, public_key=None, private_key=None, classic_address=None, seed=None):
        self.public_key = public_key
        self.private_key = private_key
        self.classic_address = classic_address
        self.seed = seed

    def get_wallet(self) -> Wallet:
        return Wallet(seed=self.seed, sequence=0)
