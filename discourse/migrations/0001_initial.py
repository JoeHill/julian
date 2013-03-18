# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Note'
        db.create_table('discourse_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prioritya', self.gf('django.db.models.fields.TextField')(default='')),
            ('priorityb', self.gf('django.db.models.fields.TextField')(default='')),
            ('priorityc', self.gf('django.db.models.fields.TextField')(default='')),
            ('priorityd', self.gf('django.db.models.fields.TextField')(default='')),
            ('prioritye', self.gf('django.db.models.fields.TextField')(default='')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('discourse', ['Note'])

        # Adding model 'Discourse'
        db.create_table('discourse_discourse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('discourse', ['Discourse'])

        # Adding model 'Node'
        db.create_table('discourse_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('discourse', ['Node'])

        # Adding model 'EdgeType'
        db.create_table('discourse_edgetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('discourse', ['EdgeType'])

        # Adding model 'Edge'
        db.create_table('discourse_edge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_node_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('to_node_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('edge_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discourse.EdgeType'])),
            ('discourse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discourse.Discourse'])),
            ('note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discourse.Note'])),
        ))
        db.send_create_signal('discourse', ['Edge'])


    def backwards(self, orm):
        # Deleting model 'Note'
        db.delete_table('discourse_note')

        # Deleting model 'Discourse'
        db.delete_table('discourse_discourse')

        # Deleting model 'Node'
        db.delete_table('discourse_node')

        # Deleting model 'EdgeType'
        db.delete_table('discourse_edgetype')

        # Deleting model 'Edge'
        db.delete_table('discourse_edge')


    models = {
        'discourse.discourse': {
            'Meta': {'object_name': 'Discourse'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'discourse.edge': {
            'Meta': {'object_name': 'Edge'},
            'discourse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discourse.Discourse']"}),
            'edge_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discourse.EdgeType']"}),
            'from_node_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discourse.Note']"}),
            'to_node_id': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'discourse.edgetype': {
            'Meta': {'object_name': 'EdgeType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'discourse.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'discourse.note': {
            'Meta': {'object_name': 'Note'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prioritya': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityb': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityd': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'prioritye': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['discourse']
