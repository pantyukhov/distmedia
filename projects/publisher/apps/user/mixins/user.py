import logging
from typing import Optional
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()

logger = logging.getLogger(__name__)


class UserIdentificationMixin(object):
    @staticmethod
    def identify(username: str) -> Optional["User"]:
        UserModel = get_user_model()
        return UserModel._default_manager.filter(
            Q(**{UserModel.USERNAME_FIELD: username}) | Q(email=username) | Q(phone=username)
        ).first()


class SignMixin(object):
    def login(self, user):
        auth.login(self.request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
        return user

    def logout(self):
        auth.logout(self.request)


class UserPasswordMixin(object):
    @staticmethod
    def generate_password() -> str:
        User = get_user_model()
        return User.objects.make_random_password(length=settings.USER_PASSWORD_LENGTH)


class RegisterUserMixin(SignMixin):
    communication_type_code = "REGISTRATION"

    def register_user(
        self,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        password: str = None,
        commit=True,
        force_login=True,
        request=None,
    ) -> "User":
        User = get_user_model()
        if password is None:
            password = User.objects.make_random_password()
        """
        Create a user instance and send a new registration email (if configured
        to).
        """

        user = User.objects.filter(Q(username=username)).first()

        if user:
            raise Exception(f"User with username={username} is registered")

        if not user:
            user = User(username=username, email=email, phone=phone, first_name=first_name, last_name=last_name)

        user.is_active = True
        #   user.username = user.email
        user.set_password(password)

        if commit:
            user.save()
        # return user

        _request = request if request is not None else self.request  # type: ignore
        # user_registered.send_robust(
        #     sender=self, request=_request, user=user)

        if getattr(settings, "SEND_REGISTRATION_EMAIL", True):
            self.send_registration_email(user)

        if not force_login:
            return user

        # We have to authenticate before login
        try:
            user = authenticate(username=user.username, password=password)
        except User.MultipleObjectsReturned:
            # Handle race condition where the registration request is made
            # multiple times in quick succession.  This leads to both requests
            # passing the uniqueness check and creating users (as the first one
            # hasn't committed when the second one runs the check).  We retain
            # the first one and deactivate the dupes.
            # logger.warning(
            #     'Multiple users with identical email address and password'
            #     'were found. Marking all but one as not active.')
            # As this section explicitly deals with the form being submitted
            # twice, this is about the only place in Oscar where we don't
            # ignore capitalisation when looking up an email address.
            # We might otherwise accidentally mark unrelated users as inactive
            users = User.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.is_active = False
                u.save()

        self.login(user)

        return user

    def send_registration_email(self, user):
        code = self.communication_type_code
        # ctx = {'user': user,
        #        'site': get_current_site(self.request)}
        # messages = CommunicationEventType.objects.get_and_render(
        #     code, ctx)
        # if messages and messages['body']:
        #     Dispatcher().dispatch_user_messages(user, messages)


class UserMixin(RegisterUserMixin):
    def user_get_or_create(self, email, request):
        users = User.objects.filter(email=email)
        if len(users) > 0:
            return users[0]
        else:
            return self.register_user(email=email, request=request, force_login=True)

