# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.addParameter_field'
        db.add_column(u'xtreme_server_project', 'addParameter_field',
                      self.gf('django.db.models.fields.TextField')(default='Not Set'),
                      keep_default=False)

        # Adding field 'Project.addParameter'
        db.add_column(u'xtreme_server_project', 'addParameter',
                      self.gf('django.db.models.fields.TextField')(default='Not Set'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.addParameter_field'
        db.delete_column(u'xtreme_server_project', 'addParameter_field')

        # Deleting field 'Project.addParameter'
        db.delete_column(u'xtreme_server_project', 'addParameter')


    models = {
        u'xtreme_server.form': {
            'Meta': {'object_name': 'Form'},
            'auth_visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'form_action': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'form_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'form_found_on': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'form_method': ('django.db.models.fields.CharField', [], {'default': "'GET'", 'max_length': '10'}),
            'form_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_field_list': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Project']"})
        },
        u'xtreme_server.inputfield': {
            'Meta': {'object_name': 'InputField'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_type': ('django.db.models.fields.CharField', [], {'default': "'input'", 'max_length': '256', 'blank': 'True'})
        },
        u'xtreme_server.learntmodel': {
            'Meta': {'object_name': 'LearntModel'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learnt_model': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Page']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Project']"}),
            'query_id': ('django.db.models.fields.TextField', [], {})
        },
        u'xtreme_server.page': {
            'Meta': {'object_name': 'Page'},
            'URL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'auth_visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'connection_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_found_on': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Project']"}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'xtreme_server.project': {
            'Meta': {'object_name': 'Project'},
            'addParameter': ('django.db.models.fields.TextField', [], {'default': "'Not Set'"}),
            'addParameter_field': ('django.db.models.fields.TextField', [], {'default': "'Not Set'"}),
            'allowed_extensions': ('django.db.models.fields.TextField', [], {}),
            'allowed_protocols': ('django.db.models.fields.TextField', [], {}),
            'auth_mode': ('django.db.models.fields.TextField', [], {}),
            'consider_only': ('django.db.models.fields.TextField', [], {}),
            'exclude_fields': ('django.db.models.fields.TextField', [], {}),
            'login_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'logout_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.TextField', [], {}),
            'password_field': ('django.db.models.fields.TextField', [], {'default': "'Not Set'"}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'query_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'start_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Not Set'", 'max_length': '50'}),
            'username': ('django.db.models.fields.TextField', [], {}),
            'username_field': ('django.db.models.fields.TextField', [], {'default': "'Not Set'"})
        },
        u'xtreme_server.settings': {
            'Meta': {'object_name': 'Settings'},
            'allowed_extensions': ('django.db.models.fields.TextField', [], {}),
            'allowed_protocols': ('django.db.models.fields.TextField', [], {}),
            'auth_mode': ('django.db.models.fields.TextField', [], {}),
            'consider_only': ('django.db.models.fields.TextField', [], {}),
            'exclude_fields': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.TextField', [], {})
        },
        u'xtreme_server.vulnerability': {
            'Meta': {'object_name': 'Vulnerability'},
            'auth': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xtreme_server.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'msg_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            're_attack': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['xtreme_server']