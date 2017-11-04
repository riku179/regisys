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


class ReadOrderSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
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
            # userは編集禁止
            if field != 'user' or validated_data.get('user') is None:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))

    class Meta:
        model = Item
        fields = '__all__'
