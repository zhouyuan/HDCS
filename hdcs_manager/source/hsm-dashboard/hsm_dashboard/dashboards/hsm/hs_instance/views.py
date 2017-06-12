
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from horizon import tables

from hsm_dashboard.api import hsm as hsm_api
from .tables import HsInstanceListTable

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    """"""

    table_class = HsInstanceListTable
    template_name = 'hsm/hs_instance/index.html'

    def get_data(self):
        hs_instances = hsm_api.hs_instance_get_all(self.request)
        n_hs_instances = []
        for hs_instance in hs_instances:
            _hs_instance = {
                "id": hs_instance.id,
                "host": hs_instance.host,
                "type": hs_instance.type
            }
            n_hs_instances.append(_hs_instance)
        return n_hs_instances


def monitor(request, hs_instance_id):
    LOG.info("=========================hs_instance_id: %s" % str(hs_instance_id))
    hs_instance = hsm_api.hs_instance_get(request, hs_instance_id)
    host = hs_instance.host
    return render(request,
                  'hsm/hs_instance/monitor.html',
                  {"hs_instance_id": hs_instance_id,
                   "host": host})

def cache_io_workload(request, hs_instance_id):
    rbds = hsm_api.rbd_get_all(request)
    rbd_id_list = []
    for rbd in rbds:
        if str(rbd.hs_instance_id) == str(hs_instance_id):
            rbd_id_list.append(rbd.id)

    cache_read = 0
    cache_read_miss = 0
    cache_write = 0
    cache_write_miss = 0
    cache_bw = 0.0
    cache_latency = 0.0
    for rbd_id in rbd_id_list:
        io_workload = hsm_api.performance_metric_get_value(request, rbd_id,
                                                           "cache_io_workload")
        for i in io_workload:
            if i.metric == "cache_read":
                cache_read = cache_read + int(i.value)
            elif i.metric == "cache_read_miss":
                cache_read_miss = cache_read_miss + int(i.value)
            elif i.metric == "cache_write":
                cache_write = cache_write + int(i.value)
            elif i.metric == "cache_write_miss":
                cache_write_miss = cache_write_miss + int(i.value)
            elif i.metric == "cache_bw":
                cache_bw = cache_bw + float(i.value)
            elif i.metric == "cache_latency":
                cache_latency = cache_latency + float(i.value)
    cache_io_workload = {
        "cache_read": cache_read,
        "cache_read_miss": cache_read_miss,
        "cache_write": cache_write,
        "cache_write_miss": cache_write_miss,
        "cache_bw": cache_bw,
        "cache_latency": cache_latency
    }
    cache_io_workload = json.dumps(cache_io_workload)
    return HttpResponse(cache_io_workload)

def cache_ratio(request, hs_instance_id):
    rbds = hsm_api.rbd_get_all(request)
    rbd_id_list = []
    for rbd in rbds:
        if str(rbd.hs_instance_id) == str(hs_instance_id):
            rbd_id_list.append(rbd.id)

    cache_total_size = 0
    cache_used_size = 0
    cache_dirty_size = 0
    for rbd_id in rbd_id_list:
        ratio = hsm_api.performance_metric_get_value(request, rbd_id,
                                                     "cache_ratio")
        for i in ratio:
            if i.metric == "cache_total_size":
                cache_total_size = cache_total_size + int(i.value)
            elif i.metric == "cache_used_size":
                cache_used_size = cache_used_size + int(i.value)
            elif i.metric == "cache_dirty_size":
                cache_dirty_size = cache_dirty_size + int(i.value)
    cache_free_size = cache_total_size - cache_used_size
    cache_clean_size = cache_used_size - cache_dirty_size

    cache_ratio = {
        "cache_used_size": cache_used_size,
        "cache_dirty_size": cache_dirty_size,
        "cache_free_size": cache_free_size,
        "cache_clean_size": cache_clean_size
    }
    cache_ratio = json.dumps(cache_ratio)
    return HttpResponse(cache_ratio)
