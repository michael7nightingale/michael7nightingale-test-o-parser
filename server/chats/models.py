from django.db import models


class Chat(models.Model):
    """Chat model to store telegram chats."""
    id = models.CharField(unique=True, primary_key=True, max_length=100)

    objects = models.Manager()
