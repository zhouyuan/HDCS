
import random

from hsm import agent
from hsm import conductor
from hsm import flags
from hsm import manager
from hsm.openstack.common import log as logging
from hsm import utils

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class SchedulerManager(manager.Manager):
    """Chooses a host to create storages."""

    RPC_API_VERSION = '1.2'

    def __init__(self, service_name=None, *args, **kwargs):
        super(SchedulerManager, self).__init__(*args, **kwargs)
        self.agent_api = agent.API()
        self.conductor_api = conductor.API()

    def init_host(self):
        LOG.info('init_host in scheduler manager')

    def rbd_fetch_with_hs_instance_id(self, context, hs_instance_id):
        hs_instance = self.conductor_api.hs_instance_get(context, hs_instance_id)
        host = hs_instance['host']
        return self.agent_api.rbd_fetch_with_hs_instance_id(context, host, hs_instance_id)

    def os_and_kernel_get(self, context, server_id):
        server = self.conductor_api.server_get(context, server_id)
        host = server['host']
        return self.agent_api.os_and_kernel_get(context, host)

    def mem_get(self, context, server_id):
        server = self.conductor_api.server_get(context, server_id)
        host = server['host']
        return self.agent_api.mem_get(context, host)

    def cpu_get(self, context, server_id):
        server = self.conductor_api.server_get(context, server_id)
        host = server['host']
        return self.agent_api.cpu_get(context, host)

    def rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        host = rbd['hs_instance']['host']
        return self.agent_api.rbd_cache_config_get_by_rbd_id(context, host, rbd_id)

    def rbd_cache_config_update(self, context, rbd_cache_config_id, values):
        rbd_cache_config = self.conductor_api.\
            rbd_cache_config_get(context, rbd_cache_config_id)
        rbd_id = rbd_cache_config['rbd_id']
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        host = rbd['hs_instance']['host']
        return self.agent_api.\
            rbd_cache_config_update(context, host, rbd_cache_config_id, values)

    def hsm_summary_get(self, context):
        servers = self.conductor_api.server_get_all(context)
        if len(servers) == 0:
            summary = {"ceph_version": "--",
                       "total_hyperstash_instances": "--",
                       "total_rbds": "--"}
        else:
            rand_server = servers[random.randrange(0, len(servers))]
            host = rand_server['host']
            summary = self.agent_api.hsm_summary_get(context, host)
        _, out = utils.execute("hsm", "--version", run_as_root=True)
        hsm_version = out.strip("\n").strip(" ")
        summary["hsm_version"] = hsm_version
        return summary

    def rbd_refresh(self, context):
        hs_instances = self.conductor_api.hs_instance_get_all(context)
        for hs_instance in hs_instances:
            host = hs_instance['host']
            self.agent_api.rbd_refresh(context, host)
