#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    customer = models.ForeignKey(User, verbose_name="Пользователь", null=True, blank=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.CharField('Адрес', max_length=250, blank=True)
    cart = models.ForeignKey('cart.Cart', editable=False)
    checkout_date = models.DateTimeField(verbose_name="Дата заказа", auto_now_add=True)
    processed = models.BooleanField(default=False, verbose_name="Обработан")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
