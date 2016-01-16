# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import re
from importlib import import_module

from django import forms
from django.utils import six
from django.utils.decorators import classonlymethod
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


def format_display_label(cls_name):
    if cls_name.endswith('Field'):
        cls_name = cls_name[:-5]  # Strip trailing 'Field'

    # Precedes each group of capital letters by a whitespace except first
    return re.sub(r'([A-Z]+)', r' \1', cls_name).lstrip()


def load_class_from_string(cls_string):
    mod, cls = cls_string.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, cls)


class DynamicFormFieldRegistry(object):

    def __init__(self):
        self._fields = {}

    def get(self, key):
        return self._fields.get(key)

    def get_as_choices(self):
        for k, c in sorted(six.iteritems(self._fields)):
            yield k, c.get_display_label()

    def register(self, cls):
        if not issubclass(cls, BaseDynamicFormField):
            raise ValueError('%r must inherit from %r' % (
                cls, BaseDynamicFormField))
        key = '%s.%s' % (cls.__module__, cls.__name__)
        self._fields[key] = cls

    def unregister(self, key):
        if key in self._fields:
            del self._fields[key]


formfield_registry = DynamicFormFieldRegistry()
dynamic_form_field_registry = formfield_registry


def dynamic_form_field(cls):
    """
    A class decorator to register the class as a dynamic form field in the
    :class:`DynamicFormFieldRegistry`.
    """
    formfield_registry.register(cls)
    return cls


class DFFMetaclass(type):

    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)

        new_class = super(DFFMetaclass, cls).__new__(cls, name, bases, attrs)

        opts = {}
        super_opts = getattr(new_class, '_meta', {})
        if meta:
            excludes = getattr(meta, '_exclude', ())
            # Copy all attributes from super's options not excluded here. No
            # need to check for leading _ as this is already sorted out on the
            # super class
            for k, v in six.iteritems(super_opts):
                if k in excludes:
                    continue
                opts[k] = v
            # Copy all attributes not starting with a '_' from this Meta class
            for k, v in six.iteritems(meta.__dict__):
                if k.startswith('_') or k in excludes:
                    continue
                opts[k] = v
        else:
            opts = copy.deepcopy(super_opts)
        setattr(new_class, '_meta', opts)
        return new_class


@python_2_unicode_compatible
class BaseDynamicFormField(six.with_metaclass(DFFMetaclass)):

    cls = None
    display_label = None
    widget = None

    class Meta:
        help_text = [six.string_types, '', (forms.CharField, forms.Textarea)]
        required = [bool, True, forms.NullBooleanField]

    def __new__(cls, *args, **kwargs):
        self = super(BaseDynamicFormField, cls).__new__(cls)
        self._meta = copy.deepcopy(self.__class__._meta)
        return self

    def __init__(self, name, label, widget_attrs=None, **kwargs):
        self.name = name
        self.label = label
        self.widget_attrs = widget_attrs or {}
        self.set_options(**kwargs)

    def __str__(self):
        if isinstance(self.cls, six.string_types):
            clsname = self.cls
        else:
            clsname = '%s.%s' % (self.cls.__module__, self.cls.__name__)
        return '<%(class)s, name=%(name)s, label=%(label)s>' % {
            'class': clsname,
            'name': self.name,
            'label': self.label,
        }

    def construct(self, **kwargs):
        if isinstance(self.cls, six.string_types):
            cls_type = load_class_from_string(self.cls)
        else:
            cls_type = self.cls

        f_kwargs = {}
        for key, val in six.iteritems(self.options):
            f_kwargs[key] = val[1]

        f_kwargs['label'] = self.label

        if self.widget is not None:
            if isinstance(self.widget, six.string_types):
                widget_type = load_class_from_string(self.widget)
            else:
                widget_type = self.widget
            f_kwargs['widget'] = widget_type(**self.get_widget_attrs())

        f_kwargs.update(kwargs)  # Update the field kwargs by those given

        return cls_type(**f_kwargs)

    def contribute_to_form(self, form):
        form.fields[self.name] = self.construct()

    @classonlymethod
    def get_display_label(cls):
        if cls.display_label:
            return cls.display_label
        return format_display_label(cls.__name__)

    @property
    def options(self):
        return self._meta

    def get_widget_attrs(self):
        return self.widget_attrs

    def set_options(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            if key not in self.options:
                raise KeyError('%s is not a valid option.' % key)

            expected_type = self.options[key][0]
            if not isinstance(value, expected_type) and value is not None:
                raise TypeError('Neither of type %r nor None' % expected_type)

            self.options[key][1] = value
        self.options_valid()

    def options_valid(self):
        return True

    @classonlymethod
    def do_display_data(cls):
        return True


@dynamic_form_field
class BooleanField(BaseDynamicFormField):

    cls = 'django.forms.BooleanField'
    display_label = _('Boolean')

    class Meta:
        _exclude = ('required',)


@dynamic_form_field
class ChoiceField(BaseDynamicFormField):

    cls = 'django.forms.ChoiceField'
    display_label = _('Choices')

    class Meta:
        choices = [six.string_types, '', (forms.CharField, forms.Textarea)]

    def construct(self, **kwargs):
        value = self.options.get('choices')[1]
        choices = [(row, row) for row in value.splitlines() if row]
        return super(ChoiceField, self).construct(choices=choices)

    def options_valid(self):
        if not self.options['choices'] or not self.options['choices'][1]:
            raise ValueError('choices must not be defined for %r' % self)
        return True


@dynamic_form_field
class DateField(BaseDynamicFormField):

    cls = 'django.forms.DateField'
    display_label = _('Date')

    class Meta:
        localize = [bool, True, forms.NullBooleanField]


@dynamic_form_field
class DateTimeField(BaseDynamicFormField):

    cls = 'django.forms.DateTimeField'
    display_label = _('Date and Time')

    class Meta:
        localize = [bool, True, forms.NullBooleanField]


@dynamic_form_field
class EmailField(BaseDynamicFormField):

    cls = 'django.forms.EmailField'
    display_label = _('Email')


@dynamic_form_field
class IntegerField(BaseDynamicFormField):

    cls = 'django.forms.IntegerField'
    display_label = _('Integer')

    class Meta:
        localize = [bool, True, forms.NullBooleanField]
        max_value = [int, None, forms.IntegerField]
        min_value = [int, None, forms.IntegerField]


@dynamic_form_field
class MultiLineTextField(BaseDynamicFormField):

    cls = 'django.forms.CharField'
    display_label = _('Multi Line Text')
    widget = 'django.forms.widgets.Textarea'


@dynamic_form_field
class SingleLineTextField(BaseDynamicFormField):

    cls = 'django.forms.CharField'
    display_label = _('Single Line Text')

    class Meta:
        max_length = [int, None, forms.IntegerField]
        min_length = [int, None, forms.IntegerField]


@dynamic_form_field
class TimeField(BaseDynamicFormField):

    cls = 'django.forms.TimeField'
    display_label = _('Time')

    class Meta:
        localize = [bool, True, forms.NullBooleanField]
