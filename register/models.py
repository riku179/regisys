from django.db import models
from django.contrib.auth.models import User

# User (Django標準) -< Item -< Order の関係

class Item(models.Model):
    name = models.CharField('商品名', max_length=255)
    price = models.PositiveIntegerField('価格')
    member_price = models.IntegerField('部員価格')
    quantity = models.PositiveIntegerField('数量')

    user = models.ForeignKey(User, verbose_name='出品者', related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return '商品'


class Order(models.Model):
    is_member_price = models.BooleanField('部員価格適用', default=False)
    quantity = models.PositiveIntegerField('数量')
    created_at = models.DateTimeField('決済日', auto_now_add=True)

    item = models.ForeignKey('Item', verbose_name='商品', related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return '会計'
