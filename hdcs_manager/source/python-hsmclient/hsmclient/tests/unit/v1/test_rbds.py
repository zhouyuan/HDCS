
from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes
from hsmclient.v1 import rbds


cs = fakes.FakeClient()


class RbdsTest(utils.TestCase):

    def test_list(self):
        rl = cs.rbds.list()
        cs.assert_called('GET', '/rbds')
        for r in rl:
            self.assertIsInstance(r, rbds.Rbd)

    def test_get(self):
        rbd_id = 1234
        cs.rbds.get(rbd_id)
        cs.assert_called('GET', '/rbds/%s' % rbd_id)

    def test_refresh(self):
        cs.rbds.refresh()
        cs.assert_called('POST', '/rbds/refresh')
