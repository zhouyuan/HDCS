
import logging
from pkg_resources import get_distribution

from django.conf import settings

from keystoneclient.v2_0 import client as keystone_client

from openstack_auth.backend import KEYSTONE_CLIENT_ATTR

from horizon import exceptions

from hsm_dashboard.api import base

LOG = logging.getLogger(__name__)


def _get_endpoint_url(request, endpoint_type, catalog=None):
    if getattr(request.user, "service_catalog", None):
        return base.url_for(request,
                            service_type='identity',
                            endpoint_type=endpoint_type)
    return request.session.get('region_endpoint',
                               getattr(settings, 'OPENSTACK_KEYSTONE_URL'))

def keystoneclient(request, admin=False):
    """Returns a client connected to the Keystone backend.

    Several forms of authentication are supported:

        * Username + password -> Unscoped authentication
        * Username + password + tenant id -> Scoped authentication
        * Unscoped token -> Unscoped authentication
        * Unscoped token + tenant id -> Scoped authentication
        * Scoped token -> Scoped authentication

    Available services and data from the backend will vary depending on
    whether the authentication was scoped or unscoped.

    Lazy authentication if an ``endpoint`` parameter is provided.

    Calls requiring the admin endpoint should have ``admin=True`` passed in
    as a keyword argument.

    The client is cached so that subsequent API calls during the same
    request/response cycle don't have to be re-authenticated.
    """
    user = request.user
    if admin:
        if not user.is_superuser:
            raise exceptions.NotAuthorized
        endpoint_type = 'adminURL'
    else:
        endpoint_type = getattr(settings,
                                'OPENSTACK_ENDPOINT_TYPE',
                                'internalURL')

    # Take care of client connection caching/fetching a new client.
    # Admin vs. non-admin clients are cached separately for token matching.
    cache_attr = "_keystoneclient_admin" if admin else KEYSTONE_CLIENT_ATTR
    if hasattr(request, cache_attr) and (not user.token.id
            or getattr(request, cache_attr).auth_token == user.token.id):
        LOG.debug("Using cached client for token: %s" % user.token.id)
        conn = getattr(request, cache_attr)
    else:
        endpoint = _get_endpoint_url(request, endpoint_type)
        insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
        LOG.debug("Creating a new keystoneclient connection to %s." % endpoint)

        # TODO: to be removed in H release
        kcversion = get_distribution("python-keystoneclient").version
        if kcversion >= '0.2.0':
            conn = keystone_client.Client(
                token=user.token.id, endpoint=endpoint,
                original_ip=request.environ.get('REMOTE_ADDR', ''),
                insecure=insecure)
        else:
            conn = keystone_client.Client(
                token=user.token.id, endpoint=endpoint,
                insecure=insecure)
        setattr(request, cache_attr, conn)
    return conn

def tenant_list(request, admin=False):
    return keystoneclient(request, admin=admin).tenants.list()

def user_list(request, tenant_id=None):
    return keystoneclient(request, admin=True).users.list(tenant_id=tenant_id)

def user_get(request, user_id, admin=True):
    return keystoneclient(request, admin=admin).users.get(user_id)

def user_update_password(request, user_id, password, admin=True):
    return keystoneclient(request, admin=admin).users.update_password(user_id, password)

def keystone_can_edit_user():
    backend_settings = getattr(settings, "OPENSTACK_KEYSTONE_BACKEND", {})
    return backend_settings.get('can_edit_user', True)
