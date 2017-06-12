
from django.conf.urls import patterns, url

from .views import cache_ratio
from .views import cache_action
from .views import cache_io_workload
from .views import get_rbd_basic_info
from .views import monitor
from .views import show_cache_config_view
from .views import show_cache_config
from .views import IndexView
from .views import UpdateView
from .views import update_action

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<rbd_id>[^/]+)/monitor/$', monitor, name='monitor'),
    url(r'^(?P<rbd_id>[^/]+)/cache_ratio/$', cache_ratio, name='cache_ratio'),
    url(r'^(?P<rbd_id>[^/]+)/cache_action/$', cache_action, name='cache_action'),
    url(r'^(?P<rbd_id>[^/]+)/cache_io_workload/$', cache_io_workload, name='cache_io_workload'),
    url(r'^(?P<rbd_id>[^/]+)/get_rbd_basic_info/$', get_rbd_basic_info, name='get_rbd_basic_info'),
    url(r'^(?P<rbd_id>[^/]+)/show_cache_config_view/$', show_cache_config_view, name='show_cache_config_view'),
    url(r'^(?P<rbd_id>[^/]+)/show_cache_config/$', show_cache_config, name='show_cache_config'),
    url(r'^(?P<rbd_id>[^/]+)/update/$', UpdateView.as_view(), name='update'),
    url(r'^update_action/$', update_action, name='update_action'),
)
