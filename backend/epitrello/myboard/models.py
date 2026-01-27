from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import uuid
from django.db import models
from typing import final
from ordered_model.models import OrderedModel
from ordered_model.fields import OrderedManyToManyField


from myauth.models import User

# Create your models here.

COLOR_CHOICE = "#800080"

CATEGORY_LENGTH = 30
TITLE_LENGTH = 50
COLOR_LENGTH = 8

@final
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=TITLE_LENGTH)
    description = models.TextField()
    color = models.CharField(
        max_length=COLOR_LENGTH, default=COLOR_CHOICE
    )
    category = models.CharField(max_length=CATEGORY_LENGTH)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        to=User,
        related_name="task_owner_set",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    assigned = models.ForeignKey(
        to=User,
        related_name="task_assigned_set",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    completed = models.BooleanField(default=False)
    one_day_email_send = models.BooleanField(default=False)



@final
class UserConnected(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nb_connected = models.IntegerField()


@final
class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=TITLE_LENGTH)
    members = models.ManyToManyField(to=User)
    tasks = OrderedManyToManyField(to=Task, related_name="board_tasks_set", through="BoardTasksThroughModel")
    #
    archived = models.ManyToManyField(to=Task, related_name="board_archived_set")
    owner = models.ForeignKey(
        to=User, related_name="board_owner_set", on_delete=models.CASCADE
    )
    categories = ArrayField(models.CharField(max_length=CATEGORY_LENGTH), default=list)
    admin = models.ManyToManyField(to=User, related_name="board_admin_set")
    user_favorite = models.ManyToManyField(to=User, related_name="board_favorite_set")
    color = models.CharField(
        max_length=COLOR_LENGTH, default=COLOR_CHOICE
    )
    user_connected = models.ManyToManyField(to=UserConnected)


@final
class BoardTasksThroughModel(OrderedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order_with_respect_to = "board"

    class Meta:
        ordering = ("board", "order")
