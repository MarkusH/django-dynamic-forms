#!/usr/bin/env python
import os
import codecs
from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-dynamic-forms',
    version='0.4.0',
    description='django-dynamic-forms is a reusable Django application to create and configure forms through the admin.',
    long_description=read('README.rst'),
    author='Markus Holtermann',
    author_email='info@markusholtermann.eu',
    url='http://github.com/MarkusH/django-dynamic-forms',
    license='BSD',
    packages=[
        'dynamic_forms',
        'dynamic_forms.migrations',
        'dynamic_forms.south_migrations',
    ],
    package_data={
        'dynamic_forms': [
            'locale/*/LC_MESSAGES/*',
            'templates/dynamic_forms/*',
        ]
    },
    install_requires=[
        'Django>=1.4',
        'six',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
    ],
    zip_safe=False
)
