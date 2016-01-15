# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
from unittest import skipIf

from captcha.models import CaptchaStore
from django.test import TestCase
from django.utils.encoding import force_text

from dynamic_forms.formfields import formfield_registry as registry
from dynamic_forms.models import FormFieldModel, FormModel, FormModelData


@skipIf(sys.version_info[:2] == (3, 2),
        'django-simple-captcha is not compatible with Python 3.2')
class TestSimpleCaptcha(TestCase):

    def setUp(self):
        from dynamic_forms.contrib.simple_captcha.models import CaptchaField  # noqa
        self.captcha_key = 'dynamic_forms.contrib.simple_captcha.models.CaptchaField'

    def tearDown(self):
        registry.unregister(self.captcha_key)

    def test_default(self):
        self.fm = FormModel.objects.create(name='Form', submit_url='/form/',
            success_url='/done/',
            actions=['dynamic_forms.actions.dynamic_form_store_database'],
            form_template='dynamic_forms/form.html',
            success_template='dynamic_forms/form_success.html')
        FormFieldModel.objects.create(parent_form=self.fm,
            field_type='dynamic_forms.formfields.SingleLineTextField',
            label='Field 1', position=1)
        FormFieldModel.objects.create(parent_form=self.fm,
            field_type=self.captcha_key,
            label='CAPTCHA', position=2)
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)
        regex = r'value="([0-9a-f]{40})"'
        hash_ = re.findall(regex, force_text(response.content))[0]
        captcha_object = CaptchaStore.objects.get(hashkey=hash_)

        response = self.client.post('/form/', {
            'field-1': 'Some value',
            'captcha_0': hash_,
            'captcha_1': captcha_object.challenge,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/done/')
        data = FormModelData.objects.get()
        self.assertEqual(data.value, '{"Field 1": "Some value"}')
