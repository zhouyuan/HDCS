
import logging

from django.conf import settings

from horizon import exceptions

__all__ = ('get_service_from_catalog', 'url_for',)

LOG = logging.getLogger(__name__)


def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service['type'] == service_type:
                return service
    return None

def url_for(request, service_type, admin=False, endpoint_type=None):
    endpoint_type = endpoint_type or getattr(settings,
                                             'OPENSTACK_ENDPOINT_TYPE',
                                             'publicURL')
    catalog = request.user.service_catalog
    service = get_service_from_catalog(catalog, service_type)
    if service:
        try:
            if admin:
                return service['endpoints'][0]['adminURL']
            else:
                return service['endpoints'][0][endpoint_type]
        except (IndexError, KeyError):
            raise exceptions.ServiceCatalogException(service_type)
    else:
        raise exceptions.ServiceCatalogException(service_type)
