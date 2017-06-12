
import warnings

from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import literal_column

from hsm.db.sqlalchemy import models
from hsm.db.sqlalchemy.session import get_session
from hsm import exception
from hsm import flags
from hsm.openstack.common import log as logging
from hsm.openstack.common import timeutils

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


def is_admin_context(context):
    """Indicates if the request context is an administrator."""
    if not context:
        warnings.warn('Use of empty request context is deprecated',
                      DeprecationWarning)
        raise Exception('die')
    return context.is_admin


def is_user_context(context):
    """Indicates if the request context is a normal user."""
    if not context:
        return False
    if context.is_admin:
        return False
    if not context.user_id or not context.project_id:
        return False
    return True


def require_admin_context(f):
    """Decorator to require admin request context.

    The first argument to the wrapped function must be the context.

    """

    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise exception.AdminRequired()
        return f(*args, **kwargs)
    return wrapper


def model_query(context, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or context.read_deleted
    project_only = kwargs.get('project_only')

    query = session.query(*args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception("Unrecognized read_deleted value '%s'" % read_deleted)

    if project_only and is_user_context(context):
        query = query.filter_by(project_id=context.project_id)

    return query


@require_admin_context
def service_destroy(context, service_id):
    session = get_session()
    with session.begin():
        service_ref = service_get(context, service_id, session=session)
        service_ref.delete(session=session)


@require_admin_context
def service_get(context, service_id, session=None):
    result = model_query(
        context,
        models.Service,
        session=session).\
        filter_by(id=service_id).\
        first()
    if not result:
        raise exception.ServiceNotFound(service_id=service_id)

    return result


@require_admin_context
def service_get_all(context, disabled=None):
    query = model_query(context, models.Service)
    if disabled is not None:
        query = query.filter_by(disabled=disabled)

    return query.all()


@require_admin_context
def service_get_all_by_topic(context, topic):
    return model_query(
        context, models.Service, read_deleted="no").\
        filter_by(disabled=False).\
        filter_by(topic=topic).\
        all()


@require_admin_context
def service_get_by_args(context, host, binary):
    result = model_query(context, models.Service).\
        filter_by(host=host).\
        filter_by(binary=binary).\
        first()

    if not result:
        raise exception.HostBinaryNotFound(host=host, binary=binary)

    return result


@require_admin_context
def service_create(context, values):
    service_ref = models.Service()
    service_ref.update(values)
    if not FLAGS.enable_new_services:
        service_ref.disabled = True
    service_ref.save()
    return service_ref


@require_admin_context
def service_update(context, service_id, values):
    session = get_session()
    with session.begin():
        service_ref = service_get(context, service_id, session=session)
        service_ref.update(values)
        service_ref.save(session=session)


####################
# Server
####################
@require_admin_context
def server_create(context, values):
    server_ref = models.Server()
    server_ref.update(values)
    server_ref.save()
    return server_ref

@require_admin_context
def server_get(context, server_id, session=None):
    result = model_query(context, models.Server, session=session).\
        filter_by(id=server_id).\
        first()

    if not result:
        raise exception.ServerNotFound(server_id=server_id)

    return result

@require_admin_context
def server_get_by_host(context, host):
    return model_query(context, models.Server).\
        filter_by(host=host).\
        first()

@require_admin_context
def server_update(context, server_id, values):
    session = get_session()
    with session.begin():
        server_ref = server_get(context, server_id, session=session)
        server_ref.update(values)
        server_ref.save(session=session)

@require_admin_context
def server_get_all(context):
    session = get_session()
    with session.begin():
        query = model_query(context, models.Server)
        return query.all()

####################
# Hs_Instance
####################
@require_admin_context
def hs_instance_create(context, values):
    hs_instance_ref = models.HsInstance()
    hs_instance_ref.update(values)
    hs_instance_ref.save()
    return hs_instance_ref

@require_admin_context
def hs_instance_get_all(context):
    session = get_session()
    with session.begin():
        query = model_query(context, models.HsInstance).\
            options(joinedload('server'))
        return query.all()

@require_admin_context
def hs_instance_get(context, hs_instance_id, session=None):
    result = model_query(context, models.HsInstance, session=session).\
        filter_by(id=hs_instance_id).\
        options(joinedload('server')).\
        first()

    if not result:
        raise exception.HsInstanceNotFound(hs_instance_id=hs_instance_id)

    return result

@require_admin_context
def hs_instance_delete(context, hs_instance_id):
    session = get_session()
    with session.begin():
        session.query(models.HsInstance).\
            filter_by(id=hs_instance_id).\
            update({'deleted': True,
                    'deleted_at': timeutils.utcnow(),
                    'updated_at': literal_column('updated_at')})

@require_admin_context
def hs_instance_get_by_host(context, host, session=None):
    result = model_query(context, models.HsInstance, session=session).\
        filter_by(host=host).\
        options(joinedload('server')).\
        first()

    return result

####################
# RBD
####################
@require_admin_context
def rbd_create(context, values):
    rbd_ref = models.Rbd()
    rbd_ref.update(values)
    rbd_ref.save()
    return rbd_ref

@require_admin_context
def rbd_get_all_by_hs_instance_id(context, hs_instance_id):
    return model_query(context, models.Rbd).\
        filter_by(hs_instance_id=hs_instance_id).\
        options(joinedload('hs_instance')).\
        all()

@require_admin_context
def rbd_delete(context, rbd_id):
    session = get_session()
    with session.begin():
        session.query(models.Rbd).\
            filter_by(id=rbd_id).\
            update({'deleted': True,
                    'deleted_at': timeutils.utcnow(),
                    'updated_at': literal_column('updated_at')})

@require_admin_context
def rbd_get_all(context):
    session = get_session()
    with session.begin():
        query = model_query(context, models.Rbd).\
            options(joinedload('hs_instance'))
        return query.all()

@require_admin_context
def rbd_get(context, rbd_id, session=None):
    result = model_query(context, models.Rbd, session=session).\
        filter_by(id=rbd_id).\
        options(joinedload('hs_instance')).\
        first()

    if not result:
        raise exception.RbdNotFound(rbd_id=rbd_id)

    return result

@require_admin_context
def rbd_get_by_name(context, name, session=None):
    result = model_query(context, models.Rbd, session=session).\
        filter_by(name=name).\
        options(joinedload('hs_instance')).\
        first()

    return result

@require_admin_context
def rbd_update(context, rbd_id, values):
    session = get_session()
    with session.begin():
        rbd_ref = rbd_get(context, rbd_id, session=session)
        rbd_ref.update(values)
        rbd_ref.save(session=session)

####################
# Performance Metric
####################
def performance_metric_get_by_rbd_name(context, rbd_name):
    result = model_query(context, models.PerformanceMetric).\
        filter_by(rbd_name=rbd_name).\
        all()
    return result

####################
# RBD Cache Config
####################
def rbd_cache_config_get_all(context):
    session = get_session()
    with session.begin():
        query = model_query(context, models.RbdCacheConfig)
        return query.all()

def rbd_cache_config_get(context, rbd_cache_config_id, session=None):
    result = model_query(context, models.RbdCacheConfig, session=session).\
        filter_by(id=rbd_cache_config_id).\
        first()

    if not result:
        raise exception.RbdCacheConfigNotFound(
            rbd_cache_config_id=rbd_cache_config_id)

    return result

def rbd_cache_config_get_by_rbd_id(context, rbd_id):
    result = model_query(context, models.RbdCacheConfig).\
        filter_by(rbd_id=rbd_id).\
        first()
    return result

def rbd_cache_config_create(context, values):
    rbd_cache_config_ref = models.RbdCacheConfig()
    rbd_cache_config_ref.update(values)
    rbd_cache_config_ref.save()
    return rbd_cache_config_ref

def rbd_cache_config_delete_by_rbd_id(context, rbd_id):
    session = get_session()
    with session.begin():
        session.query(models.RbdCacheConfig).\
            filter_by(rbd_id=rbd_id).\
            update({'deleted': True,
                    'deleted_at': timeutils.utcnow(),
                    'updated_at': literal_column('updated_at')})

def rbd_cache_config_update(context, rbd_cache_config_id, values):
    session = get_session()
    with session.begin():
        rbd_cache_config_ref = rbd_cache_config_get(context,
                                          rbd_cache_config_id,
                                          session=session)
        rbd_cache_config_ref.update(values)
        rbd_cache_config_ref.save(session=session)
        return rbd_cache_config_ref

####################
# Periodic Task
####################
def performance_metric_clean_up_data(context, seconds):
    session = get_session()
    result = model_query(context, models.PerformanceMetric, session=session).\
        all()
    if not result:
        return
    last = result[-1]
    LOG.info("The latest performance metric data is %s" % str(last))
    timestamp = last.timestamp
    LOG.info("The timestamp of latest performance metric data is %s" % str(timestamp))
    min_timestamp = int(timestamp) - int(seconds)
    LOG.info("min_timestamp: %s" % str(min_timestamp))
    sql_str = "UPDATE performance_metrics SET deleted=1 WHERE timestamp < %s;" % min_timestamp
    session.execute(sql_str)
