# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import six

from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.utils.translation import ugettext, ugettext_lazy as _

from dynamic_forms.conf import settings


class ActionRegistry(object):

    def __init__(self):
        self._actions = {}

    def get(self, key):
        return self._actions.get(key, None)

    def get_as_choices(self):
        return sorted([(k, f.label) for k, f in six.iteritems(self._actions)],
                      key=lambda x: x[1])

    def register(self, func, label):
        if not callable(func):
            raise ValueError('%r must be a callable' % func)
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


@formmodel_action(ugettext('Send via email'))
def dynamic_form_send_email(form_model, form):
    mapped_data = form.get_mapped_data()

    subject = _('Form “%(formname)s” submitted') % {'formname': form_model}
    message = render_to_string('dynamic_forms/email.txt', {
        'form': form_model,
        'data': sorted(mapped_data.items()),
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = settings.DYNAMIC_FORMS_EMAIL_RECIPIENTS
    send_mail(subject, message, from_email, recipient_list)


@formmodel_action(ugettext('Store in database'))
def dynamic_form_store_database(form_model, form):
    from dynamic_forms.models import FormModelData
    mapped_data = form.get_mapped_data()
    value = json.dumps(mapped_data, cls=DjangoJSONEncoder)
    FormModelData.objects.create(form=form_model, value=value)
