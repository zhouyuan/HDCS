
import logging

from hsm import flags
import hsm.openstack.common.rpc.proxy

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class SchedulerAPI(hsm.openstack.common.rpc.proxy.RpcProxy):
    """Client side of the scheduler RPC API"""

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(SchedulerAPI, self).__init__(
            topic=topic or FLAGS.scheduler_topic,
            default_version=self.BASE_RPC_API_VERSION)

    def rbd_fetch_with_hs_instance_id(self, ctxt, hs_instance_id):
        return self.call(ctxt, self.make_msg('rbd_fetch_with_hs_instance_id',
                                             hs_instance_id=hs_instance_id))

    def os_and_kernel_get(self, ctxt, server_id):
        return self.call(ctxt, self.make_msg('os_and_kernel_get',
                                             server_id=server_id))

    def mem_get(self, ctxt, server_id):
        return self.call(ctxt, self.make_msg('mem_get',
                                             server_id=server_id))

    def cpu_get(self, ctxt, server_id):
        return self.call(ctxt, self.make_msg('cpu_get',
                                             server_id=server_id))

    def rbd_cache_config_get_by_rbd_id(self, ctxt, rbd_id):
        return self.call(ctxt, self.make_msg('rbd_cache_config_get_by_rbd_id',
                                             rbd_id=rbd_id))

    def rbd_cache_config_update(self, ctxt, rbd_cache_config_id, values):
        return self.call(ctxt, self.make_msg('rbd_cache_config_update',
                                             rbd_cache_config_id=rbd_cache_config_id,
                                             values=values))

    def hsm_summary_get(self, ctxt):
        return self.call(ctxt, self.make_msg('hsm_summary_get'))

    def rbd_refresh(self, ctxt):
        return self.call(ctxt, self.make_msg('rbd_refresh'))
