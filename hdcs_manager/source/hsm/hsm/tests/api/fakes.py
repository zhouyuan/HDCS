
import webob
import webob.dec
import webob.request

from hsm.api.openstack import wsgi as os_wsgi
from hsm import context


class FakeRequestContext(context.RequestContext):
    def __init__(self, *args, **kwargs):
        kwargs['auth_token'] = kwargs.get('auth_token', 'fake_auth_token')
        super(FakeRequestContext, self).__init__(*args, **kwargs)


class HTTPRequest(webob.Request):

    @classmethod
    def blank(cls, *args, **kwargs):
        kwargs['base_url'] = 'http://localhost/v1'
        use_admin_context = kwargs.pop('use_admin_context', False)
        out = os_wsgi.Request.blank(*args, **kwargs)
        out.environ['hsm.context'] = FakeRequestContext(
            'fake_user',
            'fake',
            is_admin=use_admin_context)
        return out
