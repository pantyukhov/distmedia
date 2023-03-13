from typing import Optional, Dict
from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers


User = get_user_model()


class LogoutSerializer(serializers.Serializer):
    pass


def field_length(fieldname):
    field = next(field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=field_length(User.USERNAME_FIELD), required=True)
    password = serializers.CharField(max_length=field_length("password"), required=True)

    def validate(self, attrs):

        self.username = attrs["username"]
        self.password = attrs["password"]

        user = authenticate(username=self.username, password=self.password)

        if user is None:
            raise serializers.ValidationError("Incorrect username or password")
        elif not user.is_active:
            raise serializers.ValidationError("User is no active")

        self.instance = user
        return attrs






class InlineUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )



class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
        )


class UserSerializer(CommonUserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
        )

