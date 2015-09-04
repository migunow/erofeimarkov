#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodecsv as csv
from django.http import HttpResponse, HttpResponseNotFound
from catalog.models import *
from catalog.utils import CustomPaginator, CustomItem, CustomItemSize
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
        itemprice = CustomItem(item, req.user).price()
        writer.writerow([item.id, itemname, ['false', 'true'][item.balance>0], 'http://erofeimarkov.ru' + item.get_absolute_url(), 'http://erofeimarkov.ru' + item.get_212x281_preview(), u'Подарки и цветы/Ювелирные изделия', 'false', str(itemprice),  u'RUR'])

    return response

def wikimartFeed(request):
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

    def createParamElement(name, value, unit=None):
        node = doc.createElement("param")
        node.setAttribute("name", name)
        if unit:
            node.setAttribute("unit", unit)
        node.appendChild(doc.createTextNode(unicode(value)))
        return node

    def createOfferElement(item, size=None, available=None, price=None, retail_price=None):
        el = doc.createElement("offer")
        item_id = str(item.id) if size is None else str(item.id) + "s" + str(size).replace(",", "d")
        el.setAttribute("id", item_id)
        if available is None:
            el.setAttribute("available", ['false', 'true'][item.balance>0])
        else:
            el.setAttribute("available", available and 'true' or 'false')
        el.appendChild(createTextNode("url", "http://erofeimarkov.ru" + item.get_absolute_url(size=size)))
        item_price = str(price or CustomItem(item, request.user).price())
        el.appendChild(createTextNode("price", item_price))
        if retail_price and str(retail_price) != item_price:
            el.appendChild(createTextNode("oldprice", str(retail_price)))
        if size:
            el.appendChild(createParamElement("Размер", size))
        el.appendChild(createParamElement("Вес", item.weight, unit="г"))  # вес в граммах
        #el.appendChild(createParamElement("Цвет", "желтый"))  # вот это так-то ересь, нужно поправить
        insertions = list(item.iteminsertions.all())
        description = unicode(item.name if item.name else item.type.name) + " из золота 585 пробы."
        if len(insertions) == 1:
            description += " Вставка: "
        elif len(insertions):
            description += " Вставки: "
        description_parts = []
        for insertion in insertions:
            description_part = unicode(insertion.kind.name).lower()
            if insertion.count > 1:
                description_part += " в количестве %d штук" % insertion.count
            if float(insertion.weight) > 0:
                description_part += " общим весом %s грамм" % insertion.weight
            description_parts.append(description_part)
        description += ", ".join(description_parts)
        if len(insertions):
            description += "."

        el.appendChild(createTextNode("description", description))
        el.appendChild(createParamElement("Материал, проба", "Золото (пр. 585)"))
        insertions = set([ins.kind.name for ins in item.iteminsertions.all()])

        for insertion in insertions:
            el.appendChild(createParamElement("Вставка", insertion))

        el.appendChild(createTextNode("picture", "http://erofeimarkov.ru" + item.get_212x281_preview()))
        el.appendChild(createTextNode("vendor", "Erofei Markov Jewelry"))
        el.appendChild(createTextNode("typePrefix", unicode(item.name if item.name else item.type.name)))
        el.appendChild(createTextNode("name", "Арт. " + item.article))
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
        all_sizes = item.type.get_sizes()
        available_sizes = dict ((itemsize.size, CustomItemSize(itemsize, request.user)) for itemsize in item.itemsizes_set.all())
        for size in all_sizes:
            available = size in available_sizes
            price = available and available_sizes[size].price() or None
            retail_price = available_sizes[size].item.price_retail if size in available_sizes else None
            offers.appendChild(
                createOfferElement(item, size=size, price=price, retail_price=retail_price, available=available))
        if not all_sizes:
            offers.appendChild(createOfferElement(item))

    top_element.appendChild(offers)
    response = HttpResponse(doc.toprettyxml(), content_type="text/xml")
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_wikimart_feed.xml"'
    return response
