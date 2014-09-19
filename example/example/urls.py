from django.conf.urls import include, patterns, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin


admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^dynamic_forms/',
        include('dynamic_forms.urls', namespace='dynamic_forms')),
)

# Uncomment for captcha fields
# urlpatterns += patterns('',
#     url(r'^captcha/', include('captcha.urls')),
# )
