
from webob import exc

from hsm.api.openstack import wsgi
from hsm import conductor
from hsm.openstack.common import log as logging
from hsm import scheduler

LOG = logging.getLogger(__name__)


class PerformanceMetricController(wsgi.Controller):
    """"""

    def __init__(self):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        super(PerformanceMetricController, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def index(self):
        pass

    def show(self):
        pass

    def get_value(self, req):
        """Get value of specified performance metric."""

        context = req.environ['hsm.context']
        rbd_id = req.GET['rbd_id']
        type = req.GET['type']

        if not rbd_id:
            raise exc.HTTPBadRequest("Please supply id of rbd.")

        if type not in ["cache_ratio", "cache_action",
                        "cache_io_workload", "rbd_basic_info"]:
            raise exc.HTTPBadRequest("Please supply the valid type.")

        rbd = self.conductor_api.rbd_get(context, rbd_id)
        rbd_name = rbd['name']

        result = []
        if type in ["cache_ratio", "cache_action", "cache_io_workload"]:
            values = self.conductor_api.\
                performance_metric_get_by_rbd_name(context, rbd_name)
            if type == "cache_ratio":
                result = self._generate_cache_ratio(values)
            elif type == "cache_action":
                result = self._generate_cache_action(values)
            elif type == "cache_io_workload":
                result = self._generate_cache_io_workload(values)
        elif type == "rbd_basic_info":
            result.append(rbd)
        return {'performance_metrics': result}

    def _generate_cache_ratio(self, values):
        result = []
        new_values = values[-12:]
        if len(new_values) < 12:
            return result

        valid_metric = ['cache_total_size', 'cache_used_size', 'cache_dirty_size']
        for new_value in new_values:
            metric = new_value['metric']
            if metric in valid_metric:
                value = {"metric": metric,
                         "value": new_value['value'],
                         "rbd_name": new_value['rbd_name'],
                         "timestamp": new_value['timestamp']}
                result.append(value)
        return result

    def _generate_cache_action(self, values):
        result = []
        new_values = values[-132:]
        if len(new_values) < 24:
            return result

        for v_metric in ["cache_promote", "cache_flush", "cache_evict"]:
            min_value = None
            for new_value in new_values:
                metric = new_value['metric']
                if metric == v_metric and not min_value:
                    min_value = new_value
                elif metric == v_metric and min_value:
                    value = (int(new_value['value']) - int(min_value['value'])) / 20
                    result.append({"metric": v_metric,
                                   "value": value,
                                   "rbd_name": new_value['rbd_name'],
                                   "timestamp": new_value['timestamp']})
                    min_value = new_value
        return result

    def _generate_cache_io_workload(self, values):
        result = []
        new_values = values[-24:]
        if len(new_values) < 24:
            return result

        for v_metric in ["cache_read", "cache_read_miss", "cache_write",
                         "cache_write_miss", "cache_bw", "cache_latency"]:
            min_value = None
            for new_value in new_values:
                metric = new_value['metric']
                if metric == v_metric and v_metric == "cache_latency":
                    min_value = new_value
                    continue
                if metric == v_metric and not min_value:
                    min_value = new_value
                elif metric == v_metric and min_value:
                    value = (int(new_value['value']) - int(min_value['value'])) / 20
                    result.append({"metric": v_metric,
                                   "value": value,
                                   "rbd_name": new_value['rbd_name'],
                                   "timestamp": new_value['timestamp']})
                    min_value = new_value
            if v_metric == "cache_latency":
                result.append({"metric": v_metric,
                               "value": min_value['value'],
                               "rbd_name": min_value['rbd_name'],
                               "timestamp": min_value['timestamp']})
        return result

    def get_os_and_kernel(self, req):
        """Get the information of operation system and version of kernel."""

        context = req.environ['hsm.context']

        server_id = req.GET['server_id']

        os_and_kernel = self.scheduler_api.os_and_kernel_get(context, server_id)

        return {'performance_metric': os_and_kernel}

    def get_mem(self, req):
        """Get memory info."""

        context = req.environ['hsm.context']

        server_id = req.GET['server_id']

        mem = self.scheduler_api.mem_get(context, server_id)

        return {'performance_metric': mem}

    def get_cpu(self, req):
        """Get cpu info."""

        context = req.environ['hsm.context']

        server_id = req.GET['server_id']

        cpu = self.scheduler_api.cpu_get(context, server_id)

        return {'performance_metric': cpu}

    def get_hsm_summary(self, req):
        """Get hsm summary."""

        context = req.environ['hsm.context']

        hsm_summary = self.scheduler_api.hsm_summary_get(context)

        return {'performance_metric': hsm_summary}


def create_resource():
    return wsgi.Resource(PerformanceMetricController())
