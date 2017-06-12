
import urllib

from hsmclient import base


class HsInstance(base.Resource):
    """"""

    def __repr__(self):
        return "<HsInstance: %s>" % self.id

    def delete(self):
        """"""
        self.manager.delete(self)


class HsInstanceManager(base.ManagerWithFind):
    """"""

    resource_class = HsInstance

    def create(self):
        pass

    def delete(self, hs_instance):
        """"""
        self._delete("/hs_instances/%s" % base.getid(hs_instance))

    def update(self):
        pass

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

        ret = self._list("/hs_instances%s%s" % (detail, query_str),
                         "hs_instances")
        return ret

    def get(self, hs_instance):
        """"""

        return self._get("/hs_instances/%s" % base.getid(hs_instance),
                         "hs_instance")
