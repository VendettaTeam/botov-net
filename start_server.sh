#!/usr/bin/env bash

export $(cat .env | xargs)
./manage.py runserver 0.0.0.0:8000