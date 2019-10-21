# botov-net
vk bot engine

#### Run in dev:
```bash
pipenv shell
./manage.py migrate
docker-compose up --build
./manage.py runserver 0.0.0.0:8000
celery worker -A project.settings
```

