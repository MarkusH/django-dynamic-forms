# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION
from django.contrib.auth.models import User
from django.test import TestCase
# TODO: Django >1.4:
# from django.utils.html import format_html, format_html_join
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from django.utils.translation import ugettext as _

from dynamic_forms.formfields import dynamic_form_field_registry as dffr
from dynamic_forms.models import FormModel, FormFieldModel, FormModelData


def get_fields_html():
    # TODO: Django >1.4:
    # reutrn format_html_join('\n', '<option value="{0}">{1}</option>',
    #     (df for df in dffr.get_as_choices()))
    return mark_safe(
        '\n'.join(
            '<option value="{0}">{1}</option>'.format(
                conditional_escape(df[0]),
                conditional_escape(df[1])
            )
            for df in dffr.get_as_choices()
        )
    )


class TestAdmin(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin',
            password='password', email='admin@localhost')
        self.client.login(username='admin', password='password')

    def tearDown(self):
        self.client.logout()

    def test_add_form(self):
        response = self.client.get('/admin/dynamic_forms/formmodel/add/')
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '<input type="hidden" value="3" name="fields-TOTAL_FORMS" id="id_fields-TOTAL_FORMS">', count=1, html=True)
        self.assertContains(response, '<input type="hidden" value="0" name="fields-INITIAL_FORMS" id="id_fields-INITIAL_FORMS">', count=1, html=True)

        # 3 extra forms + 1 empty for construction
        # TODO: Django >1.4: assertInHTML
        if VERSION < (1, 7):
            self.assertContains(response, 'Form Field:', count=4, html=False)
        else:
            self.assertContains(response, 'Form field:', count=4, html=False)

        # 3 extra forms + 1 empty for construction
        # don't use html=True as we don't care about the <select>-Tag
        self.assertContains(response, get_fields_html(), count=4)

        # 3 extra forms + 1 empty for construction
        self.assertContains(response, _('The options for this field will be '
            'available once it has been stored the first time.'), count=4)

    def test_change(self):
        form = FormModel.objects.create(name='Form', submit_url='/some-form/')
        response = self.client.get('/admin/dynamic_forms/formmodel/%d/' % form.pk)
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '<input type="hidden" value="3" name="fields-TOTAL_FORMS" id="id_fields-TOTAL_FORMS">', count=1, html=True)
        self.assertContains(response, '<input type="hidden" value="0" name="fields-INITIAL_FORMS" id="id_fields-INITIAL_FORMS">', count=1, html=True)

        # 3 extra forms + 1 empty for construction
        # TODO: Django >1.4: assertInHTML
        if VERSION < (1, 7):
            self.assertContains(response, 'Form Field:', count=4, html=False)
        else:
            self.assertContains(response, 'Form field:', count=4, html=False)

        # 3 extra forms + 1 empty for construction
        # don't use html=True as we don't care about the <select>-Tag
        self.assertContains(response, get_fields_html(), count=4)

        # 3 extra forms + 1 empty for construction
        self.assertContains(response, _('The options for this field will be '
            'available once it has been stored the first time.'), count=4)

    def test_add_and_change_post(self):
        data = {
            'name': 'Some Name',
            'submit_url': '/form/',
            'success_url': '/done/form/',
            'actions': 'dynamic_forms.actions.dynamic_form_send_email',
            'form_template': 'template1.html',
            'success_template': 'template2.html',

            'fields-TOTAL_FORMS': 1,
            'fields-INITIAL_FORMS': 0,
            'fields-MAX_NUM_FORMS': 1000,

            'fields-0-field_type': 'dynamic_forms.formfields.SingleLineTextField',
            'fields-0-label': 'String Field',
            'fields-0-name': 'string-field',
            'fields-0-position': 0,
            '_save': True,
        }
        response = self.client.post('/admin/dynamic_forms/formmodel/add/', data)
        self.assertRedirects(response, '/admin/dynamic_forms/formmodel/')
        self.assertEqual(FormModel.objects.all().count(), 1)
        self.assertEqual(FormFieldModel.objects.all().count(), 1)

        form_pk = FormModel.objects.get().pk
        field_pk = FormFieldModel.objects.get().pk

        data = {
            'name': 'Some Name',
            'submit_url': '/form/',
            'success_url': '/done/form/',
            'actions': 'dynamic_forms.actions.dynamic_form_send_email',
            'form_template': 'template1.html',
            'success_template': 'template2.html',

            'fields-TOTAL_FORMS': 1,
            'fields-INITIAL_FORMS': 1,
            'fields-MAX_NUM_FORMS': 1000,

            'fields-0-field_type': 'dynamic_forms.formfields.SingleLineTextField',
            'fields-0-label': 'String Field',
            'fields-0-name': 'string-field',
            'fields-0-position': 0,
            'fields-0-_options_0': 'Some help text',
            'fields-0-_options_1': 100,
            'fields-0-_options_2': 5,
            'fields-0-_options_3': 3,  # No
            'fields-0-id': field_pk,
            'fields-0-parent_form': form_pk,
            '_save': True,
        }
        response = self.client.post('/admin/dynamic_forms/formmodel/%d/' % form_pk, data)
        self.assertRedirects(response, '/admin/dynamic_forms/formmodel/')
        self.assertEqual(FormModel.objects.all().count(), 1)
        self.assertEqual(FormFieldModel.objects.all().count(), 1)

        options = FormFieldModel.objects.get().options
        self.assertEqual(options, {
            'min_length': 5, 
            'help_text': 'Some help text',
            'max_length': 100, 
            'required': False
        })

    def test_change_with_fields(self):
        form = FormModel.objects.create(name='Form', submit_url='/some-form/')
        ffb = FormFieldModel.objects.create(parent_form=form, label='B',
            field_type='dynamic_forms.formfields.BooleanField', position=0)
        ffb.options = {'help_text': 'Some help for boolean'}
        ffb.save()
        ffsl = FormFieldModel.objects.create(parent_form=form, label='SL',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            position=1)
        ffsl.options = {
            'help_text': 'Some help for single line',
            'required': False,
            'max_length': 100,
        }
        ffsl.save()
        ffd = FormFieldModel.objects.create(parent_form=form, label='D',
            field_type='dynamic_forms.formfields.DateField', position=2)
        ffd.options = {
            'localize': True,
        }
        ffd.save()

        response = self.client.get('/admin/dynamic_forms/formmodel/%d/' % form.pk)
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '<input type="hidden" value="6" name="fields-TOTAL_FORMS" id="id_fields-TOTAL_FORMS">', count=1, html=True)
        self.assertContains(response, '<input type="hidden" value="3" name="fields-INITIAL_FORMS" id="id_fields-INITIAL_FORMS">', count=1, html=True)

        # 3 existing + 3 extra forms + 1 empty for construction
        # TODO: Django >1.4: assertInHTML
        if VERSION < (1, 7):
            self.assertContains(response, 'Form Field:', count=7, html=False)
        else:
            self.assertContains(response, 'Form field:', count=7, html=False)

        # 3 extra forms + 1 empty for construction
        # don't use html=True as we don't care about the <select>-Tag
        self.assertContains(response, get_fields_html(), count=4)

        # 3 extra forms + 1 empty for construction
        self.assertContains(response, _('The options for this field will be '
            'available once it has been stored the first time.'), count=4)

        # Boolean Field
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '''
            <div>
                <label for="id_fields-0-_options_0"> Options:</label>
                <div style="display:inline-block;">
                    <label for="id_fields-0-_options_0">help_text:</label>
                        <textarea rows="10" name="fields-0-_options_0" id="id_fields-0-_options_0" cols="40">
                            Some help for boolean
                        </textarea>
                </div>
            </div>''', count=1, html=True)

        # Single Line Text Field
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '''
            <div>
                <label for="id_fields-1-_options_0"> Options:</label>
                <div style="display:inline-block;">
                    <label for="id_fields-1-_options_0">help_text:</label>
                        <textarea rows="10" name="fields-1-_options_0" id="id_fields-1-_options_0" cols="40">
                            Some help for single line
                        </textarea><br>
                    <label for="id_fields-1-_options_1">max_length:</label>
                        <input type="text" name="fields-1-_options_1" id="id_fields-1-_options_1" value="100"><br>
                    <label for="id_fields-1-_options_2">min_length:</label>
                        <input type="text" name="fields-1-_options_2" id="id_fields-1-_options_2"><br>
                    <label for="id_fields-1-_options_3">required:</label>
                        <select name="fields-1-_options_3" id="id_fields-1-_options_3">
                            <option value="1">Unknown</option>
                            <option value="2">Yes</option>
                            <option selected="selected" value="3">No</option>
                        </select>
                </div>
            </div>''', count=1, html=True)

        # Date Field
        # TODO: Django >1.4: assertInHTML
        self.assertContains(response, '''
            <div>
                <label for="id_fields-2-_options_0"> Options:</label>
                <div style="display:inline-block;">
                    <label for="id_fields-2-_options_0">help_text:</label>
                        <textarea rows="10" name="fields-2-_options_0" id="id_fields-2-_options_0" cols="40">
                        </textarea><br>
                    <label for="id_fields-2-_options_1">localize:</label>
                        <select name="fields-2-_options_1" id="id_fields-2-_options_1">
                            <option value="1">Unknown</option>
                            <option selected="selected" value="2">Yes</option>
                            <option value="3">No</option>
                        </select><br>
                    <label for="id_fields-2-_options_2">required:</label>
                        <select name="fields-2-_options_2" id="id_fields-2-_options_2">
                            <option selected="selected" value="1">Unknown</option>
                            <option value="2">Yes</option>
                            <option value="3">No</option>
                        </select>
                </div>
            </div>''', count=1, html=True)

    def test_delete(self):
        form = FormModel.objects.create(name='Form', submit_url='/some-form/')
        FormFieldModel.objects.create(parent_form=form, label='SL',
            field_type='dynamic_forms.formfields.SingleLineTextField')

        FormModelData.objects.create(form=form, value='{"SL": "Some String"}')

        self.assertEqual(FormModel.objects.all().count(), 1)
        self.assertEqual(FormFieldModel.objects.all().count(), 1)
        self.assertEqual(FormModelData.objects.all().count(), 1)

        response = self.client.post('/admin/dynamic_forms/formmodel/%d/delete/' % form.pk, {'post': 'yes',})
        self.assertRedirects(response, '/admin/dynamic_forms/formmodel/')

        self.assertEqual(FormModel.objects.all().count(), 0)
        self.assertEqual(FormFieldModel.objects.all().count(), 0)
        self.assertEqual(FormModelData.objects.all().count(), 1)
