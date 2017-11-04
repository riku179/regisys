from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    created_from = filters.DateTimeFilter(name='created_at', lookup_expr='gte')
    created_to = filters.DateTimeFilter(name='created_at', lookup_expr='lt')

    class Meta:
        model = Order
        fields = ['item', 'item__owner', 'created_from', 'created_to']
