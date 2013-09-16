#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f.readlines()]

from dynamic_forms import get_version

setup(
    name='django-dynamic-forms',
    version=get_version(),
    description='django-dynamic-forms is a reusable Django application to create and configure forms through the admin.',
    long_description=readme,
    author='Markus Holtermann',
    author_email='info@markusholtermann.eu',
    url='http://github.com/Markush2010/django-dynamic-forms',
    license='BSD',
    packages=[
        'dynamic_forms',
        'example',
        'example.example',
        'tests',
    ],
    package_data = {
        'dynamic_forms': [
            'locale/*/LC_MESSAGES/*',
            'templates/dynamic_forms/*',
        ],
        'example': [
            'example.db',
        ]
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False
)
