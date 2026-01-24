import sys
from uuid import UUID
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from myboard.models import Board
from myauth.models import User


def does_user_access_board(u: User, board_id: UUID):
    try:
        b = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return False
    if f"{u.id}" in [f"{x.id}" for x in b.members.all()]:
        return True
    return False



def serialize_data(v):
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return v
    if isinstance(v, UUID):
        return f"{v}"
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return v
    if v is None:
        return v
    if isinstance(v, dict):
        return serialize_data_dict(v)
    if isinstance(v, list):
        return serialize_data_array(v)
    print(f"ERROR: failed to serialize_data for {type(v).__name__} with value: {v}", file=sys.stderr)
    return v

def serialize_data_array(d: list) -> list:
    res = []
    for v in d:
        res.append(serialize_data(v))
    return res

def serialize_data_dict(d: dict) -> dict:
    res = {}
    for k, v in d.items():
        res[k] = serialize_data(v)
    return res


def send_websocket(board_id: str, type_: str, data: dict):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        raise ValueError("Channel Layer not set up")
    async_to_sync(channel_layer.group_send)(f"board_{board_id}", {
        "type": type_,
        **serialize_data_dict(data),
    })
