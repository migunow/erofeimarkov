#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import csv
import os
import decimal
import re
import datetime
import zipfile
from django.utils import timezone

from pytils.translit import slugify

from django.db import transaction, IntegrityError
from django.conf import settings

from .models import Item, Insertion, InsertionKind, ItemCategory, ItemType, ItemSizes


def load_csv(filename):

    sizable_types = ('Кольцо',)

    now1 = datetime.datetime.now()
    parse_to_int = lambda price: int(re.sub('[^0-9]+', '', price))
    categories = list(ItemCategory.objects.values_list('id', 'name'))
    item_types = list(ItemType.objects.values_list('id', 'name'))
    insertion_types = list(InsertionKind.objects.values_list('id', 'name'))
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';'.encode('utf-8'))

        with transaction.atomic():
            Item.objects.all().update(is_deleted=True)
            for count, row in enumerate(spamreader, start=1):
                # print('строка {0}'.format(count))
                if not row:
                    # print('конец файла')
                    break
                if count == 1:
                    continue
                row = [x.decode('utf-8') for x in row]

                article = row[0]

                if not article:
                    # print('строка {0}.нет артикула. пропускаю'.format(count))
                    continue

                category = row[1]
                if not category:
                    # print('строка {0}.нет категории. пропускаю'.format(count))
                    continue
                if not any([_category[1] == category for _category in categories]):
                    # print('строка {0}.нет категории. создаю категорию "{1}"'.format(count, category))
                    new_category = ItemCategory(name=category)
                    new_category.save()
                    categories.append((new_category.id, new_category.name))

                item_type = row[2]
                if not item_type:
                    # print('строка {0}.нет такого типа изделия'.format(count))
                    continue
                if not any([_item_type[1] == item_type for _item_type in item_types]):
                    # print('строка {0}.нет такого типа. создаю тип "{1}"'.format(count, item_type))
                    new_item_type = ItemType(name=item_type)
                    new_item_type.save()
                    item_types.append((new_item_type.id, new_item_type.name))

                weight = decimal.Decimal(row[4].replace(',', '.'))
                if not row[5] or not row[6] or not row[7]:
                    # print('строка {0}.нет одной из цен. пропускаю'.format(count))
                    continue
                price_retail = parse_to_int(row[5].split(',')[0])
                price_wholesale = parse_to_int(row[6].split(',')[0])
                price_primary_wholesale = parse_to_int(row[6].split(',')[0])
                if row[8]:
                    balance = parse_to_int(row[8].split(',')[0])
                else:
                    balance = 0
                item_name = row[11]
                raw_insetion = row[10]
                try:
                    item = Item.objects.get(article=article)
                except Item.DoesNotExist:
                    item = Item()
                    item.article = article
                item.category_id = [_category[0] for _category in categories if _category[1] == category][0]
                item.type_id = [_item_type[0] for _item_type in item_types if _item_type[1] == item_type][0]
                item.weight = weight
                item.price_retail = price_retail
                item.price_wholesale = price_wholesale
                item.price_primary_wholesale = price_primary_wholesale
                item.balance = balance
                item.name = item_name
                item.is_deleted = False
                item.save()

                #удаляем все вставки
                item.iteminsertions.all().delete()

                #добавляем вставки
                if raw_insetion:
                    insertions = raw_insetion.split('#')
                    for insertion_count, insertion in enumerate(insertions, start=1):
                        raw_fields = insertion.split(',')
                        fields = dict([_field.split(':') for _field in raw_fields])
                        fields['count'] = int(fields['count'])
                        try:
                            fields['weight'] = decimal.Decimal(fields['weight'])
                        except decimal.InvalidOperation:
                            # print('строка {0}, вставка {1}.нет веса. пропускаю'.format(count, insertion_count))
                            continue

                        insertion_type = fields['type']

                        if not insertion_type:
                            # print('строка {0}, вставка {1}.пустая категории у вставки. пропускаю'.format(count, insertion_count))
                            continue
                        if not any([_insertion_type[1] == insertion_type for _insertion_type in insertion_types]):
                            # print('строка {0}, вставка {1}. создаю новую категорию для вставки'.format(count, insertion_count))
                            new_insertion_type = InsertionKind(name=insertion_type)
                            new_insertion_type.save()
                            insertion_types.append((new_insertion_type.id, new_insertion_type.name))

                        fields['kind_id'] = [_insertion_type[0] for _insertion_type in insertion_types if _insertion_type[1] == insertion_type][0]
                        fields['item_id'] = item.id
                        del fields['type']
                        new_insertion = Insertion(**fields)
                        new_insertion.save()

                # если у изделия есть размеры, то удаляем их и впоследствии создаем заново
                if item_type in sizable_types:
                    ItemSizes.objects.filter(item=item).delete()

    now2 = datetime.datetime.now()
    delta = now2 - now1
    # print(delta)

    #еще раз проходимся по файлу, чтобы добавить все размеры, за 1 проход это сделать невозможно
    
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';'.encode('utf-8'))

        with transaction.atomic():
            now = timezone.now()
            connected_items = []
            total_count = {}
            for count, row in enumerate(spamreader, start=1):
                # print('строка {0}'.format(count))
                if not row:
                    # print('конец файла')
                    break
                if count == 1:
                    continue
                row = [x.decode('utf-8') for x in row]

                article = row[0]

                if not article:
                    # print('строка {0}.нет артикула. пропускаю'.format(count))
                    continue

                category = row[1]
                if not category:
                    # print('строка {0}.нет категории. пропускаю'.format(count))
                    continue

                item_type = row[2]
                if not item_type:
                    # print('строка {0}.нет такого типа изделия'.format(count))
                    continue
                if item_type not in sizable_types:
                    continue

                if not row[3]:
                    size = ''
                else:
                    size = row[3].strip('0').strip(',')
                weight = decimal.Decimal(row[4].replace(',', '.'))
                if not row[5] or not row[6] or not row[7]:
                    # print('строка {0}.нет одной из цен. пропускаю'.format(count))
                    continue

                code = row[9]

                if row[8]:
                    balance = parse_to_int(row[8].split(',')[0])
                else:
                    balance = 0

                price_retail = parse_to_int(row[5].split(',')[0])
                price_wholesale = parse_to_int(row[6].split(',')[0])
                price_primary_wholesale = parse_to_int(row[6].split(',')[0])
                #выставляем нулевые цены в сам товар, чтобы нигде случайно не показать эту цену.
                #расчет для колец ведется в зависимости от размера
                item = Item.objects.get(article=article)

                connected_items.append(item.id)

                item_sizes = ItemSizes()
                item_sizes.item = item
                item_sizes.size = size
                item_sizes.price_retail = price_retail
                item_sizes.price_wholesale = price_wholesale
                item_sizes.price_primary_wholesale = price_primary_wholesale
                item_sizes.weight = weight
                item_sizes.code = code
                #проверим на существование
                # try:
                item_sizes.save()

                
                total_count[item] = total_count.get(item, 0) + balance

            for itemkey in total_count:
                itemkey.balance = total_count[itemkey]
                itemkey.save()
            


def attach_images(filename):
    dirname = os.path.join(settings.MEDIA_ROOT, Item.IMAGE_UPLOAD_TO).encode('utf-8')

    articles = list()
    with zipfile.ZipFile(filename, "r") as f:
        for name in f.namelist():
            try:
                if type(name) is str:
                    unicode_name = name.decode('UTF-8')
                else:
                    unicode_name = name
            except UnicodeDecodeError:
                unicode_name = name.decode('cp866')
            unicode_name = unicode_name.split('.')[:-1]
            unicode_name = '.'.join(unicode_name)
            articles.append(unicode_name)
            unicode_name = slugify(unicode_name) + '.jpg'
            unicode_name = unicode_name.encode('utf-8')
            file_name = os.path.join(dirname, unicode_name)
            f2 = open(file_name, 'w')
            f2.write(f.read(name))
            f2.close()
    f.close()

    items = Item.objects.filter(article__in=articles)
    for item in items:
        item.resize_all()
