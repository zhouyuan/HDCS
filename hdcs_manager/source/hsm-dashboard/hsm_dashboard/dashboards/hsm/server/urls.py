
from django.conf.urls import patterns, url

from .views import activate
from .views import IndexView
from .views import monitor
from .views import get_os_and_kernel
from .views import get_cpu
from .views import get_mem

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^activate/$', activate, name='activate'),
    url(r'^(?P<server_id>[^/]+)/monitor/$', monitor, name='monitor'),
    url(r'^(?P<server_id>[^/]+)/get_os_and_kernel/$', get_os_and_kernel, name='get_os_and_kernel'),
    url(r'^(?P<server_id>[^/]+)/get_cpu/$', get_cpu, name='get_cpu'),
    url(r'^(?P<server_id>[^/]+)/get_mem/$', get_mem, name='get_mem'),
)
