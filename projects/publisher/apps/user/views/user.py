from apps.core.authorisations import CsrfExemptSessionAuthentication
from apps.core.http import get_response, get_error_response
from apps.user.mixins import SignMixin
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.views import APIView

from apps.user import serializers

User = get_user_model()


def get(request, format=None):
    if request.user.is_authenticated:
        ser = serializers.UserSerializer(request.user, many=False)
        return get_response(ser.data)

    return get_response(status_code=status.HTTP_204_NO_CONTENT)


class LoginView(SignMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = serializers.LoginSerializer

    def get(self, request, format=None):
        """
        Get Authorized user information or HTTP_401_UNAUTHORIZED
        """
        if request.user.is_authenticated:
            ser = serializers.UserSerializer(request.user, many=False)
            return get_response(ser.data)
        return get_error_response(status_code=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """
        Authorize user
        """
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            user = self.login(ser.instance)
            ser = serializers.UserSerializer(user, many=False)
            return get_response(ser.data)

        return get_error_response(ser.errors, status_code=status.HTTP_400_BAD_REQUEST)


class LogoutView(SignMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = serializers.LogoutSerializer

    def get(self, request):
        """
        Logout
        """
        self.logout()
        return get_response()
