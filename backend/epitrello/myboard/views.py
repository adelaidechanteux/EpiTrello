from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from myauth.middleware import require_logged
from myboard.models import Task, Board

# Create your views here.

@require_http_methods(["GET"])
@require_logged
def board_id(request, board_id: str):
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
            }
            for member in board.members
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
            for task in board.tasks
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
            for task in board.archived
        ],
    }
    return JsonResponse(res)
