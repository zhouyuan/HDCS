
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from horizon import tables

from .tables import ServerListTable
from hsm_dashboard.api import hsm as hsm_api

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    """"""

    table_class = ServerListTable
    template_name = "hsm/server/index.html"

    def get_data(self):
        servers = hsm_api.server_get_all(self.request)
        n_servers = []
        for server in servers:
            _server = {
                "id": server.id,
                "host": server.host,
                "ip": server.ip,
                "status": server.status
            }
            n_servers.append(_server)
        return n_servers

def activate(request):
    body = json.loads(request.body)
    server_id_list = body['server_id_list']
    print "========================"
    print server_id_list

    try:
        for server_id in server_id_list:
            hsm_api.server_activate(request, server_id)
        ret = {"error_code": "", "info": "Succeed to activate servers!"}
    except Exception, e:
        print e.message
        ret = {"error_code": "-1", "error_msg": e.message}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def monitor(request, server_id):
    LOG.info("=========================server_id: %s" % str(server_id))
    server = hsm_api.server_get(request, server_id)
    host = server.host
    return render(request,
                  'hsm/server/monitor.html',
                  {"server_id": server_id,
                   "host": host})

def get_os_and_kernel(request, server_id):
    result = hsm_api.performance_metric_get_os_and_kernel(request, server_id)
    os_and_kernel_info = {
        "distributor_id": result.distributor_id,
        "release": result.release,
        "codename": result.codename,
        "kernel": result.kernel
    }
    os_and_kernel_info = json.dumps(os_and_kernel_info)
    return HttpResponse(os_and_kernel_info)

def get_mem(request, server_id):
    result = hsm_api.performance_metric_get_mem(request, server_id)
    mem_info = {
        "total": str(int(result.total) / 1024 / 1024) + " MB",
        "available": str(int(result.available) / 1024 / 1024) + " MB",
        "used": str(int(result.used) / 1024 / 1024) + " MB",
        "free": str(int(result.free) / 1024 / 1024) + " MB",
        "buffers": str(int(result.buffers) / 1024 / 1024) + " MB",
        "cached": str(int(result.cached) / 1024 / 1024) + " MB"
    }
    mem_info = json.dumps(mem_info)
    return HttpResponse(mem_info)

def get_cpu(request, server_id):
    result = hsm_api.performance_metric_get_cpu(request, server_id)
    cpu_info = {
        "user": result.user,
        "nice": result.nice,
        "system": result.system,
        "idle": result.idle,
        "iowait": result.iowait
    }
    cpu_info = json.dumps(cpu_info)
    return HttpResponse(cpu_info)
