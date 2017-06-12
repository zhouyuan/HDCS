
import urllib

from hsmclient import base


class Rbd(base.Resource):
    """"""

    def __repr__(self):
        return "<Rbd: %s>" % self.id


class RbdManager(base.ManagerWithFind):
    """"""

    resource_class = Rbd

    def create(self):
        pass

    def delete(self):
        pass

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

        ret = self._list("/rbds%s%s" % (detail, query_str), "rbds")
        return ret

    def get(self, rbd):
        """"""

        return self._get("/rbds/%s" % base.getid(rbd), "rbd")

    def refresh(self):
        """"""

        return self.api.client.post("/rbds/refresh")
