from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import uuid
from django.db import models

from myauth.models import User

# Create your models here.

COLOR_CHOICES = [
    ("#800080", "Purple"),
    ("#FF69B4", "Pink"),
]

CATEGORY_LENGTH = 30


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(
        max_length=7, choices=COLOR_CHOICES, default=COLOR_CHOICES[0][0]
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
    position_index = models.IntegerField()


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(to=User)
    tasks = models.ManyToManyField(to=Task, related_name="board_tasks_set")
    archived = models.ManyToManyField(to=Task, related_name="board_archived_set")
    owner = models.ForeignKey(
        to=User, related_name="board_owner_set", on_delete=models.CASCADE
    )
    categories = ArrayField(models.CharField(max_length=CATEGORY_LENGTH), default=list)
    admin = models.ManyToManyField(to=User, related_name="board_admin_set")
