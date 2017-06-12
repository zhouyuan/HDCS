
import urllib

from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes


cs = fakes.FakeClient()


class PerformanceMetricsTest(utils.TestCase):

    def test_get_value(self):
        type_list = ['cache_ratio',
                     'cache_action',
                     'cache_io_workload',
                     'rbd_basic_info']
        for type in type_list:
            rbd_id = 1234
            cs.performance_metrics.get_value(rbd_id, type)
            qparams = {"rbd_id": rbd_id,
                       "type": type}
            query_string = "?%s" % urllib.urlencode(qparams)
            cs.assert_called('GET', '/performance_metrics/get_value%s' %
                             query_string)

    def test_get_os_and_kernel(self):
        server_id = 1234
        cs.performance_metrics.get_os_and_kernel(server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        cs.assert_called('GET', '/performance_metrics/get_os_and_kernel%s' %
                         query_string)

    def test_get_mem(self):
        server_id = 1234
        cs.performance_metrics.get_mem(server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        cs.assert_called('GET', '/performance_metrics/get_mem%s' %
                         query_string)

    def test_get_cpu(self):
        server_id = 1234
        cs.performance_metrics.get_cpu(server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        cs.assert_called('GET', '/performance_metrics/get_cpu%s' %
                         query_string)

    def test_get_hsm_summary(self):
        cs.performance_metrics.get_hsm_summary()
        cs.assert_called('GET', '/performance_metrics/get_hsm_summary')
