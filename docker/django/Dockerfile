FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
COPY manage.py /code

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system

ADD project /code/project