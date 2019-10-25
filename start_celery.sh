#!/usr/bin/env bash

export $(cat .env | xargs)

if [ $(uname -s) == "MINGW64_NT-6.1" ]
then
  celery -A project.settings worker -l into -P eventlet
else
  celery worker -A project.settings
fi
