# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


settings.EMAIL_RECIPIENTS = getattr(
    settings,
    'EMAIL_RECIPIENTS',
    [mail[1] for mail in settings.ADMINS]
)

settings.FORM_TEMPLATES = getattr(
    settings,
    'FORM_TEMPLATES',
    [
        ('dynamic_forms/form.html', _('Default form template')),
    ]
)

settings.SUCCESS_TEMPLATES = getattr(
    settings,
    'SUCCESS_TEMPLATES',
    [
        ('dynamic_forms/form_success.html', _('Default success template')),
    ]
)
