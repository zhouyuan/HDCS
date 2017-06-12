
from django.conf.urls import patterns, url

from .views import cache_io_workload
from .views import cache_ratio
from .views import monitor
from .views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<hs_instance_id>[^/]+)/monitor/$', monitor, name='monitor'),
    url(r'^(?P<hs_instance_id>[^/]+)/cache_io_workload/$', cache_io_workload, name='cache_io_workload'),
    url(r'^(?P<hs_instance_id>[^/]+)/cache_ratio/$', cache_ratio, name='cache_ratio'),
)
