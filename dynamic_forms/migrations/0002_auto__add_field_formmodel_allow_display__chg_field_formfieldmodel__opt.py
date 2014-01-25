# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FormModel.allow_display'
        db.add_column('dynamic_forms_formmodel', 'allow_display',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'FormFieldModel._options'
        db.alter_column('dynamic_forms_formfieldmodel', '_options', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'FormModelData.display_key'
        db.add_column('dynamic_forms_formmodeldata', 'display_key',
                      self.gf('django.db.models.fields.CharField')(blank=True, db_index=True, null=True, unique=True, max_length=24, default=None),
                      keep_default=False)


        # Changing field 'FormModelData.submitted'
        db.alter_column('dynamic_forms_formmodeldata', 'submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting field 'FormModel.allow_display'
        db.delete_column('dynamic_forms_formmodel', 'allow_display')


        # Changing field 'FormFieldModel._options'
        db.alter_column('dynamic_forms_formfieldmodel', '_options', self.gf('django.db.models.fields.TextField')())
        # Deleting field 'FormModelData.display_key'
        db.delete_column('dynamic_forms_formmodeldata', 'display_key')


        # Changing field 'FormModelData.submitted'
        db.alter_column('dynamic_forms_formmodeldata', 'submitted', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'dynamic_forms.formfieldmodel': {
            'Meta': {'object_name': 'FormFieldModel', 'unique_together': "(('parent_form', 'name'),)", 'ordering': "['parent_form', 'position']"},
            '_options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '50'}),
            'parent_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dynamic_forms.FormModel']", 'related_name': "'fields'"}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'blank': 'True', 'default': '0'})
        },
        'dynamic_forms.formmodel': {
            'Meta': {'object_name': 'FormModel', 'ordering': "['name']"},
            'actions': ('dynamic_forms.fields.TextMultiSelectField', [], {'default': "''"}),
            'allow_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'form_template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'dynamic_forms/form.html'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'submit_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'success_template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'dynamic_forms/form_success.html'"}),
            'success_url': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"})
        },
        'dynamic_forms.formmodeldata': {
            'Meta': {'object_name': 'FormModelData'},
            'display_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True', 'unique': 'True', 'max_length': '24', 'default': 'None'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['dynamic_forms.FormModel']", 'related_name': "'data'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        }
    }

    complete_apps = ['dynamic_forms']