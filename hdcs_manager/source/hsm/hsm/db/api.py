
from oslo_config import cfg

from hsm import flags
from hsm import utils

db_opts = [
    cfg.StrOpt('db_backend',
               default='sqlalchemy',
               help='The backend to use for db'),
    cfg.BoolOpt('enable_new_services',
                default=True,
                help='Services to be added to the available pool on create')]

FLAGS = flags.FLAGS
FLAGS.register_opts(db_opts)

IMPL = utils.LazyPluggable('db_backend',
                           sqlalchemy='hsm.db.sqlalchemy.api')

####################
# Service
####################
def service_destroy(context, service_id):
    """Destroy the service or raise if it does not exist."""
    return IMPL.service_destroy(context, service_id)

def service_get(context, service_id):
    """Get a service or raise if it does not exist."""
    return IMPL.service_get(context, service_id)

def service_get_all(context, disabled=None):
    """Get all services."""
    return IMPL.service_get_all(context, disabled)

def service_get_all_by_topic(context, topic):
    """Get all services for a given topic."""
    return IMPL.service_get_all_by_topic(context, topic)

def service_get_by_args(context, host, binary):
    """Get the state of an service by node name and binary."""
    return IMPL.service_get_by_args(context, host, binary)

def service_create(context, values):
    """Create a service from the values dictionary."""
    return IMPL.service_create(context, values)

def service_update(context, service_id, values):
    """Set the given properties on an service and update it.

    Raises NotFound if service does not exist.

    """
    return IMPL.service_update(context, service_id, values)

####################
# Server
####################
def server_create(context, values):
    """Create a new server."""
    return IMPL.server_create(context, values)

def server_get_by_host(context, host):
    """Get a server by name."""
    return IMPL.server_get_by_host(context, host)

def server_update(context, server_id, values):
    """Update a server by server id."""
    return IMPL.server_update(context, server_id, values)

def server_get_all(context):
    """Get a list of servers."""
    return IMPL.server_get_all(context)

def server_get(context, server_id):
    """Get a detail info of a server by id."""
    return IMPL.server_get(context, server_id)

####################
# Hs_Instance
####################
def hs_instance_create(context, values):
    """Create a new hyperstash instance."""
    return IMPL.hs_instance_create(context, values)

def hs_instance_get_all(context):
    """Get a list of hyperstash instances."""
    return IMPL.hs_instance_get_all(context)

def hs_instance_get(context, hs_instance_id):
    """Get a detail info of a hyperstash instance by id."""
    return IMPL.hs_instance_get(context, hs_instance_id)

def hs_instance_delete(context, hs_instance_id):
    """Delete the hyperstash instance from the db."""
    return IMPL.hs_instance_delete(context, hs_instance_id)

def hs_instance_get_by_host(context, host):
    """Get a detail info of a hyperstash instance by host."""
    return IMPL.hs_instance_get_by_host(context, host)

####################
# RBD
####################
def rbd_create(context, values):
    """Create a new rbd info into db."""
    return IMPL.rbd_create(context, values)

def rbd_get_all_by_hs_instance_id(context, hs_instance_id):
    """Get a list of rbds by hyperstash instance id."""
    return IMPL.rbd_get_all_by_hs_instance_id(context, hs_instance_id)

def rbd_delete(context, rbd_id):
    """Delete the rbd from the db."""
    return IMPL.rbd_delete(context, rbd_id)

def rbd_get_all(context):
    """Get a list of rbds."""
    return IMPL.rbd_get_all(context)

def rbd_get(context, rbd_id):
    """Get a detail info of a rbd by id."""
    return IMPL.rbd_get(context, rbd_id)

def rbd_get_by_name(context, name):
    """Get a detail info of a rbd by name."""
    return IMPL.rbd_get_by_name(context, name)

def rbd_update(context, rbd_id, values):
    """Update a rbd by rbd id."""
    return IMPL.rbd_update(context, rbd_id, values)

####################
# Performance Metric
####################
def performance_metric_get_by_rbd_name(context, rbd_name):
    """Get values by rbd name."""
    return IMPL.performance_metric_get_by_rbd_name(context, rbd_name)

####################
# RBD Cache Config
####################
def rbd_cache_config_get_all(context):
    """Get a list of rbd cache configs."""
    return IMPL.rbd_cache_config_get_all(context)

def rbd_cache_config_get(context, rbd_cache_config_id):
    """Get a detail info of a rbd cache config by id."""
    return IMPL.rbd_cache_config_get(context, rbd_cache_config_id)

def rbd_cache_config_get_by_rbd_id(context, rbd_id):
    """Get a detail info of a rbd cache config by rbd id."""
    return IMPL.rbd_cache_config_get_by_rbd_id(context, rbd_id)

def rbd_cache_config_create(context, values):
    """Create a new rbd cache config into db."""
    return IMPL.rbd_cache_config_create(context, values)

def rbd_cache_config_delete_by_rbd_id(context, rbd_id):
    """Delete a rbd cache config by rbd id."""
    return IMPL.rbd_cache_config_delete_by_rbd_id(context, rbd_id)

def rbd_cache_config_update(context, rbd_cache_config_id, values):
    """Update a rbd cache config by id."""
    return IMPL.rbd_cache_config_update(context, rbd_cache_config_id, values)

####################
# Periodic Task
####################
def performance_metric_clean_up_data(context, seconds):
    IMPL.performance_metric_clean_up_data(context, seconds)
