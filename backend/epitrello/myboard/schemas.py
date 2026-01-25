from uuid import UUID
from ninja import Schema
from myboard.models import Task

class OUTError(Schema):
    code: str
    message: str

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


class OUTBoardMinSchema(Schema):
    id: UUID
    title: str
    color: str


class OUTBoardsMinSchema(Schema):
    boards: list[OUTBoardMinSchema]
    owned: list[OUTBoardMinSchema]
    favorite: list[OUTBoardMinSchema]
    admin: list[OUTBoardMinSchema]


class InInvitBoardSchema(Schema):
    email: str
    admin: bool

class InCreateBoardSchema(Schema):
    title: str
    color: str

class InCreateTask(Schema):
    title: str
    description: str | None = None
    category: str
    color: str | None = None
    date_start: str | None = None
    date_end: str | None = None
    assigned: str | None = None

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

class InUpdateBoard(Schema):
    title: str | None = None
    owner: str | None = None
    color: str | None = None

class InDeleteMember(Schema):
    email: str

class InUpdateRole(Schema):
    email: str
    admin: bool

class InUpdateCategory(Schema):
    categories: list[str]

class InUpdateFavorite(Schema):
    favorite: bool
