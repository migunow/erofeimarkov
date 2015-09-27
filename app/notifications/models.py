# -*- coding: utf-8 -*-
from django.db import models


class EmailContact(models.Model):
    email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = "E-mail адрес для оповещений"
        verbose_name_plural = "E-mail адреса для оповещений"


class SMSContact(models.Model):
    phoneno = models.CharField(max_length=15)

    def __unicode__(self):
        return self.phoneno

    class Meta:
        verbose_name = "Номер для СМС-оповещений"
        verbose_name_plural = "Номера для СМС-оповещений"


class NotificationTemplate(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name=u"Название")

    use_sms =  models.BooleanField(default=False, verbose_name=u"Оповещать через смс")
    sms_template = models.TextField(blank=True, verbose_name=u"Шаблон смс",
                                    help_text=u"Поддерживает простое форматирование: параметры обернутые в фигурные скобки будут заменены соответствующими значениями (например, {phone})")

    use_email = models.BooleanField(verbose_name=u"Оповещть через e-mail")
    email_subject = models.CharField(max_length=255, blank=True, verbose_name="Тема письма",
                                     help_text=u"Поддерживает простое форматирование")
    email_from = models.CharField(max_length=255, blank=True, verbose_name="Адрес отправителя",
                                  help_text=u"Человекочитаемое имя <username@example.com>",
                                  default="Erofeimarkov.ru <noreply@erofeimarkov.ru>")
    email_template = models.TextField(blank=True, verbose_name="Шаблон письма",
                                     help_text=u"Поддерживает расширенное форматирование (django-шаблон)")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Шаблон оповещений"
        verbose_name_plural = u"Шаблоны оповещений"
