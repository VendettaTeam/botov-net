FROM ubuntu:18.04

ENV LANG C.UTF-8

# RHVoice block
RUN apt-get -y update
RUN apt-get install -y scons gcc git flite flite1-dev expat libunistring-dev \
libsox-dev libpulse-dev libao-dev build-essential libc6-dev g++-multilib python-lxml python3.7

RUN git clone https://github.com/Olga-Yakovleva/RHVoice

RUN cd RHVoice && scons X11=no
RUN cd RHVoice && scons install
RUN cd RHVoice && ldconfig

RUN mkdir /usr/share/RHVoice-data


# flask block
RUN apt-get install -y python3-pip
RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --deploy --system

ADD speech /code/speech