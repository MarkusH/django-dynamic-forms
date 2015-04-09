from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dynamic_forms/', include('dynamic_forms.urls', namespace='dynamic_forms')),
)

# Uncomment for captcha fields
# from django.conf.urls import patterns
# urlpatterns += patterns('',
#     url(r'^captcha/', include('captcha.urls')),
# )
