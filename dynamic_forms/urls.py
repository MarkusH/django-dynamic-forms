# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('dynamic_forms.views',
    url(r'show/(?P<display_key>[a-zA-Z0-9]{24})/$', 'data_set_detail',
        name='data-set-detail'),
)
