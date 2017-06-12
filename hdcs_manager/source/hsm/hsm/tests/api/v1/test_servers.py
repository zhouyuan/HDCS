
import datetime

from hsm.api.v1 import servers
from hsm.conductor import api
from hsm import test
from hsm.tests.api import fakes
from hsm.tests.api.v1 import stubs


class ServerApiTest(test.TestCase):

    def setUp(self):
        super(ServerApiTest, self).setUp()
        self.controller = servers.ServerController()

    def test_server_list(self):
        self.stubs.Set(api.API, 'server_get_all', stubs.stub_server_get_all)

        req = fakes.HTTPRequest.blank('/v1/servers')
        res_dict = self.controller.index(req)
        expected = {'servers': [
            {"id": 1234,
            "ip": "1.2.3.4",
            "host": "1234",
            "id_rsa_pub": "fake id rsa pub",
            "status": "fake status",
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)},
            {"id": 5678,
            "ip": "5.6.7.8",
            "host": "5678",
            "id_rsa_pub": "fake id rsa pub",
            "status": "fake status",
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)},
            {"id": 9012,
            "ip": "9.0.1.2",
            "host": "9012",
            "id_rsa_pub": "fake id rsa pub",
            "status": "fake status",
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)},
        ]}
        self.assertEqual(res_dict, expected)

    def test_server_get(self):
        self.stubs.Set(api.API, 'server_get', stubs.stub_server_get)

        req = fakes.HTTPRequest.blank('/v1/servers/1234')
        res_dict = self.controller.show(req, 1234)
        expected = {'server': {
            "id": 1234,
            "ip": "fake ip",
            "host": "fake host",
            "id_rsa_pub": "fake id rsa pub",
            "status": "available",
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": datetime.datetime(1, 1, 1, 1, 1, 1)
        }}
        self.assertEqual(res_dict, expected)

    def test_server_activate(self):
        self.stubs.Set(api.API, 'server_get', stubs.stub_server_get)
        self.stubs.Set(api.API, 'hs_instance_create', stubs.stub_hs_instance_create)
        self.stubs.Set(api.API, 'server_update', stubs.stub_server_update)

        body = {
            "activate": None
        }
        req = fakes.HTTPRequest.blank('/v1/servers/1234/action', body)
        resp = self.controller.activate(req, 1234, body)
        self.assertEqual(resp.status_int, 202)
