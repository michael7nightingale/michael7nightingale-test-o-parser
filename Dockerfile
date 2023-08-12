FROM python:3.11-slim

COPY bot ./bot
COPY server ./server
COPY dev.env ./dev.env
COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install -y mariadb-client libmariadb3 python3-dev gcc

RUN pip install mysql\
    && pip install --upgrade pip\
    && pip install -r requirements.txt

EXPOSE 8000
