
import webob.exc

from hsm.api import extensions
from hsm import db
from hsm import exception
from hsm.openstack.common import log as logging
from hsm.openstack.common import timeutils
from hsm import utils

LOG = logging.getLogger(__name__)
authorize = extensions.extension_authorizer('storage', 'services')


class ServiceController(object):
    def index(self, req):
        """
        Return a list of all running services. Filter by host & service name.
        """
        context = req.environ['hsm.context']
        authorize(context)
        now = timeutils.utcnow()
        services = db.service_get_all(context)

        host = ''
        if 'host' in req.GET:
            host = req.GET['host']
        service = ''
        if 'service' in req.GET:
            service = req.GET['service']
        binary = ''
        if 'binary' in req.GET:
            binary = req.GET['binary']

        if host:
            services = [s for s in services if s['host'] == host]
        binary_key = binary or service
        if binary_key:
            services = [s for s in services if s['binary'] == binary_key]

        svcs = []
        for svc in services:
            delta = now - (svc['updated_at'] or svc['created_at'])
            alive = abs(utils.total_seconds(delta))
            art = (alive and "up") or "down"
            active = 'enabled'
            if svc['disabled']:
                active = 'disabled'
            svcs.append({"binary": svc['binary'], 'host': svc['host'],
                         'zone': svc['availability_zone'],
                         'status': active, 'state': art,
                         'updated_at': svc['updated_at']})
        return {'services': svcs}

    def update(self, req, id, body):
        """Enable/Disable scheduling for a service"""
        context = req.environ['hsm.context']
        authorize(context)

        if id == "enable":
            disabled = False
        elif id == "disable":
            disabled = True
        else:
            raise webob.exc.HTTPNotFound("Unknown action")

        try:
            host = body['host']
        except (TypeError, KeyError):
            raise webob.exc.HTTPBadRequest()

        service = body.get('service', '')
        binary = body.get('binary', '')
        binary_key = binary or service
        if not binary_key:
            raise webob.exc.HTTPBadRequest()

        try:
            svc = db.service_get_by_args(context, host, binary_key)
            if not svc:
                raise webob.exc.HTTPNotFound('Unknown service')

            db.service_update(context, svc['id'], {'disabled': disabled})
        except exception.ServiceNotFound:
            raise webob.exc.HTTPNotFound("service not found")

        status = id + 'd'
        return {'host': host,
                'service': service,
                'disabled': disabled,
                'binary': binary,
                'status': status}

class Services(extensions.ExtensionDescriptor):
    """Services support"""

    name = "Services"
    alias = "hsm-services"
    updated = "2016-11-18T00:00:00-00:00"

    def get_resources(self):
        resources = []
        resource = extensions.ResourceExtension('hsm-services',
                                                ServiceController())
        resources.append(resource)
        return resources
