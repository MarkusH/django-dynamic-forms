#!/bin/bash

flake8 dynamic_forms --exclude=*migrations* --ignore=E128,E501
coverage run `which django-admin.py` test --pythonpath=./ --settings=tests.settings $@ || exit 1
coverage xml
coverage report -m
