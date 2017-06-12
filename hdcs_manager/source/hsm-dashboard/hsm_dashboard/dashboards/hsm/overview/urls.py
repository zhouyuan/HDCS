
from django.conf.urls import patterns, url

from .views import index
from .views import hsm_summary
from .views import cache_io_workload
from .views import cache_ratio

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^hsm_summary/$', hsm_summary, name='hsm_summary'),
    url(r'^cache_io_workload/$', cache_io_workload, name='cache_io_workload'),
    url(r'^cache_ratio/$', cache_ratio, name='cache_ratio'),
)
