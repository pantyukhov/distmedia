import base64
import json
from typing import Optional

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from apps.xrpl.dataclass.account import Account


def get_wallet(request) -> Optional[Account]:
    data = request.META.get('HTTP_X_WALLET_AUTH', None)
    if not data:
        return data

    data = json.loads(base64.b64decode(data))

    return Account(**data)


class AccountMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # get_customer(request)
        request.account_wallet = SimpleLazyObject(lambda: get_wallet(request))
