from typing import override
from ninja import Router, Schema
from ninja.security import HttpBearer, APIKeyHeader
from channels.db import database_sync_to_async, aclose_old_connections
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from uuid import UUID
import sys

from myauth.models import User
from myauth.middleware import check_google_auth, check_test_auth


def auth_websocket(idtoken: str):
    if idtoken.startswith("Bearer "):
        return check_google_auth(idtoken)
    if settings.ENVIRON == "test" and idtoken.startswith("Test "):
        return check_test_auth(idtoken)
    return None


class AuthGoogleBearer(HttpBearer):
    @override
    def authenticate(self, request: HttpRequest, token: str):
        m = check_google_auth(f"Bearer {token}")
        if not isinstance(m, User):
            print(f"-------------- bad {m} | {token} | {m.text}", file=sys.stderr)
            return
        request.session["member_id"] = f"{m.id}"
        return m


AUTH_CHECKS = [AuthGoogleBearer()]

if settings.ENVIRON == "test":

    class AuthTest(APIKeyHeader):
        param_name = "Authorization"

        @override
        def authenticate(self, request: HttpRequest, key: str | None):
            if key is None:
                return
            try:
                m = check_test_auth(key)
            except Exception as e:
                print(f"ERROR {self.__class__}:authenticate: {e}")
                m = None
            if not isinstance(m, User):
                return
            request.session["member_id"] = f"{m.id}"
            return m

    class AuthMinTest(AuthTest):
        param_name = "authorization"

    class AuthHttpTest(AuthTest):
        param_name = "Http-Authorization"

    AUTH_CHECKS.extend((AuthTest(), AuthMinTest(), AuthHttpTest()))

router = Router(auth=AUTH_CHECKS, tags=["auth"])


class OUTMemberSchema(Schema):
    id: UUID
    username: str
    profile_picture: str
    email: str


@router.get("/user/login/", response={200: OUTMemberSchema})
def user_login(request: HttpRequest):
    assert isinstance(request.auth, User)
    return request.auth
