import uuid
from django.db import models
from django.conf import settings

# Create your models here.

AUTH_PROVIDERS = [
    ("ggl", "Google"),
]


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    profile_picture = models.URLField(default=f"{settings.STATIC_URL}question_mark.png")
    email = models.EmailField()
    authprovider = models.CharField(max_length=3, choices=AUTH_PROVIDERS)
    authuserid = models.CharField(max_length=30)
