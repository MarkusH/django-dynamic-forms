# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.contrib import admin
from django.forms.utils import flatatt
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dynamic_forms.formfields import formfield_registry
from dynamic_forms.models import FormFieldModel, FormModel, FormModelData


class ReadOnlyWidget(forms.Widget):

    def __init__(self, attrs=None, **kwargs):
        self.show_text = kwargs.pop('show_text', None)
        super(ReadOnlyWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        content = ''
        if value is not None:
            content = value
        if self.show_text is not None:
            content = self.show_text
        final_attrs = self.build_attrs(attrs)
        return format_html('<span{0}>{1}</span>',
            flatatt(final_attrs),
            force_text(content),
        )


class OptionsWidget(forms.MultiWidget):

    def __init__(self, option_names, widgets, attrs=None):
        self.option_names = option_names
        super(OptionsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        mapping = json.loads(value) if value else {}
        return [mapping.get(key) for key in self.option_names]

    def format_output(self, rendered_widgets, id_):
        output = []
        i = 0
        for n, (r, w) in six.moves.zip(self.option_names, rendered_widgets):
            output.append(
                format_html(
                    '<label for="{0}_{1}">{2}:</label>{3}',
                    w.id_for_label(id_), i, n, r
                )
            )
            i += 1

        return mark_safe('<div style="display:inline-block;">' +
            ('<br />\n'.join(output)) + '</div>')

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            rendered = widget.render(name + '_%s' % i, widget_value,
                final_attrs)
            output.append((rendered, widget))
        return mark_safe(self.format_output(output, id_))


class OptionsField(forms.MultiValueField):

    def __init__(self, meta, *args, **kwargs):
        self.option_names = []
        self.option_fields = []
        self.option_widgets = []
        initial = {}
        for name, option in sorted(meta.items()):
            self.option_names.append(name)
            initial[name] = option[1]
            formfield = option[2]
            if isinstance(formfield, forms.Field):
                self.option_fields.append(formfield)
                self.option_widgets.append(formfield.widget)
            elif isinstance(formfield, (tuple, list)):
                if isinstance(formfield[0], forms.Field):
                    self.option_fields.append(formfield[0])
                else:
                    self.option_fields.append(formfield[0]())
                if isinstance(formfield[1], forms.Widget):
                    self.option_widgets.append(formfield[1])
                else:
                    self.option_widgets.append(formfield[1]())
            elif isinstance(formfield, type):
                self.option_fields.append(formfield())
                self.option_widgets.append(formfield.widget)
        kwargs['widget'] = OptionsWidget(self.option_names,
            self.option_widgets)
        if 'initial' in kwargs:
            kwargs['initial'].update(initial)
        else:
            kwargs['initial'] = initial
        super(OptionsField, self).__init__(self.option_fields, *args, **kwargs)

    def compress(self, data_list):
        data = {}
        for name, value in six.moves.zip(self.option_names, data_list):
            if value is not None:
                data[name] = value
        return json.dumps(data)


class AdminFormModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminFormModelForm, self).__init__(*args, **kwargs)
        choices = self.fields['actions'].choices
        self.fields['actions'].choices = sorted(choices, key=lambda x: x[1])


class AdminFormFieldInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        meta = None
        if instance:
            df = formfield_registry.get(instance.field_type)
            if df:
                meta = df._meta
        super(AdminFormFieldInlineForm, self).__init__(*args, **kwargs)
        choices = self.fields['field_type'].choices
        self.fields['field_type'].choices = sorted(choices, key=lambda x: x[1])
        if meta is not None:
            self.fields['_options'] = OptionsField(meta, required=False,
                label=_('Options'))
        else:
            self.fields['_options'].widget = ReadOnlyWidget(show_text=_(
                'The options for this field will be available once it has '
                'been stored the first time.'
            ))


class FormFieldModelInlineAdmin(admin.StackedInline):
    extra = 3
    form = AdminFormFieldInlineForm
    list_display = ('field_type', 'name', 'label')
    model = FormFieldModel
    prepopulated_fields = {"name": ("label",)}


class FormModelAdmin(admin.ModelAdmin):
    form = AdminFormModelForm
    inlines = (FormFieldModelInlineAdmin,)
    list_display = ('name', 'submit_url', 'success_url', 'allow_display')
    model = FormModel

admin.site.register(FormModel, FormModelAdmin)


class FormModelDataAdmin(admin.ModelAdmin):
    fields = ('form', 'value', 'submitted', 'show_url_link')
    list_display = ('form', 'pretty_value', 'submitted')
    model = FormModelData
    readonly_fields = ('submitted', 'show_url_link',)

admin.site.register(FormModelData, FormModelDataAdmin)
