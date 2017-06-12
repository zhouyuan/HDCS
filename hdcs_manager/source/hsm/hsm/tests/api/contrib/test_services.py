
from hsm.api.contrib import services
from hsm import context
from hsm import db
from hsm import exception
from hsm.openstack.common import timeutils
from hsm import policy
from hsm import test
from hsm.tests.api import fakes
from datetime import datetime


fake_services_list = [{'binary': 'hsm-agent',
                       'host': 'host1',
                       'availability_zone': 'hsm',
                       'id': 1,
                       'disabled': False,
                       'updated_at': datetime(2012, 10, 29, 13, 42, 2),
                       'created_at': datetime(2012, 9, 18, 2, 46, 27)},
                      {'binary': 'hsm-scheduler',
                       'host': 'host1',
                       'availability_zone': 'hsm',
                       'id': 2,
                       'disabled': False,
                       'updated_at': datetime(2012, 10, 29, 13, 42, 5),
                       'created_at': datetime(2012, 9, 18, 2, 46, 27)},
                      {'binary': 'hsm-conductor',
                       'host': 'host1',
                       'availability_zone': 'hsm',
                       'id': 3,
                       'disabled': False,
                       'updated_at': datetime(2012, 9, 19, 6, 55, 34),
                       'created_at': datetime(2012, 9, 18, 2, 46, 28)},
                      ]


class FakeRequest(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {}


# NOTE(uni): deprecating service request key, binary takes precedence
# Still keeping service key here for API compability sake.
class FakeRequestWithService(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {"service": "hsm-agent"}


class FakeRequestWithBinary(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {"binary": "hsm-agent"}


class FakeRequestWithHost(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {"host": "host1"}


# NOTE(uni): deprecating service request key, binary takes precedence
# Still keeping service key here for API compability sake.
class FakeRequestWithHostService(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {"host": "host1", "service": "hsm-agent"}


class FakeRequestWithHostBinary(object):
        environ = {"hsm.context": context.get_admin_context()}
        GET = {"host": "host1", "binary": "hsm-agent"}


def fake_service_get_all(context):
    return fake_services_list


def fake_service_get_by_host_binary(context, host, binary):
    for service in fake_services_list:
        if service['host'] == host and service['binary'] == binary:
            return service
    return None


def fake_service_get_by_id(value):
    for service in fake_services_list:
        if service['id'] == value:
            return service
    return None


def fake_service_update(context, service_id, values):
    service = fake_service_get_by_id(service_id)
    if service is None:
        raise exception.ServiceNotFound(service_id=service_id)
    else:
        return {'host': 'host1', 'service': 'hsm-agent',
                'disabled': values['disabled']}


def fake_policy_enforce(context, action, target):
    pass


def fake_utcnow():
    return datetime(2012, 10, 29, 13, 42, 11)


class ServicesTest(test.TestCase):

    def setUp(self):
        super(ServicesTest, self).setUp()

        self.stubs.Set(db, "service_get_all", fake_service_get_all)
        self.stubs.Set(timeutils, "utcnow", fake_utcnow)
        self.stubs.Set(db, "service_get_by_args",
                       fake_service_get_by_host_binary)
        self.stubs.Set(db, "service_update", fake_service_update)
        self.stubs.Set(policy, "enforce", fake_policy_enforce)

        self.context = context.get_admin_context()
        self.controller = services.ServiceController()

    def tearDown(self):
        super(ServicesTest, self).tearDown()

    def test_services_list(self):
        req = FakeRequest()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)},
                    {'binary': 'hsm-scheduler',
                     'host': 'host1', 'zone': 'hsm',
                     'status': 'enabled', 'state': 'up',
                     'updated_at': datetime(2012, 10, 29, 13, 42, 5)},
                    {'binary': 'hsm-conductor', 'host': 'host1',
                     'zone': 'hsm',
                     'status': 'enabled', 'state': 'up',
                     'updated_at': datetime(2012, 9, 19, 6, 55, 34)}]}
        self.assertEqual(res_dict, response)

    def test_services_list_with_host(self):
        req = FakeRequestWithHost()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)},
                    {'binary': 'hsm-scheduler',
                     'host': 'host1', 'zone': 'hsm',
                     'status': 'enabled', 'state': 'up',
                     'updated_at': datetime(2012, 10, 29, 13, 42, 5)},
                    {'binary': 'hsm-conductor', 'host': 'host1',
                     'zone': 'hsm',
                     'status': 'enabled', 'state': 'up',
                     'updated_at': datetime(2012, 9, 19, 6, 55, 34)}]}
        self.assertEqual(res_dict, response)

    def test_services_list_with_service(self):
        req = FakeRequestWithService()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)}]}
        self.assertEqual(res_dict, response)

    def test_services_list_with_binary(self):
        req = FakeRequestWithBinary()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)}]}
        self.assertEqual(res_dict, response)

    def test_services_list_with_host_service(self):
        req = FakeRequestWithHostService()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)}]}
        self.assertEqual(res_dict, response)

    def test_services_list_with_host_binary(self):
        req = FakeRequestWithHostBinary()
        res_dict = self.controller.index(req)

        response = {'services': [{'binary': 'hsm-agent',
                    'host': 'host1', 'zone': 'hsm',
                    'status': 'enabled', 'state': 'up',
                    'updated_at': datetime(2012, 10, 29, 13, 42, 2)}]}
        self.assertEqual(res_dict, response)

    def test_services_enable_with_service_key(self):
        body = {'host': 'host1', 'service': 'hsm-agent'}
        req = fakes.HTTPRequest.blank('/v1/fake/os-services/enable')
        res_dict = self.controller.update(req, "enable", body)

        self.assertEqual(res_dict['status'], 'enabled')

    def test_services_enable_with_binary_key(self):
        body = {'host': 'host1', 'binary': 'hsm-agent'}
        req = fakes.HTTPRequest.blank('/v1/fake/os-services/enable')
        res_dict = self.controller.update(req, "enable", body)

        self.assertEqual(res_dict['status'], 'enabled')
