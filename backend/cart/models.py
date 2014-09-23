#coding: utf-8
from django.db import models


class Cart(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now=True)
    checked_out = models.BooleanField(default=False, verbose_name='Когда сформирован заказ')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ('-creation_date',)

    def __unicode__(self):
        return u'{} от {}'.format(self.id, self.creation_date)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=u'Корзина')
    quantity = models.PositiveIntegerField(u'Количество')
    product = models.ForeignKey('catalog.Item', verbose_name=u'Изделие')
    size = models.CharField(u'Размер (только для колец)', max_length=5, null=True, blank=True, default=None)

    class Meta:
        verbose_name = u'Позиция в корзине'
        verbose_name_plural = u'Позиции в корзине'
        ordering = ('cart', '-id',)
        unique_together = ('product', 'size', 'cart')

    def save(self, *args, **kwargs):
        if self.size == u'':
            self.size = None
        super(Item, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{} штук под артикулом {} в корзине №{}'.format(self.quantity, self.product.article, self.cart_id)

