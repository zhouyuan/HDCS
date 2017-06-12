
from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes
from hsmclient.v1 import servers

cs = fakes.FakeClient()


class ServersTest(utils.TestCase):

    def test_list(self):
        sl = cs.servers.list()
        cs.assert_called('GET', '/servers')
        for s in sl:
            self.assertIsInstance(s, servers.Server)

    def test_get(self):
        server_id = 1234
        cs.servers.get(server_id)
        cs.assert_called('GET', '/servers/%s' % server_id)

    def test_activate(self):
        server = cs.servers.get(1234)
        cs.servers.activate(server)
        cs.assert_called('POST', '/servers/1234/action')
