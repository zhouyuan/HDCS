
from hsm.api.openstack import wsgi
from hsm.api.views import versions as views_versions

VERSIONS = {
    "v1.0": {
        "id": "v1.0",
        "status": "CURRENT",
        "updated": "2012-01-04T11:33:21Z",
        "links": [
            {
                "rel": "describedby",
                "type": "application/pdf",
                "href": "http://jorgew.github.com/block-storage-api/"
                        "content/os-block-storage-1.0.pdf",
            },
            {
                "rel": "describedby",
                "type": "application/vnd.sun.wadl+xml",
                "href": "http://docs.rackspacecloud.com/"
                        "servers/api/v1.1/application.wadl",
            },
        ],
        "media-types": [
            {
                "base": "application/xml",
                "type": "application/vnd.openstack.storage+xml;version=1",
            },
            {
                "base": "application/json",
                "type": "application/vnd.openstack.storage+json;version=1",
            }
        ],
    }

}


class Versions(wsgi.Resource):

    def __init__(self):
        super(Versions, self).__init__(None)

    def index(self, req):
        """Return all versions."""
        builder = views_versions.get_view_builder(req)
        return builder.build_versions(VERSIONS)

    @wsgi.response(300)
    def multi(self, req):
        """Return multiple choices."""
        builder = views_versions.get_view_builder(req)
        return builder.build_choices(VERSIONS, req)

    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        args = {}
        if request_environment['PATH_INFO'] == '/':
            args['action'] = 'index'
        else:
            args['action'] = 'multi'

        return args

class HardwareVersionV1(object):
    def show(self, req):
        builder = views_versions.get_view_builder(req)
        return builder.build_version(VERSIONS['v1.0'])

def create_resource():
    return wsgi.Resource(HardwareVersionV1())
