
import urllib

from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes
from hsmclient.v1 import rbd_cache_configs


cs = fakes.FakeClient()


class RbdCacheConfigsTest(utils.TestCase):

    def test_list(self):
        rccl = cs.rbd_cache_configs.list()
        cs.assert_called('GET', '/rbd_cache_configs')
        for rcc in rccl:
            self.assertIsInstance(rcc, rbd_cache_configs.RbdCacheConfig)

    def test_get(self):
        rbd_cache_config_id = 1234
        cs.rbd_cache_configs.get(rbd_cache_config_id)
        cs.assert_called('GET', '/rbd_cache_configs/%s' %
                         rbd_cache_config_id)

    def test_get_by_rbd_id(self):
        rbd_id = 1234
        cs.rbd_cache_configs.get_by_rbd_id(rbd_id)
        qparams = {"rbd_id": rbd_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        cs.assert_called('GET', '/rbd_cache_configs/get_by_rbd_id%s' %
                         query_string)
