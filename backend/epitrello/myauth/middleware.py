from hashlib import md5
from myauth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from google.oauth2 import id_token as ggl_id_token
from google.auth.transport import requests as ggl_requests
from django.conf import settings
from base64 import b64decode
import sys


def check_google_auth(id_token: str) -> HttpResponseForbidden | User:
    authprovider = "ggl"
    id_token = id_token[len("Bearer ") :]
    user_id = ""
    user_email = ""
    user_picture = ""
    user_name = ""
    try:
        idinfo: dict[str, str] = ggl_id_token.verify_oauth2_token(
            id_token, ggl_requests.Request()
        )
        user_id = idinfo["sub"]
        user_email = idinfo["email"]
        user_picture = idinfo.get("picture")
        user_name = idinfo["name"]
    except ValueError as esc:
        return HttpResponseForbidden(
            f"Google auth provider did not validate your id token: {esc}",
            content_type="plain/text",
        )
    try:
        m = User.objects.get(authuserid__exact=user_id, authprovider__exact=authprovider)
    except User.DoesNotExist:
        wargs = {}
        if user_picture is not None:
            wargs["profile_picture"] = user_picture
        m = User(
            username=user_name,
            email=user_email,
            authprovider=authprovider,
            authuserid=user_id,
            **wargs,
        )
        m.save()
    return m

def check_test_auth(id_token: str) -> HttpResponseForbidden | User:
    authprovider = "tst"
    if settings.ENVIRON != "test":
        return HttpResponseForbidden(
            "Google auth provider did not validate your id token",
            content_type="plain/text",
        )
    id_token = id_token[len("Test ") :]
    id_token = b64decode(id_token).decode()
    user_email, user_name = id_token.split(":")
    user_id = md5(user_email.encode()).hexdigest()[:29]
    user_picture = None
    try:
        m = User.objects.get(authuserid__exact=user_id, authprovider__exact=authprovider)
    except User.DoesNotExist:
        wargs = {}
        if user_picture is not None:
            wargs["profile_picture"] = user_picture
        m = User(
            username=user_name,
            email=user_email,
            authprovider=authprovider,
            authuserid=user_id,
            **wargs,
        )
        m.save()
    return m


def require_logged(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if "Authorization" not in request.headers:
            return HttpResponseBadRequest(
                "Missing 'Authorization' header", content_type="text/plain"
            )
        if request.session.get("member_id", None) is not None:
            return func(request, *args, **kwargs)
        id_token = request.headers["Authorization"]
        m = None
        if id_token.startswith("Bearer "):
            m = check_google_auth(id_token)
        elif id_token.startswith("Test "):
            m = check_test_auth(id_token)
        else:
            return HttpResponseBadRequest(
                "Authorization must be a bearer", content_type="text/plain"
            )
        if not isinstance(m, User):
            return m
        request.session["member_id"] = f"{m.id}"
        return func(request, *args, **kwargs)

    return wrapper
