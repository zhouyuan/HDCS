
import urlparse

from hsmclient import client as base_client
from hsmclient.tests.unit import fakes
from hsmclient.tests.unit import utils
from hsmclient.v1 import client


class FakeClient(fakes.FakeClient, client.Client):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, 'username', 'password',
                               'project_id', 'auth_url',
                               extensions=kwargs.get('extensions'))
        self.client = FakeHTTPClient(**kwargs)


class FakeHTTPClient(base_client.HTTPClient):

    def __init__(self, **kwargs):
        self.username = 'username'
        self.password = 'password'
        self.auth_url = 'auth_url'
        self.callstack = []
        self.management_url = 'http://10.0.2.15:8787/v1/fake'

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'body' not in kwargs
        elif method == 'PUT':
            assert 'body' in kwargs

        # Call the method
        args = urlparse.parse_qsl(urlparse.urlparse(url)[4])
        kwargs.update(args)
        munged_url = url.rsplit('?', 1)[0]
        munged_url = munged_url.strip('/').replace('/', '_').replace('.', '_')
        munged_url = munged_url.replace('-', '_')

        callback = "%s_%s" % (method.lower(), munged_url)

        if not hasattr(self, callback):
            raise AssertionError('Called unknown API method: %s %s, '
                                 'expected fakes method name: %s' %
                                 (method, url, callback))

        # Note the call
        self.callstack.append((method, url, kwargs.get('body', None)))
        status, headers, body = getattr(self, callback)(**kwargs)
        r = utils.TestResponse({
            "status_code": status,
            "text": body,
            "headers": headers,
        })
        return r, body

    #
    # List all extensions
    #
    def get_extensions(self, **kw):
        exts = [
            {
                "alias": "FAKE-1",
                "description": "Fake extension number 1",
                "links": [],
                "name": "Fake1",
                "namespace": ("http://docs.openstack.org/"
                              "/ext/fake1/api/v1.1"),
                "updated": "2017-02-08T00:00:00+00:00"
            },
            {
                "alias": "FAKE-2",
                "description": "Fake extension number 2",
                "links": [],
                "name": "Fake2",
                "namespace": ("http://docs.openstack.org/"
                              "/ext/fake1/api/v1.1"),
                "updated": "2017-02-08T00:00:00+00:00"
            },
        ]
        return (200, {}, {"extensions": exts, })

    #
    # Hyperstash Instances
    #
    def get_hs_instances(self):
        hs_instances = [
            {
                "id": 1234,
                "type": "master",
                "host": "host1234",
                "server_id": 1234,
                "deleted": False,
                "deleted_at": None,
                "created_at": "2017-02-08T00:00:00+00:00",
                "updated_at": None,
                "server": {
                    "id": 1234,
                    "status": "active",
                    "ip": "10.0.0.11",
                    "host": "host1234",
                    "id_rsa_pub": "id_rsa_pub_1234",
                    "deleted": False,
                    "deleted_at": None,
                    "created_at": "2017-02-08T00:00:00+00:00",
                    "updated_at": None
                }
            },
            {
                "id": 5678,
                "type": "master",
                "host": "host5678",
                "server_id": 5678,
                "deleted": False,
                "deleted_at": None,
                "created_at": "2017-02-08T00:00:00+00:00",
                "updated_at": None,
                "server": {
                    "id": 5678,
                    "status": "active",
                    "ip": "10.0.0.22",
                    "host": "host5678",
                    "id_rsa_pub": "id_rsa_pub_5678",
                    "deleted": False,
                    "deleted_at": None,
                    "created_at": "2017-02-08T00:00:00+00:00",
                    "updated_at": None
                }
            }
        ]
        return (200, {}, {"hs_instances": hs_instances})

    def delete_hs_instances_1234(self, **kw):
        return (202, {}, None)

    def get_hs_instances_1234(self, **kw):
        hs_instance_1234 = {
            "id": 1234,
            "type": "master",
            "host": "host1234",
            "server_id": 1234,
            "deleted": False,
            "deleted_at": None,
            "created_at": "2017-02-08T00:00:00+00:00",
            "updated_at": None,
            "server": {
                "id": 1234,
                "status": "active",
                "ip": "10.0.0.11",
                "host": "host1234",
                "id_rsa_pub": "id_rsa_pub_1234",
                "deleted": False,
                "deleted_at": None,
                "created_at": "2017-02-08T00:00:00+00:00",
                "updated_at": None
            }
        }
        return (200, {}, {'hs_instance': hs_instance_1234})

    #
    # Performance Metrics
    #
    def get_performance_metrics_get_value(self, **kw):
        type = kw['type']
        performance_metrics = []
        if type == 'cache_ratio':
            performance_metrics = [
                {
                    "timestamp": 1484878824,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_total_size"
                },
                {
                    "timestamp": 1484878824,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_used_size"
                },
                {
                    "timestamp": 1484878824,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_dirty_size"
                }
            ]
        elif type == 'cache_action':
            performance_metrics = [
                {
                    "timestamp": 1484878784,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_promote"
                },
                {
                    "timestamp": 1484878784,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_flush"
                },
                {
                    "timestamp": 1484878784,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_evict"
                }
            ]
        elif type == 'cache_io_workload':
            performance_metrics = [
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_read"
                },
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_read_miss"
                },
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_write"
                },
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_write_miss"
                },
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_bw"
                },
                {
                    "timestamp": 1484879184,
                    "value": 0,
                    "rbd_name": "tt",
                    "metric": "cache_latency"
                }
            ]
        elif type == 'rbd_basic_info':
            performance_metrics = [
                {
                    "features": None,
                    "name": "tt",
                    "format": 1,
                    "deleted": False,
                    "created_at": "2017-02-08T00:00:00.000000",
                    "block_name_prefix": "rb.0.220c.2ae8944a",
                    "hs_instance": {
                        "server_id": 1234,
                        "deleted": False,
                        "created_at": "2017-02-08T00:00:00.000000",
                        "updated_at": None,
                        "host": "host1234",
                        "deleted_at": None,
                        "type": "master",
                        "id": 1234
                    },
                    "updated_at": None,
                    "hs_instance_id": 1234,
                    "order": 22,
                    "objects": 256,
                    "flags": None,
                    "object_size": 4194304,
                    "deleted_at": None,
                    "id": 1234,
                    "size": 1073741824
                }
            ]
        return (200, {}, {'performance_metrics': performance_metrics})

    def get_performance_metrics_get_os_and_kernel(self, **kw):
        performance_metric = {
            "release": "7.1.1503",
            "kernel": "3.10.0-229.el7.x86_64",
            "codename": "Core",
            "distributor_id": "centos"
        }
        return (200, {}, {'performance_metric': performance_metric})

    def get_performance_metrics_get_mem(self, **kw):
        performance_metric = {
            "available": 188022784,
            "used": 1853497344,
            "cached": 112148480,
            "free": 75874304,
            "total": 1929371648,
            "buffers": 0
        }
        return (200, {}, {'performance_metric': performance_metric})

    def get_performance_metrics_get_cpu(self, **kw):
        performance_metric = {
            "softirq": 0,
            "irq": 0,
            "system": 0,
            "guest": 0,
            "idle": 97.6,
            "user": 2.4,
            "guest_nice": 0,
            "iowait": 0,
            "steal": 0,
            "nice": 0
        }
        return (200, {}, {'performance_metric': performance_metric})

    def get_performance_metrics_get_hsm_summary(self, **kw):
        performance_metric = {
            "total_rbds": 1,
            "hsm_version": "1.0.1",
            "ceph_version": "10.2.2",
            "total_hyperstash_instances": 1
        }
        return (200, {}, {'performance_metric': performance_metric})

    #
    # Rbd Cache Configs
    #
    def get_rbd_cache_configs(self, **kw):
        rbd_cache_configs = [
            {
                "cache_ratio_health": 0.5,
                "cache_ratio_max": 0.7,
                "cache_dirty_ratio_min": 0.1,
                "clean_start": 0,
                "rbd_id": 1234,
                "cache_total_size": 2147483647,
                "cache_evict_interval": 1,
                "created_at": "2017-02-08T00:00:00.000000",
                "enable_memory_usage_tracker": True,
                "updated_at": None,
                "deleted": False,
                "cache_flush_interval": 1,
                "cache_service_threads_num": 64,
                "object_size": 4096,
                "agent_threads_num": 128,
                "cache_dir": "/mnt/hyperstash_0",
                "deleted_at": None,
                "cache_flush_queue_depth": 256,
                "id": 1234,
                "messenger_port": 8081,
                "log_to_file": "/opt/hyperstash.log"
            }
        ]
        return (200, {}, {'rbd_cache_configs': rbd_cache_configs})

    def get_rbd_cache_configs_1234(self, **kw):
        rbd_cache_config = {
            "cache_ratio_health": 0.5,
            "cache_ratio_max": 0.7,
            "cache_dirty_ratio_min": 0.1,
            "clean_start": 0,
            "rbd_id": 1234,
            "cache_total_size": 2147483647,
            "cache_evict_interval": 1,
            "created_at": "2017-02-08T00:00:00.000000",
            "enable_memory_usage_tracker": True,
            "updated_at": None,
            "deleted": False,
            "cache_flush_interval": 1,
            "cache_service_threads_num": 64,
            "object_size": 4096,
            "agent_threads_num": 128,
            "cache_dir": "/mnt/hyperstash_0",
            "deleted_at": None,
            "cache_flush_queue_depth": 256,
            "id": 1234,
            "messenger_port": 8081,
            "log_to_file": "/opt/hyperstash.log"
        }
        return (200, {}, {'rbd_cache_config': rbd_cache_config})

    def get_rbd_cache_configs_get_by_rbd_id(self, **kw):
        rbd_cache_config = {
            "cache_ratio_health": 0.5,
            "cache_ratio_max": 0.7,
            "cache_dirty_ratio_min": 0.1,
            "clean_start": 0,
            "rbd_id": 1234,
            "cache_total_size": 2147483647,
            "cache_evict_interval": 1,
            "created_at": "2017-02-08T00:00:00.000000",
            "enable_memory_usage_tracker": True,
            "updated_at": None,
            "deleted": False,
            "cache_flush_interval": 1,
            "cache_service_threads_num": 64,
            "object_size": 4096,
            "agent_threads_num": 128,
            "cache_dir": "/mnt/hyperstash_0",
            "deleted_at": None,
            "cache_flush_queue_depth": 256,
            "id": 1234,
            "messenger_port": 8081,
            "log_to_file": "/opt/hyperstash.log"
        }
        return (200, {}, {'rbd_cache_config': rbd_cache_config})

    #
    # Rbds
    #
    def get_rbds(self, **kw):
        rbds = [
            {
                "features": None,
                "name": "tt",
                "format": 1,
                "deleted": False,
                "created_at": "2017-02-08T00:00:00.000000",
                "block_name_prefix": "rb.0.220c.2ae8944a",
                "hs_instance": {
                    "server_id": 1234,
                    "deleted": False,
                    "created_at": "2017-02-08T00:00:00.000000",
                    "updated_at": None,
                    "host": "controller",
                    "deleted_at": None,
                    "type": "master",
                    "id": 1234
                },
                "updated_at": None,
                "hs_instance_id": 1234,
                "order": 22,
                "objects": 256,
                "flags": None,
                "object_size": 4194304,
                "deleted_at": None,
                "id": 1234,
                "size": 1073741824
            }
        ]
        return (200, {}, {'rbds': rbds})

    def get_rbds_1234(self, **kw):
        rbd = {
            "features": None,
            "name": "tt",
            "format": 1,
            "deleted": False,
            "created_at": "2017-02-08T00:00:00.000000",
            "block_name_prefix": "rb.0.220c.2ae8944a",
            "hs_instance": {
                "server_id": 1234,
                "deleted": False,
                "created_at": "2017-02-08T00:00:00.000000",
                "updated_at": None,
                "host": "controller",
                "deleted_at": None,
                "type": "master",
                "id": 1234
            },
            "updated_at": None,
            "hs_instance_id": 1234,
            "order": 22,
            "objects": 256,
            "flags": None,
            "object_size": 4194304,
            "deleted_at": None,
            "id": 1234,
            "size": 1073741824
        }
        return (200, {}, {'rbd': rbd})

    def post_rbds_refresh(self):
        return (200, {}, None)

    #
    # Servers
    #
    def get_servers(self, **kw):
        servers = [
            {
                "status": "active",
                "deleted": False,
                "ip": "10.0.0.11",
                "created_at": "2017-02-08T00:00:00.000000",
                "updated_at": "2017-02-08T00:00:00.000000",
                "id": 1234,
                "host": "host1234",
                "deleted_at": None,
                "id_rsa_pub": "id_rsa_pub_1234"
            }
        ]
        return (200, {}, {'servers': servers})

    def get_servers_1234(self, **kw):
        server = {
            "status": "active",
            "deleted": False,
            "ip": "10.0.0.11",
            "created_at": "2017-02-08T00:00:00.000000",
            "updated_at": "2017-02-08T00:00:00.000000",
            "id": 1234,
            "host": "host1234",
            "deleted_at": None,
            "id_rsa_pub": "id_rsa_pub_1234"
        }
        return (200, {}, {'server': server})

    def post_servers_1234_action(self, body, **kw):
        _body = None
        resp = 202
        assert len(list(body)) == 1
        action = list(body)[0]
        if action == 'activate':
            assert body[action] is None
            return (resp, {}, _body)
