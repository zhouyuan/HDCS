
from hsm import flags
from hsm.openstack.common import log as logging
from hsm.scheduler import rpcapi

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class API(object):
    """Scheduler API that does updates via RPC to the SchedulerManager."""

    def __init__(self):
        self.scheduler_rpcapi = rpcapi.SchedulerAPI()

    def rbd_fetch_with_hs_instance_id(self, context, hs_instance_id):
        return self.scheduler_rpcapi.rbd_fetch_with_hs_instance_id(context, hs_instance_id)

    def os_and_kernel_get(self, context, server_id):
        return self.scheduler_rpcapi.os_and_kernel_get(context, server_id)

    def mem_get(self, context, server_id):
        return self.scheduler_rpcapi.mem_get(context, server_id)

    def cpu_get(self, context, server_id):
        return self.scheduler_rpcapi.cpu_get(context, server_id)

    def rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
        return self.scheduler_rpcapi.rbd_cache_config_get_by_rbd_id(context, rbd_id)

    def rbd_cache_config_update(self, context, rbd_cache_config_id, values):
        return self.scheduler_rpcapi.rbd_cache_config_update(context,
                                                             rbd_cache_config_id,
                                                             values)

    def hsm_summary_get(self, context):
        return self.scheduler_rpcapi.hsm_summary_get(context)

    def rbd_refresh(self, context):
        return self.scheduler_rpcapi.rbd_refresh(context)
