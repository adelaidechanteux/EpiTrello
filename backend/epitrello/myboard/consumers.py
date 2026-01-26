import json

from typing import override
from uuid import UUID
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from myauth.api import auth_websocket
from myboard.utils import does_user_access_board

class BoardRealTime(WebsocketConsumer):
    board_id: UUID | None = None
    room_group_name: str = ""
    is_connected: bool = False

    @override
    def connect(self) -> None:
        self.board_id = UUID(self.scope.get("url_route", {}).get("kwargs", {}).get("board_id", "No Board ID provided"), version=4)
        self.room_group_name = f"board_{self.board_id}"
        self.accept()

    @override
    def disconnect(self, code: int) -> None:
        if self.is_connected:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    @override
    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        if text_data is None:
            return
        text_data_json = json.loads(text_data)
        if "type" not in text_data_json:
            return
        # Login
        if text_data_json["type"] == "login" and "Authorization" in text_data_json:
            m = auth_websocket(text_data_json["Authorization"])
            if m is None:
                self.is_connected = False
                self.send(text_data=json.dumps({"type": "login", "code": "UserUnknown", "error": "User does not exists"}))
                return
            if not does_user_access_board(m, self.board_id):
                self.is_connected = False
                self.send(text_data=json.dumps({"type": "login", "code": "BoardPermission", "error": "User is not in the board members"}))
                return
            self.is_connected = True
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.send(text_data=json.dumps({"type": "login", "success": True}))
            return
        #async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": text_data_json})

    # def chat_message(self, event: dict):
    #     self.send(text_data=json.dumps(event["message"]))

    def f_invit_board(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_invit_board",
            "admin": event["admin"],
            "user": event["user"],
        }))

    def f_delete_member(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_member",
            "id": event["id"],
        }))

    def f_delete_board(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_board",
            "id": event["id"],
        }))

    def f_update_board(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_board",
            "board_title": event["board_title"],
            "board_owner": event["board_owner"],
            "board_color": event["board_color"],
        }))

    def f_update_categories(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_categories",
            "categories": event["categories"],
        }))

    def f_create_task(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_create_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
        }))

    def f_delete_task(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_task",
            "id": event["id"],
        }))

    def f_deleteforce_task(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_delete_task",
            "id": event["id"],
        }))

    def f_update_task(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
        }))

    def f_restore_task(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_restore_task",
            "task": event["task"],
            "board_categories": event["board_categories"],
        }))

    def f_update_role(self, event: dict):
        if not self.is_connected:
            return
        self.send(text_data=json.dumps({
            "type": "f_update_role",
            "user": event["user"],
            "admin": event["admin"],
        }))
