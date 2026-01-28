import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trellobackend.settings")


app = Celery("trellobackend", broker="redis://valkey")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # every 4 hours.
    sender.add_periodic_task(
        30,
        send_email_task_near_date_end.s(),
        name="check tasks that are near the end and send an email to the assignee or the owner.",
    )


@app.task(bind=True, ignore_result=True)
def send_email_task_near_date_end(self):
    print(f"Request1")
    from myboard.models import Task
    from django.utils import timezone
    from django.conf import settings
    from django.core.mail import send_mail
    from datetime import timedelta

    nb_send = 0
    tasks = Task.objects.filter(
        date_end__gte=(timezone.now() + timedelta(days=1)), one_day_email_send=False
    )
    for task in tasks:
        target = task.assigned if task.assigned is not None else task.owner
        if target is None:
            continue
        boards = task.board_tasks_set.all()
        if len(boards) == 0:
            continue
        send_mail(
            "EpiTrello | A Task is near the End",
            f"The task '{task.title}' in the board '{boards[0].title}' that is assigned to you, is supposed to finish in 1 day.",
            settings.EMAIL_SENDER,
            [f"{target.email}"],
        )
        task.one_day_email_send = True
        task.save(update_fields=["one_day_email_send"])
        nb_send += 1
    print(f"Request2: {nb_send}")
