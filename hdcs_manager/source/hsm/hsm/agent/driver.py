
from hsm import flags
from hsm.openstack.common import log as logging
from hsm import utils

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class CephDriver(object):
    """"""
    def __init__(self):
        pass

    def ceph_osd_pool_ls(self, format="json"):
        cmds = [
            'ceph',
            'osd',
            'pool',
            'ls',
            '-f',
            format
        ]
        out, _ = utils.execute(*cmds, run_as_root=True)
        return out

    def rbd_ls(self, pool, format="json"):
        cmds = [
            'rbd',
            'ls',
            '-p',
            pool,
            '--format',
            format
        ]
        out, _ = utils.execute(*cmds, run_as_root=True)
        return out

    def rbd_info(self, rbd, pool, format="json"):
        cmds = [
            'rbd',
            'info',
            rbd,
            '-p',
            pool,
            '--format',
            format
        ]
        out, _ = utils.execute(*cmds, run_as_root=True)
        return out

    def ceph_version(self):
        cmds = [
            'ceph',
            '--version'
        ]
        try:
            out, _ = utils.execute(*cmds, run_as_root=True)
            ceph_version = " ".join(out.split(" ")[2:3]).strip("\n").strip(" ")
        except:
            ceph_version = "--"
        return ceph_version
