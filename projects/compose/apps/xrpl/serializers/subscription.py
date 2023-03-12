from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.xrpl.dataclass.subscription import Subscription


class CreateSubscriptionSerializer(serializers.Serializer):
    public_key = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SubscriptionSerializer(DataclassSerializer):
    class Meta:
        dataclass = Subscription
