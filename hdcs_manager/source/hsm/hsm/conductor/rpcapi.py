
import logging

from hsm import flags
import hsm.openstack.common.rpc.proxy

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class ConductorAPI(hsm.openstack.common.rpc.proxy.RpcProxy):
    """Client side of the conductor RPC API"""

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(ConductorAPI, self).__init__(
            topic=topic or FLAGS.conductor_topic,
            default_version=self.BASE_RPC_API_VERSION)

    ####################
    # Server
    ####################
    def server_create(self, ctxt, values):
        return self.call(ctxt, self.make_msg('server_create',
                                             values=values))

    def server_get_by_host(self, ctxt, host):
        return self.call(ctxt, self.make_msg('server_get_by_host',
                                             host=host))

    def server_update(self, ctxt, server_id, values):
        return self.call(ctxt, self.make_msg('server_update',
                                             server_id=server_id,
                                             values=values))

    def server_get_all(self, ctxt):
        return self.call(ctxt, self.make_msg('server_get_all'))

    def server_get(self, ctxt, server_id):
        return self.call(ctxt, self.make_msg('server_get',
                                             server_id=server_id))

    ####################
    # Hs_Instance
    ####################
    def hs_instance_create(self, ctxt, values):
        return self.call(ctxt, self.make_msg('hs_instance_create',
                                             values=values))

    def hs_instance_get_all(self, ctxt):
        return self.call(ctxt, self.make_msg('hs_instance_get_all'))

    def hs_instance_get(self, ctxt, hs_instance_id):
        return self.call(ctxt, self.make_msg('hs_instance_get',
                                             hs_instance_id=hs_instance_id))

    def hs_instance_delete(self, ctxt, hs_instance_id):
        return self.call(ctxt, self.make_msg('hs_instance_delete',
                                             hs_instance_id=hs_instance_id))

    def hs_instance_get_by_host(self, ctxt, host):
        return self.call(ctxt, self.make_msg('hs_instance_get_by_host',
                                             host=host))

    ####################
    # RBD
    ####################
    def rbd_create(self, ctxt, values):
        return self.call(ctxt, self.make_msg('rbd_create',
                                             values=values))

    def rbd_get_all_by_hs_instance_id(self, ctxt, hs_instance_id):
        return self.call(ctxt, self.make_msg('rbd_get_all_by_hs_instance_id',
                                             hs_instance_id=hs_instance_id))

    def rbd_delete(self, ctxt, rbd_id):
        return self.call(ctxt, self.make_msg('rbd_delete',
                                             rbd_id=rbd_id))

    def rbd_get_all(self, ctxt):
        return self.call(ctxt, self.make_msg('rbd_get_all'))

    def rbd_get(self, ctxt, rbd_id):
        return self.call(ctxt, self.make_msg('rbd_get',
                                             rbd_id=rbd_id))

    def rbd_get_by_name(self, ctxt, name):
        return self.call(ctxt, self.make_msg('rbd_get_by_name',
                                             name=name))

    def rbd_update(self, ctxt, rbd_id, values):
        return self.call(ctxt, self.make_msg('rbd_update',
                                             rbd_id=rbd_id,
                                             values=values))

    ####################
    # Performance Metric
    ####################
    def performance_metric_get_by_rbd_name(self, ctxt, rbd_name):
        return self.call(ctxt, self.make_msg('performance_metric_get_by_rbd_name',
                                             rbd_name=rbd_name))

    ####################
    # RBD Cache Config
    ####################
    def rbd_cache_config_get_all(self, ctxt):
        return self.call(ctxt, self.make_msg('rbd_cache_config_get_all'))

    def rbd_cache_config_get(self, ctxt, rbd_cache_config_id):
        return self.call(ctxt, self.make_msg('rbd_cache_config_get',
                                             rbd_cache_config_id=rbd_cache_config_id))

    def rbd_cache_config_get_by_rbd_id(self, ctxt, rbd_id):
        return self.call(ctxt, self.make_msg('rbd_cache_config_get_by_rbd_id',
                                             rbd_id=rbd_id))

    def rbd_cache_config_create(self, ctxt, values):
        return self.call(ctxt, self.make_msg('rbd_cache_config_create',
                                             values=values))

    def rbd_cache_config_delete_by_rbd_id(self, ctxt, rbd_id):
        return self.call(ctxt, self.make_msg('rbd_cache_config_delete_by_rbd_id',
                                             rbd_id=rbd_id))

    def rbd_cache_config_update(self, ctxt, rbd_cache_config_id, values):
        return self.call(ctxt, self.make_msg('rbd_cache_config_update',
                                             rbd_cache_config_id=rbd_cache_config_id,
                                             values=values))
