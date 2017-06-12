
import datetime

from hsm.api.v1 import hs_instances
from hsm.conductor import api
from hsm import test
from hsm.tests.api import fakes
from hsm.tests.api.v1 import stubs


class HsInstanceApiTest(test.TestCase):

    def setUp(self):
        super(HsInstanceApiTest, self).setUp()
        self.controller = hs_instances.HsInstanceController()

    def test_hs_instance_delete(self):
        self.stubs.Set(api.API, 'hs_instance_get',
                       stubs.stub_hs_instance_get)
        self.stubs.Set(api.API, 'rbd_get_all_by_hs_instance_id',
                       stubs.stub_rbd_get_all_by_hs_instance_id)
        self.stubs.Set(api.API, 'hs_instance_delete',
                       stubs.stub_hs_instance_delete)

        req = fakes.HTTPRequest.blank('/v1/hs_instances/1234')
        resp = self.controller.delete(req, 1234)
        self.assertEqual(resp.status_int, 202)

    def test_hs_instance_list(self):
        self.stubs.Set(api.API, 'hs_instance_get_all',
                       stubs.stub_hs_instance_get_all)

        req = fakes.HTTPRequest.blank('/v1/hs_instances')
        res_dict = self.controller.index(req)
        expected = {'hs_instances': [
            {"id": 1234,
             "type": "fake type",
             "host": "fake host",
             "deleted": False,
             "deleted_at": None,
             "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
             "updated_at": None,
             "server_id": 1234},
            {"id": 5678,
             "type": "fake type",
             "host": "fake host",
             "deleted": False,
             "deleted_at": None,
             "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
             "updated_at": None,
             "server_id": 5678}
        ]}
        self.assertEqual(res_dict, expected)

    def test_hs_instance_get(self):
        self.stubs.Set(api.API, 'hs_instance_get',
                       stubs.stub_hs_instance_get)

        req = fakes.HTTPRequest.blank('/v1/hs_instances/1234')
        res_dict = self.controller.show(req, 1234)
        expected = {'hs_instance': {
            "id": 1234,
            "type": "fake type",
            "host": "fake host",
            "deleted": False,
            "deleted_at": None,
            "created_at": datetime.datetime(1, 1, 1, 1, 1, 1),
            "updated_at": None,
            "server_id": 1234
        }}
        self.assertEqual(res_dict, expected)
