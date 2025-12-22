from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from myauth.middleware import require_logged
from django.http import Http404, HttpResponse, JsonResponse

from myauth.models import User


# Create your views here.


@csrf_exempt
@require_http_methods(["POST"])
@require_logged
def user_login(_):
    try:
        u = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        raise Http404("User does not exists")
    res = {
        "id": f"{u.id}",
        "username": f"{u.username}",
        "profile_picture": f"{u.profile_picture}",
        "email": f"{u.email}",
    }
    return JsonResponse(res)
