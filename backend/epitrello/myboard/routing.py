from django.urls import re_path

from myboard import consumers

websocket_urlpatterns = [
    re_path(r"ws/board/(?P<board_id>[\w-]+)/$", consumers.BoardRealTime.as_asgi()),
]
