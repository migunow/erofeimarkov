#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodecsv as csv
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from django.views.decorators.http import condition
from catalog.models import *
from catalog.utils import CustomPaginator, CustomItem, CustomItemSize
from xml.dom.minidom import DOMImplementation
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

DESCRIPTION_RE_FORM = unicode(r"(?P<form>Кр|Круг|Г|Груша|П|Принцесса|М|Маркиз|И|Изумруд|Овал|Квадрат|Багет|Цитрин|Оникс|Пр)(?:[\. \-]+(?:55|56|57|65))?")
DESCRIPTION_RE_OGR = unicode(r"(?P<ogr>\d/\d{1,2})")
DESCRIPTION_RE = re.compile(u"(?:%s)?[ ]*%s?" % (DESCRIPTION_RE_FORM, DESCRIPTION_RE_OGR))
INSERTION_FORMS = {
    "Кр": "Круг",
    "Г": "Грушевидный",
    "П": "Принцесса",
    "М": "Маркиз",
    "И": "Изумруд",
    "Пр": "Прямоугольник"
}

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

def brilshopFeed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_brilshop_feed.csv"'

    categories = {}
    for itemtype in ItemType.objects.all():
        categories[itemtype.id] = itemtype.name

    def gen_row(item, available, price=None, size=None):
        insertions = list(item.iteminsertions.all())

        buffer = []
        buffer.append(unicode(item.name if item.name else item.type.name) + " из золота 585 пробы.")
        if len(insertions) == 1:
            buffer.append(" Вставка: ")
        elif len(insertions):
            buffer.append(" Вставки: ")
        description_parts = []
        short_desc_parts = []
        for insertion in insertions:
            short_desc_re = DESCRIPTION_RE.match(insertion.description.strip())
            short_desc = []
            short_desc.append(insertion.kind.name.title())
            short_desc.append(str(insertion.count))
            short_desc.append(str(insertion.weight))
            if short_desc_re:
                ngroups = short_desc_re.groupdict()
                ogr = ngroups.get("ogr", None) or ""
                if ogr:
                    short_desc.append(ogr)
                form = (ngroups.get("form", None) or "").title()
                if form:
                    short_desc.append(INSERTION_FORMS.get(form, form))
            else:
                logger.error("Cannot parse description: " + insertion.description)
                short_desc = []
            if short_desc:
                short_desc_parts.append(" ".join(short_desc))

            description_part = unicode(insertion.kind.name).lower()
            if insertion.count > 1:
                description_part += " в количестве %d штук" % insertion.count
            if insertion.weight > 0:
                description_part += " общим весом %s грамм" % insertion.weight
            description_parts.append(description_part)
        if len(description_parts):
            buffer.append(", ".join(description_parts))
            buffer.append(".")
        description = "".join(buffer)
        short_description = ",".join(short_desc_parts)

        price = price or CustomItem(item, request.user).price()
        return [item.article, categories[item.type.id], item.weight, price,
                short_description, "", "Красное", str(size or ""), "585", "",
                description, available]

    writer = csv.writer(response, delimiter = str(';'))
    writer.writerow(["Артикул", "Категория", "Вес", "Цена", "Вставки", "Гарнитур", "Цвет",
                     "Размер", "Проба", "Коллекция", "Описание", "Наличие"])
    for item in Item.objects.filter(is_deleted=False)\
                            .prefetch_related("itemsizes_set")\
                            .prefetch_related("iteminsertions"):
        all_sizes = item.type.get_sizes()

        price = None
        if all_sizes:
            available_sizes = dict ((itemsize.size, CustomItemSize(itemsize, request.user))
                                    for itemsize in item.itemsizes_set.all())
            for size in all_sizes:
                price = item.balance > 0 and size in available_sizes and available_sizes[size].price() or None
                available = "1" if size in available_sizes else "0"
                writer.writerow(gen_row(item, available, price, size))
        else:
            available = "1" if item.balance>0 else "0"
            writer.writerow(gen_row(item, available))

    return response

def genWikimartFeed(request):

    def createTextNode(nodeName, value):
        return '<{0}>{1}</{0}>\n'.format(nodeName, value)

    def createCategoryElement(category):
        return '<category id="{0}">{1}</category>\n'.format(category.id, category.name)

    def createParamElement(name, value, unit=None):
        template = u'<param name="{0}"{2}>{1}</param>\n'
        if unit:
            unit = u' unit="{0}"'.format(unit)
        else:
            unit = u""
        node = template.format(name, value, unit)
        return node

    def createOfferElement(item, size=None, available=None, price=None, retail_price=None):
        buffer = []

        buffer.append(createTextNode("currencyId", "RUR"))
        buffer.append(createTextNode("categoryId", str(item.type.id)))
        buffer.append(createTextNode("picture", "http://erofeimarkov.ru" + item.get_212x281_preview()))
        buffer.append(createTextNode("delivery", "true"))
        buffer.append(createTextNode("typePrefix", unicode(item.name if item.name else item.type.name)))
        buffer.append(createTextNode("vendor", "Erofei Markov Jewelry"))

        buffer.append(createTextNode("model", "Арт. " + item.article))

        buffer.append("<description>")

        insertions = list(item.iteminsertions.all())
        buffer.append(unicode(item.name if item.name else item.type.name) + " из золота 585 пробы.")
        if len(insertions) == 1:
            buffer.append(" Вставка: ")
        elif len(insertions):
            buffer.append(" Вставки: ")
        description_parts = []
        for insertion in insertions:
            description_part = unicode(insertion.kind.name).lower()
            if insertion.count > 1:
                description_part += " в количестве %d штук" % insertion.count
            if insertion.weight > 0:
                description_part += " общим весом %s грамм" % insertion.weight
            description_parts.append(description_part)
        buffer.append(", ".join(description_parts))
        if len(insertions):
            buffer.append(".")
        buffer.append('</description>\n')

        buffer.append(createParamElement("Материал, проба", "Золото (пр. 585)"))

        insertions = set([ins.kind.name for ins in insertions])
        for insertion in insertions:
            buffer.append(createParamElement("Вставка", insertion))
        buffer.append(createParamElement("Вес", item.weight, unit="г"))  # вес в граммах


        return "".join(buffer)


    # 1. generate doctype
    # 2. generate yml tag
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    buffer = []
    buffer.append('<?xml version="1.0" encoding="utf-8"?>')
    buffer.append('<!DOCTYPE yml_catalog SYSTEM "shops.dtd">')
    buffer.append('<yml_catalog date="{0}">\n'.format(timestamp))
    yield "\n".join(buffer)

    # 3. generate shops tag
    buffer = []
    buffer.append("<shop>\n")
    buffer.append(createTextNode("name", "Ерофей Марков"))
    buffer.append(createTextNode("company", "Ювелирная Компания &quot;Ерофей Марков&quot;"))
    buffer.append(createTextNode("url", "http://erofeimarkov.ru/catalog"))

    # 3.1. create currencies tag
    buffer.append("<currencies>")
    buffer.append('<currency id="{0}" rate="{1}"/>'.format("RUR", "1"))
    buffer.append("</currencies>\n")

    # 3.2. create categories element
    buffer.append('<categories>\n')
    for itemtype in ItemType.objects.filter():
        buffer.append(createCategoryElement(itemtype))
    buffer.append('</categories>\n')

    yield "".join(buffer)


    # 6. create offers element
    yield "<offers>\n"
    for item in Item.objects.filter(is_deleted=False).prefetch_related("itemsizes_set").prefetch_related("iteminsertions"):
        all_sizes = item.type.get_sizes()
        available_sizes = dict ((itemsize.size, CustomItemSize(itemsize, request.user))
                                for itemsize in item.itemsizes_set.all())
        base_offer = createOfferElement(item)
        for size in all_sizes:
            buffer = []
            available = size in available_sizes
            price = available and available_sizes[size].price() or None
            retail_price = available_sizes[size].item.price_retail if size in available_sizes else None
            item_id = str(item.id) if size is None else str(item.id) + "s" + str(size).replace(",", "d")
            available = available and 'true' or 'false'

            buffer.append('<offer id="{0}" available="{1}" type="vendor.model">\n'.format(item_id, available))
            url = "http://erofeimarkov.ru" + item.get_absolute_url(size=size)
            buffer.append(createTextNode("url", url))
            item_price = str(price or CustomItem(item, request.user).price()).replace(",", ".")
            buffer.append(createTextNode("price", item_price))
            #if retail_price and str(retail_price) != item_price:
            #    buffer.append(createTextNode("oldprice", str(retail_price).replace(",", ".")))
            buffer.append(base_offer)
            if size:
                buffer.append(createParamElement("Размер", str(size).replace(",", ".")))
            buffer.append('</offer>\n')
            yield "".join(buffer)
        if not all_sizes:
            available = ['false', 'true'][item.balance>0]
            url = "http://erofeimarkov.ru" + item.get_absolute_url()
            item_price = CustomItem(item, request.user).price()
            retail_price = CustomItem(item, request.user).price_retail()
            buffer = []
            buffer.append('<offer id="{0}" available="{1}">\n'.format(item_id, available))
            buffer.append(createTextNode("url", url))
            buffer.append(createTextNode("price", item_price))
            buffer.append(base_offer)
            #if retail_price and str(retail_price) != item_price:
            #    buffer.append(createTextNode("oldprice", str(retail_price)))
            buffer.append('</offer>\n')
            yield "".join(buffer)
    buffer = []
    buffer.append('</offers>\n')
    buffer.append("\n</shop>\n")
    buffer.append('</yml_catalog>')
    yield "\n".join(buffer)


#@condition(etag_func=None)
def wikimartFeed(request):
    #response = StreamingHttpResponse(genWikimartFeed(request), content_type="text/xml")
    response = HttpResponse("".join(genWikimartFeed(request)), content_type="text/xml")
    response['Content-Disposition'] = 'attachment; filename="erofeimarkov_wikimart_feed.xml"'
    return response
