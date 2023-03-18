from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from apps.libs.encryption.keys import generate_keys
from apps.xrpl.serializers import CreateAccountSerializer, AccountSerializer
from apps.xrpl.service.xrpl import xrpl_service


class AccountViewSet(viewsets.ViewSet):
    serializer_class = CreateAccountSerializer

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
        return Response(AccountSerializer(instance=self.request.account_wallet).data)


    @action(detail=False, methods=['post'])
    def generate_keys(self, request, pk=None):
        private_key, public_key = generate_keys()
        return Response({'private_key': private_key, "public_key": public_key})

    @action(detail=False, methods=['post'])
    def generate_keys(self, request, pk=None):
        private_key, public_key = generate_keys()
        return Response({'private_key': private_key, "public_key": public_key})
