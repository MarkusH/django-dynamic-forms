# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.text import capfirst

from dynamic_forms.conf import settings
from dynamic_forms.forms import MultiSelectFormField


class TextMultiSelectField(six.with_metaclass(models.SubfieldBase,
                                              models.TextField)):
    # http://djangosnippets.org/snippets/2753/

    widget = CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.separate_values_by = kwargs.pop('separate_values_by', '\n')
        super(TextMultiSelectField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(TextMultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def _func(self, fieldname=name, choicedict=dict(self.choices)):
                return self.separate_values_by.join([
                    choicedict.get(value, value) for value in
                    getattr(self, fieldname)
                ])
            setattr(cls, 'get_%s_display' % self.name, _func)

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
        if value is not None:
            return (value if isinstance(value, list) else
                value.split(self.separate_values_by))
        return []

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


if 'south' in settings.INSTALLED_APPS:  # pragma: no cover
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(patterns=['dynamic_forms\.fields'],
        rules=[((TextMultiSelectField,), [], {})])
