import json

from typing import override
from uuid import UUID
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from myauth.api import auth_websocket
from myboard.utils import does_user_access_board, connect_user_board, disconnect_user_board
from django.http import HttpResponseForbidden

class BoardRealTime(WebsocketConsumer):
    board_id: UUID | None = None
    room_group_name: str = ""
    user_connected: UUID | None = None

    @override
    def connect(self) -> None:
        self.board_id = UUID(self.scope.get("url_route", {}).get("kwargs", {}).get("board_id", "No Board ID provided"), version=4)
        self.room_group_name = f"board_{self.board_id}"
        self.accept()

    @override
    def disconnect(self, code: int) -> None:
        if self.board_id is None:
            return
        if self.user_connected is None:
            return
        _ = disconnect_user_board(self.user_connected, self.board_id)
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    @override
    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        if self.board_id is None:
            return
        if text_data is None:
            return
        text_data_json = json.loads(text_data)
        if "type" not in text_data_json:
            return
        # Login
        if text_data_json["type"] == "login" and "Authorization" in text_data_json:
            m = auth_websocket(text_data_json["Authorization"])
            if m is None or isinstance(m, HttpResponseForbidden):
                self.user_connected = None
                self.send(text_data=json.dumps({"type": "login", "success": False, "code": "UserUnknown", "error": "User does not exists"}))
                return
            if not does_user_access_board(m, self.board_id):
                self.user_connected = None
                self.send(text_data=json.dumps({"type": "login", "success": False, "code": "BoardPermission", "error": "User is not in the board members"}))
                return
            self.user_connected = m.id
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            connected = connect_user_board(m, self.board_id)
            if connected is False:
                self.send(text_data=json.dumps({"type": "login", "success": False, "code": "InternalError", "error": "Internal Error"}))
                return
            self.send(text_data=json.dumps({"type": "login", "success": True, "connected": connected}))
            return
        #async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": text_data_json})

    # def chat_message(self, event: dict):
    #     self.send(text_data=json.dumps(event["message"]))

    def f_invit_board(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_invit_board",
            "admin": event["admin"],
            "user": event["user"],
            "from_user": event["from_user"],
        }))

    def f_delete_member(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_member",
            "id": event["id"],
            "from_user": event["from_user"],
        }))

    def f_delete_board(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_board",
            "id": event["id"],
            "from_user": event["from_user"],
        }))

    def f_update_board(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_board",
            "board_title": event["board_title"],
            "board_owner": event["board_owner"],
            "board_color": event["board_color"],
            "from_user": event["from_user"],
        }))

    def f_update_categories(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_categories",
            "categories": event["categories"],
            "from_user": event["from_user"],
        }))

    def f_create_task(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_create_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
            "from_user": event["from_user"],
        }))

    def f_delete_task(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_task",
            "id": event["id"],
            "from_user": event["from_user"],
        }))

    def f_deleteforce_task(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_task",
            "id": event["id"],
            "from_user": event["from_user"],
        }))

    def f_update_task(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
            "from_user": event["from_user"],
        }))

    def f_restore_task(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_restore_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
            "from_user": event["from_user"],
        }))

    def f_update_role(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_role",
            "user": event["user"],
            "admin": event["admin"],
            "from_user": event["from_user"],
        }))

    def f_connected_user(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_connected_user",
            "user": event["user"],
            "from_user": event["from_user"],
        }))

    def f_disconnected_user(self, event: dict):
        if self.user_connected is None:
            return
        self.send(text_data=json.dumps({
            "type": "f_disconnected_user",
            "user": event["user"],
            "from_user": event["from_user"],
        }))
