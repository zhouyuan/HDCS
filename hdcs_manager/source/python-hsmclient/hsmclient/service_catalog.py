
import hsmclient.exceptions


class ServiceCatalog(object):
    """Helper methods for dealing with a Keystone Service Catalog."""

    def __init__(self, resource_dict):
        self.catalog = resource_dict

    def get_token(self):
        return self.catalog['access']['token']['id']

    def url_for(self, attr=None, filter_value=None,
                service_type=None, endpoint_type='publicURL',
                service_name=None, hsm_service_name=None):
        """Fetch the public URL from the Compute service for
        a particular endpoint attribute. If none given, return
        the first. See tests for sample service catalog.
        """
        matching_endpoints = []
        if 'endpoints' in self.catalog:
            # We have a bastardized service catalog. Treat it special. :/
            for endpoint in self.catalog['endpoints']:
                if not filter_value or endpoint[attr] == filter_value:
                    matching_endpoints.append(endpoint)
            if not matching_endpoints:
                raise hsmclient.exceptions.EndpointNotFound()

        # We don't always get a service catalog back ...
        if 'serviceCatalog' not in self.catalog['access']:
            return None

        # Full catalog ...
        catalog = self.catalog['access']['serviceCatalog']

        for service in catalog:
            if service.get("type") != service_type:
                continue

            if (service_name and service_type == 'compute' and
                    service.get('name') != service_name):
                continue

            if (hsm_service_name and service_type == 'hsm' and
                    service.get('name') != hsm_service_name):
                continue

            endpoints = service['endpoints']
            for endpoint in endpoints:
                if not filter_value or endpoint.get(attr) == filter_value:
                    endpoint["serviceName"] = service.get("name")
                    matching_endpoints.append(endpoint)

        if not matching_endpoints:
            raise hsmclient.exceptions.EndpointNotFound()
        elif len(matching_endpoints) > 1:
            raise hsmclient.exceptions.AmbiguousEndpoints(
                endpoints=matching_endpoints)
        else:
            return matching_endpoints[0][endpoint_type]
