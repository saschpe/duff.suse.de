# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Allocation'
        db.create_table('libvirt_allocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['libvirt.Domain'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['libvirt.Service'])),
            ('running', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('libvirt', ['Allocation'])

        # Adding model 'Service'
        db.create_table('libvirt_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('protocol', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('libvirt', ['Service'])


    def backwards(self, orm):
        # Deleting model 'Allocation'
        db.delete_table('libvirt_allocation')

        # Deleting model 'Service'
        db.delete_table('libvirt_service')


    models = {
        'libvirt.allocation': {
            'Meta': {'ordering': "('domain', 'service')", 'object_name': 'Allocation'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['libvirt.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['libvirt.Service']"})
        },
        'libvirt.domain': {
            'Meta': {'ordering': "('id', 'name')", 'object_name': 'Domain'},
            'cpu_time': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'max_memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['libvirt.Network']", 'through': "orm['libvirt.Interface']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['libvirt.Service']", 'through': "orm['libvirt.Allocation']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'vcpus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'libvirt.interface': {
            'Meta': {'ordering': "('domain', 'mac_address')", 'object_name': 'Interface'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['libvirt.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['libvirt.Network']"})
        },
        'libvirt.network': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Network'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bridge_name': ('django.db.models.fields.CharField', [], {'default': "'virbr0'", 'max_length': '16'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'forward_mode': ('django.db.models.fields.CharField', [], {'default': "'nat'", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'persistent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'libvirt.service': {
            'Meta': {'ordering': "('port', 'name')", 'object_name': 'Service'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'protocol': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['libvirt']