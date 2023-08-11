FROM python:3.11

COPY bot ./bot
COPY server ./server
COPY dev.env ./dev.env
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000
