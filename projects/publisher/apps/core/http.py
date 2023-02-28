from typing import Dict, Optional, Union

from rest_framework import status
from rest_framework.response import Response


def get_result(message: Union[str, int, bool] = None) -> Optional[Dict]:
    return {"result": message} if message is not None else None


def get_response(message: Union[str, int, bool] = None, status_code: int = status.HTTP_200_OK) -> Response:
    return Response(data=get_result(message), status=status_code)


def get_error_response(
        message: Union[str, int, bool] = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
) -> Response:
    return Response(get_error(message), status=status_code)


def get_error(message: Union[str, int, bool] = None) -> Optional[Dict]:
    return {"error": message} if message is not None else None
