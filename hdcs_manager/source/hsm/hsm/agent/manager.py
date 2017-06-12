
import json
import os
import platform
import psutil

from hsm.agent import driver
from hsm import conductor
from hsm import context
from hsm import flags
from hsm import manager
from hsm.openstack.common import log as logging
from hsm.openstack.common import periodic_task
from hsm import utils

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class AgentManager(manager.Manager):
    """"""

    RPC_API_VERSION = '1.0'

    def __init__(self, service_name=None, *args, **kwargs):
        super(AgentManager, self).__init__(*args, **kwargs)
        self.context = context.get_admin_context()
        self.conductor_api = conductor.API()
        self.ceph_driver = driver.CephDriver()

    def init_node_into_db(self):
        LOG.info("initialize the agent node into db.")

        out, _ = utils.execute("hostname", "-I", run_as_root=True)
        ips_list = out.strip("\n").strip(" ").split(" ")
        ips = None
        for ip in ips_list:
            if not ips:
                ips = ip
            else:
                ips = ips + "," + ip
        LOG.info("ips are %s" % ips)

        out, _ = utils.execute("hostname", run_as_root=True)
        host = out.strip("\n").strip(" ")
        LOG.info("host is %s" % host)

        id_rsa_pub_path = FLAGS.id_rsa_pub
        LOG.info("id_rsa_pub_path is %s" % id_rsa_pub_path)
        id_rsa_pub = utils.read_file_as_root(id_rsa_pub_path).strip("\n").strip(" ")

        server_info = {
            "host": host,
            "ip": ips,
            "status": "available",
            "id_rsa_pub": id_rsa_pub
        }

        server = self.conductor_api.server_get_by_host(self.context, host=host)
        if not server:
            self.conductor_api.server_create(self.context, values=server_info)
        else:
            server_info.pop("status")
            server_id = server.get("id")
            self.conductor_api.server_update(self.context, server_id=server_id, values=server_info)

    def rbd_fetch_with_hs_instance_id(self, context, hs_instance_id):
        LOG.info("Fetch rbd info from hyperstash instance %s into db." % hs_instance_id)

        general_conf = "/etc/rbc/general.conf"
        rbds = []
        if os.path.exists(general_conf):
            file_obj = open(general_conf)
            for line in file_obj.readlines():
                line = line.strip("\n")
                if line.startswith("[") and line != "[global]":
                    rbd_name = line.lstrip("[").rstrip("]")
                    rbds.append(rbd_name)
        LOG.info("RBD %s on hyperstash instance %s" % (str(rbds), hs_instance_id))

        pools_list = self.ceph_driver.ceph_osd_pool_ls(format="json")
        pools_list = json.loads(pools_list)
        pools_with_rbds = []
        for pool in pools_list:
            rbds_all = self.ceph_driver.rbd_ls(pool, format="json")
            rbds_all = json.loads(rbds_all)
            pools_with_rbds.append(
                {
                    'pool': pool,
                    'rbds': rbds_all
                }
            )
        for rbd in rbds:
            for pool_with_rbd in pools_with_rbds:
                if rbd in pool_with_rbd['rbds']:
                    pool = pool_with_rbd['pool']
                    rbd_info = self.ceph_driver.rbd_info(rbd, pool, format="json")
                    rbd_info = json.loads(rbd_info)
                    features = rbd_info.get('features', None)
                    _features = None
                    if features:
                        for feature in features:
                            if not _features:
                                _features = feature
                            else:
                                _features = _features + "," + feature
                    rbd_info['features'] = _features
                    flags = rbd_info.get('flags', None)
                    _flags = None
                    if flags:
                        for flag in flags:
                            if not _flags:
                                _flags = flag
                            else:
                                _flags = _flags + "," + flag
                    rbd_info['flags'] = _flags
                    rbd_info['hs_instance_id'] = hs_instance_id
                    self.conductor_api.rbd_create(context, rbd_info)

    def os_and_kernel_get(self, context):
        LOG.info("Get the OS and Kernel information.")

        # OS info
        distributor_id, release, codename = platform.dist()

        # Kernel info
        uname_result = list(platform.uname())
        kernel = uname_result[2]

        result = {"distributor_id": distributor_id,
                  "release": release,
                  "codename": codename,
                  "kernel": kernel}
        return result

    def mem_get(self, context):
        LOG.info("Get the memory information.")

        vm = psutil.virtual_memory()
        result = {
            "total": vm.total,
            "available": vm.available,
            "used": vm.used,
            "free": vm.free,
            "buffers": vm.buffers,
            "cached": vm.cached
        }
        return result

    def cpu_get(self, context):
        LOG.info("Get the cpu information.")

        cpu_times_percent = psutil.cpu_times_percent()
        result = {
            "user": cpu_times_percent.user,
            "nice": cpu_times_percent.nice,
            "system": cpu_times_percent.system,
            "idle": cpu_times_percent.idle,
            "iowait": cpu_times_percent.iowait,
            "irq": cpu_times_percent.irq,
            "softirq": cpu_times_percent.softirq,
            "steal": cpu_times_percent.steal,
            "guest": cpu_times_percent.guest,
            "guest_nice": cpu_times_percent.guest_nice
        }
        return result

    def rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        rbd_name = rbd['name']
        rbd_cache_config_info = {}
        keys = RBD_CACHE_CONFIG_STRING_KEY + RBD_CACHE_CONFIG_INT_KEY + \
               RBD_CACHE_CONFIG_BOOL_KEY + RBD_CACHE_CONFIG_FLOAT_KEY
        for key in keys:
            key, value = self._fetch_rbd_cache_config_value_from_file(rbd_name, key)
            key, value = self._format_rbd_cache_config_value_into_db(key, value)
            rbd_cache_config_info[key] = value
        rbd_cache_config_info['rbd_id'] = rbd_id
        rbd_cache_config = self.conductor_api.\
            rbd_cache_config_create(context, rbd_cache_config_info)
        return rbd_cache_config

    def hsm_summary_get(self, context):
        ceph_version = self.ceph_driver.ceph_version()
        hs_instances = self.conductor_api.hs_instance_get_all(context)
        total_hyperstash_instances = len(hs_instances)
        rbds = self.conductor_api.rbd_get_all(context)
        total_rbds = len(rbds)
        hsm_summary = {
            "ceph_version": ceph_version,
            "total_hyperstash_instances": total_hyperstash_instances,
            "total_rbds": total_rbds
        }
        return hsm_summary

    def rbd_refresh(self, context):
        self._update_rbd(context)

    ####################
    # Periodic Task
    ####################
    @periodic_task.periodic_task(spacing=300)
    def _update_rbd(self, context):
        LOG.info("Periodic task to update rbd")

        out, _ = utils.execute("hostname", run_as_root=True)
        host = out.strip("\n").strip(" ")
        LOG.info("host is %s" % host)

        hs_instance = self.conductor_api.hs_instance_get_by_host(context, host)
        if not hs_instance:
            return
        hs_instance_id = hs_instance['id']
        rbds_in_db = self.conductor_api.\
            rbd_get_all_by_hs_instance_id(context, hs_instance_id)
        rbds_name_in_db = []
        for rbd_in_db in rbds_in_db:
            rbds_name_in_db.append(rbd_in_db['name'])

        general_conf = "/etc/rbc/general.conf"
        rbds = []
        if os.path.exists(general_conf):
            file_obj = open(general_conf)
            for line in file_obj.readlines():
                line = line.strip("\n")
                if line.startswith("[") and line != "[global]":
                    rbd_name = line.lstrip("[").rstrip("]")
                    rbds.append(rbd_name)
        LOG.info("RBD %s on hyperstash instance %s" % (str(rbds), hs_instance_id))

        pools_list = self.ceph_driver.ceph_osd_pool_ls(format="json")
        pools_list = json.loads(pools_list)
        pools_with_rbds = []
        for pool in pools_list:
            rbds_all = self.ceph_driver.rbd_ls(pool, format="json")
            rbds_all = json.loads(rbds_all)
            pools_with_rbds.append(
                {
                    'pool': pool,
                    'rbds': rbds_all
                }
            )
        rbds_name_in_ceph = []
        for rbd in rbds:
            for pool_with_rbd in pools_with_rbds:
                if rbd in pool_with_rbd['rbds']:
                    rbds_name_in_ceph.append(rbd)
                    pool = pool_with_rbd['pool']
                    rbd_info = self.ceph_driver.rbd_info(rbd, pool, format="json")
                    rbd_info = json.loads(rbd_info)
                    features = rbd_info.get('features', None)
                    _features = None
                    if features:
                        for feature in features:
                            if not _features:
                                _features = feature
                            else:
                                _features = _features + "," + feature
                    rbd_info['features'] = _features
                    flags = rbd_info.get('flags', None)
                    _flags = None
                    if flags:
                        for flag in flags:
                            if not _flags:
                                _flags = flag
                            else:
                                _flags = _flags + "," + flag
                    rbd_info['flags'] = _flags
                    rbd_info['hs_instance_id'] = hs_instance_id
                    if rbd not in rbds_name_in_db:
                        self.conductor_api.rbd_create(context, rbd_info)
                    else:
                        rbd_in_db = self.conductor_api.rbd_get_by_name(context, rbd)
                        rbd_id = rbd_in_db['id']
                        self.conductor_api.rbd_update(context, rbd_id, rbd_info)
        for rbd_name_in_db in rbds_name_in_db:
            if rbd_name_in_db not in rbds_name_in_ceph:
                rbd_in_db = self.conductor_api.rbd_get_by_name(context, rbd_name_in_db)
                rbd_id = rbd_in_db['id']
                self.conductor_api.rbd_cache_config_delete_by_rbd_id(context, rbd_id)
                self.conductor_api.rbd_delete(context, rbd_id)

    def rbd_cache_config_update(self, context, rbd_cache_config_id, values):
        rbd_cache_config = self.conductor_api.\
            rbd_cache_config_get(context, rbd_cache_config_id)
        rbd_id = rbd_cache_config['rbd_id']
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        rbd_name = rbd['name']
        for key in values:
            value = values[key]
            key, value = self._format_rbd_cache_config_value_into_file(key, value)
            self._set_rbd_cache_config_value_into_file(rbd_name, key, value)
        rbd_cache_config_info = {}
        for key in values:
            value = values[key]
            key, value = self._format_rbd_cache_config_value_into_db(key, value)
            rbd_cache_config_info[key] = value
        new_rbd_cache_config = self.conductor_api.rbd_cache_config_update(
            context, rbd_cache_config_id, rbd_cache_config_info)
        return new_rbd_cache_config

    def _format_rbd_cache_config_value_into_db(self, key, value):
        formats = {
            'cacheservice_threads_num': 'cache_service_threads_num',
            'enable_MemoryUsageTracker': 'enable_memory_usage_tracker'
        }
        key = formats.get(key, key)
        if key in RBD_CACHE_CONFIG_INT_KEY:
            value = int(value)
        elif key in RBD_CACHE_CONFIG_BOOL_KEY:
            if value in ['true', 'True', True]:
                value = True
            else:
                value = False
        elif key in RBD_CACHE_CONFIG_FLOAT_KEY:
            value = float(value)
        else:
            value = value
        return key, value

    def _format_rbd_cache_config_value_into_file(self, key, value):
        if key in RBD_CACHE_CONFIG_BOOL_KEY:
            if value in ['true', 'True', True]:
                value = 'true'
            else:
                value = 'false'
        formats = {
            'cache_service_threads_num': 'cacheservice_threads_num',
            'enable_memory_usage_tracker': 'enable_MemoryUsageTracker'
        }
        key = formats.get(key, key)
        return key, value

    def _fetch_rbd_cache_config_value_from_file(self, rbd_name, key):
        formats = {
            'cache_service_threads_num': 'cacheservice_threads_num',
            'enable_memory_usage_tracker': 'enable_MemoryUsageTracker'
        }
        key = formats.get(key, key)
        cmd = ['crudini',
               '--get',
               RBD_CACHE_CONFIG_FILE_PATH,
               rbd_name,
               key]
        out, _ = utils.execute(*cmd, run_as_root=True)
        value = out.strip('\n')
        if value:
            return key, value
        cmd = ['crudini',
               '--get',
               RBD_CACHE_CONFIG_FILE_PATH,
               'global',
               key]
        out, _ = utils.execute(*cmd, run_as_root=True)
        value = out.strip('\n')
        return key, value

    def _set_rbd_cache_config_value_into_file(self, rbd_name, key, value):
        cmd = ['crudini',
               '--set',
               RBD_CACHE_CONFIG_FILE_PATH,
               rbd_name,
               key,
               value]
        utils.execute(*cmd, run_as_root=True)


RBD_CACHE_CONFIG_FILE_PATH = '/etc/rbc/general.conf'

RBD_CACHE_CONFIG_STRING_KEY = [
    'cache_dir',
    'log_to_file'
]

RBD_CACHE_CONFIG_INT_KEY = [
    'clean_start',
    'object_size',
    'cache_total_size',
    'cache_flush_interval',
    'cache_evict_interval',
    'cache_flush_queue_depth',
    'agent_threads_num',
    'cache_service_threads_num',
    'messenger_port'
]

RBD_CACHE_CONFIG_BOOL_KEY = [
    'enable_memory_usage_tracker'
]

RBD_CACHE_CONFIG_FLOAT_KEY = [
    'cache_dirty_ratio_min',
    'cache_ratio_health',
    'cache_ratio_max'
]

RBD_CACHE_CONFIG_TEMPLATE="""
[global]
cache_dir=/mnt/hyperstash_0
clean_start=0
enable_MemoryUsageTracker=false
object_size=4096
cache_total_size=10737418240
cache_dirty_ratio_min=0.1
cache_ratio_health=0.5
cache_ratio_max=0.7
cache_flush_interval=1
cache_evict_interval=1
cache_flush_queue_depth=256
agent_threads_num=128
cacheservice_threads_num=64
messenger_port=8081
log_to_file=/opt/hyperstash.log
"""
