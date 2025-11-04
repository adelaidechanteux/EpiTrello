from django.urls import path
from myauth import views

urlpatterns = [
    path("", views.user_login),
]
