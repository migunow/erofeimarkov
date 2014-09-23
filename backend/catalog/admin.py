#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.contrib import admin
from catalog.models import *


class InsertionAdmin(admin.TabularInline):
    model = Insertion


class SizesAdmin(admin.TabularInline):
    model = ItemSizes


class ItemAdmin(admin.ModelAdmin):
    list_display = ('article', 'category', 'type', 'price_retail', 'price_wholesale', 'price_primary_wholesale',)
    list_filter = ('category', 'type', 'new',)
    search_fields = ('=article',)
    inlines = (InsertionAdmin, SizesAdmin,)
    filter_horizontal = ('relatedItems',)


class ItemSetAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)


class ItemSizesAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'size', 'price_retail', 'price_wholesale', 'price_primary_wholesale', 'weight', 'code',)


class FileUploaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'my_csv', 'my_images',)


admin.site.register(ItemCategory)
admin.site.register(ItemType)
admin.site.register(Item, ItemAdmin)
admin.site.register(InsertionKind)
admin.site.register(ItemSet, ItemSetAdmin)
admin.site.register(ItemSizes, ItemSizesAdmin)
admin.site.register(FileUploader, FileUploaderAdmin)
admin.site.register(Insertion)
