
import datetime

from hsm.api.v1 import rbds
from hsm import test
from hsm.conductor import api as conductor_api
from hsm.scheduler import api as scheduler_api
from hsm.tests.api.v1 import stubs
from hsm.tests.api import fakes


class RbdApiTest(test.TestCase):

    def setUp(self):
        super(RbdApiTest, self).setUp()
        self.controller = rbds.RbdController()

    def test_rbd_list(self):
        self.stubs.Set(conductor_api.API, 'rbd_get_all',
                       stubs.stub_rbd_get_all)

        req = fakes.HTTPRequest.blank('/v1/rbds')
        res_dict = self.controller.index(req)
        expected = {'rbds': [
            {"id": 1234,
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
             "hs_instance_id": 1234},
            {"id": 5678,
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
             "hs_instance_id": 5678}
        ]}
        self.assertEqual(res_dict, expected)

    def test_rbd_get(self):
        self.stubs.Set(conductor_api.API, 'rbd_get',
                       stubs.stub_rbd_get)

        req = fakes.HTTPRequest.blank('/v1/rbds/1234')
        res_dict = self.controller.show(req, 1234)
        expected = {'rbd': {
            "id": 1234,
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
            "hs_instance_id": 1234
        }}
        self.assertEqual(res_dict, expected)

    def test_rbd_refresh(self):
        self.stubs.Set(scheduler_api.API, 'rbd_refresh',
                       stubs.stub_rbd_refresh)

        req = fakes.HTTPRequest.blank('/v1/rbds/refresh', None)
        resp = self.controller.refresh(req, None)
        self.assertEqual(resp.status_int, 200)
