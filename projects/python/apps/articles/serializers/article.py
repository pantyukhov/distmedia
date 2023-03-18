from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.articles.dataclass.article import Article, PurchaseArticle
from apps.articles.service.article import article_service
from apps.xrpl.service.xrpl import xrpl_service


class ArticleSerializer(DataclassSerializer):
    class Meta:
        dataclass = Article

    def create(self, validated_data):
        return article_service.upload_article(validated_data)




class PurchaseArticle(DataclassSerializer):
    class Meta:
        dataclass = PurchaseArticle
