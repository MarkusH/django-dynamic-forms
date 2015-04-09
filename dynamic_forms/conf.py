# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

settings.DYNAMIC_FORMS_EMAIL_RECIPIENTS = getattr(
    settings,
    'DYNAMIC_FORMS_EMAIL_RECIPIENTS',
    [mail[1] for mail in settings.ADMINS]
)

settings.DYNAMIC_FORMS_FORM_TEMPLATES = getattr(
    settings,
    'DYNAMIC_FORMS_FORM_TEMPLATES',
    [
        ('dynamic_forms/form.html', _('Default form template')),
    ]
)

settings.DYNAMIC_FORMS_SUCCESS_TEMPLATES = getattr(
    settings,
    'DYNAMIC_FORMS_SUCCESS_TEMPLATES',
    [
        ('dynamic_forms/form_success.html', _('Default success template')),
    ]
)
