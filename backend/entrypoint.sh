#!/usr/bin/env bash

./manage.py migrate

celery -A trellobackend worker -l INFO &
celery -A trellobackend beat -l INFO &

exec daphne -b 0.0.0.0 -p 5081 trellobackend.asgi:application
