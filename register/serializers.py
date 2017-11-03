from rest_framework import serializers
from .models import *

__all__ = [
    'ItemSerializer',
    'OrderSerializer'
]


class ItemSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        for field in self.fields:
            # userは編集禁止
            if field != 'user' or validated_data.get('user') is None:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
