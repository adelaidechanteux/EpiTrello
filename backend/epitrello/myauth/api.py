from typing import override
from ninja import Router, Schema
from ninja.security import HttpBearer, APIKeyHeader
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from uuid import UUID

from myauth.models import User
from myauth.middleware import check_google_auth, check_test_auth


class AuthGoogleBearer(HttpBearer):
    @override
    def authenticate(self, request: HttpRequest, token: str):
        m = check_google_auth(f"Bearer {token}")
        if not isinstance(m, User):
            return
        request.session["member_id"] = f"{m.id}"
        return m

class AuthTest(APIKeyHeader):
    param_name = "Authorization"

    @override
    def authenticate(self, request: HttpRequest, key: str | None):
        if key is None:
            return
        m = check_test_auth(key)
        if not isinstance(m, User):
            return
        request.session["member_id"] = f"{m.id}"
        return m

AUTH_CHECKS = [AuthGoogleBearer()]

if settings.ENVIRON == "test":
    AUTH_CHECKS.append(AuthTest())

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
