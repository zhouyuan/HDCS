
import logging

from hsm import flags
from hsm.openstack.common import rpc
import hsm.openstack.common.rpc.proxy

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class AgentAPI(hsm.openstack.common.rpc.proxy.RpcProxy):
    """"""

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(AgentAPI, self).__init__(topic=topic or FLAGS.agent_topic,
                                       default_version=self.BASE_RPC_API_VERSION)

    def rbd_fetch_with_hs_instance_id(self, ctxt, host, hs_instance_id):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('rbd_fetch_with_hs_instance_id',
                                             hs_instance_id=hs_instance_id),
                         topic, version='1.0', timeout=6000)

    def os_and_kernel_get(self, ctxt, host):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('os_and_kernel_get'),
                         topic, version='1.0', timeout=6000)

    def mem_get(self, ctxt, host):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('mem_get'),
                         topic, version='1.0', timeout=6000)

    def cpu_get(self, ctxt, host):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('cpu_get'),
                         topic, version='1.0', timeout=6000)

    def rbd_cache_config_get_by_rbd_id(self, ctxt, host, rbd_id):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('rbd_cache_config_get_by_rbd_id',
                                             rbd_id=rbd_id),
                         topic, version='1.0', timeout=6000)

    def rbd_cache_config_update(self, ctxt, host, rbd_cache_config_id, values):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('rbd_cache_config_update',
                                             rbd_cache_config_id=rbd_cache_config_id,
                                             values=values),
                         topic, version='1.0', timeout=6000)

    def hsm_summary_get(self, ctxt, host):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('hsm_summary_get'),
                         topic, version='1.0', timeout=6000)

    def rbd_refresh(self, ctxt, host):
        topic = rpc.queue_get_for(ctxt, self.topic, host)
        return self.call(ctxt, self.make_msg('rbd_refresh'),
                         topic, version='1.0', timeout=6000)
