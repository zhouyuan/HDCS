
from hsm.agent import rpcapi
from hsm import flags
from hsm.openstack.common import log as logging

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class API(object):
    """"""

    def __init__(self):
        self.agent_rpcapi = rpcapi.AgentAPI()

    def rbd_fetch_with_hs_instance_id(self, context, host, hs_instance_id):
        return self.agent_rpcapi.rbd_fetch_with_hs_instance_id(context, host,
                                                               hs_instance_id)

    def os_and_kernel_get(self, context, host):
        return self.agent_rpcapi.os_and_kernel_get(context, host)

    def mem_get(self, context, host):
        return self.agent_rpcapi.mem_get(context, host)

    def cpu_get(self, context, host):
        return self.agent_rpcapi.cpu_get(context, host)

    def rbd_cache_config_get_by_rbd_id(self, context, host, rbd_id):
        return self.agent_rpcapi.rbd_cache_config_get_by_rbd_id(context, host, rbd_id)

    def rbd_cache_config_update(self, context, host, rbd_cache_config_id, values):
        return self.agent_rpcapi.\
            rbd_cache_config_update(context, host, rbd_cache_config_id, values)

    def hsm_summary_get(self, context, host):
        return self.agent_rpcapi.hsm_summary_get(context, host)

    def rbd_refresh(self, context, host):
        return self.agent_rpcapi.rbd_refresh(context, host)
