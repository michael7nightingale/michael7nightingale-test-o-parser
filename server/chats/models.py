from django.db import models


class Chat(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=100)

    objects = models.Manager()
