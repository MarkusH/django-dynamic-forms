#!/usr/bin/env python
import codecs
import os

from setuptools import find_packages, setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-dynamic-forms',
    version='0.5.2',
    description='django-dynamic-forms is a reusable Django application to create and configure forms through the admin.',
    long_description=read('README.rst'),
    author='Markus Holtermann',
    author_email='info@markusholtermann.eu',
    url='http://github.com/MarkusH/django-dynamic-forms',
    license='BSD',
    packages=find_packages(exclude=('docs', 'example', 'tests', 'tests.*')),
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ],
    zip_safe=False
)
