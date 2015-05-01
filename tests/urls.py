from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dynamic_forms/',
        include('dynamic_forms.urls', namespace='dynamic_forms')),
    url(r'^captcha/', include('captcha.urls')),
]
