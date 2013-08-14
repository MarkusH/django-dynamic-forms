# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from dynamic_forms.actions import action_registry
from dynamic_forms.forms import FormModelForm


class DynamicFormView(FormView):

    form_class = FormModelForm

    def dispatch(self, request, *args, **kwargs):
        # TODO: Django >1.4
        # self.form_model = self.kwargs.pop('model')

        return super(DynamicFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DynamicFormView, self).get_context_data(**kwargs)
        context.update({
            'model': self.form_model,
            'name': self.form_model.name,
            'submit_url': self.form_model.submit_url,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(DynamicFormView, self).get_form_kwargs()
        kwargs['model'] = self.form_model
        return kwargs

    def get_success_url(self):
        return self.form_model.success_url

    def get_template_names(self):
        return self.form_model.form_template

    def form_valid(self, form):
        for actionkey in self.form_model.actions:
            action = action_registry.get(actionkey)
            if action is None:
                continue
            action(self.form_model, form)
        messages.success(self.request,
            _('Thank you for submitting this form.'))
        return super(DynamicFormView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
            _('An error occurred during submitting this form.'))
        return super(DynamicFormView, self).form_invalid(form)

    # TODO: Django <1.5
    def get(self, request, *args, **kwargs):
        self.form_model = self.kwargs.pop('model')
        return super(DynamicFormView, self).get(request, *args, **kwargs)

    # TODO: Django <1.5
    def post(self, request, *args, **kwargs):
        self.form_model = self.kwargs.pop('model')
        return super(DynamicFormView, self).post(request, *args, **kwargs)


class DynamicTemplateView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        # TODO: Django >1.4
        # self.form_model = self.kwargs.pop('model')
        return super(DynamicTemplateView, self).dispatch(request, *args,
            **kwargs)

    def get_template_names(self):
        return self.form_model.success_template

    # TODO: Django <1.5
    def get(self, request, *args, **kwargs):
        self.form_model = self.kwargs.pop('model')
        return super(DynamicTemplateView, self).get(request, *args, **kwargs)
