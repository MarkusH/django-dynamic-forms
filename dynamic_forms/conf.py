# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class DynamicFormsConf(AppConf):
    EMAIL_RECIPIENTS = [mail[1] for mail in settings.ADMINS]
    FORM_TEMPLATES = (
        ('dynamic_forms/form.html', _('Default form template')),
    )
    SUCCESS_TEMPLATES = (
        ('dynamic_forms/form_success.html', _('Default success template')),
    )
