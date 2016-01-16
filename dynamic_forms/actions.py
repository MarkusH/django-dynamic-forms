# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import warnings

from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from dynamic_forms.conf import settings
from dynamic_forms.utils import RemovedIn06Warning, is_old_style_action


class ActionRegistry(object):

    def __init__(self):
        self._actions = {}

    def get(self, key):
        return self._actions.get(key)

    def get_as_choices(self):
        for k, f in sorted(six.iteritems(self._actions)):
            yield k, f.label

    def register(self, func, label):
        if not callable(func):
            raise ValueError('%r must be a callable' % func)

        if is_old_style_action(func):
            warnings.warn('The formmodel action "%s" is missing the third '
                          'argument "request". You should update your code to '
                          'match action(form_model, form, request).' % label,
                          RemovedIn06Warning)

        func.label = label
        key = '%s.%s' % (func.__module__, func.__name__)
        self._actions[key] = func

    def unregister(self, key):
        if key in self._actions:
            del self._actions[key]


action_registry = ActionRegistry()


def formmodel_action(label):
    def decorator(func):
        action_registry.register(func, label)
        return func
    return decorator


@formmodel_action(_('Send via email'))
def dynamic_form_send_email(form_model, form, request):
    mapped_data = form.get_mapped_data()

    subject = _('Form “%(formname)s” submitted') % {'formname': form_model}
    message = render_to_string('dynamic_forms/email.txt', {
        'form': form_model,
        'data': sorted(mapped_data.items()),
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    if form_model.recipient_email:
        recipient_list = [form_model.recipient_email]
    else:
        recipient_list = settings.DYNAMIC_FORMS_EMAIL_RECIPIENTS
    send_mail(subject, message, from_email, recipient_list)


@formmodel_action(_('Store in database'))
def dynamic_form_store_database(form_model, form, request):
    from dynamic_forms.models import FormModelData
    mapped_data = form.get_mapped_data()
    value = json.dumps(mapped_data, cls=DjangoJSONEncoder)
    data = FormModelData.objects.create(form=form_model, value=value)
    return data
