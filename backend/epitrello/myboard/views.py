from uuid import UUID
import sys
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError

from myauth.middleware import require_logged
from myauth.models import User
from myboard.models import Task, Board


# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
@require_logged
def get_board(request, board_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exist")
    res = {
        "title": f"{board.title}",
        "id": f"{board.id}",
        "favorite": False, # TODO
        "members": {
            f"{member.id}": {
                "profile_picture": f"{member.profile_picture}",
                "username": f"{member.username}",
                "email": f"{member.email}",
                "owner": member.id == board.owner.id,
                "id": f"{member.id}",
            }
            for member in board.members.all()
        },
        "tasks": [
            {
                "title": f"{task.title}",
                "description": f"{task.description}",
                "color": f"{task.color}",
                "category": f"{task.category}",
                "date_start": None if task.date_start is None else f"{task.date_start}",
                "date_end": None if task.date_end is None else f"{task.date_end}",
                "date_creation": f"{task.date_creation}",
                "owner": f"{task.owner.id}",
                "assigned": None if task.assigned is None else f"{task.assigned.id}",
                "completed": task.completed,
                "id": f"{task.id}",
            }
            for task in board.tasks.all()
        ],
        "archived": [
            {
                "title": f"{task.title}",
                "description": f"{task.description}",
                "color": f"{task.color}",
                "category": f"{task.category}",
                "date_start": None if task.date_start is None else f"{task.date_start}",
                "date_end": None if task.date_end is None else f"{task.date_end}",
                "date_creation": f"{task.date_creation}",
                "owner": f"{task.owner.id}",
                "assigned": None if task.assigned is None else f"{task.assigned.id}",
                "completed": task.completed,
                "id": f"{task.id}",
            }
            for task in board.archived.all()
        ],
    }
    return JsonResponse(res)


@csrf_exempt
@require_http_methods(["POST"])
@require_logged
def invit_board_id(request, board_id: UUID):
    if request.content_type != "application/json":
        return HttpResponseBadRequest("Content-Type must be 'application/json'", content_type="text/plain")
    try:
        POST = json.loads(request.body.decode())
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        return HttpResponseBadRequest(f"Bad format for json body {e}", content_type="text/plain")
    email = POST.get("email")
    is_admin = POST.get("admin")
    if email is None or is_admin is None:
        return HttpResponseBadRequest(f"Missing '{'email' if email is None else 'admin'}' in post body", content_type="text/plain")
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exist")
    if f"{board.owner.id}" != request.session["member_id"]:
        return HttpResponseForbidden("You are not the owner of the board", content_type="text/plain")
    try:
        user: User = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404("User from email does not exists")
    board.members.add(user)
    return JsonResponse({})

@csrf_exempt
@require_http_methods(["POST"])
@require_logged
def create_board(request):
    if request.content_type != "application/json":
        return HttpResponseBadRequest("Content-Type must be 'application/json'", content_type="text/plain")
    try:
        POST = json.loads(request.body.decode())
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        return HttpResponseBadRequest(f"Bad format for json body {e}", content_type="text/plain")
    title = POST.get("title")
    if title is None:
        return HttpResponseBadRequest("Missing 'title' in post body", content_type="text/plain")
    if len(title) >= 50:
        return HttpResponseBadRequest("Too many characters in 'title' in post body", content_type="text/plain")
    try:
        owner = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        raise Http404("User does not exists")
    board = Board(title=title, owner=owner)
    board.save()
    board.members.add(owner)
    res = {
        "id": f"{board.id}"
    }
    return JsonResponse(res)

@csrf_exempt
@require_http_methods(["GET"])
@require_logged
def delete_board(request, board_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exists")
    if f"{board.owner.id}" != request.session["member_id"]:
        return HttpResponseForbidden("You are not the owner of the board", content_type="text/plain")
    board.delete()
    return JsonResponse({})


@csrf_exempt
@require_http_methods(["POST"])
@require_logged
def create_task(request, board_id: UUID):
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exists")
    if request.content_type != "application/json":
        return HttpResponseBadRequest("Content-Type must be 'application/json'", content_type="text/plain")
    try:
        POST = json.loads(request.body.decode())
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        return HttpResponseBadRequest(f"Bad format for json body {e}", content_type="text/plain")
    try:
        owner = User.objects.get(pk=request.session["member_id"])
    except User.DoesNotExist:
        raise Http404("User does not exists")
    title = POST.get("title")
    description = POST.get("description")
    category = POST.get("category")
    if title is None or description is None or category is None:
        return HttpResponseBadRequest("Missing one of 'title', 'description', or 'category'", content_type="text/plain")
    if len(title) >= 50 or len(category) >= 30:
        return HttpResponseBadRequest("Value of 'title' is more than 49 char or 'category' is more than 29", content_type="text/plain")
    optional_arg = {}
    if "color" in POST:
        optional_arg["color"] = POST.get("color")
    if "date_start" in POST:
        optional_arg["date_start"] = POST.get("date_start")
    if "date_end" in POST:
        optional_arg["date_end"] = POST.get("date_end")
    if "assigned" in POST:
        optional_arg["assigned"] = POST.get("assigned")
    try:
        task = Task(title=title, description=description, category=category, owner=owner, **optional_arg)
        task.save()
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        return HttpResponseServerError("Failed to save", content_type="text/plain")
    board.tasks.add(task)
    res = {
        "title": f"{task.title}",
        "description": f"{task.description}",
        "color": f"{task.color}",
        "category": f"{task.category}",
        "date_start": None if task.date_start is None else f"{task.date_start}",
        "date_end": None if task.date_end is None else f"{task.date_end}",
        "date_creation": f"{task.date_creation}",
        "owner": f"{task.owner.id}",
        "assigned": None if task.assigned is None else f"{task.assigned.id}",
        "completed": task.completed,
        "id": f"{task.id}",
    }
    return JsonResponse(res)


@csrf_exempt
@require_http_methods(["GET"])
@require_logged
def delete_task(request, board_id: UUID, task_id: UUID):
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exists")
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exists")
    if board.tasks.filter(pk=task_id).count() == 0:
        return HttpResponseBadRequest("Task is not in the Board tasks", content_type="text/plain")
    board.tasks.remove(task)
    board.archived.add(task)
    return JsonResponse({})


@csrf_exempt
@require_http_methods(["GET"])
@require_logged
def deleteforce_task(request, board_id: UUID, task_id: UUID):
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exists")
    try:
        board: Board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404("Board does not exists")
    if board.archived.filter(pk=task_id).count() == 0:
        return HttpResponseBadRequest("Task is not in the Board tasks", content_type="text/plain")
    board.archived.remove(task)
    task.delete()
    return JsonResponse({})


@csrf_exempt
@require_http_methods(["POST"])
@require_logged
def update_task(request, task_id: UUID):
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exists")
    if request.content_type != "application/json":
        return HttpResponseBadRequest("Content-Type must be 'application/json'", content_type="text/plain")
    try:
        POST = json.loads(request.body.decode())
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        return HttpResponseBadRequest(f"Bad format for json body {e}", content_type="text/plain")
    if "owner" in POST and task.owner is not None:
        if POST["owner"] != f"{task.owner.id}":
            if request.session["member_id"] != f"{task.owner.id}":
                return HttpResponseForbidden("Attempt to change owner but user is not the owner")
    optional_arg = []
    def set_optional(key: str):
        if key in POST:
            optional_arg.append(key)
            setattr(task, key, POST.get(key))
    set_optional("title")
    set_optional("description")
    set_optional("color")
    set_optional("category")
    set_optional("date_start")
    set_optional("date_end")
    set_optional("owner")
    set_optional("assigned")
    set_optional("completed")
    task.save(update_fields=optional_arg)
    task = Task.objects.get(pk=task.id)
    res = {
        "title": f"{task.title}",
        "description": f"{task.description}",
        "color": f"{task.color}",
        "category": f"{task.category}",
        "date_start": None if task.date_start is None else f"{task.date_start}",
        "date_end": None if task.date_end is None else f"{task.date_end}",
        "date_creation": f"{task.date_creation}",
        "owner": f"{task.owner.id}",
        "assigned": None if task.assigned is None else f"{task.assigned.id}",
        "completed": task.completed,
        "id": f"{task.id}",
    }
    return JsonResponse(res)
