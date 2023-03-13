from io import UnsupportedOperation

from django.conf import settings
from mcs import APIClient, BucketAPI, OnchainAPI
from mcs.upload.onchain_upload import OnchainUpload

from apps.articles.dataclass.article import Article


class ArticleService:
    def __init__(self, api_key=None, access_token=None, network=None, private_key=None, rpc_endpoint = None):
        self._mcs_api = None
        self._bucket_client = None
        self.bucket_name = "ARTICLES_BUCKET"
        self.api_key = api_key or settings.MCS_API_KEY
        self.access_token = access_token or settings.MCS_ACCESS_TOKEN
        self.chain_name = network or "polygon.mainnet"
        self.private_key = private_key or settings.ONCHIN_PRIVATE_KEY
        self.rpc_endpoint = rpc_endpoint or settings.ONCHIN_RPC_ENDPOINT


    @property
    def mcs_api(self) -> APIClient:
        if self._mcs_api is None:
            self._mcs_api = APIClient(self.api_key, self.access_token, self.chain_name)

        return self._mcs_api

    @property
    def bucket_client(self) -> BucketAPI:
        if self._bucket_client is None:
            self._bucket_client = BucketAPI(self.mcs_api)

        return self._bucket_client

    def get_articles(self):
        return []
        # return self.bucket_client.(self.bucket_name)

    def upload_article(self, article: Article):
        file_path = "/Users/pavelpantukhov/Desktop/Screenshot 2023-02-28 at 12.32.56.png"
        upload_handle = OnchainUpload(self.chain_name, self.private_key, self.rpc_endpoint, self.api_key, self.access_token, file_path)
        print(upload_handle)



article_service = ArticleService()
