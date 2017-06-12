
import webob

from hsm.api.openstack import wsgi
from hsm import conductor
from hsm import flags
from hsm.openstack.common import log as logging

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)


class HsInstanceController(wsgi.Controller):
    """"""

    def __init__(self):
        self.conductor_api = conductor.API()
        super(HsInstanceController, self).__init__()

    def create(self):
        pass

    def delete(self, req, id):
        """
        Delete(Remove) hyperstash instance from the HSM(Hyperstash Manager).
        Delete it from the hs_instance table from db and stop to collect the
        performance metrics of the hyperstash and its' rbd performance metrics.
        """

        context = req.environ['hsm.context']
        hs_instance = self.conductor_api.hs_instance_get(context, id)
        server_id = hs_instance['server_id']

        # Update the related server status as available
        values = {
            "status": "available"
        }
        self.conductor_api.server_update(context, server_id, values)

        # Delete the rbds on the hyperstash instance
        # Delete the rbds related cache config
        rbds = self.conductor_api.rbd_get_all_by_hs_instance_id(context, id)
        for rbd in rbds:
            self.conductor_api.rbd_cache_config_delete_by_rbd_id(context, rbd['id'])
            self.conductor_api.rbd_delete(context, rbd['id'])

        # Delete it from the hs_instance table from db
        self.conductor_api.hs_instance_delete(context, id)

        # TODO
        # Stop to collect the performance metrics of the hyperstash and its'
        # rbd performance metrics
        return webob.Response(status_int=202)

    def update(self):
        pass

    def index(self, req):
        """Get a list of hyperstash instances."""

        context = req.environ['hsm.context']

        hs_instances = self.conductor_api.hs_instance_get_all(context)

        return {"hs_instances": hs_instances}

    def show(self, req, id):
        """Get a detail info of a hyperstash instance by id."""

        context = req.environ['hsm.context']

        hs_instance = self.conductor_api.hs_instance_get(context, id)

        return {"hs_instance": hs_instance}


def create_resource():
    return wsgi.Resource(HsInstanceController())
