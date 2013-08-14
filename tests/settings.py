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
    'dynamic_forms',
    'tests',
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

MIGRATION_MODULES = {
    'dynamic_forms': 'dynamic_forms.dj_migrations',
}

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (
    os.path.join(RUNTESTS_DIR, 'templates'),
)

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
