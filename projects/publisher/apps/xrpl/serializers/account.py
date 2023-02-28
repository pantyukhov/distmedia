from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.xrpl.dataclass.account import Account

class CreateAccountSerializer(serializers.Serializer):
    pass


class AccountSerializer(DataclassSerializer):
    class Meta:
        dataclass = Account

