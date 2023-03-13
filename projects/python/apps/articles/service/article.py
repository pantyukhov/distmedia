from io import UnsupportedOperation

import requests
from django.conf import settings

from apps.articles.dataclass.article import Article
from apps.libs.encryption.keys import encrypt


class ArticleService:

    def get_articles(self):
        return []
        # return self.bucket_client.(self.bucket_name)

    def upload_article(self, article: Article):
        data = encrypt(article.dumps(), settings.PUBLISHER_ENCRYPTION_CASE["public_key"])
        r = requests.post("http://localhost:9090/api/publish", json={
            'article': {
                "content": str(data),
            },
            "topic": '12321321',
        })
        # file_path = "/Users/pavelpantukhov/Desktop/Screenshot 2023-02-28 at 12.32.56.png"
        # upload_handle = OnchainUpload(self.chain_name, self.private_key, self.rpc_endpoint, self.api_key, self.access_token, file_path)
        # print(upload_handle)


article_service = ArticleService()
