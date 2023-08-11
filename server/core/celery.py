from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = Celery()
application.config_from_object("django.conf:settings", namespace="CELERY")
application.autodiscover_tasks()
