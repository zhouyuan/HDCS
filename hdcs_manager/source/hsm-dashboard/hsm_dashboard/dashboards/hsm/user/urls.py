
from django.conf.urls import patterns, url

from .views import IndexView
from .views import UpdateView
from .views import update_pwd

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^update/(?P<user_id>[^/]+)/$', UpdateView.as_view(), name='update'),
    url(r'^update_pwd/$', update_pwd, name='update_pwd'),
)
