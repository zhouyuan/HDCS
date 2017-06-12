
import os

import fixtures
import mox
from oslo_config import cfg
import stubout
import testtools

from hsm.openstack.common import log as logging
from hsm.openstack.common import timeutils
from hsm.tests import conf_fixture


test_opts = [
    cfg.BoolOpt('fake_tests',
                default=True,
                help='should we use everything for testing'), ]

CONF = cfg.CONF
CONF.register_opts(test_opts)

LOG = logging.getLogger(__name__)


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each test method to initialize test environment."""
        super(TestCase, self).setUp()

        test_timeout = os.environ.get('OS_TEST_TIMEOUT', 0)
        try:
            test_timeout = int(test_timeout)
        except ValueError:
            # If timeout value is invalid do not set a timeout.
            test_timeout = 0
        if test_timeout > 0:
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))
        self.useFixture(fixtures.NestedTempfile())
        self.useFixture(fixtures.TempHomeDir())

        if (os.environ.get('OS_STDOUT_CAPTURE') == 'True' or
                os.environ.get('OS_STDOUT_CAPTURE') == '1'):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if (os.environ.get('OS_STDERR_CAPTURE') == 'True' or
                os.environ.get('OS_STDERR_CAPTURE') == '1'):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        self.log_fixture = self.useFixture(fixtures.FakeLogger())

        conf_fixture.set_defaults(CONF)
        CONF([], default_config_files=[])

        self.start = timeutils.utcnow()

        self.log_fixture = self.useFixture(fixtures.FakeLogger())

        self.mox = mox.Mox()
        self.stubs = stubout.StubOutForTesting()
        self.addCleanup(CONF.reset)
        self.addCleanup(self.mox.UnsetStubs)
        self.addCleanup(self.stubs.UnsetAll)
        self.addCleanup(self.stubs.SmartUnsetAll)
        self.addCleanup(self.mox.VerifyAll)
        self.injected = []
        self._services = []

    def tearDown(self):
        """Runs after each test method to tear down test environment."""

        # Stop any timers
        for x in self.injected:
            try:
                x.stop()
            except AssertionError:
                pass

        # Kill any services
        for x in self._services:
            try:
                x.kill()
            except Exception:
                pass

        # Delete attributes that don't start with _ so they don't pin
        # memory around unnecessarily for the duration of the test
        # suite
        for key in [k for k in self.__dict__.keys() if k[0] != '_']:
            del self.__dict__[key]
        super(TestCase, self).tearDown()
