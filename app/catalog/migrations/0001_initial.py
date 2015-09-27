# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemCategory'
        db.create_table(u'catalog_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'catalog', ['ItemCategory'])

        # Adding model 'ItemType'
        db.create_table(u'catalog_itemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sizes', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['ItemType'])

        # Adding model 'InsertionKind'
        db.create_table(u'catalog_insertionkind', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'catalog', ['InsertionKind'])

        # Adding model 'Item'
        db.create_table(u'catalog_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price_retail', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_wholesale', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_primary_wholesale', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ItemCategory'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ItemType'])),
            ('new', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('balance', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sorting_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=500)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('special_price', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'catalog', ['Item'])

        # Adding M2M table for field relatedItems on 'Item'
        m2m_table_name = db.shorten_name(u'catalog_item_relatedItems')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_item', models.ForeignKey(orm[u'catalog.item'], null=False)),
            ('to_item', models.ForeignKey(orm[u'catalog.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_item_id', 'to_item_id'])

        # Adding model 'ItemSizes'
        db.create_table(u'catalog_itemsizes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price_retail', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_wholesale', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_primary_wholesale', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Item'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'catalog', ['ItemSizes'])

        # Adding unique constraint on 'ItemSizes', fields ['item', 'size']
        db.create_unique(u'catalog_itemsizes', ['item_id', 'size'])

        # Adding model 'ItemSet'
        db.create_table(u'catalog_itemset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'catalog', ['ItemSet'])

        # Adding M2M table for field items on 'ItemSet'
        m2m_table_name = db.shorten_name(u'catalog_itemset_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemset', models.ForeignKey(orm[u'catalog.itemset'], null=False)),
            ('item', models.ForeignKey(orm[u'catalog.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['itemset_id', 'item_id'])

        # Adding model 'Insertion'
        db.create_table(u'catalog_insertion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'iteminsertions', to=orm['catalog.Item'])),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.InsertionKind'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Insertion'])

        # Adding model 'FileUploader'
        db.create_table(u'catalog_fileuploader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('my_csv', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('my_images', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['FileUploader'])


    def backwards(self, orm):
        # Removing unique constraint on 'ItemSizes', fields ['item', 'size']
        db.delete_unique(u'catalog_itemsizes', ['item_id', 'size'])

        # Deleting model 'ItemCategory'
        db.delete_table(u'catalog_itemcategory')

        # Deleting model 'ItemType'
        db.delete_table(u'catalog_itemtype')

        # Deleting model 'InsertionKind'
        db.delete_table(u'catalog_insertionkind')

        # Deleting model 'Item'
        db.delete_table(u'catalog_item')

        # Removing M2M table for field relatedItems on 'Item'
        db.delete_table(db.shorten_name(u'catalog_item_relatedItems'))

        # Deleting model 'ItemSizes'
        db.delete_table(u'catalog_itemsizes')

        # Deleting model 'ItemSet'
        db.delete_table(u'catalog_itemset')

        # Removing M2M table for field items on 'ItemSet'
        db.delete_table(db.shorten_name(u'catalog_itemset_items'))

        # Deleting model 'Insertion'
        db.delete_table(u'catalog_insertion')

        # Deleting model 'FileUploader'
        db.delete_table(u'catalog_fileuploader')


    models = {
        u'catalog.fileuploader': {
            'Meta': {'object_name': 'FileUploader'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my_csv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'my_images': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'catalog.insertion': {
            'Meta': {'object_name': 'Insertion'},
            'count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'iteminsertions'", 'to': u"orm['catalog.Item']"}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.InsertionKind']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'})
        },
        u'catalog.insertionkind': {
            'Meta': {'object_name': 'InsertionKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'catalog.itemset': {
            'Meta': {'object_name': 'ItemSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalog.Item']", 'symmetrical': 'False'})
        },
        u'catalog.itemsizes': {
            'Meta': {'ordering': "(u'item', u'size')", 'unique_together': "((u'item', u'size'),)", 'object_name': 'ItemSizes'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Item']"}),
            'price_primary_wholesale': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_retail': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_wholesale': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'catalog.itemtype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'ItemType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sizes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['catalog']