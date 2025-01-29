from typing import Any, Dict, List

from rest_framework import serializers
from .models import Order, OrderStatus


class OrderStatusSerializer(serializers.ModelSerializer[OrderStatus]):
    class Meta:
        model = OrderStatus
        fields = ['id', 'name', 'description']


class ItemSerializer(serializers.Serializer[Dict[str, Any]]):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer[Order]):
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']

    total_price = serializers.DecimalField(required=False,
                                           allow_null=True,
                                           default=None,
                                           max_digits=10,
                                           decimal_places=2)

    def validate_items(self, value: List[Dict[str, Any]]) -> Any:
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list of dictionaries.")
        for item in value:
            if 'price' not in item:
                raise serializers.ValidationError("Each item must have a 'price' field.")
        return value

    def create(self, validated_data: Dict[str, Any]) -> Any:
        items = validated_data.get('items', [])
        validated_data['total_price'] = sum(item['price'] for item in items)
        return super().create(validated_data)

    def update(self, instance: Any, validated_data: Dict[str, Any]) -> Any:
        if 'items' in validated_data:
            items = validated_data['items']
            instance.total_price = sum(item['price'] for item in items)
        return super().update(instance, validated_data)