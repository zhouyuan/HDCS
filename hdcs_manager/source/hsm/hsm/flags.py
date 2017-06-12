
import os
import socket

from oslo_config import cfg
from hsm import version

FLAGS = cfg.CONF

def parse_args(argv, default_config_files=None):
    FLAGS(argv[1:], project='hsm',
          version=version.version_string(),
          default_config_files=default_config_files)

class UnrecognizedFlag(Exception):
    pass


def _get_my_ip():
    """
    Returns the actual ip of the local machine.

    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, a Google DNS server is used, but the specific address does not
    matter much.  No traffic is actually sent.
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

core_opts = [
    cfg.StrOpt('sql_connection',
               default='sqlite:///$state_path/$sqlite_db',
               help='The SQLAlchemy connection string used to connect to the '
                    'database',
               secret=True),
    cfg.IntOpt('sql_connection_debug',
               default=0,
               help='Verbosity of SQL debugging information. 0=None, '
                    '100=Everything'),
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help='File name for the paste.deploy config for hsm-api'),
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               help='Directory where the hsm python module is installed'),
    cfg.StrOpt('bindir',
               default='$pybasedir/bin',
               help='Directory where hsm binaries are installed'),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help="Top-level directory for maintaining hsm's state"), ]


debug_opts = [
]


FLAGS.register_cli_opts(core_opts)
FLAGS.register_cli_opts(debug_opts)

global_opts = [
    cfg.StrOpt('hsm_config',
               default='/etc/hsm/hsm.conf',
               help='hsm.conf'),
    cfg.StrOpt('hsm_user',
               default='hsm',
               help='user name of hsm'),
    cfg.StrOpt('my_ip',
               default=_get_my_ip(),
               help='ip address of this host'),
    cfg.StrOpt('agent_topic',
               default='hsm-agent',
               help='the topic agent nodes listen on'),
    cfg.StrOpt('conductor_topic',
               default='hsm-conductor',
               help='the topic conductor nodes listen on'),
    cfg.StrOpt('scheduler_topic',
               default='hsm-scheduler',
               help='the topic scheduler nodes listen on'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help="Deploy v1 of the Hsm API. "),
    cfg.BoolOpt('api_rate_limit',
                default=True,
                help='whether to rate limit the api'),
    cfg.ListOpt('hsmapi_storage_ext_list',
                default=[],
                help='Specify list of extensions to load when using osapi_'
                     'storage_extension option with hsm.api.contrib.'
                     'select_extensions'),
    cfg.MultiStrOpt('hsmapi_storage_extension',
                    default=['hsm.api.contrib.standard_extensions'],
                    help='osapi storage extension to load'),
    cfg.IntOpt('osapi_max_limit',
               default=1000,
               help='the maximum number of items returned in a single '
                    'response from a collection resource'),
    cfg.IntOpt('sql_idle_timeout',
               default=3600,
               help='timeout before idle sql connections are reaped'),
    cfg.IntOpt('sql_max_retries',
               default=10,
               help='maximum db connection retries during startup. '
                    '(setting -1 implies an infinite retry count)'),
    cfg.IntOpt('sql_retry_interval',
               default=10,
               help='interval between retries of opening a sql connection'),
    cfg.StrOpt('conductor_manager',
               default='hsm.conductor.manager.ConductorManager',
               help='full class name for the Manager for Conductor'),
    cfg.StrOpt('id_rsa_pub',
               default='/root/.ssh/id_rsa.pub',
               help='id_rsa.pub'),
    cfg.StrOpt('key_name',
               default='/root/.ssh/id_rsa',
               help='the name of key'),
    cfg.StrOpt('etc_hosts',
               default='/etc/hosts',
               help='host name list'),
    cfg.StrOpt('agent_manager',
               default='hsm.agent.manager.AgentManager',
               help='full class name for the Manager for Conductor'),
    cfg.StrOpt('hsm_config_path',
               default='/etc/hsm/',
               help='configure path of hsm to reside hsm.conf api-paste.ini'),
    cfg.StrOpt('scheduler_manager',
               default='hsm.scheduler.manager.SchedulerManager',
               help='full class name for the Manager for Scheduler'),
    cfg.StrOpt('host',
               default=socket.gethostname().split('.')[0],
               help='Name of this node.  This can be an opaque identifier.  '
                    'It is not necessarily a hostname, FQDN, or IP address.'),
    cfg.StrOpt('storage_availability_zone',
               default='hsm',
               help='availability zone of this node'),
    cfg.StrOpt('root_helper',
               default='sudo',
               help='Deprecated: command to use for running commands as root'),
    cfg.StrOpt('rootwrap_config',
               default=None,
               help='Path to the rootwrap configuration file to use for '
                    'running commands as root'),
    cfg.BoolOpt('monkey_patch',
                default=False,
                help='Whether to log monkey patching'),
    cfg.ListOpt('monkey_patch_modules',
                default=[],
                help='List of modules/decorators to monkey patch'),
    cfg.IntOpt('service_down_time',
               default=60,
               help='maximum time since last check-in for up service'),
    cfg.StrOpt('storage_api_class',
               default='hsm.storage.api.API',
               help='The full class name of the storage API class to use'),
    cfg.StrOpt('auth_strategy',
               default='noauth',
               help='The strategy to use for auth. Supports noauth, keystone, '
                    'and deprecated.')]

FLAGS.register_opts(global_opts)
