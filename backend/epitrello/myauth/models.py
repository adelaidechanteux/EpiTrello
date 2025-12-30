import uuid
from django.db import models
from django.conf import settings
from typing import final

# Create your models here.

AUTH_PROVIDERS = [
    ("ggl", "Google"),
    ("tst", "Test"),
]


@final
class User(models.Model):
    # id = models.UUIDField[uuid.UUID, uuid.UUID](primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.CharField[str, str](max_length=30)
    # profile_picture = models.URLField[str, str](default=f"{settings.STATIC_URL}question_mark.png")
    # email = models.EmailField[str, str]()
    # authprovider = models.CharField[str, str](max_length=3, choices=AUTH_PROVIDERS)
    # authuserid = models.CharField[str, str](max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    profile_picture = models.URLField(default=f"{settings.STATIC_URL}question_mark.png")
    email = models.EmailField()
    authprovider = models.CharField(max_length=3, choices=AUTH_PROVIDERS)
    authuserid = models.CharField(max_length=30)
