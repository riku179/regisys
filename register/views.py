from rest_framework import viewsets, mixins, response, status, permissions
from rest_framework.decorators import list_route
from rest_framework.request import Request
from django.db.models.deletion import ProtectedError
import re
from .serializers import *
from .models import *
from .permissions import *
from .filters import OrderFilter

__all__ = [
    'ItemViewSet',
    'OrderViewSet'
]


class ItemViewSet(viewsets.ModelViewSet):
    """
    itemのcreate/retrieve/update/deleteが可能
    itemのownerならupdate/deleteが可能
    他の人は閲覧のみ
    deleteはそのitemのorder存在していないときのみ可能
    """
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated, ItemPermission]
    filter_fields = ('owner',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadItemSerializer
        else:
            return WriteItemSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':'この商品で既に会計がされています'})
        else:
            return response.Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    orderのcreate/retrieveが可能
    adminのみcreate可能
    他の人は閲覧のみ
    """
    queryset = Order.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_class = OrderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOrderSerializer
        else:
            return WriteOrderSerializer


    @list_route()
    def aggregate(self, request: Request):
        """
        出品者毎の期間中の総売上金
        クエリパラメータfromとtoが必須('2017-01-01 01:01:01'をurlエンコードした形式)
        """
        dt_from = request.query_params.get('from')
        dt_to = request.query_params.get('to')

        if dt_from is None or dt_to is None:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':'期間を指定してください'})

        if re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', dt_from) is None \
            or re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', dt_to) is None:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':'データの形式が不正です'})

        rows = Order.objects.raw('''
        SELECT orders.id, auth_user.username, sum(orders.price * orders.quantity) AS 'sales' \
        FROM orders \
        JOIN items ON orders.item_id = items.id \
        JOIN auth_user ON items.owner_id = auth_user.id \
        WHERE created_at BETWEEN %s AND %s \
        GROUP BY items.owner_id''', [dt_from, dt_to])

        results = dict()
        for row in rows:
            results[row.username] = int(row.sales)
        import sys
        print(results, file=sys.stderr)

        return response.Response(data=results)
