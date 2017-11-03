from rest_framework import viewsets, mixins, response, status, permissions
from django.db.models.deletion import ProtectedError
from .serializers import *
from .models import *
from .permissions import *

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
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated, ItemPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
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
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
