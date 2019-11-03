# botov-net
vk bot engine

#### Run in dev:
```bash
pipenv shell
cp .env.sample .env
./manage.py migrate
docker-compose up --build
./manage.py runserver 0.0.0.0:8000
./manage.py search_index --rebuild

unix:
    celery worker -A project.settings
win:
    celery -A project.settings worker -l into -P eventlet

```

