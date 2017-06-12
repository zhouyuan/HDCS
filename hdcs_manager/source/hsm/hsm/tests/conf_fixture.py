
from oslo_config import cfg


CONF = cfg.CONF


def set_defaults(conf):
    conf.set_default('fake_rabbit', True)
    conf.set_default('rpc_backend', 'hsm.openstack.common.rpc.impl_fake')
    conf.set_default('verbose', True)
