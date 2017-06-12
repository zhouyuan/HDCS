
import webob
from webob import exc

from hsm.api.openstack import wsgi
from hsm import conductor
from hsm import flags
from hsm.openstack.common import log as logging
from hsm import scheduler

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)


class ServerController(wsgi.Controller):
    """"""

    def __init__(self):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        super(ServerController, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def index(self, req):
        """Get a list of servers."""

        context = req.environ['hsm.context']

        servers = self.conductor_api.server_get_all(context)

        return {"servers": servers}

    def show(self, req, id):
        """Get a detail info of a server by id."""

        context = req.environ['hsm.context']

        server = self.conductor_api.server_get(context, id)

        return {"server": server}

    @wsgi.response(202)
    @wsgi.action("activate")
    def activate(self, req, id, body):
        """To activate the server as hyperstash instance."""

        context = req.environ['hsm.context']

        db_server = self.conductor_api.server_get(context, id)
        status = db_server['status']
        if status == "active":
            raise exc.HTTPBadRequest(explanation="The server is already active now.")

        # Create a new hyperstash instance. Default type is master.
        LOG.info("Create a new hyperstash instance. Default type is master.")
        server = self.conductor_api.server_get(context, id)
        n_hs_instance = {
            "host": server['host'],
            "type": "master",
            "server_id": id
        }
        hs_instance = self.conductor_api.hs_instance_create(context, n_hs_instance)

        try:
            # Fetch all rbd info into db on this new hyperstash instance.
            self.scheduler_api.rbd_fetch_with_hs_instance_id(context, hs_instance['id'])

            # Set the server status as active
            LOG.info("Set the server status as active.")
            values = {
                "status": "active"
            }
            self.conductor_api.server_update(context, id, values)
        except:
            self.conductor_api.hs_instance_delete(context, hs_instance['id'])
            raise exc.HTTPBadRequest(explanation="Fail to activate the server as hyperstash instance")
        return webob.Response(status_int=202)


def create_resource():
    return wsgi.Resource(ServerController())
