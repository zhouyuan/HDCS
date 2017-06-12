
from hsm.api import extensions
from hsm import flags
from hsm.openstack.common import log as logging

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


def standard_extensions(ext_mgr):
    extensions.load_standard_extensions(ext_mgr, LOG, __path__, __package__)


def select_extensions(ext_mgr):
    extensions.load_standard_extensions(ext_mgr, LOG, __path__, __package__,
                                        FLAGS.hsmapi_storage_ext_list)
