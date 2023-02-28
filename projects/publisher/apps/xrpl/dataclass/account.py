from dataclasses import dataclass
from typing import Optional


@dataclass
class Account:
    public_key: Optional[str]
    private_key: Optional[str]
    classic_address: Optional[str]

