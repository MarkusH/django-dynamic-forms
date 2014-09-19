# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormModel'
        db.create_table(u'dynamic_forms_formmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('submit_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('success_url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('actions', self.gf('dynamic_forms.fields.TextMultiSelectField')(default='')),
            ('form_template', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('success_template', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'dynamic_forms', ['FormModel'])

        # Adding model 'FormFieldModel'
        db.create_table(u'dynamic_forms_formfieldmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['dynamic_forms.FormModel'])),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('_options', self.gf('django.db.models.fields.TextField')(default='{}', blank=True)),
            ('position', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'dynamic_forms', ['FormFieldModel'])

        # Adding unique constraint on 'FormFieldModel', fields ['parent_form', 'name']
        db.create_unique(u'dynamic_forms_formfieldmodel', ['parent_form_id', 'name'])

        # Adding model 'FormModelData'
        db.create_table(u'dynamic_forms_formmodeldata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='data', null=True, on_delete=models.SET_NULL, to=orm['dynamic_forms.FormModel'])),
            ('value', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'dynamic_forms', ['FormModelData'])


    def backwards(self, orm):
        # Removing unique constraint on 'FormFieldModel', fields ['parent_form', 'name']
        db.delete_unique(u'dynamic_forms_formfieldmodel', ['parent_form_id', 'name'])

        # Deleting model 'FormModel'
        db.delete_table(u'dynamic_forms_formmodel')

        # Deleting model 'FormFieldModel'
        db.delete_table(u'dynamic_forms_formfieldmodel')

        # Deleting model 'FormModelData'
        db.delete_table(u'dynamic_forms_formmodeldata')


    models = {
        u'dynamic_forms.formfieldmodel': {
            'Meta': {'ordering': "['position']", 'unique_together': "(('parent_form', 'name'),)", 'object_name': 'FormFieldModel'},
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            '_options': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'parent_form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['dynamic_forms.FormModel']"}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'dynamic_forms.formmodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'FormModel'},
            'actions': ('dynamic_forms.fields.TextMultiSelectField', [], {'default': "''"}),
            'form_template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'submit_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'success_template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'success_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        u'dynamic_forms.formmodeldata': {
            'Meta': {'object_name': 'FormModelData'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['dynamic_forms.FormModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        }
    }

    complete_apps = ['dynamic_forms']