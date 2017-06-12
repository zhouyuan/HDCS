
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm import relationship

from hsm.db.sqlalchemy.session import get_session
from hsm import exception
from hsm.openstack.common import log as logging
from hsm.openstack.common import timeutils

LOG = logging.getLogger(__name__)

BASE = declarative_base()


class HsmBase(object):
    """Base class for Hsm Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False

    created_at = Column(DateTime, default=timeutils.utcnow)
    updated_at = Column(DateTime, onupdate=timeutils.utcnow)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def __init__(self):
        self._i = None

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        try:
            session.flush()
        except IntegrityError, e:
            if str(e).endswith('is not unique'):
                raise exception.Duplicate(str(e))
            else:
                raise

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = timeutils.utcnow()
        self.save(session=session)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()


class Service(BASE, HsmBase):
    """Represents a running service on a host."""

    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    host = Column(String(255))
    binary = Column(String(255))
    topic = Column(String(255))
    report_count = Column(Integer, nullable=False, default=0)
    disabled = Column(Boolean, default=False)
    availability_zone = Column(String(255), default='hsm')


class Server(BASE, HsmBase):
    """Represents a server."""

    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    ip = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    id_rsa_pub = Column(String(1024), nullable=False)


class HsInstance(BASE, HsmBase):
    """Represents a hyperstash instance."""

    __tablename__ = 'hs_instances'

    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)
    server = relationship(
        Server,
        backref="hs_instances",
        foreign_keys=server_id,
        primaryjoin='and_(HsInstance.server_id == Server.id,'
                    'Server.deleted == 0)'
    )


class Rbd(BASE, HsmBase):
    """Represents a rbd."""

    __tablename__ = 'rbds'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    objects = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    object_size = Column(Integer, nullable=False)
    block_name_prefix = Column(String(255), nullable=False)
    format = Column(Integer, nullable=False)
    features = Column(String(255))
    flags = Column(String(255))
    hs_instance_id = Column(Integer, ForeignKey('hs_instances.id'), nullable=False)
    hs_instance = relationship(
        HsInstance,
        backref="rbds",
        foreign_keys=hs_instance_id,
        primaryjoin='and_(Rbd.hs_instance_id == HsInstance.id,'
                    'HsInstance.deleted == 0)'
    )


class PerformanceMetric(BASE, HsmBase):
    """Represents a performance metric."""

    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True)
    metric = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    rbd_name = Column(String(255), nullable=False)
    timestamp = Column(Integer, nullable=False)


class RbdCacheConfig(BASE, HsmBase):
    """Reprsents a rbd cache config."""

    __tablename__ = 'rbd_cache_configs'

    id = Column(Integer, primary_key=True)
    cache_dir = Column(String(255), nullable=False)
    clean_start = Column(Integer, nullable=False)
    enable_memory_usage_tracker = Column(Boolean, default=False)
    object_size = Column(Integer, nullable=False)
    cache_total_size = Column(Integer, nullable=False)
    cache_dirty_ratio_min = Column(Float, nullable=False)
    # cache_dirty_ratio_max = Column(Float, nullable=False)
    cache_ratio_health = Column(Float, nullable=False)
    cache_ratio_max = Column(Float, nullable=False)
    cache_flush_interval = Column(Integer, nullable=False)
    cache_evict_interval = Column(Integer, nullable=False)
    cache_flush_queue_depth = Column(Integer, nullable=False)
    agent_threads_num = Column(Integer, nullable=False)
    cache_service_threads_num = Column(Integer, nullable=False)
    messenger_port = Column(Integer, nullable=False)
    log_to_file = Column(String(255), nullable=False)
    rbd_id = Column(Integer, ForeignKey('rbds.id'), nullable=False)
    rbd = relationship(
        Rbd,
        backref="rbd_cache_configs",
        foreign_keys=rbd_id,
        primaryjoin='and_(RbdCacheConfig.rbd_id == Rbd.id,'
                    'Rbd.deleted == 0)'
    )


class Setting(BASE, HsmBase):
    """Represents a setting."""

    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    default_value = Column(String(255), nullable=False)
    description = Column(String(255))
