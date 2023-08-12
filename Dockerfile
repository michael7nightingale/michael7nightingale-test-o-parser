FROM python:3.11

COPY bot ./bot
COPY server ./server
COPY dev.env ./dev.env
COPY requirements.txt requirements.txt

RUN apt update
RUN apt-get install -y wget sudo
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo apt install -y -f ./google-chrome-stable_current_amd64.deb

RUN --mount=type=cache,target=/root/.cache/pip pip install pyyaml
RUN pip install -r requirements.txt --default-timeout=700

EXPOSE 8000
