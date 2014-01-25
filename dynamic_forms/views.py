# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, DetailView, FormView

from dynamic_forms.actions import action_registry
from dynamic_forms.forms import FormModelForm
from dynamic_forms.models import FormModelData


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


class DynamicDataMixin(object):

    slug_field = 'display_key'
    slug_url_kwarg = 'display_key'
    template_name_404 = 'dynamic_forms/data_set_404.html'

    def get(self, request, *args, **kwargs):
        try:
            return super(DynamicDataMixin, self).get(request, *args, **kwargs)
        except Http404:
            return self.render_404({})

    def get_template_names_404(self):
        return [self.template_name_404]

    def render_404(self, context=None, **response_kwargs):
        ctx = {
            'display_key': self.kwargs.get(self.slug_url_kwarg, None)
        }
        if context:
            ctx.update(context)
        return self.response_class(request=self.request,
            template=self.get_template_names_404(), context=ctx, status=404,
            **response_kwargs)


class DynamicDataSetDetailView(DynamicDataMixin, DetailView):

    model = FormModelData
    template_name = 'dynamic_forms/data_set.html'

data_set_detail = DynamicDataSetDetailView.as_view()
