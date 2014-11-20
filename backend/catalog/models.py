#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import json
import os

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from pytils.translit import slugify

from PIL import Image, ImageOps


class ItemCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория изделия'
        verbose_name_plural = 'Категории изделий'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип')
    sizes = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Тип изделия'
        verbose_name_plural = 'Типы изделий'
        ordering = ('name',)

    def get_sizes(self):
        if not self.sizes:
            return []
        else:
            return self.sizes.split(';')
    
    def get_sizes_serialized(self):
        return json.dumps(self.get_sizes)

    def __unicode__(self):
        return self.name


class InsertionKind(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'тип вставки'
        verbose_name_plural = 'типы вставок'

    def __unicode__(self):
        return self.name


class ItemFields(models.Model):
    """
    Общие поля для позиции и для колец. Для каждого кольца своя цена в зависимости от размера и свой штрихкод
    """
    price_retail = models.PositiveIntegerField('Розничная цена')
    price_wholesale = models.PositiveIntegerField('Оптовая цена')
    price_primary_wholesale = models.PositiveIntegerField('Первичная оптовая цена')

    weight = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Вес')
    code = models.CharField('Штрихкод', max_length=50, blank=True)

    class Meta:
        abstract = True


class Item(ItemFields):
    name = models.CharField(max_length=100, verbose_name='Название', blank=True, null=True)
    article = models.CharField(max_length=50, verbose_name='Артикул', unique=True, db_index=True)
    category = models.ForeignKey(ItemCategory, verbose_name='Категория')
    type = models.ForeignKey(ItemType, verbose_name='Тип')
    IMAGE_UPLOAD_TO = 'items'
    # image = models.ImageField(upload_to=IMAGE_UPLOAD_TO, blank=True, null=True, verbose_name='Фотография')
    relatedItems = models.ManyToManyField('self', blank=True, verbose_name='С этим изделием покупают')
    new = models.BooleanField(default=False, verbose_name='Новинка')
    balance = models.PositiveIntegerField('Остаток', default=0)
    sorting_order = models.PositiveIntegerField(default=500)
    is_deleted = models.BooleanField('Удален из каталога',default=False)
    special = models.BooleanField(verbose_name="Акция", default=False)
    special_price = models.PositiveIntegerField(verbose_name="Акционная цена", default=0)

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ('sorting_order', '-balance',)

    def __unicode__(self):
        return self.article

    def get_full_name(self):
        return '{} <br> <span style="font-size:15px;text-transform: none;">Арт. {}</span>'.format(self.name or self.category.name, self.article)

    def get_absolute_url(self):
        return reverse('catalog:item', kwargs={'item_id': str(self.id)})

    def preview(self, width, height):
        dimensions_folder = '{0}x{1}'.format(width, height)
        path_to_thumbnail_dir = os.path.join('/media', self.IMAGE_UPLOAD_TO, 'thumbnails', dimensions_folder)
        return '{0}/{1}.jpg'. format(path_to_thumbnail_dir, slugify(self.article)).encode('utf-8')

    def get_212x281_preview(self):
        return self.preview(212, 281)

    def get_60x60_preview(self):
        return self.preview(60, 60)

    def get_512x512_preview(self):
        return self.preview(512, 512)

    def resize_all(self):
        """
        сжималка при загрузке новых картинок
        """
        self.resize(212, 281)
        self.resize(60, 60)
        self.resize(512, 512)

    def resize(self, width, height, dowatermark=False):
        """
        Создает превьюхи для изображений
        """
        dimensions_folder = '{0}x{1}'.format(width, height)
        #проверяем, что существует папка с превьюхами
        path_to_thumbnail_dir = os.path.join(
            settings.MEDIA_ROOT, self.IMAGE_UPLOAD_TO, 'thumbnails', dimensions_folder).encode('utf-8')
        if not os.path.exists(path_to_thumbnail_dir):
            os.makedirs(path_to_thumbnail_dir)

        original_path = os.path.join(settings.MEDIA_ROOT, self.IMAGE_UPLOAD_TO)
        original_filename = '{0}/{1}.jpg'.format(original_path, slugify(self.article)).encode('utf-8')
        try:
            image = Image.open(original_filename)
        except IOError:
            # print('Image not found')
            return
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        if dowatermark:
            wm = Image.open(settings.WATERMARK_PATH)
            wmsize = image.size[0]/2
            if wmsize < 100:
                wmsize = 100
            wm.thumbnail((wmsize, wmsize), Image.ANTIALIAS)
            image.paste(wm, (image.size[0]/2-wm.size[0]/2, image.size[1]/2-wm.size[1]/2), wm)
        path_to_thumbnail = '{0}/{1}.jpg'.format(path_to_thumbnail_dir, slugify(self.article)).encode('utf-8')
        image.save(path_to_thumbnail, "JPEG", quality=100)


class ItemSizes(ItemFields):
    """
    Существует только для колец. В зависимости от размера кольца разные цены, штрихкод и вес
    """
    when_created = models.DateTimeField('Время создания', auto_now=True)
    item = models.ForeignKey('Item')
    size = models.CharField('Размер', max_length=5)

    class Meta:
        verbose_name = 'Размер кольца'
        verbose_name_plural = 'Размеры колец'
        ordering = ('item', 'size')
        unique_together = ('item', 'size')

    def __unicode__(self):
        return unicode(self.id)


class ItemSet(models.Model):
    items = models.ManyToManyField(Item, verbose_name='изделия')

    class Meta:
        verbose_name = 'гарнитур'
        verbose_name_plural = 'гарнитуры'


class Insertion(models.Model):
    item = models.ForeignKey(Item, verbose_name='Изделие', related_name='iteminsertions')
    kind = models.ForeignKey(InsertionKind, verbose_name='Тип вставки')
    count = models.IntegerField(blank=True, null=True, verbose_name='Количество вставок')
    weight = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Вес')
    description = models.CharField('Описание', max_length=100, blank=True)

    class Meta:
        verbose_name = 'вставка'
        verbose_name_plural = 'вставки'

    def __unicode__(self):
        return self.kind.name


class FileUploader(models.Model):
    UPLOAD_TO_CSV = 'csv'
    UPLOAD_TO_IMAGES = 'images'
    my_csv = models.FileField('Каталог в csv', upload_to=UPLOAD_TO_CSV, blank=True)
    my_images = models.FileField('Архив с изображениями', upload_to=UPLOAD_TO_IMAGES, blank=True)

    class Meta:
        verbose_name = '_ЗАГРУЗКА КАТАЛОГА_'
        verbose_name_plural = '_ЗАГРУЗКА КАТАЛОГА_'

    def __unicode__(self):
        return 'ЗАГРУЗИТЬ'

    def save(self, *args, **kwargs):
        super(FileUploader, self).save(args, kwargs)
        from catalog.load_csv import load_csv, attach_images
        if self.my_csv:
            load_csv(self.my_csv.file.name)
        if self.my_images:
            attach_images(self.my_images.file.name)
