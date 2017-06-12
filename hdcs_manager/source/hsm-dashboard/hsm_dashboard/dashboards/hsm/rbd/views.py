
import json
import logging
import time

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

from horizon import exceptions
from horizon import forms
from horizon import tables

from .forms import UpdateRbdCacheConfigForm
from .tables import RbdListTable
from hsm_dashboard.api import hsm as hsm_api

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    """"""

    table_class = RbdListTable
    template_name = "hsm/rbd/index.html"

    def get_data(self):
        rbds = hsm_api.rbd_get_all(self.request)
        n_rbds = []
        for rbd in rbds:
            _rbd = {
                "id": rbd.id,
                "name": rbd.name,
                "hs_instance_host": rbd.hs_instance['host'],
                "size": int(rbd.size)/1024/1024,
                "objects": rbd.objects,
                "order": rbd.order,
                "format": rbd.format
            }
            n_rbds.append(_rbd)
        return n_rbds

def monitor(request, rbd_id):
    LOG.info("=========================rbd_id: %s" % str(rbd_id))
    rbd = hsm_api.rbd_get(request, rbd_id)
    rbd_name = rbd.name
    return render(request,
                  'hsm/rbd/monitor.html',
                  {"rbd_id": rbd_id,
                   "rbd_name": rbd_name})

def cache_ratio(request, rbd_id):
    result = hsm_api.performance_metric_get_value(request, rbd_id, "cache_ratio")
    cache_ratio = {}
    cache_total_size = 0
    cache_used_size = 0
    cache_dirty_size = 0
    for i in result:
        if i.metric == 'cache_total_size':
            cache_total_size = int(i.value)
        elif i.metric == 'cache_used_size':
            cache_used_size = int(i.value)
            cache_ratio['cache_used_size'] = cache_used_size
        elif i.metric == 'cache_dirty_size':
            cache_dirty_size = int(i.value)
            cache_ratio['cache_dirty_size'] = cache_dirty_size
    cache_ratio['cache_free_size'] = cache_total_size - cache_used_size
    cache_ratio['cache_clean_size'] = cache_used_size - cache_dirty_size
    cache_ratio = json.dumps(cache_ratio)
    return HttpResponse(cache_ratio)

def cache_action(request, rbd_id):
    result = hsm_api.performance_metric_get_value(request, rbd_id, "cache_action")
    cache_action = {}
    cache_action['date'] = []
    cache_action['cache_promote'] = []
    cache_action['cache_flush'] = []
    cache_action['cache_evict'] = []
    for i in result:
        value = i.value
        timestr = i.timestamp
        timearry = time.localtime(timestr)
        timestyle = time.strftime("%H:%M:%S", timearry)
        if timestyle not in cache_action['date']:
            cache_action['date'].append(timestyle)
        if i.metric == "cache_promote":
            cache_action['cache_promote'].append(value)
        elif i.metric == "cache_flush":
            cache_action['cache_flush'].append(value)
        elif i.metric == "cache_evict":
            cache_action['cache_evict'].append(value)
    cache_action = json.dumps(cache_action)
    return HttpResponse(cache_action)

def cache_io_workload(request, rbd_id):
    result = hsm_api.performance_metric_get_value(request, rbd_id, "cache_io_workload")

    cache_read = 0
    cache_read_miss = 0
    cache_write = 0
    cache_write_miss = 0
    cache_bw = 0.0
    cache_latency = 0.0
    for i in result:
        if i.metric == "cache_read":
            cache_read = i.value
        elif i.metric == "cache_read_miss":
            cache_read_miss = i.value
        elif i.metric == "cache_write":
            cache_write = i.value
        elif i.metric == "cache_write_miss":
            cache_write_miss = i.value
        elif i.metric == "cache_bw":
            cache_bw = i.value
        elif i.metric == "cache_latency":
            cache_latency = i.value
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

def get_rbd_basic_info(request, rbd_id):
    result = hsm_api.performance_metric_get_value(request, rbd_id, "rbd_basic_info")
    rbd = result[0]
    rbd_basic_info = {}
    rbd_basic_info['name'] = rbd.name
    rbd_basic_info['size'] = rbd.size
    rbd_basic_info['objects'] = rbd.objects
    rbd_basic_info['order'] = rbd.order
    rbd_basic_info['object_size'] = rbd.object_size
    rbd_basic_info['block_name_prefix'] = rbd.block_name_prefix
    rbd_basic_info['format'] = rbd.format
    rbd_basic_info['features'] = rbd.features
    rbd_basic_info['flags'] = rbd.flags
    rbd_basic_info = json.dumps(rbd_basic_info)
    return HttpResponse(rbd_basic_info)

def show_cache_config_view(request, rbd_id):
    LOG.info("=========================rbd_id: %s" % str(rbd_id))
    rbd = hsm_api.rbd_get(request, rbd_id)
    rbd_name = rbd.name
    return render(request,
                  'hsm/rbd/show_cache_config.html',
                  {"rbd_id": rbd_id,
                   "rbd_name": rbd_name})

def show_cache_config(request, rbd_id):
    cache_config = hsm_api.rbd_cache_config_get_by_rbd_id(request, rbd_id)
    if cache_config.enable_memory_usage_tracker:
        enable_memory_usage_tracker = "true"
    else:
        enable_memory_usage_tracker = "false"

    result = {
        "cache_dir": cache_config.cache_dir,
        "clean_start": cache_config.clean_start,
        "enable_memory_usage_tracker": enable_memory_usage_tracker,
        "object_size": cache_config.object_size,
        "cache_total_size": cache_config.cache_total_size,
        "cache_dirty_ratio_min": cache_config.cache_dirty_ratio_min,
        "cache_ratio_health": cache_config.cache_ratio_health,
        "cache_ratio_max": cache_config.cache_ratio_max,
        "cache_flush_interval": cache_config.cache_flush_interval,
        "cache_evict_interval": cache_config.cache_evict_interval,
        "cache_flush_queue_depth": cache_config.cache_flush_queue_depth,
        "agent_threads_num": cache_config.agent_threads_num,
        "cache_service_threads_num": cache_config.cache_service_threads_num,
        "messenger_port": cache_config.messenger_port,
        "log_to_file": cache_config.log_to_file
    }
    result = json.dumps(result)
    return HttpResponse(result)

class UpdateView(forms.ModalFormView):
    form_class = UpdateRbdCacheConfigForm
    template_name = 'hsm/rbd/update_cache_config.html'
    success_url = reverse_lazy('horizon:hsm:rbd:index')

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                hsm_api.rbd_cache_config_get_by_rbd_id(self.request,
                                                       self.kwargs['rbd_id'])
                rbd_cache_configs = hsm_api.rbd_cache_config_get_all(self.request)
                for config in rbd_cache_configs:
                    if str(config.rbd_id) == self.kwargs['rbd_id']:
                        self._object = config
            except:
                redirect = reverse_lazy('horizon:hsm:rbd:index')
                exceptions.handle(self.request,
                                  'Unable to Edit Rbd Cache Config.',
                                  redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['rbd_cache_config'] = self.get_object()
        print self.get_object()
        return context

    def get_initial(self):
        rbd_cache_config = self.get_object()
        return {
            'id': rbd_cache_config.id,
            'cache_dir': rbd_cache_config.cache_dir,
            'clean_start': rbd_cache_config.clean_start,
            'enable_memory_usage_tracker': rbd_cache_config.enable_memory_usage_tracker,
            'object_size': rbd_cache_config.object_size,
            'cache_total_size': rbd_cache_config.cache_total_size,
            'cache_dirty_ratio_min': rbd_cache_config.cache_dirty_ratio_min,
            'cache_ratio_health': rbd_cache_config.cache_ratio_health,
            'cache_ratio_max': rbd_cache_config.cache_ratio_max,
            'cache_flush_interval': rbd_cache_config.cache_flush_interval,
            'cache_evict_interval': rbd_cache_config.cache_evict_interval,
            'cache_flush_queue_depth': rbd_cache_config.cache_flush_queue_depth,
            'agent_threads_num': rbd_cache_config.agent_threads_num,
            'cache_service_threads_num': rbd_cache_config.cache_service_threads_num,
            'messenger_port': rbd_cache_config.messenger_port,
            'log_to_file': rbd_cache_config.log_to_file
        }

def update_action(request):
    data = json.loads(request.body)
    rbd_cache_config_id = data.pop('id')
    try:
        hsm_api.rbd_cache_config_update(request, rbd_cache_config_id, data)
        status = 'info'
        msg = 'Succeed to update rbd cache config!'
    except:
        status = 'error'
        msg = 'Fail to update rbd cache config!'
    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)
