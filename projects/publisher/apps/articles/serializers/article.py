from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.articles.dataclass.article import Article
from apps.articles.service.article import article_service


class ArticleSerializer(DataclassSerializer):
    class Meta:
        dataclass = Article

    def create(self, validated_data):
        return article_service.upload_article(validated_data)
