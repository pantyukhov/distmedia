from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]

