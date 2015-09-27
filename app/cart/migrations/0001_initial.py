# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cart'
        db.create_table(u'cart_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cart', ['Cart'])

        # Adding model 'Item'
        db.create_table(u'cart_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Item'])),
            ('size', self.gf('django.db.models.fields.CharField')(default=None, max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal(u'cart', ['Item'])

        # Adding unique constraint on 'Item', fields ['product', 'size', 'cart']
        db.create_unique(u'cart_item', ['product_id', 'size', 'cart_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Item', fields ['product', 'size', 'cart']
        db.delete_unique(u'cart_item', ['product_id', 'size', 'cart_id'])

        # Deleting model 'Cart'
        db.delete_table(u'cart_cart')

        # Deleting model 'Item'
        db.delete_table(u'cart_item')


    models = {
        u'cart.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cart.item': {
            'Meta': {'ordering': "('cart', '-id')", 'unique_together': "(('product', 'size', 'cart'),)", 'object_name': 'Item'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Item']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'catalog.item': {
            'Meta': {'ordering': "(u'sorting_order', u'-balance')", 'object_name': 'Item'},
            'article': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'balance': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemCategory']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_primary_wholesale': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_retail': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_wholesale': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relatedItems': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'relatedItems_rel_+'", 'blank': 'True', 'to': u"orm['catalog.Item']"}),
            'sorting_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '500'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'special_price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemType']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'})
        },
        u'catalog.itemcategory': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'ItemCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'catalog.itemtype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'ItemType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sizes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['cart']