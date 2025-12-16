from uuid import UUID
import sys
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponseForbidden

from myauth.middleware import require_logged
from myauth.models import User
from myboard.models import Task, Board


# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
@require_logged
def board_id(request, board_id: UUID):
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
                "class": f"{task.category}",
                "date_start": f"{task.date_start}",
                "date_end": f"{task.date_end}",
                "date_creation": f"{task.date_creation}",
                "owner": f"{task.owner.id}",
                "assigned": f"{task.assigned.id}",
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
                "class": f"{task.category}",
                "date_start": f"{task.date_start}",
                "date_end": f"{task.date_end}",
                "date_creation": f"{task.date_creation}",
                "owner": f"{task.owner.id}",
                "assigned": f"{task.assigned.id}",
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
