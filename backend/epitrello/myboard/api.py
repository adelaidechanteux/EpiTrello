from uuid import UUID
from ninja import Router, Schema
from django.http import HttpRequest, HttpResponse
from collections import OrderedDict
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from myboard.models import Board, Task, TITLE_LENGTH, CATEGORY_LENGTH, COLOR_LENGTH
from myauth.models import User
from myauth.api import AUTH_CHECKS


router = Router(auth=AUTH_CHECKS, tags=["board"])


class OUTError(Schema):
    code: str
    message: str


OUTERROR_BoardDoesNotExists = (404, {"code": "BoardDoesNotExists", "message": "Board does not exists"})
OUTERROR_TaskDoesNotExists = (404, {"code": "TaskDoesNotExists", "message": "Task does not exists"})
OUTERROR_UserDoesNotExists = (404, {"code": "UserDoesNotExists", "message": "User does not exists"})
OUTERROR_MissingPermission = (403, {"code": "MissingPermission", "message": "Connected User has not enough permissions"})
OUTERROR_BadValue = (400, {"code": "BadValue", "message": "Value in a body value item does not meet requirements"})
OUTERROR_TaskIsInvalid = (400, {"code": "TaskIsInvalid", "message": "Task is not in the good state to be processed by this call"})


def send_websocket(board_id: str, type_: str, data: dict):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        raise ValueError("Channel Layer not set up")
    async_to_sync(channel_layer.group_send)(f"board_{board_id}", {
        "type": type_,
        **data,
    })


class OUTMemberSchema(Schema):
    id: UUID
    username: str
    email: str
    profile_picture: str


class OUTTaskSchema(Schema):
    id: UUID
    title: str
    description: str
    color: str
    category: str
    date_start: str | None
    date_end: str | None
    date_creation: str
    owner: OUTMemberSchema
    assigned: OUTMemberSchema | None
    completed: bool

    @staticmethod
    def resolve_date_start(obj: Task):
        if obj.date_start:
            return f"{obj.date_start}"
        return
    @staticmethod
    def resolve_date_end(obj: Task):
        if obj.date_end:
            return f"{obj.date_end}"
        return
    @staticmethod
    def resolve_date_creation(obj: Task):
        return f"{obj.date_creation}"


class OUTBoardSchema(Schema):
    title: str
    id: UUID
    favorite: bool = False
    members: list[OUTMemberSchema]
    tasks: list[OUTTaskSchema]
    archived: list[OUTTaskSchema]
    owner: OUTMemberSchema
    categories: list[str]
    admin: list[OUTMemberSchema]
    color: str


class OUTOKSchema(Schema):
    ok: bool = True


@router.get("/get/board/{board_id}/", response={200: OUTBoardSchema, 403: OUTError, 404: OUTError})
def get_board(request: HttpRequest, board_id: UUID):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    return board


class OUTBoardMinSchema(Schema):
    id: UUID
    title: str
    color: str


class OUTBoardsMinSchema(Schema):
    boards: list[OUTBoardMinSchema]
    owned: list[OUTBoardMinSchema]
    favorite: list[OUTBoardMinSchema]
    admin: list[OUTBoardMinSchema]


@router.get("/boards/", response={200: OUTBoardsMinSchema})
def board_member(request: HttpRequest):
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    return {
        "boards": user.board_set.all().distinct(),
        "owned": user.board_owner_set.all().distinct(),
        "admin": user.board_admin_set.all().distinct(),
        "favorite": user.board_favorite_set.all().distinct(),
    }


class InInvitBoardSchema(Schema):
    email: str
    admin: bool


@router.post("/invit/board/{board_id}/", response={200: OUTOKSchema, 403: OUTError, 404: OUTError})
def invit_board(request: HttpRequest, board_id: UUID, body: InInvitBoardSchema):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.admin.contains(user):
        return OUTERROR_MissingPermission
    try:
        target = User.objects.get(email=body.email)
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    board.members.add(target)
    if body.admin:
        board.admin.add(target)
    send_websocket(f"{board_id}", "f_invit_board", {
        "admin": body.admin,
        "user": OUTMemberSchema.from_orm(target).dict()
    })
    return {}

class InCreateBoardSchema(Schema):
    title: str
    color: str

@router.post("/create/board/", response={200: OUTBoardSchema, 400: OUTError, 404: OUTError})
def create_board(request: HttpRequest, body: InCreateBoardSchema):
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if len(body.title) >= TITLE_LENGTH:
        return OUTERROR_BadValue
    if len(body.color) >= COLOR_LENGTH:
        return OUTERROR_BadValue
    board = Board(title=body.title, owner=user, color=body.color)
    board.save()
    board.members.add(user)
    board.admin.add(user)
    return board


@router.put("/delete/board/{board_id}/", response={200: OUTOKSchema, 403: OUTError, 404: OUTError})
def delete_board(request: HttpRequest, board_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    if request.session["member_id"] != f"{board.owner.id}":
        return OUTERROR_MissingPermission
    board.delete()
    send_websocket(f"{board_id}", "f_delete_board", {
        "id": f"{board_id}"
    })
    return {}


class InCreateTask(Schema):
    title: str
    description: str | None = None
    category: str
    color: str | None = None
    date_start: str | None = None
    date_end: str | None = None
    assigned: str | None = None

@router.post("create/task/{board_id}/", response={200: OUTTaskSchema, 400: OUTError, 403: OUTError,  404: OUTError})
def create_task(request: HttpRequest, board_id: UUID, body: InCreateTask):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    if len(body.title) >= TITLE_LENGTH or len(body.category) >= CATEGORY_LENGTH:
        return OUTERROR_BadValue
    if body.color is not None and len(body.color) >= COLOR_LENGTH:
        return OUTERROR_BadValue
    if body.description is None:
        body.description = ""
    optional_arg = {}
    for key in ("color", "date_start", "date_end", "assigned"):
        if getattr(body, key) is not None:
            optional_arg[key] = getattr(body, key)
    task = Task(
        title=body.title,
        description=body.description,
        category=body.category,
        owner=user,
        **optional_arg,
    )
    task.save()
    board.tasks.add(task)
    old_category = board.categories
    new_category = list(OrderedDict.fromkeys(board.categories + [f"{task.category}"]))
    if old_category != new_category:
        board.categories = new_category
        board.save(update_fields=["categories"])
    send_websocket(f"{board_id}", "f_create_task", {
        "task": OUTTaskSchema.from_orm(task).dict(),
        "board_categories": new_category,
    })
    return task


@router.put("/delete/task/{board_id}/{task_id}/", response={200: OUTOKSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def delete_task(request: HttpRequest, board_id: UUID, task_id: UUID):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return OUTERROR_TaskDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    if not board.tasks.contains(task):
        return OUTERROR_TaskIsInvalid
    board.tasks.remove(task)
    board.archived.add(task)
    send_websocket(f"{board_id}", "f_delete_task", {
        "id": f"{task_id}",
    })
    return {}


@router.put("/deleteforce/task/{board_id}/{task_id}/", response={200: OUTOKSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def deleteforce_task(request: HttpRequest, board_id: UUID, task_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return OUTERROR_TaskDoesNotExists
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.admin.contains(user):
        return OUTERROR_MissingPermission
    if not board.archived.contains(task):
        return OUTERROR_TaskIsInvalid
    board.archived.remove(task)
    task.delete()
    send_websocket(f"{board_id}", "f_deleteforce_task", {
        "id": f"{task_id}",
    })
    return {}


@router.put("/restore/task/{board_id}/{task_id}/", response={200: OUTOKSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def restore_task(request: HttpRequest, board_id: UUID, task_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return OUTERROR_TaskDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    if not board.archived.contains(task):
        return OUTERROR_TaskIsInvalid
    board.archived.remove(task)
    board.tasks.add(task)
    old_category = board.categories
    new_category = list(OrderedDict.fromkeys(board.categories + [f"{task.category}"]))
    if old_category != new_category:
        board.categories = new_category
        board.save(update_fields=["categories"])
    send_websocket(f"{board_id}", "f_restore_task", {
            "task": OUTTaskSchema.from_orm(task).dict(),
            "board_categories": new_category,
    })
    return {}


class InUpdateTask(Schema):
    title: str | None = None
    description: str | None = None
    color: str | None = None
    category: str | None = None
    date_start: str | None = None
    date_end: str | None = None
    owner: str | None = None
    assigned: str | None = None
    completed: bool | None = None
    order: int | None = None


@router.put("/update/task/{board_id}/{task_id}/", response={200: OUTTaskSchema, 403: OUTError, 404: OUTError})
def update_task(request: HttpRequest, board_id: UUID, task_id: UUID, body: InUpdateTask):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return OUTERROR_TaskDoesNotExists
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    if body.title is not None and len(body.title) >= TITLE_LENGTH:
        return OUTERROR_BadValue
    if body.category is not None and len(body.category) >= CATEGORY_LENGTH:
        return OUTERROR_BadValue
    if body.color is not None and len(body.color) >= COLOR_LENGTH:
        return OUTERROR_BadValue
    optional_arg: list[str] = []
    for key in ("title", "description", "color", "category", "date_start", "date_end", "owner", "assigned", "completed"):
        if getattr(body, key) is not None:
            setattr(task, key, getattr(body, key))
            optional_arg.append(key)
    if len(optional_arg) != 0:
        task.save(update_fields=optional_arg)
    if body.order is not None:
        task.boardtasksthroughmodel_set.all().first().to(body.order)
    task = Task.objects.get(pk=task.id)
    old_category = board.categories
    new_category = list(OrderedDict.fromkeys(board.categories + [f"{task.category}"]))
    if old_category != new_category:
        board.categories = new_category
        board.save(update_fields=["categories"])
    send_websocket(f"{board_id}", "f_update_task", {
        "task": OUTTaskSchema.from_orm(task).dict(),
        "board_categories": new_category,
    })
    return task


class InUpdateBoard(Schema):
    title: str | None = None
    owner: str | None = None
    color: str | None = None


@router.put("/update/board/{board_id}/", response={200: OUTBoardSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def update_board(request: HttpRequest, board_id: UUID, body: InUpdateBoard):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    try:
        target = None
        if body.owner is not None:
            target = User.objects.get(email=body.owner)
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if body.owner is not None:
        if f"{target.id}" != f"{board.owner.id}":
            if request.session["member_id"] != f"{board.owner.id}":
                return OUTERROR_MissingPermission
        body.owner = target
    if body.title is not None and len(body.title) >= TITLE_LENGTH:
        return OUTERROR_BadValue
    if body.color is not None and len(body.color) >= COLOR_LENGTH:
        return OUTERROR_BadValue
    optional_arg: list[str] = []
    for key in ("title", "owner", "color"):
        if getattr(body, key) is not None:
            setattr(board, key, getattr(body, key))
            optional_arg.append(key)
    board.save(update_fields=optional_arg)
    send_websocket(f"{board_id}", "f_update_board", {
        "board_title": f"{board.title}",
        "board_owner": OUTMemberSchema.from_orm(board.owner).dict()
    })
    return board


class InDeleteMember(Schema):
    email: str


@router.put("/delete/member/{board_id}/", response={200: OUTBoardSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def delete_member(request: HttpRequest, board_id: UUID, body: InDeleteMember):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    try:
        target = User.objects.get(email=body.email)
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.admin.contains(user):
        return OUTERROR_MissingPermission
    if f"{target.id}" == f"{board.owner.id}":
        return OUTERROR_BadValue
    if f"{user.id}" == f"{board.owner.id}":
        board.members.remove(target)
        board.admin.remove(target)
        board.user_favorite.remove(target)
        send_websocket(f"{board_id}", "f_delete_member", {
            "id": f"{target.id}",
        })
        return board
    if board.admin.contains(target):
        return OUTERROR_MissingPermission
    board.members.remove(target)
    board.admin.remove(target)
    board.user_favorite.remove(target)
    send_websocket(f"{board_id}", "f_delete_member", {
        "id": f"{target.id}",
    })
    return board


class InUpdateCategory(Schema):
    categories: list[str]


@router.put("/update/categories/{board_id}/", response={200: OUTBoardSchema, 400: OUTError, 403: OUTError, 404: OUTError})
def update_categories(request: HttpRequest, board_id: UUID, body: InUpdateCategory):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    categories_present = set([f"{x.category}" for x in board.tasks.all()])
    if not all([x in body.categories for x in categories_present]):
        return OUTERROR_BadValue
    board.categories = list(OrderedDict.fromkeys(body.categories))
    board.save(update_fields=["categories"])
    send_websocket(f"{board_id}", "f_update_categories", {
        "categories": board.categories,
    })
    return board


class InUpdateRole(Schema):
    email: str
    admin: bool


@router.put("/update/role/{board_id}/", response={200: OUTOKSchema, 403: OUTError, 404: OUTError})
def update_role(request: HttpRequest, board_id: UUID, body: InUpdateRole):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    try:
        target = User.objects.get(email=body.email)
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if f"{board.owner.id}" != f"{user.id}":
        return OUTERROR_MissingPermission
    if f"{board.owner.id}" == f"{target.id}":
        return OUTERROR_MissingPermission
    if body.admin:
        board.admin.add(target)
    else:
        board.admin.remove(target)
    send_websocket(f"{board_id}", "f_update_role", {
        "user_email": f"{target.email}",
        "admin": body.admin,
    })
    return {}

class InUpdateFavorite(Schema):
    favorite: bool


@router.put("/update/favorite/{board_id}/", response={200: OUTOKSchema, 403: OUTError, 404: OUTError})
def update_favorite(request: HttpRequest, board_id: UUID, body: InUpdateFavorite):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    try:
        user = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if not board.members.contains(user):
        return OUTERROR_MissingPermission
    if body.favorite:
        board.user_favorite.add(user)
    else:
        board.user_favorite.remove(user)
    return {}
