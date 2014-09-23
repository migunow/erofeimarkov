#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.contrib import admin

from .models import Cart, Item

admin.site.register(Cart)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'quantity', 'product', 'size')

admin.site.register(Item, CartItemAdmin)
