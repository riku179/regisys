from django.db import models
from django.contrib.auth.models import User

__all__ = [
    'Item',
    'Order'
]


# User (Django標準) -< Item -< Order の関係

class Item(models.Model):
    name = models.CharField('商品名', max_length=255)
    price = models.PositiveIntegerField('価格')
    member_price = models.PositiveIntegerField('部員価格')
    quantity = models.PositiveIntegerField('数量')

    owner = models.ForeignKey(User, verbose_name='出品者', related_name='items', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items'


class Order(models.Model):
    price = models.PositiveIntegerField('価格')
    quantity = models.PositiveIntegerField('数量')
    created_at = models.DateTimeField('決済日', auto_now_add=True)

    item = models.ForeignKey('Item', verbose_name='商品', related_name='orders', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.item.name} x{self.quantity}'

    class Meta:
        db_table = 'orders'
