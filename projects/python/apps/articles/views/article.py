from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from apps.articles.serializers import ArticleSerializer, PurchaseArticle
from apps.articles.service.article import article_service
from apps.xrpl.service.xrpl import xrpl_service


class ArticleViewSet(CreateModelMixin, viewsets.ViewSet):
    serializer_class = ArticleSerializer

    serializers = {
        'purchase_article': PurchaseArticle,
        # etc.
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializer_class)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = article_service.upload_article(request.account_wallet, serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        addresses = self.request.query_params.getlist('addresses', [])
        items = article_service.get_articles(addresses)
        return Response(items)

    @action(detail=False, methods=['post'])
    def purchase_article(self, request):
        serializer = PurchaseArticle(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = xrpl_service.purchase_article(request.account_wallet, serializer.validated_data.nft_id)

        return Response(data)
