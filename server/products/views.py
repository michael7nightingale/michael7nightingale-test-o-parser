from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from chats.models import Chat
from .tasks import parse_products_task
from .models import Product
from .serializers import (
     ProductListSerializer, ProductRetrieveSerializer, ParseTaskCreateSerializer,

)


class ProductViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "product_id"

    def list(self, request, *args, **kwargs):
        chat_id = request.GET.get('chat')
        if chat_id is None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(parse_task__chat__id=chat_id).filter(
                parse_task=get_object_or_404(Chat, id=chat_id).parse_tasks.last()
            )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs) -> Serializer:
        match self.action:
            case "create":
                serializer = ParseTaskCreateSerializer
            case "list":
                serializer = ProductListSerializer
            case "retrieve":
                serializer = ProductRetrieveSerializer
            case _:
                serializer = ProductRetrieveSerializer
        return serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parse_products_task.apply_async(
            args=(serializer.validated_data.get("n"), serializer.validated_data.get("chat_id"))
        )
        return Response("Your task is started!")
