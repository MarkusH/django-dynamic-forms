# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from copy import deepcopy

from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from dynamic_forms.actions import (action_registry, dynamic_form_send_email,
    dynamic_form_store_database)
from dynamic_forms.forms import FormModelForm
from dynamic_forms.models import FormFieldModel, FormModel, FormModelData


def some_action(model, form):
    pass


class TestActionRegistry(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key1 = 'dynamic_forms.actions.dynamic_form_send_email'
        cls.key2 = 'dynamic_forms.actions.dynamic_form_store_database'
        cls.key3 = 'tests.test_actions.some_action'

        cls.action_registry_backup = deepcopy(action_registry)

    def tearDown(self):
        global action_registry
        action_registry = deepcopy(self.action_registry_backup)

    def test_default(self):
        self.assertEqual(action_registry._actions, {
            self.key1: dynamic_form_send_email,
            self.key2: dynamic_form_store_database,
        })

    def test_get_default_action(self):
        self.assertEqual(action_registry.get(self.key1),
            dynamic_form_send_email)
        self.assertEqual(action_registry.get(self.key2),
            dynamic_form_store_database)

    def test_get_default_actions_as_choices(self):
        self.assertEqual(action_registry.get_as_choices(), [
            (self.key1, 'Send via email'),
            (self.key2, 'Store in database')
        ])

    def test_register(self):
        action_registry.register(some_action, 'My Label')
        func = action_registry.get(self.key3)
        self.assertEqual(func, some_action)
        self.assertEqual(func.label, 'My Label')

    def test_register_not_callable(self):
        self.assertRaises(ValueError, action_registry.register,
            'not a callable', 'Label')

    def test_unregister(self):
        action_registry.register(some_action, 'My Label')
        action_registry.unregister(self.key3)

        self.assertIsNone(action_registry.get(self.key3))
        self.assertEqual(action_registry.get_as_choices(), [
            ('dynamic_forms.actions.dynamic_form_send_email',
                'Send via email'),
            ('dynamic_forms.actions.dynamic_form_store_database',
                'Store in database')
        ])

    def test_unregister_not_exists(self):
        action_registry.unregister('key-does-not-exist')


class TestActions(TestCase):

    def setUp(self):
        self.form_model = FormModel.objects.create(name='Form',
            submit_url='/form/', success_url='/form/done/')
        FormFieldModel.objects.create(parent_form=self.form_model, label='Str',
            field_type='dynamic_forms.formfields.SingleLineTextField',
            position=1)
        FormFieldModel.objects.create(parent_form=self.form_model, label='DT',
            field_type='dynamic_forms.formfields.DateTimeField',
            position=2)
        self.form = FormModelForm(model=self.form_model, data={
            'str': 'Some string to store',
            'dt': datetime.datetime(2013, 8, 29, 12, 34, 56, 789000),
        })

    def test_store_database(self):
        self.assertTrue(self.form.is_valid())
        dynamic_form_store_database(self.form_model, self.form)
        self.assertEqual(FormModelData.objects.count(), 1)
        data = FormModelData.objects.get()
        self.assertEqual(
            data.value,
            '{"Str": "Some string to store", "DT": "2013-08-29T12:34:56.789"}'
        )

    @override_settings(DYNAMIC_FORMS_EMAIL_RECIPIENTS=['mail@example.com'])
    def test_send_email(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(mail.outbox, [])
        dynamic_form_send_email(self.form_model, self.form)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Form “Form” submitted')
        self.assertEqual(message.body, '''Hello,

you receive this e-mail because someone submitted the form “Form”.

DT: Aug. 29, 2013, 12:34 p.m.
Str: Some string to store
''')
        self.assertEqual(message.recipients(), ['mail@example.com'])
        self.assertEqual(message.from_email, 'webmaster@localhost')
