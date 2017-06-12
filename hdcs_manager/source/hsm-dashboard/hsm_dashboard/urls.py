
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

import horizon

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/hsm_ui/hsm/')),
    url(r'^auth/', include('openstack_auth.urls')),
    url(r'^home/', RedirectView.as_view(url='/hsm_ui/hsm/')),
    url(r'', include(horizon.urls))
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^500/$', 'django.views.defaults.server_error')
    )
