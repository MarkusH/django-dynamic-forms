# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.decorators import classonlymethod

from dynamic_forms.actions import action_registry
from dynamic_forms.forms import FormModelForm
from dynamic_forms.models import FormFieldModel, FormModel


class TestAction(object):

    calls = 0
    args = []

    __name__ = "TestAction"

    def __call__(self, form_model, form):
        TestAction.calls += 1
        TestAction.args.append((form_model, form))

    @classonlymethod
    def clear(cls):
        cls.calls = 0
        cls.args = []


class TestAction2(object):

    __name__ = "TestAction2"

    def __call__(self):
        pass



class TestViews(TestCase):

    def setUp(self):
        action_registry.register(TestAction(), 'Some action')
        action_registry.register(TestAction2(), 'Some action2')

        self.fm = FormModel.objects.create(name='Form', submit_url='/form/',
            success_url='/done/', actions=['tests.test_views.TestAction'],
            form_template='dynamic_forms/form.html',
            success_template='dynamic_forms/form_success.html')
        self.field1 = FormFieldModel.objects.create(parent_form=self.fm,
            field_type='dynamic_forms.formfields.SingleLineTextField',
            label='String Field', position=1)
        self.field2 = FormFieldModel.objects.create(parent_form=self.fm,
            field_type='dynamic_forms.formfields.BooleanField',
            label='Field for Boolean', position=2)
        self.field3 = FormFieldModel.objects.create(parent_form=self.fm,
            field_type='dynamic_forms.formfields.DateTimeField',
            label='Date and time', position=3)
        self.form = FormModelForm(model=self.fm)

    def tearDown(self):
        TestAction.clear()
        action_registry.unregister('tests.test_views.TestAction')
        action_registry.unregister('tests.test_views.TestAction2')

    def test_get_form(self):
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], FormModelForm)
        self.assertTemplateUsed(response, 'dynamic_forms/form.html')

    def test_post_form(self):
        response = self.client.post('/form/', {
            'string-field': 'Some submitted string',
            'field-for-boolean': True,
            'date-and-time': '2013-09-07 12:34:56'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/done/')
        self.assertEqual(TestAction.calls, 1)
        self.assertEqual(TestAction.args[0][0], self.fm)
        self.assertIsInstance(TestAction.args[0][1], FormModelForm)
        self.assertEqual(TestAction.args[0][1].get_mapped_data(), OrderedDict([
            ('String Field', 'Some submitted string',),
            ('Field for Boolean', True,),
            ('Date and time', datetime.datetime(2013, 9, 7, 12, 34, 56),),
        ]))

    def test_post_form_invalid_form(self):
        response = self.client.post('/form/', {
            'field-for-boolean': 'foo',
            'date-and-time': 'Hello world'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<li>This field is required.</li>',
            count=1, html=True)
        self.assertContains(response, '<li>Enter a valid date/time.</li>',
            count=1, html=True)
        self.assertEqual(TestAction.calls, 0)
        self.assertEqual(TestAction.args, [])

    def test_post_form_invalid_action(self):
        self.fm.actions = ['tests.test_views.TestAction', 'invalid.action']
        self.fm.save()
        response = self.client.post('/form/', {
            'string-field': 'Some submitted string',
            'field-for-boolean': True,
            'date-and-time': '2013-09-07 12:34:56'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/done/')
        self.assertEqual(TestAction.calls, 1)
        self.assertEqual(TestAction.args[0][0], self.fm)
        self.assertIsInstance(TestAction.args[0][1], FormModelForm)
        self.assertEqual(TestAction.args[0][1].get_mapped_data(), OrderedDict([
            ('String Field', 'Some submitted string',),
            ('Field for Boolean', True,),
            ('Date and time', datetime.datetime(2013, 9, 7, 12, 34, 56),),
        ]))

    def test_get_done(self):
        response = self.client.get('/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dynamic_forms/form_success.html')

    def test_form_not_found(self):
        response = self.client.get('/form/does/not/exist/')
        self.assertEqual(response.status_code, 404)

    def test_form_error(self):
        self.fm.actions = ['tests.test_views.TestAction2']
        self.fm.save()
        response = self.client.post('/form/', {
            'string-field': 'Some submitted string',
            'field-for-boolean': True,
            'date-and-time': '2013-09-07 12:34:56'
        })
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_form_error_debug(self):
        self.fm.actions = ['tests.test_views.TestAction2']
        self.fm.save()
        self.assertRaises(TypeError, self.client.post, '/form/', {
            'string-field': 'Some submitted string',
            'field-for-boolean': True,
            'date-and-time': '2013-09-07 12:34:56'
        })
