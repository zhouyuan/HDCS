
import urllib

import fixtures
from requests_mock.contrib import fixture as requests_mock_fixture

from hsmclient import client
from hsmclient import shell
from hsmclient.tests.unit.fixture_data import keystone_client
from hsmclient.tests.unit import utils
from hsmclient.tests.unit.v1 import fakes


cs = fakes.FakeClient()


class ShellTest(utils.TestCase):

    FAKE_ENV = {
        'HSM_USERNAME': 'username',
        'HSM_PASSWORD': 'password',
        'HSM_PROJECT_ID': 'project_id',
        'HSM_URL': keystone_client.BASE_URL,
    }

    def setUp(self):
        super(ShellTest, self).setUp()
        for var in self.FAKE_ENV:
            self.useFixture(fixtures.EnvironmentVariable(var,
                                                         self.FAKE_ENV[var]))

        self.shell = shell.OpenStackHsmShell()

        self.old_get_client_class = client.get_client_class
        client.get_client_class = lambda *_: fakes.FakeClient

        self.requests = self.useFixture(requests_mock_fixture.Fixture())
        self.requests.register_uri(
            'GET', keystone_client.BASE_URL,
            text=keystone_client.keystone_request_callback)

    def tearDown(self):
        if hasattr(self.shell, 'cs'):
            self.shell.cs.clear_callstack()

        client.get_client_class = self.old_get_client_class
        super(ShellTest, self).tearDown()

    def run_command(self, cmd):
        self.shell.main(cmd.split())

    def assert_called(self, method, url, body=None, **kwargs):
        return self.shell.cs.assert_called(method, url, body, **kwargs)

    def assert_called_anytime(self, method, url, body=None):
        return self.shell.cs.assert_called_anytime(method, url, body)

    #
    # Servers
    #
    def test_list_servers(self):
        self.run_command('server-list')
        self.assert_called('GET', '/servers')

    def test_show_server(self):
        self.run_command('server-show 1234')
        self.assert_called('GET', '/servers/1234')

    def test_activate_server(self):
        self.run_command('server-activate 1234')
        self.assert_called('POST', '/servers/1234/action')

    #
    # Hyperstash Instances
    #
    def test_list_hs_instances(self):
        self.run_command('hs-instance-list')
        self.assert_called('GET', '/hs_instances')

    def test_show_hs_instance(self):
        self.run_command('hs-instance-show 1234')
        self.assert_called('GET', '/hs_instances/1234')

    #
    # Rbds
    #
    def test_list_rbds(self):
        self.run_command('rbd-list')
        self.assert_called('GET', '/rbds')

    def test_show_rbd(self):
        self.run_command('rbd-show 1234')
        self.assert_called('GET', '/rbds/1234')

    def test_refresh_rbds(self):
        self.run_command('rbd-refresh')
        self.assert_called('POST', '/rbds/refresh')

    #
    # Performance Metrics
    #
    def test_get_value_performance_metrics(self):
        rbd_id = 1234
        for type in ['cache_ratio', 'cache_action',
                     'cache_io_workload', 'rbd_basic_info']:
            self.run_command('performance-metric-get-value --rbd-id %s '
                             '--type %s' % (rbd_id, type))
            qparams = {"rbd_id": rbd_id,
                       "type": type}
            query_string = "?%s" % urllib.urlencode(qparams)
            self.assert_called('GET', '/performance_metrics/get_value%s' %
                               query_string)

    def test_get_os_and_kernel_performance_metrics(self):
        server_id = 1234
        self.run_command('performance-metric-get-os-and-kernel '
                         '--server-id %s' % server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        self.assert_called('GET', '/performance_metrics/get_os_and_kernel%s' %
                           query_string)

    def test_get_mem_performance_metrics(self):
        server_id = 1234
        self.run_command('performance-metric-get-mem '
                         '--server-id %s' % server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        self.assert_called('GET', '/performance_metrics/get_mem%s' %
                           query_string)

    def test_get_cpu_performance_metrics(self):
        server_id = 1234
        self.run_command('performance-metric-get-cpu '
                         '--server-id %s' % server_id)
        qparams = {"server_id": server_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        self.assert_called('GET', '/performance_metrics/get_cpu%s' %
                           query_string)

    def test_get_hsm_summary_performance_metrics(self):
        self.run_command('performance-metric-get-hsm-summary')
        self.assert_called('GET', '/performance_metrics/get_hsm_summary')

    #
    # Rbd Cache Configs
    #
    def test_list_rbd_cache_configs(self):
        self.run_command('rbd-cache-config-list')
        self.assert_called('GET', '/rbd_cache_configs')

    def test_show_rbd_cache_config(self):
        self.run_command('rbd-cache-config-show 1234')
        self.assert_called('GET', '/rbd_cache_configs/1234')

    def test_show_rbd_cache_config_by_rbd_id(self):
        rbd_id = 1234
        self.run_command('rbd-cache-config-show-by-rbd-id '
                         '--rbd-id %s' % rbd_id)
        qparams = {"rbd_id": rbd_id}
        query_string = "?%s" % urllib.urlencode(qparams)
        self.assert_called('GET', '/rbd_cache_configs/get_by_rbd_id%s' %
                           query_string)
