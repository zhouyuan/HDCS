
from horizon import tables

from hsm_dashboard.api import hsm as hsm_api

class UpdateRow(tables.Row):
    ajax = False

    def get_data(self, request, volume_id):
        server = hsm_api.server_get(request, volume_id)
        return server

class ActivateAction(tables.LinkAction):
    name = "activate"
    verbose_name = "Activate"
    classes = ('btn-primary',)
    url = "horizon:hsm:server:index"


class MonitorServerAction(tables.LinkAction):
    name = "monitor"
    verbose_name = "Monitor"
    url = "horizon:hsm:server:monitor"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True


class ServerListTable(tables.DataTable):
    """"""

    id = tables.Column("id", verbose_name="ID")
    host = tables.Column("host", verbose_name="Host")
    ip = tables.Column("ip", verbose_name="IP")
    status = tables.Column("status", verbose_name="Status")

    class Meta:
        name = "servers"
        verbose_name = "Servers"
        # status_columns = ["status"]
        row_class = UpdateRow
        table_actions = (ActivateAction,)
        row_actions = (MonitorServerAction,)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
