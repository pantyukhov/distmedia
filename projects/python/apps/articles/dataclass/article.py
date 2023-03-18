import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class PurchaseArticle:
    nft_id: Optional[str]

@dataclass
class Article:
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]

    def dumps(self):
        return json.dumps({
            "title": self.title,
            "description": self.description,
            "content": self.content
        })

