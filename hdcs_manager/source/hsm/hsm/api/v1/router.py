
from hsm.api import extensions
import hsm.api.openstack
from hsm.api.v1 import hs_instances
from hsm.api.v1 import performance_metrics
from hsm.api.v1 import rbd_cache_configs
from hsm.api.v1 import rbds
from hsm.api.v1 import servers
from hsm.api import versions

from hsm.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class APIRouter(hsm.api.openstack.APIRouter):
    """
    Routes requests on the OpenStack API to the appropriate controller
    and method.
    """
    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper, ext_mgr):
        self.resources['versions'] = versions.create_resource()
        mapper.connect("versions", "/",
                       controller=self.resources['versions'],
                       action='show')

        mapper.redirect("", "/")

        self.resources['servers'] = servers.create_resource()
        mapper.resource("server", "servers",
                        controller=self.resources['servers'],
                        collection={},
                        member={'action': 'POST'})

        self.resources['hs_instances'] = hs_instances.create_resource()
        mapper.resource("hs_instance", "hs_instances",
                        controller=self.resources['hs_instances'],
                        collection={},
                        member={'action': 'POST'})

        self.resources['rbds'] = rbds.create_resource()
        mapper.resource("rbd", "rbds",
                        controller=self.resources['rbds'],
                        collection={'refresh': 'POST'},
                        member={'action': 'POST'})

        self.resources['performance_metrics'] = performance_metrics.create_resource()
        mapper.resource("performance_metric", "performance_metrics",
                        controller=self.resources['performance_metrics'],
                        collection={'get_value': 'GET',
                                    'get_os_and_kernel': 'GET',
                                    'get_mem': 'GET',
                                    'get_cpu': 'GET',
                                    'get_hsm_summary': 'GET'},
                        member={'action': 'POST'})

        self.resources['rbd_cache_configs'] = rbd_cache_configs.create_resource()
        mapper.resource("rbd_cache_config", "rbd_cache_configs",
                        controller=self.resources['rbd_cache_configs'],
                        collection={'get_by_rbd_id': 'GET'},
                        member={'action': 'POST'})
