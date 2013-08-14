# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json
import six

from django import forms
from django.db.utils import IntegrityError
from django.test import TestCase

from dynamic_forms.models import FormFieldModel, FormModel, FormModelData


class TestModels(TestCase):

    def test_str(self):
        fm1 = FormModel.objects.create(name='Form 1', submit_url='/')
        self.assertEqual(six.text_type(fm1), 'Form 1')

    def test_unique_name(self):
        FormModel.objects.create(name='Form', submit_url='/')
        self.assertRaises(IntegrityError, FormModel.objects.create,
            name='Form', submit_url='/2/')

    def test_unique_submit_url(self):
        FormModel.objects.create(name='Form 1', submit_url='/')
        self.assertRaises(IntegrityError, FormModel.objects.create,
            name='Form 2', submit_url='/')

    def test_suplicate_success_url(self):
        FormModel.objects.create(name='Form 1', submit_url='/1/')
        FormModel.objects.create(name='Form 2', submit_url='/2/',
            success_url='/2/done/')

    def test_urls_no_trailing(self):
        fm1 = FormModel.objects.create(name='No Trailing 1',
            submit_url='/some/form', success_url='/some/form/send')
        self.assertEqual(fm1.submit_url, '/some/form/')
        self.assertEqual(fm1.success_url, '/some/form/send/')

        fm2 = FormModel.objects.create(name='No Trailing 2',
            submit_url='/some/form2')
        self.assertEqual(fm2.submit_url, '/some/form2/')
        self.assertEqual(fm2.success_url, '/some/form2/done/')

    def test_urls_trailing(self):
        fm1 = FormModel.objects.create(name='With Trailing 1',
            submit_url='/some/form/', success_url='/some/form/send/')
        self.assertEqual(fm1.submit_url, '/some/form/')
        self.assertEqual(fm1.success_url, '/some/form/send/')

        fm2 = FormModel.objects.create(name='With Trailing 2',
            submit_url='/some/form2/')
        self.assertEqual(fm2.submit_url, '/some/form2/')
        self.assertEqual(fm2.success_url, '/some/form2/done/')

    def test_get_fields_as_dict(self):
        fm = FormModel.objects.create(name='Form', submit_url='/form/')
        names = ('sapiente', 'nihil', 'quidem', 'earum', 'quod')
        labels = ('quo', 'adipisci', 'nesciunt', 'aspernatur', 'molestiae')
        for i, (name, label) in enumerate(six.moves.zip(names, labels), 1):
            FormFieldModel.objects.create(parent_form=fm, name=name,
                label=label, position=i,
                field_type='dynamic_forms.formfields.SingleLineTextField')
        self.assertEqual(
            list(fm.get_fields_as_dict().items()),
            list(six.moves.zip(names, labels))
        )


class TestFormFieldModel(TestCase):

    def setUp(self):
        self.form = FormModel.objects.create(name='Form', submit_url='/form/')

    def test_str(self):
        ff = FormFieldModel.objects.create(parent_form=self.form,
            field_type='dynamic_forms.formfields.SingleLineTextField',
            label='Field')
        self.assertEqual(six.text_type(ff), 'Field “Field” in form “Form”')

    def test_options_update(self):
        ff = FormFieldModel.objects.create(parent_form=self.form, label='F',
            field_type='dynamic_forms.formfields.SingleLineTextField')
        self.assertEqual(ff.options, {})

        opts = {'required': True}
        ff.options = opts
        self.assertEqual(ff.options, opts)

        opts = {'min_length': 10, 'max_length': 100}
        ff.options = opts
        self.assertEqual(ff.options, opts)

    def test_options_subsequent_get(self):
        ff = FormFieldModel.objects.create(parent_form=self.form, label='F',
            field_type='dynamic_forms.formfields.SingleLineTextField')
        self.assertEqual(ff.options, {})

        opts = {'required': True}
        ff.options = opts
        self.assertFalse(hasattr(ff, '_options_cached'))
        self.assertEqual(ff.options, opts)
        self.assertTrue(hasattr(ff, '_options_cached'))
        self.assertEqual(ff.options, opts)
        self.assertTrue(hasattr(ff, '_options_cached'))

        opts = {'min_length': 10, 'max_length': 100}
        ff.options = opts
        self.assertFalse(hasattr(ff, '_options_cached'))
        self.assertEqual(ff.options, opts)
        self.assertTrue(hasattr(ff, '_options_cached'))
        self.assertEqual(ff.options, opts)
        self.assertTrue(hasattr(ff, '_options_cached'))

    def test_options_subsequent_set(self):
        ff = FormFieldModel.objects.create(parent_form=self.form, label='F',
            field_type='dynamic_forms.formfields.SingleLineTextField')
        self.assertEqual(ff.options, {})

        opts = {'required': True}
        ff.options = opts
        self.assertFalse(hasattr(ff, '_options_cached'))

        opts = {'min_length': 10, 'max_length': 100}
        ff.options = opts
        self.assertFalse(hasattr(ff, '_options_cached'))

    def test_options_fallback_empty(self):
        ff1 = FormFieldModel.objects.create(parent_form=self.form, label='F1',
            field_type='dynamic_forms.formfields.SingleLineTextField')
        ff2 = FormFieldModel.objects.create(parent_form=self.form, label='F2',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options=None)
        ff3 = FormFieldModel.objects.create(parent_form=self.form, label='F3',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='')
        ff4 = FormFieldModel.objects.create(parent_form=self.form, label='F4',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='{}')
        ff5 = FormFieldModel.objects.create(parent_form=self.form, label='F5',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='Something')
        self.assertEqual(ff1.options, {})
        self.assertEqual(ff2.options, {})
        self.assertEqual(ff3.options, {})
        self.assertEqual(ff4.options, {})
        self.assertEqual(ff5.options, {})

    def test_invalid_option(self):
        ff = FormFieldModel.objects.create(parent_form=self.form, label='F1',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='{"invalid_key": "invalid value"}')
        self.assertEqual(ff.options, {})

    def test_get_form_field_kwargs(self):
        ff = FormFieldModel(label='Label', name="my-label",
            field_type='dynamic_forms.formfields.SingleLineTextField')
        self.assertEqual(ff.get_form_field_kwargs(), {
            'label': 'Label',
            'name': 'my-label',
        })

        ff = FormFieldModel(label='Label', name="my-label",
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='{"max_length": 123}')
        self.assertEqual(ff.get_form_field_kwargs(), {
            'label': 'Label',
            'max_length': 123,
            'name': 'my-label',
        })

        ff = FormFieldModel(label='Label', name="my-label",
            field_type='dynamic_forms.formfields.SingleLineTextField',
            _options='{"name": "some-name", "label": "some label", "a": "b"}')
        self.assertEqual(ff.get_form_field_kwargs(), {
            'a': 'b',
            'label': 'Label',
            'name': 'my-label',
        })

    def test_generate_form_field(self):
        form = forms.Form()
        ff1 = FormFieldModel(label='Label', name="my-label",
            field_type='dynamic_forms.formfields.SingleLineTextField')
        ff1.generate_form_field(form)
        ff2 = FormFieldModel(label='Label2', name="label2",
            field_type='dynamic_forms.formfields.BooleanField')
        ff2.generate_form_field(form)

        self.assertHTMLEqual(form.as_p(),
            '<p><label for="id_my-label">Label:</label> <input type="text" '
            'id="id_my-label" name="my-label" /></p>\n<p><label '
            'for="id_label2">Label2:</label> <input id="id_label2" '
            'name="label2" type="checkbox" /></p>')


class TestFormModelData(TestCase):

    def setUp(self):
        self.fm = FormModel.objects.create(name='Form', submit_url='/form/')

    def test_str(self):
        FormModelData.objects.create(form=self.fm, value={})
        fmd = FormModelData.objects.get()
        self.assertEqual(six.text_type(fmd), 'Form: “Form” on %s' % (
            fmd.submitted,))

    def test_submitted(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(seconds=2)
        future = now + datetime.timedelta(seconds=2)
        FormModelData.objects.create(form=self.fm, value={})
        fmd = FormModelData.objects.get()
        self.assertLess(past, fmd.submitted)
        self.assertGreater(future, fmd.submitted)

    def test_pretty_value(self):
        data = json.dumps({
            'Some Key': 'Some value',
            'Another key': 'Another value',
            'Test': 'data',
        })
        fmd = FormModelData.objects.create(form=self.fm, value=data)
        self.assertEqual(fmd.pretty_value(), '<dl>'
            '<dt>Another key</dt><dd>Another value</dd>'
            '<dt>Some Key</dt><dd>Some value</dd>'
            '<dt>Test</dt><dd>data</dd>'
            '</dl>')

    def test_pretty_value_not_json(self):
        data = 'Some plain text value that is not JSON'
        fmd = FormModelData.objects.create(form=self.fm, value=data)
        self.assertEqual(fmd.pretty_value(), data)
