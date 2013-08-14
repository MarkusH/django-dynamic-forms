# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class DynamicFormsConf(AppConf):
    EMAIL_RECIPIENTS = [mail[1] for mail in settings.ADMINS]
