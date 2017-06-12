
import datetime

from hsm import test
from hsm.api.v1 import performance_metrics
from hsm.conductor import api as conductor_api
from hsm.tests.api.v1 import stubs
from hsm.tests.api import fakes
from hsm.scheduler import api as scheduler_api


class PerformanceMetricApiTest(test.TestCase):

    def setUp(self):
        super(PerformanceMetricApiTest, self).setUp()
        self.controller = performance_metrics.PerformanceMetricController()

    def test_pm_get_value_by_cache_ratio_type(self):
        self.stubs.Set(conductor_api.API, 'rbd_get',
                       stubs.stub_rbd_get)
        self.stubs.Set(conductor_api.API, 'performance_metric_get_by_rbd_name',
                       stubs.stub_performance_metric_get_by_rbd_name)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_value?rbd_id=1234&type=cache_ratio')
        res_dict = self.controller.get_value(req)
        expected = {'performance_metrics': [
            {"metric": "cache_total_size",
             "rbd_name": "fake rbd name",
             "value": "10737418240",
             "timestamp": 1484878824},
            {"metric": "cache_used_size",
             "rbd_name": "fake rbd name",
             "value": "1024000",
             "timestamp": 1484878824},
            {"metric": "cache_dirty_size",
             "rbd_name": "fake rbd name",
             "value": "102400",
             "timestamp": 1484878824}]}
        self.assertEqual(res_dict, expected)

    def test_pm_get_value_by_cache_action_type(self):
        self.stubs.Set(conductor_api.API, 'rbd_get',
                       stubs.stub_rbd_get)
        self.stubs.Set(conductor_api.API, 'performance_metric_get_by_rbd_name',
                       stubs.stub_performance_metric_get_by_rbd_name)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_value?rbd_id=1234&type=cache_action')
        res_dict = self.controller.get_value(req)
        expected = {'performance_metrics': [
            {"metric": "cache_promote",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484878784},
            {"metric": "cache_flush",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484878784},
            {"metric": "cache_evict",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484878784}]}
        self.assertEqual(res_dict, expected)

    def test_pm_get_value_by_cache_io_workload_type(self):
        self.stubs.Set(conductor_api.API, 'rbd_get',
                       stubs.stub_rbd_get)
        self.stubs.Set(conductor_api.API, 'performance_metric_get_by_rbd_name',
                       stubs.stub_performance_metric_get_by_rbd_name)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_value?rbd_id=1234&type=cache_io_workload')
        res_dict = self.controller.get_value(req)
        expected = {'performance_metrics': [
            {"metric": "cache_read",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484879184},
            {"metric": "cache_read_miss",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484879184},
            {"metric": "cache_write",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484879184},
            {"metric": "cache_write_miss",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484879184},
            {"metric": "cache_bw",
             "rbd_name": "fake rbd name",
             "value": 0,
             "timestamp": 1484879184},
            {"metric": "cache_latency",
             "rbd_name": "fake rbd name",
             "value": "4",
             "timestamp": 1484879184}]}
        self.assertEqual(res_dict, expected)

    def test_pm_get_value_by_rbd_basic_info_type(self):
        self.stubs.Set(conductor_api.API, 'rbd_get',
                       stubs.stub_rbd_get)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_value?rbd_id=1234&type=rbd_basic_info')
        res_dict = self.controller.get_value(req)
        expected = {'performance_metrics': [
            {"id": u'1234',
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
             "hs_instance_id": u'1234'}]}
        self.assertEqual(res_dict, expected)

    def test_pm_get_os_and_kernel(self):
        self.stubs.Set(scheduler_api.API, 'os_and_kernel_get',
                       stubs.stub_os_and_kernel_get)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_os_and_kernel?server_id=1234')
        res_dict = self.controller.get_os_and_kernel(req)
        expected = {'performance_metric': {
            "release": "fake release",
            "kernel": "fake kernel",
            "codename": "fake codename",
            "distributor_id": "fake distributor id"
        }}
        self.assertEqual(res_dict, expected)

    def test_pm_get_mem(self):
        self.stubs.Set(scheduler_api.API, 'mem_get',
                       stubs.stub_mem_get)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_mem?server_id=1234')
        res_dict = self.controller.get_mem(req)
        expected = {'performance_metric': {
            "available": 188022784,
            "used": 1853497344,
            "cached": 112148480,
            "free": 75874304,
            "total": 1929371648,
            "buffers": 0
        }}
        self.assertEqual(res_dict, expected)

    def test_pm_get_cpu(self):
        self.stubs.Set(scheduler_api.API, 'cpu_get',
                       stubs.stub_cpu_get)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_cpu?server_id=1234')
        res_dict = self.controller.get_cpu(req)
        expected = {'performance_metric': {
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
        }}
        self.assertEqual(res_dict, expected)

    def test_pm_get_hsm_summary(self):
        self.stubs.Set(scheduler_api.API, 'hsm_summary_get',
                       stubs.stub_hsm_summary_get)

        req = fakes.HTTPRequest.blank('/v1/performance_metrics/'
                                      'get_hsm_summary')
        res_dict = self.controller.get_hsm_summary(req)
        expected = {'performance_metric': {
            "total_rbds": 1,
            "hsm_version": "fake hsm version",
            "ceph_version": "fake ceph version",
            "total_hyperstash_instances": 1
        }}
        self.assertEqual(res_dict, expected)
