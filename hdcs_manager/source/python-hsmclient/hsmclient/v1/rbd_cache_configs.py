
import urllib

from hsmclient import base


class RbdCacheConfig(base.Resource):
    """"""

    def __repr__(self):
        return "<RbdCacheConfig: %s>" % self.id


class RbdCacheConfigManager(base.ManagerWithFind):
    """"""

    resource_class = RbdCacheConfig

    def create(self):
        pass

    def delete(self):
        pass

    def update(self, rbd_cache_config, **kwargs):
        """"""

        if not kwargs:
            return

        body = {'rbd_cache_config': kwargs}

        return self._update('/rbd_cache_configs/%s' %
                            base.getid(rbd_cache_config), body)

    def list(self, detailed=False, search_opts=None):
        """"""

        if search_opts is None:
            search_opts = {}

        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_str = "?%s" % urllib.urlencode(qparams) if qparams else ""

        detail = ""
        if detailed:
            detail = "/detail"

        ret = self._list("/rbd_cache_configs%s%s" % (detail, query_str),
                         "rbd_cache_configs")
        return ret

    def get(self, rbd_cache_config):
        """"""

        return self._get("/rbd_cache_configs/%s" %
                         base.getid(rbd_cache_config), "rbd_cache_config")

    def get_by_rbd_id(self, rbd_id):
        """"""

        qparams = {}
        if rbd_id:
            qparams['rbd_id'] = rbd_id

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/rbd_cache_configs/get_by_rbd_id%s" %
                         query_string, "rbd_cache_config")
