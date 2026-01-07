from uuid import UUID
from ninja import Router, Schema
from django.http import HttpRequest, HttpResponse
from collections import OrderedDict

from myboard.models import Board, Task
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


class OUTOKSchema(Schema):
    ok: bool = True


@router.get("/get/board/{board_id}/", response={200: OUTBoardSchema, 404: OUTError})
def get_board(request: HttpRequest, board_id: UUID):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    return board


class OUTBoardMinSchema(Schema):
    id: UUID
    title: str


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
    permissions = [f"{x.id}" for x in board.admin.all()] + [f"{board.owner.id}"]
    if request.session["member_id"] not in permissions:
        return OUTERROR_MissingPermission
    try:
        user = User.objects.get(email=body.email)
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    board.members.add(user)
    if body.admin:
        board.admin.add(user)
    return {}

class InCreateBoardSchema(Schema):
    title: str

@router.post("/create/board/", response={200: OUTBoardSchema, 400: OUTError, 404: OUTError})
def create_board(request: HttpRequest, body: InCreateBoardSchema):
    try:
        user: User = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        return OUTERROR_UserDoesNotExists
    if len(body.title) >= 50:
        return OUTERROR_BadValue
    board = Board(title=body.title, owner=user)
    board.save()
    board.members.add(user)
    return board


@router.put("/delete/board/{board_id}/", response={200: OUTOKSchema, 403: OUTError, 404: OUTError})
def delete_board(request: HttpRequest, board_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    permissions = [f"{board.owner.id}"]
    if request.session["member_id"] not in permissions:
        return OUTERROR_MissingPermission
    board.delete()
    return {}


class InCreateTask(Schema):
    title: str
    description: str
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
    permissions = [f"{x.id}" for x in board.members.all()]
    if f"{user.id}" not in permissions:
        return OUTERROR_MissingPermission
    if len(body.title) >= 50 or len(body.category) >= 30:
        return OUTERROR_BadValue
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
    categories = set(board.categories)
    categories.add(f"{task.category}")
    board.categories = list(categories)
    board.save(update_fields=["categories"])
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
    permissions = [f"{x.id}" for x in board.members.all()]
    if f"{user.id}" not in permissions:
        return OUTERROR_MissingPermission
    if board.tasks.filter(pk=task.id).distinct().count() == 0:
        return OUTERROR_TaskIsInvalid
    board.tasks.remove(task)
    board.archived.add(task)
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
    permissions = [f"{x.id}" for x in board.admin.all()] + [f"{board.owner.id}"]
    if f"{user.id}" not in permissions:
        return OUTERROR_MissingPermission
    if board.archived.filter(pk=task.id).distinct().count() == 0:
        return OUTERROR_TaskIsInvalid
    board.archived.remove(task)
    task.delete()
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
    permissions = [f"{x.id}" for x in board.members.all()]
    if f"{user.id}" not in permissions:
        return OUTERROR_MissingPermission
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
    permissions = [f"{x.id}" for x in board.admin.all()] + [f"{board.owner.id}"]
    if f"{user.id}" not in permissions:
        return OUTERROR_MissingPermission
    if body.owner is not None:
        if body.owner != f"{board.owner.id}":
            if request.session["member_id"] != f"{board.owner.id}":
                return OUTERROR_MissingPermission
            try:
                _ = User.objects.get(pk=body.owner)
            except User.DoesNotExist:
                return OUTERROR_UserDoesNotExists
    optional_arg: list[str] = []
    for key in ("title", "owner", "color"):
        if getattr(body, key) is not None:
            setattr(board, key, getattr(body, key))
            optional_arg.append(key)
    board.save(update_fields=optional_arg)
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
    permission_admin = [f"{x.id}" for x in board.admin.all()]
    permission_owner = [f"{board.owner.id}"]
    if f"{user.id}" not in (permission_admin + permission_owner):
        return OUTERROR_MissingPermission
    if f"{target.id}" in permission_owner:
        return OUTERROR_BadValue
    if f"{user.id}" in permission_admin and f"{target.id}" in permission_admin:
        return OUTERROR_MissingPermission
    board.members.remove(target)
    if f"{target.id}" in permission_admin:
        board.admin.remove(target)
    return board


class InUpdateCategory(Schema):
    categories: list[str]


@router.put("/update/categories/{board_id}/", response={200: OUTBoardSchema, 400: OUTError, 404: OUTError})
def update_categories(request: HttpRequest, board_id: UUID, body: InUpdateCategory):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return OUTERROR_BoardDoesNotExists
    categories_present = set([f"{x.category}" for x in board.tasks.all()])
    if not all([x in body.categories for x in categories_present]):
        return OUTERROR_BadValue
    board.categories = list(OrderedDict.fromkeys(body.categories))
    board.save(update_fields=["categories"])
    return board
