FROM python:2.7

RUN mkdir -p /app
ADD gremlins /app/gremlins
ADD setup.py  /app/setup.py

WORKDIR /app
RUN python setup.py develop

VOLUME /app/gremlins/profiles
