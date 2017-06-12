
from __future__ import print_function

import sys
import time

from hsmclient import exceptions
from hsmclient import utils


def _poll_for_status(poll_fn, obj_id, action, final_ok_states,
                     poll_period=5, show_progress=True):
    """Blocks while an action occurs. Periodically shows progress."""
    def print_progress(progress):
        if show_progress:
            msg = ('\rInstance %(action)s... %(progress)s%% complete'
                   % dict(action=action, progress=progress))
        else:
            msg = '\rInstance %(action)s...' % dict(action=action)

        sys.stdout.write(msg)
        sys.stdout.flush()

    print()
    while True:
        obj = poll_fn(obj_id)
        status = obj.status.lower()
        progress = getattr(obj, 'progress', None) or 0
        if status in final_ok_states:
            print_progress(100)
            print("\nFinished")
            break
        elif status == "error":
            print("\nError %(action)s instance" % {'action': action})
            break
        else:
            print_progress(progress)
            time.sleep(poll_period)


####################
# Server
####################
@utils.service_type('hsm')
def do_server_list(cs, args):
    """Lists all servers."""

    servers = cs.servers.list()
    columns = ["ID", "Host", "IP", "Status"]
    utils.print_list(servers, columns)


@utils.arg('server',
           metavar='<server>',
           help='Name or ID of a server.')
@utils.service_type('hsm')
def do_server_show(cs, args):
    """Shows details info of a server."""

    server = utils.find_resource(cs.servers, args.server)
    if isinstance(server, dict):
        utils.print_dict(server)
    else:
        utils.print_dict(server._info)


@utils.arg('server',
           metavar='<server>',
           help='Name or ID of a server.')
@utils.service_type('hsm')
def do_server_activate(cs, args):
    """Activates a server as a hyperstash instance."""

    try:
        cs.servers.activate(args.server)
        print("Succeed to activate a server as a hyperstash instance.")
    except Exception:
        raise exceptions.CommandError("Fail to activate a server.")


####################
# HsInstance
####################
@utils.service_type('hsm')
def do_hs_instance_list(cs, args):
    """Lists all hyperstash instances."""

    hs_instances = cs.hs_instances.list()
    columns = ["ID", "Host", "Type", "Server ID"]
    utils.print_list(hs_instances, columns)


@utils.arg('hs_instance',
           metavar='<hs_instance>',
           help='Name or ID of a hyperstash instance.')
@utils.service_type('hsm')
def do_hs_instance_show(cs, args):
    """Shows details info of a hyperstash instance."""

    hs_instance = utils.find_resource(cs.hs_instances, args.hs_instance)
    if isinstance(hs_instance, dict):
        utils.print_dict(hs_instance)
    else:
        utils.print_dict(hs_instance._info)


####################
# RBD
####################
@utils.service_type('hsm')
def do_rbd_list(cs, args):
    """Lists all rbds."""

    rbds = cs.rbds.list()
    columns = ["ID", "Name", "Size", "Objects", "Order",
               "Object Size", "Block Name Prefix", "Format",
               "Features", "Flags", "Hs Instance ID"]
    utils.print_list(rbds, columns)


@utils.arg('rbd',
           metavar='<rbd>',
           help='Name or ID of a rbd.')
@utils.service_type('hsm')
def do_rbd_show(cs, args):
    """Shows details info of a rbd."""

    rbd = utils.find_resource(cs.rbds, args.rbd)
    if isinstance(rbd, dict):
        utils.print_dict(rbd)
    else:
        utils.print_dict(rbd._info)


@utils.service_type('hsm')
def do_rbd_refresh(cs, args):
    """Refresh the rbd info."""
    cs.rbds.refresh()


####################
# Performance Metric
####################
@utils.arg('--rbd-id',
           metavar='<rbd-id>',
           help='Id of rbd.')
@utils.arg('--type',
           metavar='<type>',
           help='Metric type(cache_ratio, cache_action, '
                'cache_io_workload and rbd_basic_info).')
@utils.service_type('hsm')
def do_performance_metric_get_value(cs, args):
    """Gets the value of hyperstash performance metric by rbd id and type."""
    if not args.rbd_id:
        raise exceptions.CommandError("you need specify a rbd_id")
    if not args.type:
        raise exceptions.CommandError("you need specify a type")
    performance_metrics = \
        cs.performance_metrics.get_value(args.rbd_id, args.type)
    columns = ["Metric", "Value", "RBD Name", "TimeStamp"]
    if args.type == "rbd_basic_info":
        columns = ["ID", "Name", "Size", "Objects", "Order",
                   "Object Size", "Block Name Prefix", "Format",
                   "Features", "Flags"]
    utils.print_list(performance_metrics, columns)


@utils.arg('--server-id',
           metavar='<server-id>',
           help='Id of server.')
@utils.service_type('hsm')
def do_performance_metric_get_os_and_kernel(cs, args):
    """Gets os and kernel information."""
    if not args.server_id:
        raise exceptions.CommandError("you need specify a server_id")
    performance_metric = \
        cs.performance_metrics.get_os_and_kernel(args.server_id)
    if isinstance(performance_metric, dict):
        utils.print_dict(performance_metric)
    else:
        utils.print_dict(performance_metric._info)


@utils.arg('--server-id',
           metavar='<server-id>',
           help='Id of server.')
@utils.service_type('hsm')
def do_performance_metric_get_mem(cs, args):
    """Gets memory information."""
    if not args.server_id:
        raise exceptions.CommandError("you need specify a server_id")
    performance_metric = cs.performance_metrics.get_mem(args.server_id)
    if isinstance(performance_metric, dict):
        utils.print_dict(performance_metric)
    else:
        utils.print_dict(performance_metric._info)


@utils.arg('--server-id',
           metavar='<server-id>',
           help='Id of server.')
@utils.service_type('hsm')
def do_performance_metric_get_cpu(cs, args):
    """Gets cpu information."""
    if not args.server_id:
        raise exceptions.CommandError("you need specify a server_id")
    performance_metric = cs.performance_metrics.get_cpu(args.server_id)
    if isinstance(performance_metric, dict):
        utils.print_dict(performance_metric)
    else:
        utils.print_dict(performance_metric._info)


@utils.service_type('hsm')
def do_performance_metric_get_hsm_summary(cs, args):
    """Gets hsm summary."""
    performance_metric = cs.performance_metrics.get_hsm_summary()
    if isinstance(performance_metric, dict):
        utils.print_dict(performance_metric)
    else:
        utils.print_dict(performance_metric._info)


####################
# RBD Cache Config
####################
@utils.service_type('hsm')
def do_rbd_cache_config_list(cs, args):
    """Lists all rbd cache configs."""

    rbd_cache_configs = cs.rbd_cache_configs.list()
    columns = ["ID", "Cache Dir", "Clean Start", "Enable Memory Usage Tracker",
               "Object Size", "Cache Total Size", "Cache Dirty Ratio Min",
               "Cache Ratio Health", "Cache Ratio Max", "Cache Flush Interval",
               "Cache Evict Interval", "Cache Flush Queue Depth",
               "Agent Threads Num", "Cache Service Threads Num",
               "Messenger Port"]
    utils.print_list(rbd_cache_configs, columns)


@utils.arg('rbd_cache_config',
           metavar='<rbd_cache_config>',
           help='Name or ID of a rbd cache config.')
@utils.service_type('hsm')
def do_rbd_cache_config_show(cs, args):
    """Shows details info of a rbd cache config."""

    rbd_cache_config = utils.find_resource(cs.rbd_cache_configs,
                                           args.rbd_cache_config)
    if isinstance(rbd_cache_config, dict):
        utils.print_dict(rbd_cache_config)
    else:
        utils.print_dict(rbd_cache_config._info)


@utils.arg('--rbd-id',
           metavar='<rbd-id>',
           help='ID of a rbd.')
@utils.service_type('hsm')
def do_rbd_cache_config_show_by_rbd_id(cs, args):
    """Shows details info of a rbd cache config by rbd id."""

    rbd_cache_config = cs.rbd_cache_configs.get_by_rbd_id(args.rbd_id)
    if isinstance(rbd_cache_config, dict):
        utils.print_dict(rbd_cache_config)
    else:
        utils.print_dict(rbd_cache_config._info)


@utils.arg('rbd_cache_config',
           metavar='<rbd_cache_config>',
           help='ID of a rbd cache config.')
@utils.arg('--cache-dir',
           metavar='<cache-dir>',
           help='The directory to put cache.')
@utils.arg('--clean-start',
           dest='clean_start',
           action='store_true',
           default=False,
           help='Reload metadata from rocksdb then start.')
@utils.arg('--enable-memory-usage-tracker',
           dest='enable_memory_usage_tracker',
           action='store_true',
           default=False,
           help='Enable memory usage tracker.')
@utils.arg('--object-size',
           metavar='<object-size>',
           help='The size of object.')
@utils.arg('--cache-total-size',
           metavar='<cache-total-size>',
           help='The total size of cache.')
@utils.arg('--cache-dirty-ratio-min',
           metavar='<cache-dirty-ratio-min>',
           help='The min ratio of dirty cache.')
@utils.arg('--cache-ratio-health',
           metavar='<cache-ratio-health>',
           help='The health ratio of cache.')
@utils.arg('--cache-ratio-max',
           metavar='<cache-ratio-max>',
           help='The max ratio of cache.')
@utils.arg('--cache-flush-interval',
           metavar='<cache-flush-interval>',
           help='The flush interval of cache.')
@utils.arg('--cache-evict-interval',
           metavar='<cache-evict-interval>',
           help='The evict interval of cache.')
@utils.arg('--cache-flush-queue-depth',
           metavar='<cache-flush-queue-depth>',
           help='The flush queue depth of cache.')
@utils.arg('--agent-threads-num',
           metavar='<agent-threads-num>',
           help='The number of agent threads.')
@utils.arg('--cache-service-threads-num',
           metavar='<cache-service-threads-num>',
           help='The number of cache service threads.')
@utils.arg('--messenger-port',
           metavar='<messenger-port>',
           help='The port of messenger.')
@utils.arg('--log-to-file',
           metavar='<log-to-file>',
           help='The file name to log.')
@utils.service_type('hsm')
def do_rbd_cache_config_update(cs, args):
    """Updates a rbd cache config by id."""

    rbd_cache_config_resource = [
        'cache_dir', 'clean_start', 'enable_memory_usage_tracker',
        'object_size', 'cache_total_size', 'cache_dirty_ratio_min',
        'cache_ratio_health', 'cache_ratio_max', 'cache_flush_interval',
        'cache_evict_interval', 'cache_flush_queue_depth', 'agent_threads_num',
        'cache_service_threads_num', 'messenger_port', 'log_to_file'
    ]

    config_kwargs = {}
    for resource in rbd_cache_config_resource:
        val = getattr(args, resource, None)
        if resource == "clean_start" and val:
            val = 1
        elif resource == "clean_start" and val:
            val = 0
        if resource == "enable_memory_usage_tracker" and val:
            val = True
        elif resource == "enable_memory_usage_tracker" and not val:
            val = False
        if val:
            config_kwargs[resource] = val
        elif resource in ["enable_memory_usage_tracker", "clean_start"]:
            config_kwargs[resource] = val
    try:
        cs.rbd_cache_configs.update(args.rbd_cache_config, **config_kwargs)
        print("Succeed to update a rbd cache config.")
    except Exception:
        raise exceptions.CommandError("Fail to update a rbd cache config.")


# TODO tag for those not completed commands
# It will be removed later
def _is_developing(method, message):
    print('\033[1;31;40m')
    print('*' * 50)
    print('*Method:\t%s' % method)
    print('*Description:\t%s' % message)
    print('*Status:\t%s' % "Not Completed Now!")
    print('*' * 50)
    print('\033[0m')
