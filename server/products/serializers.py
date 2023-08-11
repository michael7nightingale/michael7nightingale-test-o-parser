from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, ParseTask


class ProductCreateSerializer(serializers.ModelSerializer):

    def validated_discount(self, value: int) -> int:
        if not (0 <= value < 100):
            raise ValidationError(f"Discount {value} is not in integer range [0; 100).")
        return value

    def validated_price(self, value: int) -> int:
        if not value > 0:
            raise ValidationError(f"Price mus be positive.")
        return value

    class Meta:
        model = Product
        fields = ('id', "price", "title", "discount")


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ParseTaskCreateSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1, max_value=50, default=10)
    chat_id = serializers.CharField()
