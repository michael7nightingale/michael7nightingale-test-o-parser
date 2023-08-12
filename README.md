<h1 align='center'>Ozone Products Parser</h1>

This is DRF based API for parsing products of the seller at Ozone online marketplace.
Frontend is the telegram bot, which notifies you when parsing task is finished.


<h2 align='center'>Stack</h2>
- `Python 3.11`;
- `Django 4.2`;
- `DRF 3.14`;
- `Celery`;
- `PostgreSQL`;
- `bs4`;
- `aiogram`;
- `django-adminlte2`;


<h2 align='center'>Project structure</h2>
- server: django project root;
  - core: django configuration application;
  - api: base api application to include api urls from other apps;
  - chats: application to register chat on chat`s id;
  - products: products application (parser tasks and products);
  - service: other logic package (parser and telegram);
  

- bot: telegram bot application;
  - main.py: bot entry point;
  - handlers.py: bot handlers;
  - keyboards.py: bot keyboards factories;
  - parsers.py: response content parsers for messages;
  - connector.py: requests api functions;



<h2 align='center'>Running</h2>
Run the application and all the integrations using docker:
```commandline
docker-compose up -d --build
```

If you have windows installed as OS, you shall need 4 terminal windows:

### 1)
First of all run redis using https://github.com/redis-windows/redis-windows/releases or ...:
```commandline
docker run redis:5
```

### 2)
Run django application:
```commandline
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 3)
Run celery worker(-s):
```commandline
celery -A server.core worker -l info --pool=solo
```

### 4)
Run Telegram bot:
```commandline
cd bot
python main.py
```