#coding: utf-8
from django.contrib import admin
from .models import EmailContact, SMSContact

admin.site.register(EmailContact)
admin.site.register(SMSContact)
