from django.contrib import admin

from myboard.models import Board, Task, UserConnected, BoardTasksThroughModel

# Register your models here.

admin.site.register(Board)
admin.site.register(Task)
admin.site.register(UserConnected)
admin.site.register(BoardTasksThroughModel)
