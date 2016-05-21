# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils import six
from django.utils.text import capfirst

from dynamic_forms.forms import MultiSelectFormField


try:
    # SubfieldBase is deprecated in Django 1.8 and removed in 1.10
    class BaseTextMultiSelectField(six.with_metaclass(models.SubfieldBase, models.TextField)):
        pass
except AttributeError:
    class BaseTextMultiSelectField(models.TextField):
        pass


class TextMultiSelectField(BaseTextMultiSelectField):
    # http://djangosnippets.org/snippets/2753/

    widget = CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.separate_values_by = kwargs.pop('separate_values_by', '\n')
        super(TextMultiSelectField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(TextMultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def _func(self, fieldname=name):
                return self.separate_values_by.join([
                    self.choices.get(value, value) for value in
                    getattr(self, fieldname)
                ])
            setattr(cls, 'get_%s_display' % self.name, _func)

    def deconstruct(self):
        name, path, args, kwargs = super(TextMultiSelectField, self).deconstruct()
        kwargs['separate_values_by'] = self.separate_values_by
        if kwargs.get('separate_values_by') == '\n':
            del kwargs['separate_values_by']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {
            'choices': self.choices,
            'help_text': self.help_text,
            'label': capfirst(self.verbose_name),
            'required': not self.blank,
            'separate_values_by': self.separate_values_by,
        }
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        defaults['widget'] = self.widget
        return MultiSelectFormField(**defaults)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, list):
            return self.separate_values_by.join(value)

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        chces = []
        for choice_selected in arr_choices:
            chces.append(choice_selected[0])
        return chces

    def get_prep_value(self, value):
        return value

    def to_python(self, value):
        if value is None:
            return []

        if isinstance(value, list):
            return value

        return value.split(self.separate_values_by)

    def validate(self, value, model_instance):
        """
        :param callable convert: A callable to be applied for each choice
        """
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if opt_select not in arr_choices:
                raise ValidationError(
                    self.error_messages['invalid_choice'] % value)
        return

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def get_internal_type(self):
        return "TextField"
