
import distutils.version as dist_version
import os

from hsm.db import migration
from hsm.db.sqlalchemy.session import get_engine
from hsm import exception
from hsm.openstack.common import log as logging

import migrate
from migrate.versioning import util as migrate_util
import sqlalchemy

LOG = logging.getLogger(__name__)

@migrate_util.decorator
def patched_with_engine(f, *a, **kw):
    url = a[0]
    engine = migrate_util.construct_engine(url, **kw)

    try:
        kw['engine'] = engine
        return f(*a, **kw)
    finally:
        if isinstance(engine, migrate_util.Engine) and engine is not url:
            migrate_util.log.debug('Disposing SQLAlchemy engine %s', engine)
            engine.dispose()

# TODO(jkoelker) When migrate 0.7.3 is released and hsm depends
#                on that version or higher, this can be removed
MIN_PKG_VERSION = dist_version.StrictVersion('0.7.3')
if (not hasattr(migrate, '__version__') or
    dist_version.StrictVersion(migrate.__version__) < MIN_PKG_VERSION):
    migrate_util.with_engine = patched_with_engine

# NOTE(jkoelker) Delay importing migrate until we are patched
from migrate import exceptions as versioning_exceptions
from migrate.versioning import api as versioning_api
from migrate.versioning.repository import Repository

_REPOSITORY = None

def db_sync(version=None):
    if version is not None:
        try:
            version = int(version)
        except ValueError:
            raise exception.Error("version should be an integer")

    current_version = db_version()
    repository = _find_migrate_repo()
    if version is None or version > current_version:
        return versioning_api.upgrade(get_engine(), repository, version)
    else:
        return versioning_api.downgrade(get_engine(), repository,
                                        version)

def db_version():
    repository = _find_migrate_repo()
    try:
        return versioning_api.db_version(get_engine(), repository)
    except versioning_exceptions.DatabaseNotControlledError:
        # If we aren't version controlled we may already have the database
        # in the state from before we started version control, check for that
        # and set up version_control appropriately
        meta = sqlalchemy.MetaData()
        engine = get_engine()
        meta.reflect(bind=engine)
        tables = meta.tables
        if len(tables) == 0:
            db_version_control(migration.INIT_VERSION)
            return versioning_api.db_version(get_engine(), repository)
        else:
            raise exception.Error("Upgrade DB using Essex release first.")

def db_version_control(version=None):
    repository = _find_migrate_repo()
    versioning_api.version_control(get_engine(), repository, version)
    return version

def _find_migrate_repo():
    """Get the path for the migrate repository."""
    global _REPOSITORY
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'migrate_repo')
    assert os.path.exists(path)
    if _REPOSITORY is None:
        _REPOSITORY = Repository(path)
    return _REPOSITORY
