
import datetime

def stub_server(id, **kwargs):
    server = {
        "id": id,
        "ip": "fake ip",
        "host": "fake host",
        "id_rsa_pub": "fake id rsa pub",
        "status": "fake status",
        "deleted": False,
        "deleted_at": None,
        "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
        "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
    }
    server.update(kwargs)
    return server

def stub_hs_instance(id, server_id=None, **kwargs):
    if server_id:
        fake_server_id = server_id
    else:
        fake_server_id = id
    hs_instance = {
        "id": id,
        "type": "fake type",
        "host": "fake host",
        "deleted": False,
        "deleted_at": None,
        "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
        "updated_at": None,
        "server_id": fake_server_id
    }
    hs_instance.update(kwargs)
    return hs_instance

def stub_rbd(id, hs_instance_id=None, **kwargs):
    if hs_instance_id:
        fake_hs_instance_id = hs_instance_id
    else:
        fake_hs_instance_id = id
    rbd = {
        "id": id,
        "name": "fake name",
        "format": 1,
        "features": None,
        "order": 22,
        "size": 1073741824,
        "objects": 256,
        "object_size": 4194304,
        "block_name_prefix": "fake block name prefix",
        "flags": None,
        "deleted": False,
        "deleted_at": None,
        "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
        "updated_at": None,
        "hs_instance_id": fake_hs_instance_id
    }
    return rbd

def stub_pm_cache_ratio():
    pm_cache_ratio = [
        {
            "id": 112,
            "metric": "cache_total_size",
            "rbd_name": "fake rbd name",
            "value": "10737418240",
            "timestamp": 1484878824,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 134,
            "metric": "cache_used_size",
            "rbd_name": "fake rbd name",
            "value": "1024000",
            "timestamp": 1484878824,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 156,
            "metric": "cache_dirty_size",
            "rbd_name": "fake rbd name",
            "value": "102400",
            "timestamp": 1484878824,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        }
    ]
    return pm_cache_ratio

def stub_pm_cache_action():
    pm_cache_action = [
        {
            "id": 212,
            "metric": "cache_promote",
            "rbd_name": "fake rbd name",
            "value": "1234",
            "timestamp": 1484878784,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 234,
            "metric": "cache_flush",
            "rbd_name": "fake rbd name",
            "value": "829",
            "timestamp": 1484878784,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 256,
            "metric": "cache_evict",
            "rbd_name": "fake rbd name",
            "value": "599",
            "timestamp": 1484878784,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        }
    ]
    return pm_cache_action

def stub_pm_cache_io_workload():
    pm_cache_io_workload = [
        {
            "id": 312,
            "metric": "cache_read",
            "rbd_name": "fake rbd name",
            "value": "121",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 313,
            "metric": "cache_read_miss",
            "rbd_name": "fake rbd name",
            "value": "9",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 314,
            "metric": "cache_write",
            "rbd_name": "fake rbd name",
            "value": "324",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 315,
            "metric": "cache_write_miss",
            "rbd_name": "fake rbd name",
            "value": "2",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 316,
            "metric": "cache_bw",
            "rbd_name": "fake rbd name",
            "value": "591",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        },
        {
            "id": 317,
            "metric": "cache_latency",
            "rbd_name": "fake rbd name",
            "value": "4",
            "timestamp": 1484879184,
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        }
    ]
    return pm_cache_io_workload

def stub_rbd_cache_config(id, **kwargs):
    rbd_cache_config = {
        "id": id,
        "cache_ratio_health": 0.5,
        "cache_ratio_max": 0.7,
        "cache_dirty_ratio_min": 0.1,
        "clean_start": 0,
        "rbd_id": 1234,
        "cache_total_size": 2147483647,
        "cache_evict_interval": 1,
        "enable_memory_usage_tracker": True,
        "cache_flush_interval": 1,
        "cache_service_threads_num": 64,
        "object_size": 4096,
        "agent_threads_num": 128,
        "cache_dir": "/mnt/fake",
        "cache_flush_queue_depth": 256,
        "messenger_port": 8081,
        "log_to_file": "/fake",
        "deleted": False,
        "deleted_at": None,
        "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
        "updated_at": None
    }
    rbd_cache_config.update(kwargs)
    return rbd_cache_config

def stub_server_get_all(self, context):
    return [stub_server(1234, ip="1.2.3.4", host="1234"),
            stub_server(5678, ip="5.6.7.8", host="5678"),
            stub_server(9012, ip="9.0.1.2", host="9012")]

def stub_server_get(self, context, server_id):
    return stub_server(1234, status="available")

def stub_server_update(self, context, server_id, values):
    pass

def stub_hs_instance_create(self, context, values):
    type = values["type"]
    host = values["host"]
    server_id = values["server_id"]
    return stub_hs_instance(1,
                            type=type,
                            host=host,
                            server_id=server_id)

def stub_hs_instance_delete(self, context, hs_instance_id):
    pass

def stub_hs_instance_get(self, context, hs_instance_id):
    return stub_hs_instance(hs_instance_id)

def stub_rbd_get_all_by_hs_instance_id(self, context, hs_instance_id):
    return [stub_rbd(1234, hs_instance_id),
            stub_rbd(5678, hs_instance_id),
            stub_rbd(9012, hs_instance_id)]

def stub_hs_instance_get_all(self, context):
    return [stub_hs_instance(1234, server_id=1234),
            stub_hs_instance(5678, server_id=5678)]

def stub_rbd_get_all(self, context):
    return [stub_rbd(1234),
            stub_rbd(5678)]

def stub_rbd_get(self, context, rbd_id):
    return stub_rbd(rbd_id)

def stub_rbd_refresh(self, context):
    pass

def stub_performance_metric_get_by_rbd_name(self, context, rbd_name):
    return stub_pm_cache_ratio() + \
           stub_pm_cache_action() + \
           stub_pm_cache_io_workload() + \
           stub_pm_cache_ratio() + \
           stub_pm_cache_action() + \
           stub_pm_cache_io_workload()

def stub_os_and_kernel_get(self, context, hs_instance_id):
    return {"release": "fake release",
            "kernel": "fake kernel",
            "codename": "fake codename",
            "distributor_id": "fake distributor id"}

def stub_mem_get(self, context, hs_instance_id):
    return {"available": 188022784,
            "used": 1853497344,
            "cached": 112148480,
            "free": 75874304,
            "total": 1929371648,
            "buffers": 0}

def stub_cpu_get(self, context, hs_instance_id):
    return {"softirq": 0,
            "irq": 0,
            "system": 0,
            "guest": 0,
            "idle": 97.6,
            "user": 2.4,
            "guest_nice": 0,
            "iowait": 0,
            "steal": 0,
            "nice": 0}

def stub_hsm_summary_get(self, context):
    return {"total_rbds": 1,
            "hsm_version": "fake hsm version",
            "ceph_version": "fake ceph version",
            "total_hyperstash_instances": 1}

def stub_rbd_cache_config_update(self, context, rbd_cache_config_id, values):
    return stub_rbd_cache_config(rbd_cache_config_id,
                                 cache_dir="/mnt/fake")

def stub_rbd_cache_config_get_all(self, context):
    return [stub_rbd_cache_config(1234)]

def stub_rbd_cache_config_get(self, context, rbd_cache_config_id):
    return stub_rbd_cache_config(rbd_cache_config_id)

def stub_rbd_cache_config_get_by_rbd_id(self, context, rbd_id):
    return stub_rbd_cache_config(1234, rbd_id=int(rbd_id))
