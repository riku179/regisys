from rest_framework import viewsets, mixins, response, status, permissions
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
    deleteはそのitemのorderが発生していないときのみ可能
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.orders:
            return response.Response(status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_destroy(instance)
            return response.Response(status.HTTP_204_NO_CONTENT)


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
