
import urllib

from hsmclient import base


class Server(base.Resource):
    """"""

    def __repr__(self):
        return "<Server: %s>" % self.id


class ServerManager(base.ManagerWithFind):
    """"""

    resource_class = Server

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

        ret = self._list("/servers%s%s" % (detail, query_str), "servers")
        return ret

    def get(self, server):
        """"""

        return self._get("/servers/%s" % base.getid(server), "server")

    def _action(self, action, server, info=None, **kwargs):
        """
        Perform a server "action" -- activate
        """

        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/servers/%s/action' % base.getid(server)
        return self.api.client.post(url, body=body)

    def activate(self, server):
        """"""

        return self._action('activate', server, None)
