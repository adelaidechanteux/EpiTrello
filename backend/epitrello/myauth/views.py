from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from myauth.middleware import require_logged
from django.http import HttpResponse

# Create your views here.


@require_http_methods(["POST"])
@require_logged
def user_login(_):
    return HttpResponse(status=200)
