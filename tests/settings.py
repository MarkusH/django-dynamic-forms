# -*- coding: utf-8 -*-
import os.path
import django

RUNTESTS_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'captcha',
    'tests',
)
if django.VERSION[:2] < (1, 7):
    INSTALLED_APPS = INSTALLED_APPS + (
        'dynamic_forms',
    )
else:
    INSTALLED_APPS = INSTALLED_APPS + (
        'dynamic_forms.apps.DynamicFormsConfig',
    )

SECRET_KEY = 'test-secret-key'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dynamic_forms.middlewares.FormModelMiddleware',
)

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (
    os.path.join(RUNTESTS_DIR, 'templates'),
)

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

DYNAMIC_FORMS_FORM_TEMPLATES = (
    ('dynamic_forms/form.html', 'Default form template'),
    ('template1.html', 'Test tempate 1'),
)
DYNAMIC_FORMS_SUCCESS_TEMPLATES = (
    ('dynamic_forms/form_success.html', 'Default success template'),
    ('template2.html', 'Test template 2'),
)
