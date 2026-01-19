from uuid import UUID
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
