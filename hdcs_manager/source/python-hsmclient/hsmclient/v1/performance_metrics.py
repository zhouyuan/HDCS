
import urllib

from hsmclient import base


class PerformanceMetric(base.Resource):
    """"""

    def __repr__(self):
        return "<PerformanceMetric: %s>" % self.id


class PerformanceMetricManager(base.ManagerWithFind):
    """"""

    resource_class = PerformanceMetric

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def list(self, detailed=False, search_opts=None):
        pass

    def get(self):
        pass

    def get_value(self, rbd_id, type):
        """"""

        qparams = {}
        if rbd_id:
            qparams['rbd_id'] = rbd_id
        if type:
            qparams['type'] = type

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._list("/performance_metrics/get_value%s" %
                          query_string, "performance_metrics")

    def get_os_and_kernel(self, server_id):
        """"""

        qparams = {}
        if server_id:
            qparams['server_id'] = server_id

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/performance_metrics/get_os_and_kernel%s" %
                         query_string, "performance_metric")

    def get_mem(self, server_id):
        """"""

        qparams = {}
        if server_id:
            qparams['server_id'] = server_id

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/performance_metrics/get_mem%s" %
                         query_string, "performance_metric")

    def get_cpu(self, server_id):
        """"""

        qparams = {}
        if server_id:
            qparams['server_id'] = server_id

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/performance_metrics/get_cpu%s" %
                         query_string, "performance_metric")

    def get_hsm_summary(self):
        """"""

        return self._get("/performance_metrics/get_hsm_summary",
                         "performance_metric")
