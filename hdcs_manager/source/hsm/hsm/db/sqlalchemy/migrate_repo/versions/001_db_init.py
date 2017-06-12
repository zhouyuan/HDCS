
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table


def define_tables(meta):
    services = Table(
        'services', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('host', String(255)),
        Column('binary', String(255)),
        Column('topic', String(255)),
        Column('report_count', Integer, nullable=False),
        Column('disabled', Boolean),
        Column('availability_zone', String(255)),
        mysql_engine='InnoDB'
    )

    servers = Table(
        'servers', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('host', String(255), nullable=False),
        Column('ip', String(255), nullable=False),
        Column('status', String(255), nullable=False),
        Column('id_rsa_pub', String(1024), nullable=False),
        mysql_engine='InnoDB'
    )

    hs_instances = Table(
        'hs_instances', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('host', String(255), nullable=False),
        Column('type', String(255), nullable=False),
        Column('server_id', Integer, ForeignKey('servers.id'), nullable=False),
        mysql_engine='InnoDB'
    )

    rbds = Table(
        'rbds', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(255), nullable=False),
        Column('size', Integer, nullable=False),
        Column('objects', Integer, nullable=False),
        Column('order', Integer, nullable=False),
        Column('object_size', Integer, nullable=False),
        Column('block_name_prefix', String(255), nullable=False),
        Column('format', Integer, nullable=False),
        Column('features', String(255)),
        Column('flags', String(255)),
        Column('hs_instance_id', Integer, nullable=False),
        mysql_engine='InnoDB'
    )

    performance_metrics = Table(
        'performance_metrics', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('metric', String(255), nullable=False),
        Column('value', String(255), nullable=False),
        Column('rbd_name', String(255), nullable=False),
        Column('timestamp', Integer, nullable=False),
        mysql_engine='InnoDB'
    )

    rbd_cache_configs = Table(
        'rbd_cache_configs', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('cache_dir', String(255), nullable=False),
        Column('clean_start', Integer, nullable=False),
        Column('enable_memory_usage_tracker', Boolean, nullable=False),
        Column('object_size', Integer, nullable=False),
        Column('cache_total_size', Integer, nullable=False),
        Column('cache_dirty_ratio_min', Float, nullable=False),
        # Column('cache_dirty_ratio_max', Float, nullable=False),
        Column('cache_ratio_health', Float, nullable=False),
        Column('cache_ratio_max', Float, nullable=False),
        Column('cache_flush_interval', Integer, nullable=False),
        Column('cache_evict_interval', Integer, nullable=False),
        Column('cache_flush_queue_depth', Integer, nullable=False),
        Column('agent_threads_num', Integer, nullable=False),
        Column('cache_service_threads_num', Integer, nullable=False),
        Column('messenger_port', Integer, nullable=False),
        Column('log_to_file', String(255), nullable=False),
        Column('rbd_id', Integer, nullable=False),
        mysql_engine='InnoDB'
    )

    settings = Table(
        'settings', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(255), nullable=False),
        Column('value', String(255), nullable=False),
        Column('default_value', String(255), nullable=False),
        Column('description', String(255)),
        mysql_engine='InnoDB'
    )

    return [services,
            servers,
            hs_instances,
            rbds,
            performance_metrics,
            rbd_cache_configs,
            settings]


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    # create all tables
    # Take care on create order for those with FK dependencies
    tables = define_tables(meta)

    for table in tables:
        table.create()

    if migrate_engine.name == "mysql":
        tables = ["services",
                  "servers",
                  "hs_instances",
                  "rbds",
                  "performance_metrics",
                  "rbd_cache_configs",
                  "settings"]

        migrate_engine.execute("SET foreign_key_checks = 0")
        for table in tables:
            migrate_engine.execute(
                "ALTER TABLE %s CONVERT TO CHARACTER SET utf8" % table)
        migrate_engine.execute("SET foreign_key_checks = 1")
        migrate_engine.execute(
            "ALTER DATABASE %s DEFAULT CHARACTER SET utf8" %
            migrate_engine.url.database)
        migrate_engine.execute("ALTER TABLE %s Engine=InnoDB" % table)
