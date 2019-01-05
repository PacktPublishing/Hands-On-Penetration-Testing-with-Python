# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'xtreme_server_project', (
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('start_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('query_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('allowed_extensions', self.gf('django.db.models.fields.TextField')()),
            ('allowed_protocols', self.gf('django.db.models.fields.TextField')()),
            ('consider_only', self.gf('django.db.models.fields.TextField')()),
            ('exclude_fields', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='Not Set', max_length=50)),
            ('login_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('logout_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.TextField')()),
            ('password', self.gf('django.db.models.fields.TextField')()),
            ('username_field', self.gf('django.db.models.fields.TextField')(default='Not Set')),
            ('password_field', self.gf('django.db.models.fields.TextField')(default='Not Set')),
            ('auth_mode', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'xtreme_server', ['Project'])

        # Adding model 'Page'
        db.create_table(u'xtreme_server_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('URL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auth_visited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status_code', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('connection_details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Project'])),
            ('page_found_on', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'xtreme_server', ['Page'])

        # Adding model 'Form'
        db.create_table(u'xtreme_server_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Project'])),
            ('form_found_on', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('form_name', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('form_method', self.gf('django.db.models.fields.CharField')(default='GET', max_length=10)),
            ('form_action', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('form_content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('auth_visited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('input_field_list', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'xtreme_server', ['Form'])

        # Adding model 'InputField'
        db.create_table(u'xtreme_server_inputfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Form'])),
            ('input_type', self.gf('django.db.models.fields.CharField')(default='input', max_length=256, blank=True)),
        ))
        db.send_create_signal(u'xtreme_server', ['InputField'])

        # Adding model 'Vulnerability'
        db.create_table(u'xtreme_server_vulnerability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Form'])),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('re_attack', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('project', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('timestamp', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('msg_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('msg', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('auth', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'xtreme_server', ['Vulnerability'])

        # Adding model 'Settings'
        db.create_table(u'xtreme_server_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allowed_extensions', self.gf('django.db.models.fields.TextField')()),
            ('allowed_protocols', self.gf('django.db.models.fields.TextField')()),
            ('consider_only', self.gf('django.db.models.fields.TextField')()),
            ('exclude_fields', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.TextField')()),
            ('password', self.gf('django.db.models.fields.TextField')()),
            ('auth_mode', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'xtreme_server', ['Settings'])

        # Adding model 'LearntModel'
        db.create_table(u'xtreme_server_learntmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Project'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Page'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xtreme_server.Form'])),
            ('query_id', self.gf('django.db.models.fields.TextField')()),
            ('learnt_model', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'xtreme_server', ['LearntModel'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'xtreme_server_project')

        # Deleting model 'Page'
        db.delete_table(u'xtreme_server_page')

        # Deleting model 'Form'
        db.delete_table(u'xtreme_server_form')

        # Deleting model 'InputField'
        db.delete_table(u'xtreme_server_inputfield')

        # Deleting model 'Vulnerability'
        db.delete_table(u'xtreme_server_vulnerability')

        # Deleting model 'Settings'
        db.delete_table(u'xtreme_server_settings')

        # Deleting model 'LearntModel'
        db.delete_table(u'xtreme_server_learntmodel')


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