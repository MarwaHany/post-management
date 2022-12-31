from functools import wraps
from django.contrib.auth import authenticate
from http import HTTPStatus

from django.http import JsonResponse


def authenticate_user(decorated_method):
    @wraps(decorated_method)
    def wrapped(request, *args, **kwargs):
        if not (
            request.headers.get("username") and request.headers.get("authorization")
        ):
            return JsonResponse(
                {"message": "please enter both -> username and api_key."},
                status=HTTPStatus.BAD_REQUEST,
            )
        else:
            user = authenticate(
                request,
                username=request.headers.get("username"),
                password=request.headers.get("authorization"),
            )
            if user is None:
                return JsonResponse(
                    {"message": "forbidden"}, status=HTTPStatus.UNAUTHORIZED
                )
            else:
                return decorated_method(request, *args, **kwargs)

    return wrapped
