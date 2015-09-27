# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotificationTemplate'
        db.create_table(u'notifications_notificationtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('use_sms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sms_template', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('use_email', self.gf('django.db.models.fields.BooleanField')()),
            ('email_subject', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email_from', self.gf('django.db.models.fields.CharField')(default='Erofeimarkov.ru <noreply@erofeimarkov.ru>', max_length=255, blank=True)),
            ('email_template', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'notifications', ['NotificationTemplate'])


    def backwards(self, orm):
        # Deleting model 'NotificationTemplate'
        db.delete_table(u'notifications_notificationtemplate')


    models = {
        u'notifications.emailcontact': {
            'Meta': {'object_name': 'EmailContact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'notifications.notificationtemplate': {
            'Meta': {'object_name': 'NotificationTemplate'},
            'email_from': ('django.db.models.fields.CharField', [], {'default': "'Erofeimarkov.ru <noreply@erofeimarkov.ru>'", 'max_length': '255', 'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'sms_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'use_email': ('django.db.models.fields.BooleanField', [], {}),
            'use_sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'notifications.smscontact': {
            'Meta': {'object_name': 'SMSContact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phoneno': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['notifications']