#coding: utf-8
from django.contrib import admin
from .models import EmailContact, SMSContact, NotificationTemplate

admin.site.register(EmailContact)
admin.site.register(SMSContact)
admin.site.register(NotificationTemplate)
