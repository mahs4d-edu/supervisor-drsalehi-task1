FROM python:3.6-alpine

LABEL MAINTAINER="Mahdi Sadeghi"

USER root

RUN ["pip", "install", "pipenv"]

ENV RABBITMQ_HOST="rabbitmq"
ENV RABBITMQ_PORT=5672

VOLUME "/data/telecrawl/sessions"

WORKDIR /app

COPY "./Pipfile*" "./"
RUN ["pipenv", "install", "--system", "--ignore-pipfile"]

COPY "." "."

WORKDIR /app/src
CMD ["python", "-u", "main.py"]
