# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six

from copy import deepcopy

from django import forms
from django.test import TestCase

from dynamic_forms.formfields import (dynamic_form_field_registry as registry,
    BaseDynamicFormField, BooleanField, ChoiceField, DateField, DateTimeField,
    EmailField, IntegerField, MultiLineTextField, SingleLineTextField,
    TimeField, format_display_type)


class CharField(BaseDynamicFormField):
    cls = forms.CharField


class Char2Field(BaseDynamicFormField):
    cls = 'django.forms.fields.CharField'


class MetaField(BaseDynamicFormField):
    cls = 'django.forms.fields.CharField'

    class Meta:
        _not_an_option = 'ignore in options'
        _exclude = ('help_text', 'required', 'pointless', '_exclude')
        max_length = [int, None, forms.IntegerField]
        pointless = [bool, True, forms.BooleanField]


class WidgetedField(BaseDynamicFormField):
    cls = 'django.forms.fields.CharField'
    widget = 'django.forms.widgets.Textarea'


class Widgeted2Field(BaseDynamicFormField):
    cls = forms.CharField
    widget = forms.Textarea


class NotAField(object):
    cls = 'django.forms.CharField'


class TestUtils(TestCase):

    def test_format_display_type(self):
        self.assertEqual(format_display_type('SomeClassField'), 'Some Class')
        self.assertEqual(format_display_type('SomeClass'), 'Some Class')
        self.assertEqual(format_display_type('SomeFOOClass'), 'Some FOOClass')


class TestDynamicFormFieldRegistry(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = 'dynamic_forms.formfields.%s'

        cls.names = ('BooleanField', 'ChoiceField', 'DateField',
            'DateTimeField', 'EmailField', 'IntegerField',
            'MultiLineTextField', 'SingleLineTextField', 'TimeField')

        cls.registry_backup = deepcopy(registry)

    def tearDown(self):
        global registry
        registry = deepcopy(self.registry_backup)

    def test_default(self):
        self.assertEqual(registry._fields, {
            self.key % 'BooleanField': BooleanField,
            self.key % 'ChoiceField': ChoiceField,
            self.key % 'DateField': DateField,
            self.key % 'DateTimeField': DateTimeField,
            self.key % 'EmailField': EmailField,
            self.key % 'IntegerField': IntegerField,
            self.key % 'MultiLineTextField': MultiLineTextField,
            self.key % 'SingleLineTextField': SingleLineTextField,
            self.key % 'TimeField': TimeField,
        })

    def test_get_default_action(self):
        self.assertEqual(registry.get(self.key % 'BooleanField'), BooleanField)
        self.assertEqual(registry.get(self.key % 'ChoiceField'), ChoiceField)

    def test_get_default_actions_as_choices(self):
        self.assertEqual(registry.get_as_choices(), [
            (self.key % 'BooleanField', 'Boolean'),
            (self.key % 'ChoiceField', 'Choices'),
            (self.key % 'DateField', 'Date'),
            (self.key % 'DateTimeField', 'Date and Time'),
            (self.key % 'EmailField', 'Email'),
            (self.key % 'IntegerField', 'Integer'),
            (self.key % 'MultiLineTextField', 'Multi Line Text'),
            (self.key % 'SingleLineTextField', 'Single Line Text'),
            (self.key % 'TimeField', 'Time'),
        ])

    def test_register(self):
        registry.register(CharField)
        cls = registry.get('tests.test_formfields.CharField')
        self.assertEqual(cls, CharField)
        self.assertEqual(cls.get_display_type(), 'Char')

    def test_register_not_inherit(self):
        self.assertRaises(ValueError, registry.register, NotAField)

    def test_unregister(self):
        key = 'tests.test_formfields.CharField'
        registry.register(CharField)
        registry.unregister(key)

        self.assertIsNone(registry.get(key))

    def test_unregister_not_exists(self):
        registry.unregister('key-does-not-exist')


class TestGenericDynamicFormFields(TestCase):

    def test_str(self):
        charfield = CharField('name', 'Label')
        self.assertEqual(six.text_type(charfield),
            '<django.forms.fields.CharField, name=name, label=Label>')

        charfield = Char2Field('name', 'Label')
        self.assertEqual(six.text_type(charfield),
            '<django.forms.fields.CharField, name=name, label=Label>')

    def test_construct_from_class(self):
        charfield = CharField('name', 'Label')
        formfield = charfield.construct()
        self.assertTrue(isinstance(formfield, forms.CharField))

    def test_construct_from_string(self):
        charfield = Char2Field('name', 'Label')
        formfield = charfield.construct()
        self.assertTrue(isinstance(formfield, forms.CharField))

    def test_construct_options(self):
        charfield = CharField('name', 'Label', required=False, 
            help_text='Some help')
        formfield = charfield.construct()
        self.assertFalse(formfield.required)
        self.assertEqual(formfield.help_text, 'Some help')

    def test_construct_widget(self):
        textfield1 = WidgetedField('name', 'label',
            widget_attrs={'attrs': {'rows': 10}})
        formfield1 = textfield1.construct()
        self.assertTrue(isinstance(formfield1.widget, forms.Textarea))

        textfield2 = Widgeted2Field('name', 'label',
            widget_attrs={'attrs': {'rows': 10}})
        formfield2 = textfield2.construct()
        self.assertTrue(isinstance(formfield2.widget, forms.Textarea))

    def test_options(self):
        metafield = MetaField('name', 'label')
        # This check implies, that neither Meta attributes starting with a _
        # not those part of the _exclude list are available
        self.assertEqual(metafield.options, {
            'max_length': [int, None, forms.IntegerField],
        })

    def test_options_invalid(self):
        self.assertRaises(KeyError, CharField, 'name', 'Label', something=123)
        self.assertRaises(KeyError, CharField, 'name', 'Label', something=123,
            required=True)

        self.assertRaises(TypeError, CharField, 'name', 'Label', required=123)
        self.assertRaises(TypeError, CharField, 'name', 'Label', help_text=42)


class TestChoiceField(TestCase):

    def test_options_valid(self):
        self.assertRaises(ValueError, ChoiceField, 'name', 'label')
        self.assertRaises(ValueError, ChoiceField, 'name', 'label',
            choices=None)

    def test_construct(self):
        # Empty rows are not treated as choices
        choices = """Lorem ipsum
dolor sit

amet equm"""
        dynamicfield = ChoiceField('name', 'Label', choices=choices)
        formfield = dynamicfield.construct()
        self.assertTrue(isinstance(formfield, forms.ChoiceField))
        self.assertEqual(formfield.choices, [('Lorem ipsum', 'Lorem ipsum'),
            ('dolor sit', 'dolor sit'), ('amet equm', 'amet equm')])
