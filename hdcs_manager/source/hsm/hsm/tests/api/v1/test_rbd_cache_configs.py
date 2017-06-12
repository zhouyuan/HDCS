
import datetime

from hsm.api.v1 import rbd_cache_configs
from hsm import test
from hsm.scheduler import api as scheduler_api
from hsm.conductor import api as conductor_api
from hsm.tests.api import fakes
from hsm.tests.api.v1 import stubs


class RbdCacheConfigApiTest(test.TestCase):

    def setUp(self):
        super(RbdCacheConfigApiTest, self).setUp()
        self.controller = rbd_cache_configs.RbdCacheConfigController()

    def test_rbd_cache_config_update(self):
        self.stubs.Set(scheduler_api.API, 'rbd_cache_config_update',
                       stubs.stub_rbd_cache_config_update)

        req = fakes.HTTPRequest.blank('/v1/rbd_cache_configs/1234')
        body = {'rbd_cache_config': {
            'cache_dir': "/mnt/fake"
        }}
        res_dict = self.controller.update(req, 1234, body)
        expected = {'rbd_cache_config': {
            "id": 1234,
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
        }}
        self.assertEqual(res_dict, expected)

    def test_rbd_cache_config_list(self):
        self.stubs.Set(conductor_api.API, 'rbd_cache_config_get_all',
                       stubs.stub_rbd_cache_config_get_all)

        req = fakes.HTTPRequest.blank('/v1/rbd_cache_configs')
        res_dict = self.controller.index(req)
        expected = {'rbd_cache_configs': [
            {"id": 1234,
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
             "updated_at": None}]}
        self.assertEqual(res_dict, expected)

    def test_rbd_cache_config_get(self):
        self.stubs.Set(conductor_api.API, 'rbd_cache_config_get',
                       stubs.stub_rbd_cache_config_get)

        req = fakes.HTTPRequest.blank('/v1/rbd_cache_configs/1234')
        res_dict = self.controller.show(req, 1234)
        expected = {'rbd_cache_config': {
            "id": 1234,
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
        }}
        self.assertEqual(res_dict, expected)

    def test_rbd_cache_config_get_by_rbd_id(self):
        self.stubs.Set(conductor_api.API, 'rbd_cache_config_get_by_rbd_id',
                       stubs.stub_rbd_cache_config_get_by_rbd_id)

        req = fakes.HTTPRequest.blank('/v1/rbd_cache_configs/'
                                      'get_by_rbd_id?rbd_id=1234')
        res_dict = self.controller.get_by_rbd_id(req)
        expected = {'rbd_cache_config': {
            "id": 1234,
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
        }}
        self.assertEqual(res_dict, expected)
