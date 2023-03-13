from abc import ABC

from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.xrpl.dataclass.account import Account


class CreateAccountSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AccountSerializer(DataclassSerializer):
    class Meta:
        dataclass = Account
