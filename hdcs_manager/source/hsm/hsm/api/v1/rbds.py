
import webob

from hsm.api.openstack import wsgi
from hsm import conductor
from hsm.openstack.common import log as logging
from hsm import scheduler

LOG = logging.getLogger(__name__)


class RbdController(wsgi.Controller):
    """"""

    def __init__(self):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        super(RbdController, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def index(self, req):
        """Get a list of rbds."""

        context = req.environ['hsm.context']

        rbds = self.conductor_api.rbd_get_all(context)

        return {"rbds": rbds}

    def show(self, req, id):
        """Get a detail info of a rbd by id."""

        context = req.environ['hsm.context']

        rbd = self.conductor_api.rbd_get(context, id)

        return {"rbd": rbd}

    @wsgi.response(200)
    def refresh(self, req, body):
        """
        You can refresh the rbd info manually or the periodic task
        will update the rbd info.

        """

        context = req.environ['hsm.context']

        try:
            self.scheduler_api.rbd_refresh(context)
        except:
            LOG.warning("Fail to refresh the rbd info, please try again later")
        return webob.Response(status_int=200)


def create_resource():
    return wsgi.Resource(RbdController())
