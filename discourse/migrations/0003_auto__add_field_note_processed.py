# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Note.processed'
        db.add_column('discourse_note', 'processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Note.processed'
        db.delete_column('discourse_note', 'processed')


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
            'identifier': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'prioritya': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityb': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'priorityd': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'prioritye': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['discourse']