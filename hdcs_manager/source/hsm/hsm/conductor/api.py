
from oslo_config import cfg

from hsm.conductor import rpcapi
from hsm import flags
from hsm.openstack.common import log as logging

conductor_opts = [
    cfg.StrOpt('manager',
               default='hsm.conductor.manager.ConductorManager',
               help='full class name for the Manager for conductor'),
]
conductor_group = cfg.OptGroup(name='conductor',
                               title='Conductor Options')
FLAGS = flags.FLAGS
FLAGS.register_group(conductor_group)
FLAGS.register_opts(conductor_opts, conductor_group)

LOG = logging.getLogger(__name__)


class API(object):
    """Conductor API that does updates via RPC to the ConductorManager."""

    def __init__(self):
        self.conductor_rpcapi = rpcapi.ConductorAPI()

    ####################
    # Server
    ####################
    def server_create(self, context, values):
        return self.conductor_rpcapi.server_create(context, values)

    def server_get_by_host(self, context, host):
        return self.conductor_rpcapi.server_get_by_host(context, host)

    def server_update(self, context, server_id, values):
        return self.conductor_rpcapi.server_update(context, server_id, values)

    def server_get_all(self, context):
        return self.conductor_rpcapi.server_get_all(context)

    def server_get(self, context, server_id):
        return self.conductor_rpcapi.server_get(context, server_id)

    ####################
    # Hs_Instance
    ####################
    def hs_instance_create(self, context, values):
        return self.conductor_rpcapi.hs_instance_create(context, values)

    def hs_instance_get_all(self, context):
        return self.conductor_rpcapi.hs_instance_get_all(context)

    def hs_instance_get(self, context, hs_instance_id):
        return self.conductor_rpcapi.hs_instance_get(context, hs_instance_id)

    def hs_instance_delete(self, context, hs_instance_id):
        return self.conductor_rpcapi.hs_instance_delete(context, hs_instance_id)

    def hs_instance_get_by_host(self, context, host):
        return self.conductor_rpcapi.hs_instance_get_by_host(context, host)

    ####################
    # RBD
    ####################
    def rbd_create(self, context, values):
        return self.conductor_rpcapi.rbd_create(context, values)

    def rbd_get_all_by_hs_instance_id(self, context, hs_instance_id):
        return self.conductor_rpcapi.rbd_get_all_by_hs_instance_id(context, hs_instance_id)

    def rbd_delete(self, context, rbd_id):
        return self.conductor_rpcapi.rbd_delete(context, rbd_id)

    def rbd_get_all(self, context):
        return self.conductor_rpcapi.rbd_get_all(context)

    def rbd_get(self, context, rbd_id):
        return self.conductor_rpcapi.rbd_get(context, rbd_id)

    def rbd_get_by_name(self, context, name):
        return self.conductor_rpcapi.rbd_get_by_name(context, name)

    def rbd_update(self, context, rbd_id, values):
        return self.conductor_rpcapi.rbd_update(context, rbd_id, values)

    ####################
    # Performance Metric
    ####################
    def performance_metric_get_by_rbd_name(self, context, rbd_name):
        return self.conductor_rpcapi.\
            performance_metric_get_by_rbd_name(context, rbd_name)

    ####################
    # RBD Cache Config
    ####################
    def rbd_cache_config_get_all(self, context):
        return self.conductor_rpcapi.rbd_cache_config_get_all(context)

    def rbd_cache_config_get(self, context, rbd_cache_config_id):
        return self.conductor_rpcapi.rbd_cache_config_get(context, rbd_cache_config_id)

    def rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
        return self.conductor_rpcapi.rbd_cache_config_get_by_rbd_id(context, rbd_id)

    def rbd_cache_config_create(self, context, values):
        return self.conductor_rpcapi.rbd_cache_config_create(context, values)

    def rbd_cache_config_delete_by_rbd_id(self, context, rbd_id):
        return self.conductor_rpcapi.rbd_cache_config_delete_by_rbd_id(context, rbd_id)

    def rbd_cache_config_update(self, context, rbd_cache_config_id, values):
        return self.conductor_rpcapi.\
            rbd_cache_config_update(context, rbd_cache_config_id, values)
