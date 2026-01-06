"""
ASGI config for trellobackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trellobackend.settings")

django_asgi_app = get_asgi_application()

from myboard.routing import websocket_urlpatterns
from myauth.api import AuthWebsocket

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(AuthWebsocket(URLRouter(websocket_urlpatterns)))),
})

application_test = AuthMiddlewareStack(AuthWebsocket(URLRouter(websocket_urlpatterns)))
