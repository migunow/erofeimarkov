#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodecsv as csv
from django.http import HttpResponse, HttpResponseNotFound
from catalog.models import *
from xml.dom.minidom import DOMImplementation
from datetime import datetime

# Create your views here.

def googleFeed(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_google_feed.csv"'

    writer = csv.writer(response, delimiter = str('|'))
    writer.writerow(['id', 'title', 'description', 'google_product_category', 'product_type', 'link', 'image_link', 'condition', 'availability', 'price'])
    for item in Item.objects.filter(is_deleted=False):
    	itemname = item.name if item.name else item.type.name
    	writer.writerow([item.id, itemname, itemname, 'Apparel & Accessories > Jewelry', item.type.name, 'http://erofeimarkov.ru' + item.get_absolute_url(), 'http://erofeimarkov.ru' + item.get_212x281_preview(), 'new', 'in stock', str(item.price_retail) + u' рублей'])

    return response

def yamarketFeed(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_yamarket_feed.csv"'

    writer = csv.writer(response, delimiter = str(';'))
    writer.writerow(['id', 'name', 'available', 'url', 'picture', 'category', 'delivery', 'price', 'currencyId',])
    for item in Item.objects.filter(is_deleted=False):
    	itemname = item.name if item.name else item.type.name
        itemprice = item.special_price if item.special and item.special_price else item.price_retail
    	writer.writerow([item.id, itemname, ['false', 'true'][item.balance>0], 'http://erofeimarkov.ru' + item.get_absolute_url(), 'http://erofeimarkov.ru' + item.get_212x281_preview(), u'Подарки и цветы/Ювелирные изделия', 'false', str(itemprice),  u'RUR'])

    return response

def wikimartFeed(req):
    imp = DOMImplementation()
    doctype = imp.createDocumentType(
        qualifiedName='yml_catalog',
        publicId='', 
        systemId='shops.dtd',
    )
    doc = imp.createDocument(None, 'yml_catalog', doctype)
    
    def createTextNode(nodeName, value):
        node = doc.createElement(nodeName)
        node.appendChild(doc.createTextNode(value))
        return node

    def createCategoryElement(category):
        el = doc.createElement("category")
        el.setAttribute("id", str(category.id))
        el.appendChild(doc.createTextNode(category.name))
        return el

    def createOfferElement(item):
        el = doc.createElement("offer")
        el.setAttribute("id", str(item.id))
        el.setAttribute("available", ['false', 'true'][item.balance>0])
        el.appendChild(createTextNode("url", "http://erofeimarkov.ru" + item.get_absolute_url()))
        el.appendChild(createTextNode("price", str(item.price_retail)))
        el.appendChild(createTextNode("picture", "http://erofeimarkov.ru" + item.get_212x281_preview()))
        el.appendChild(createTextNode("vendor", "Erofei Markov Jewelry"))
        el.appendChild(createTextNode("typePrefix", unicode(item.name if item.name else item.type.name)))
        el.appendChild(createTextNode("name", "Арт. "+item.article))
        el.appendChild(createTextNode("categoryid", str(item.type.id)))
        el.appendChild(createTextNode("currencyid", "RUR"))
        return el 

    top_element = doc.documentElement
    top_element.setAttribute("date", datetime.now().strftime("%Y-%m-%d %H:%M"))

    shops = doc.createElement('shops')
    erofeimarkovShop = doc.createElement('shop')
    erofeimarkovShop.appendChild(createTextNode("name", "Ерофей Марков"))
    erofeimarkovShop.appendChild(createTextNode("company", "Ювелирная Компания &quot;Ерофей Марков&quot;"))
    erofeimarkovShop.appendChild(createTextNode("url", "http://erofeimarkov.ru/catalog"))
    shops.appendChild(erofeimarkovShop)
    top_element.appendChild(shops)
    
    currencies = doc.createElement("currencies")
    rur = doc.createElement("currency")
    rur.setAttribute("id", "RUR")
    rur.setAttribute("rate", "1")
    currencies.appendChild(rur)
    top_element.appendChild(currencies)

    categories = doc.createElement("categories")
    for itemtype in ItemType.objects.filter():
        categories.appendChild(createCategoryElement(itemtype))

    top_element.appendChild(categories)


    offers = doc.createElement("offers")
    for item in Item.objects.filter(is_deleted=False):
        offers.appendChild(createOfferElement(item))

    top_element.appendChild(offers)
    # print doc.toprettyxml()
    response = HttpResponse(doc.toprettyxml(), content_type="text/xml")
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_wikimart_feed.xml"'
    return response
