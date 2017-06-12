
from webob import exc

from hsm.api.openstack import wsgi
from hsm import conductor
from hsm.openstack.common import log as logging
from hsm import scheduler

LOG = logging.getLogger(__name__)


class RbdCacheConfigController(wsgi.Controller):
    """"""

    def __init__(self):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        super(RbdCacheConfigController, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self, req, id, body):
        """"""

        LOG.info("Rbd cache config update body: %s" % body)
        context = req.environ['hsm.context']

        if 'rbd_cache_config' not in body:
            raise exc.HTTPBadRequest(explanation="Not found rbd_cache_config in body")

        rbd_cache_config = self.scheduler_api.\
            rbd_cache_config_update(context, id, body['rbd_cache_config'])

        return {'rbd_cache_config': rbd_cache_config}

    def index(self, req):
        """"""

        context = req.environ['hsm.context']

        rbd_cache_configs = self.conductor_api.rbd_cache_config_get_all(context)

        return {"rbd_cache_configs": rbd_cache_configs}

    def show(self, req, id):
        """"""

        context = req.environ['hsm.context']

        rbd_cache_config = self.conductor_api.rbd_cache_config_get(context, id)

        return {"rbd_cache_config": rbd_cache_config}

    def get_by_rbd_id(self, req):
        """"""

        context = req.environ['hsm.context']

        rbd_id = req.GET['rbd_id']
        rbd_cache_config = self.conductor_api.\
            rbd_cache_config_get_by_rbd_id(context, rbd_id)

        # Not found the rbd cache config from the db, so to fetch the info
        # from the hyperstash instance.
        if not rbd_cache_config:
            LOG.info("Fetch the rbd cache config from the hyperstash instance.")
            rbd_cache_config = self.scheduler_api.\
                rbd_cache_config_get_by_rbd_id(context, rbd_id)
        return {"rbd_cache_config": rbd_cache_config}


def create_resource():
    return wsgi.Resource(RbdCacheConfigController())
