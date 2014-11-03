#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodecsv as csv
from django.http import HttpResponse, HttpResponseNotFound
from catalog.models import *

# Create your views here.

def googleFeed(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_google_feed.csv"'

    writer = csv.writer(response, delimiter ='|')
    writer.writerow(['id', 'title', 'description', 'google_product_category', 'product_type', 'link', 'image_link', 'condition', 'availability', 'price'])
    for item in Item.objects.all():
    	itemname = item.name if item.name else item.type.name
    	writer.writerow([item.id, itemname, itemname, 'Apparel & Accessories > Jewelry', item.type.name, 'http://erofeimarkov.ru' + item.get_absolute_url(), 'http://erofeimarkov.ru' + item.get_212x281_preview(), 'new', 'in stock', str(item.price_retail) + u' рублей'])

    return response

def yamarketFeed(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_yamarket_feed.csv"'

    writer = csv.writer(response, delimiter =';')
    writer.writerow(['id', 'name', 'available', 'url', 'picture', 'category', 'delivery', 'price', 'currencyId',])
    for item in Item.objects.all():
    	itemname = item.name if item.name else item.type.name
    	writer.writerow([item.id, itemname, 'true', 'http://erofeimarkov.ru' + item.get_absolute_url(), 'http://erofeimarkov.ru' + item.get_212x281_preview(), u'Подарки и цветы/Ювелирные изделия', 'true', str(item.price_retail),  u'RUR'])

    return response

def wikimartFeed(req):
    return HttpResponseNotFound('Not implemented yet')