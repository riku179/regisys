from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, base_name='item')
router.register(r'orders', OrderViewSet, base_name='order')

urlpatterns = router.urls
