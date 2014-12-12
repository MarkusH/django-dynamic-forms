# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FormModel.recipient_email'
        db.add_column(u'dynamic_forms_formmodel', 'recipient_email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FormModel.recipient_email'
        db.delete_column(u'dynamic_forms_formmodel', 'recipient_email')


    models = {
        u'dynamic_forms.formfieldmodel': {
            'Meta': {'ordering': "[u'parent_form', u'position']", 'unique_together': "((u'parent_form', u'name'),)", 'object_name': 'FormFieldModel'},
            '_options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'parent_form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'fields'", 'to': u"orm['dynamic_forms.FormModel']"}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'dynamic_forms.formmodel': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'FormModel'},
            'actions': ('dynamic_forms.fields.TextMultiSelectField', [], {'default': "u''"}),
            'allow_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'form_template': ('django.db.models.fields.CharField', [], {'default': "u'dynamic_forms/form.html'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'recipient_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'submit_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'success_template': ('django.db.models.fields.CharField', [], {'default': "u'dynamic_forms/form_success.html'", 'max_length': '100'}),
            'success_url': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'})
        },
        u'dynamic_forms.formmodeldata': {
            'Meta': {'object_name': 'FormModelData'},
            'display_key': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': 'None', 'max_length': '24', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'data'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['dynamic_forms.FormModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'})
        }
    }

    complete_apps = ['dynamic_forms']