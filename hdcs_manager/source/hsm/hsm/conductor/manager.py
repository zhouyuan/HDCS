
from hsm import db
from hsm import flags
from hsm import manager
from hsm.openstack.common import log as logging
from hsm.openstack.common import periodic_task

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class ConductorManager(manager.Manager):
    """Chooses a host to create storages."""

    RPC_API_VERSION = '1.0'

    def __init__(self, service_name=None, *args, **kwargs):
        super(ConductorManager, self).__init__(*args, **kwargs)

    def init_host(self):
        LOG.info('init_host in conductor manager ')

    ####################
    # Server
    ####################
    def server_create(self, context, values):
        return db.server_create(context, values)

    def server_get_by_host(self, context, host):
        return db.server_get_by_host(context, host)

    def server_update(self, context, server_id, values):
        return db.server_update(context, server_id, values)

    def server_get_all(self, context):
        return db.server_get_all(context)

    def server_get(self, context, server_id):
        return db.server_get(context, server_id)

    ####################
    # Hs_Instance
    ####################
    def hs_instance_create(self, context, values):
        return db.hs_instance_create(context, values)

    def hs_instance_get_all(self, context):
        return db.hs_instance_get_all(context)

    def hs_instance_get(self, context, hs_instance_id):
        return db.hs_instance_get(context, hs_instance_id)

    def hs_instance_delete(self, context, hs_instance_id):
        return db.hs_instance_delete(context, hs_instance_id)

    def hs_instance_get_by_host(self, context, host):
        return db.hs_instance_get_by_host(context, host)

    ####################
    # RBD
    ####################
    def rbd_create(self, context, values):
        return db.rbd_create(context, values)

    def rbd_get_all_by_hs_instance_id(self, context, hs_instance_id):
        return db.rbd_get_all_by_hs_instance_id(context, hs_instance_id)

    def rbd_delete(self, context, rbd_id):
        return db.rbd_delete(context, rbd_id)

    def rbd_get_all(self, context):
        return db.rbd_get_all(context)

    def rbd_get(self, context, rbd_id):
        return db.rbd_get(context, rbd_id)

    def rbd_get_by_name(self, context, name):
        return db.rbd_get_by_name(context, name)

    def rbd_update(self, context, rbd_id, values):
        return db.rbd_update(context, rbd_id, values)

    ####################
    # Performance Metric
    ####################
    def performance_metric_get_by_rbd_name(self, context, rbd_name):
        return db.performance_metric_get_by_rbd_name(context, rbd_name)

    ####################
    # RBD Cache Config
    ####################
    def rbd_cache_config_get_all(self, context):
        return db.rbd_cache_config_get_all(context)

    def rbd_cache_config_get(self, context, rbd_cache_config_id):
        return db.rbd_cache_config_get(context, rbd_cache_config_id)

    def rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
        return db.rbd_cache_config_get_by_rbd_id(context, rbd_id)

    def rbd_cache_config_create(self, context, values):
        return db.rbd_cache_config_create(context, values)

    def rbd_cache_config_delete_by_rbd_id(self, context, rbd_id):
        return db.rbd_cache_config_delete_by_rbd_id(context, rbd_id)

    def rbd_cache_config_update(self, context, rbd_cache_config_id, values):
        return db.rbd_cache_config_update(context, rbd_cache_config_id, values)

    ####################
    # Periodic Task
    ####################
    @periodic_task.periodic_task(spacing=3600)
    def _performance_metric_clean_up_data(self, context):
        LOG.info("Periodic task to clean up performance metric data")
        db.performance_metric_clean_up_data(context, 3600)
