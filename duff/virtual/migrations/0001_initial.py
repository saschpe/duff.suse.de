# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Service'
        db.create_table('virtual_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('virtual', ['Service'])

        # Adding model 'Domain'
        db.create_table('virtual_domain', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('state', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('max_memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2097152)),
            ('memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2097152)),
            ('vcpus', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('cpu_time', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('virtual', ['Domain'])

        # Adding model 'Allocation'
        db.create_table('virtual_allocation', (
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['virtual.Domain'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['virtual.Service'])),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default=0, max_length=16)),
        ))
        db.send_create_signal('virtual', ['Allocation'])


    def backwards(self, orm):
        # Deleting model 'Service'
        db.delete_table('virtual_service')

        # Deleting model 'Domain'
        db.delete_table('virtual_domain')

        # Deleting model 'Allocation'
        db.delete_table('virtual_allocation')


    models = {
        'virtual.allocation': {
            'Meta': {'ordering': "('port',)", 'object_name': 'Allocation'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['virtual.Domain']"}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['virtual.Service']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '16'})
        },
        'virtual.domain': {
            'Meta': {'ordering': "('id', 'name')", 'object_name': 'Domain'},
            'cpu_time': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'max_memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['virtual.Service']", 'through': "orm['virtual.Allocation']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'vcpus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'virtual.service': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['virtual']