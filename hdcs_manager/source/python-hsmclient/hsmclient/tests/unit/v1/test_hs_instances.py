
from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes
from hsmclient.v1 import hs_instances


cs = fakes.FakeClient()


class HsInstancesTest(utils.TestCase):

    def test_delete(self):
        hi = cs.hs_instances.list()[0]
        hi.delete()
        cs.assert_called('DELETE', '/hs_instances/1234')
        cs.hs_instances.delete('1234')
        cs.assert_called('DELETE', '/hs_instances/1234')
        cs.hs_instances.delete(hi)
        cs.assert_called('DELETE', '/hs_instances/1234')

    def test_list(self):
        hil = cs.hs_instances.list()
        cs.assert_called('GET', '/hs_instances')
        for hi in hil:
            self.assertIsInstance(hi, hs_instances.HsInstance)

    def test_get(self):
        hs_instance_id = '1234'
        cs.hs_instances.get(hs_instance_id)
        cs.assert_called('GET', '/hs_instances/%s' % hs_instance_id)
