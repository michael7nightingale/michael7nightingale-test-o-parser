from rest_framework import serializers

from .models import Chat


class ChatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', )
