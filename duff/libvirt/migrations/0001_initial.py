# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table('libvirt_domain', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('state', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('max_memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2097152)),
            ('memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2097152)),
            ('vcpus', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('cpu_time', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('libvirt', ['Domain'])

        # Adding model 'Interface'
        db.create_table('libvirt_interface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['libvirt.Domain'])),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['libvirt.Network'])),
            ('mac_address', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('libvirt', ['Interface'])

        # Adding model 'Network'
        db.create_table('libvirt_network', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('bridge_name', self.gf('django.db.models.fields.CharField')(default='virbr0', max_length=16)),
            ('forward_mode', self.gf('django.db.models.fields.CharField')(default='nat', max_length=32)),
            ('domain_name', self.gf('django.db.models.fields.CharField')(default='duff.suse.de', max_length=256)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('persistent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('libvirt', ['Network'])


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table('libvirt_domain')

        # Deleting model 'Interface'
        db.delete_table('libvirt_interface')

        # Deleting model 'Network'
        db.delete_table('libvirt_network')


    models = {
        'libvirt.domain': {
            'Meta': {'ordering': "('id', 'name')", 'object_name': 'Domain'},
            'cpu_time': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'max_memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2097152'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['libvirt.Network']", 'through': "orm['libvirt.Interface']", 'symmetrical': 'False'}),
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
            'domain_name': ('django.db.models.fields.CharField', [], {'default': "'duff.suse.de'", 'max_length': '256'}),
            'forward_mode': ('django.db.models.fields.CharField', [], {'default': "'nat'", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'persistent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['libvirt']