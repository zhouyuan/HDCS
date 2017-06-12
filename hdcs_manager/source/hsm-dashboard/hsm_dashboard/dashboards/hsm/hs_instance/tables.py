
from horizon import tables

from hsm_dashboard.api import hsm as hsm_api


class DelHsInstanceAction(tables.DeleteAction):
    data_type_singular = ("hs instance")
    data_type_plural = ("hs instances")
    classes = ("btn-del-hs-instance", )

    def allowed(self, request, datum=None):
        return True

    def delete(self, request, obj_id):
        return hsm_api.hs_instance_delete(request, obj_id)

class MonitorHsInstanceAction(tables.LinkAction):
    name = "monitor"
    verbose_name = "Monitor"
    url = "horizon:hsm:hs_instance:monitor"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True


class HsInstanceListTable(tables.DataTable):
    """"""

    id = tables.Column("id", verbose_name="ID")
    host = tables.Column("host", verbose_name="Host")
    type = tables.Column("type", verbose_name="Type")

    class Meta:
        name = "hs_instances"
        verbose_name = "Hyperstash Instances"
        # status_columns = ["status"]
        # row_class = UpdateRow
        table_actions = (DelHsInstanceAction,)
        row_actions = (MonitorHsInstanceAction,)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
