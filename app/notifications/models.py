#coding: utf-8
from django.db import models


class EmailContact(models.Model):
    email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.email


class SMSContact(models.Model):
    phoneno = models.CharField(max_length=15)

    def __unicode__(self):
        return self.phoneno
