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


class AuthWebsocket:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        idtoken = ""
        for key, value in scope["headers"]:
            if key not in (b"Authorization", b"authorization", b"Http-Authorization"):
                print(f"continue | key={key} | value={value}", file=sys.stderr)
                continue
            idtoken = value.decode()
            print(f"break | idtoken={idtoken}", file=sys.stderr)
            break
        await aclose_old_connections()
        if idtoken.startswith("Bearer "):
            m = await database_sync_to_async(check_google_auth)(idtoken)
        elif settings.ENVIRON == "test" and idtoken.startswith("Test "):
            m = await database_sync_to_async(check_test_auth)(idtoken)
        else:
            m = None
        if not isinstance(m, User):
            scope["user"] = None
            return await self.app(scope, receive, send)
        scope["user"] = m
        scope["session"]["member_id"] = f"{m.id}"
        return await self.app(scope, receive, send)


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
    class AuthAsyncTest(APIKeyHeader):
        param_name = "Authorization"
        @override
        async def authenticate(self, request: HttpRequest, key: str | None):
            print(f"------------ HEADERS {request.headers}", file=sys.stderr)
            if key is None:
                return
            await aclose_old_connections()
            try:
                m = await database_sync_to_async(check_test_auth)(key)
            except Exception as e:
                print(f"ERROR {self.__class__}:authenticate: {e}")
                m = None
            if not isinstance(m, User):
                return
            request.session["member_id"] = f"{m.id}"
            return m
    class AuthAsyncMinTest(AuthAsyncTest):
        param_name = "authorization"
    class AuthAsyncHttpTest(AuthAsyncTest):
        param_name = "Http-Authorization"
    AUTH_CHECKS.extend((AuthTest(), AuthMinTest(), AuthHttpTest(), AuthAsyncTest(), AuthAsyncMinTest(), AuthAsyncHttpTest()))

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
