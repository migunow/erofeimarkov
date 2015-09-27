# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailContact'
        db.create_table(u'notifications_emailcontact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'notifications', ['EmailContact'])

        # Adding model 'SMSContact'
        db.create_table(u'notifications_smscontact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phoneno', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'notifications', ['SMSContact'])


    def backwards(self, orm):
        # Deleting model 'EmailContact'
        db.delete_table(u'notifications_emailcontact')

        # Deleting model 'SMSContact'
        db.delete_table(u'notifications_smscontact')


    models = {
        u'notifications.emailcontact': {
            'Meta': {'object_name': 'EmailContact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'notifications.smscontact': {
            'Meta': {'object_name': 'SMSContact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phoneno': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['notifications']