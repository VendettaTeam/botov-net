#!/usr/bin/env bash

export $(cat .env | xargs)

if [ $(uname -s) == "MINGW64_NT-6.1" ]; then
  celery -A project.settings worker -l into -P eventlet
else
  if [[ $DJANGO_PROJECT_DEBUG == "True" ]]; then
    celery worker -A project.settings
  else
    celery worker -A project.settings -l ERROR
  fi
fi
