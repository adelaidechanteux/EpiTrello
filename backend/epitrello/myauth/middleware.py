from myauth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from google.oauth2 import id_token as ggl_id_token
from google.auth.transport import requests as ggl_requests
import sys


def require_logged(func):
    def wrapper(request, *args, **kwargs):
        if "Authorization" not in request.headers:
            return HttpResponseBadRequest("Missing 'Authorization' header", content_type="text/plain")
        if request.session.get("member_id", None) is not None:
            return func(request, *args, **kwargs)
        id_token = request.headers["Authorization"]
        if not id_token.startswith("Bearer "):
            return HttpResponseBadRequest("Authorization must be a bearer", content_type="text/plain")
        id_token = id_token[len("Bearer "):]
        user_id = ""
        user_email = ""
        user_picture = ""
        user_name = ""
        try:
            idinfo: dict[str, str] = ggl_id_token.verify_oauth2_token(id_token, ggl_requests.Request())
            user_id = idinfo['sub']
            user_email = idinfo['email']
            print(f"{idinfo}", file=sys.stderr)
            user_picture = idinfo.get('picture')
            user_name = idinfo['name']
        except ValueError:
            return HttpResponseForbidden("Google auth provider did not validate your id token", content_type="plain/text")
        try:
            m = User.objects.get(authuserid__exact=user_id, authprovider__exact="ggl")
        except User.DoesNotExist:
            wargs = {}
            if user_picture is not None:
                wargs["profile_picture"] = user_picture
            m = User(username=user_name, email=user_email, authprovider="ggl", authuserid=user_id, **wargs)
        request.session["member_id"] = f"{m.id}"
        return func(request, *args, **kwargs)
    return wrapper
