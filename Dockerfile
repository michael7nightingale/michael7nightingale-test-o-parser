FROM python:3.11

COPY bot ./bot
COPY server ./server
COPY dev.env ./dev.env
COPY requirements.txt requirements.txt

RUN #/bin/bash -c "sudo apt-get install libmysqlclient-dev"
RUN pip install mysqlclient

RUN pip install -r requirements.txt

EXPOSE 8000
