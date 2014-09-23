#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):

    def fullname(self, obj):
        return '%s' % obj.customer.get_full_name()

    fullname.short_description = 'Полное имя'
    readonly_fields = ('id', 'customer', 'checkout_date')
    list_display = ('id', 'customer', 'checkout_date')
    list_filter = ('checkout_date', 'processed')
    search_fields = ('=id', '=customer__username', 'customer__first_name', 'customer__last_name')
    fields = ('id', 'customer', 'name', 'phone', 'address', 'comment', 'checkout_date', 'processed')

admin.site.register(Order, OrderAdmin)