
from __future__ import absolute_import

from django.conf import settings

from hsmclient.v1 import client as hsm_client


def hsmclient(request):
    key_hsm_pass = getattr(settings, 'KEYSTONE_HSM_SERVICE_PASSWORD')
    key_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    c = hsm_client.Client('hsm',
                          key_hsm_pass,
                          'service',
                          key_url,
                          extensions=[])
    return c

####################
# Server
####################
def server_get_all(request):
    return hsmclient(request).servers.list()

def server_get(request, server_id):
    return hsmclient(request).servers.get(server_id)

def server_activate(request, server_id):
    return hsmclient(request).servers.activate(server_id)

####################
# HsInstance
####################
def hs_instance_get_all(request):
    return hsmclient(request).hs_instances.list()

def hs_instance_get(request, hs_instance_id):
    return hsmclient(request).hs_instances.get(hs_instance_id)

def hs_instance_delete(request, hs_instance_id):
    return hsmclient(request).hs_instances.delete(hs_instance_id)

####################
# RBD
####################
def rbd_get_all(request):
    return hsmclient(request).rbds.list()

def rbd_get(request, rbd_id):
    return hsmclient(request).rbds.get(rbd_id)

####################
# Performance Metric
####################
def performance_metric_get_value(request, rbd_id, type):
    return hsmclient(request).performance_metrics.get_value(rbd_id, type)

def performance_metric_get_os_and_kernel(request, server_id):
    return hsmclient(request).performance_metrics.get_os_and_kernel(server_id)

def performance_metric_get_mem(request, server_id):
    return hsmclient(request).performance_metrics.get_mem(server_id)

def performance_metric_get_cpu(request, server_id):
    return hsmclient(request).performance_metrics.get_cpu(server_id)

def performance_metric_get_hsm_summary(request):
    return hsmclient(request).performance_metrics.get_hsm_summary()

####################
# RBD Cache Config
####################
def rbd_cache_config_get_by_rbd_id(request, rbd_id):
    return hsmclient(request).rbd_cache_configs.get_by_rbd_id(rbd_id)

def rbd_cache_config_update(request, rbd_cache_config_id, values):
    return hsmclient(request).rbd_cache_configs.update(rbd_cache_config_id, **values)

def rbd_cache_config_get_all(request):
    return hsmclient(request).rbd_cache_configs.list()
