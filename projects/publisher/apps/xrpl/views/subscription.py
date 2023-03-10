from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.xrpl.serializers import CreateSubscriptionSerializer, SubscriptionSerializer
from apps.xrpl.service.xrpl import xrpl_service


class SubscriptionViewSet(viewsets.ViewSet):
    serializer_class = CreateSubscriptionSerializer

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
        serializer_class = self.serializer_class
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return Response(xrpl_service.get_subscriptions(account=self.request.account_wallet))

    def create(self, request, *args, **kwargs):
        subscription = xrpl_service.create_subscription(account=self.request.account_wallet)
        return Response(subscription, status=status.HTTP_201_CREATED)
