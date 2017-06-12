
from oslo_config import cfg

from hsm import flags
from hsm.openstack.common import importutils

db_driver_opt = cfg.StrOpt('db_driver',
                           default='hsm.db',
                           help='driver to use for database access')

FLAGS = flags.FLAGS
FLAGS.register_opt(db_driver_opt)

class Base(object):
    """DB driver is injected in the init method."""

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver = FLAGS.db_driver
        self.db = importutils.import_module(db_driver)
