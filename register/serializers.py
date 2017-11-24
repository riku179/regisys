from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

__all__ = [
    'ReadItemSerializer',
    'WriteItemSerializer',
    'ReadOrderSerializer',
    'WriteOrderSerializer'
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')


class _ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class ReadOrderSerializer(serializers.ModelSerializer):
    item = _ItemSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class WriteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ReadItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    orders = WriteOrderSerializer(many=True, read_only=True)

    class Meta:
        depth = 1
        model = Item
        fields = '__all__'


class WriteItemSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        for field in self.fields:
            # ownerは編集禁止
            if field != 'owner':
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance

    class Meta:
        model = Item
        fields = '__all__'
