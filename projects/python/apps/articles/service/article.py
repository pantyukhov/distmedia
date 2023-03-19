from io import UnsupportedOperation

import requests
from django.conf import settings

from apps.articles.dataclass.article import Article
from apps.libs.encryption.keys import encrypt
from apps.xrpl.dataclass.account import Account
from apps.xrpl.service.xrpl import xrpl_service


class ArticleService:

    def get_articles(self, addresses):
        articles = []
        for address in addresses:
            nfts = xrpl_service.get_nfts(address)
            nfts.reverse()
            for nft in nfts:
                content =  xrpl_service.read_nft_content(nft)
                if content:
                    articles.append(content)



        return articles
        # return self.bucket_client.(self.bucket_name)


    def upload_article(self, account: Account, article: Article):
       xrpl_service.upload_content(account, article.dumps())
        # file_path = "/Users/pavelpantukhov/Desktop/Screenshot 2023-02-28 at 12.32.56.png"
        # upload_handle = OnchainUpload(self.chain_name, self.private_key, self.rpc_endpoint, self.api_key, self.access_token, file_path)
        # print(upload_handle)


article_service = ArticleService()
