
import logging

from django.conf import settings
from hsm_dashboard.api import hsm as hsmapi

LOG = logging.getLogger(__name__)

def openstack(request):
    """ Context processor necessary for OpenStack Dashboard functionality.

    The following variables are added to the request context:

    ``authorized_tenants``
        A list of tenant objects which the current user has access to.

    ``regions``

        A dictionary containing information about region support, the current
        region, and available regions.
    """
    context = {}

    # Auth/Keystone context
    context.setdefault('authorized_tenants', [])
    current_dash = request.horizon['dashboard']
    needs_tenants = getattr(current_dash, 'supports_tenants', False)
    if request.user.is_authenticated() and needs_tenants:
        context['authorized_tenants'] = request.user.authorized_tenants

    # Region context/support
    available_regions = getattr(settings, 'AVAILABLE_REGIONS', [])
    regions = {'support': len(available_regions) > 1,
               'current': {'endpoint': request.session.get('region_endpoint'),
                           'name': request.session.get('region_name')},
               'available': [{'endpoint': region[0], 'name':region[1]} for
                             region in available_regions]}
    context['regions'] = regions
    context['cluster'] = {'title': "Cluster"}

    return context
