#!/usr/bin/env bash

./manage.py migrate

celery -A trellobackend worker -l INFO &
celery -A trellobackend beat -l INFO &

./manage.py test
