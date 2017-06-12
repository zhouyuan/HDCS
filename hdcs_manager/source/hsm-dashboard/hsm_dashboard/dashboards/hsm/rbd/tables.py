
from horizon import tables


class MonitorRbdAction(tables.LinkAction):
    name = "monitor"
    verbose_name = "Monitor"
    url = "horizon:hsm:rbd:monitor"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class ShowRBDCacheConfigAction(tables.LinkAction):
    name = "show cache config"
    verbose_name = "Show Cache Config"
    url = "horizon:hsm:rbd:show_cache_config_view"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class UpdateCacheConfigAction(tables.LinkAction):
    name = "update cache config"
    verbose_name = "Update Cache Config"
    url = "horizon:hsm:rbd:update"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum):
        return True

class RbdListTable(tables.DataTable):
    """"""

    id = tables.Column("id", verbose_name="ID")
    name = tables.Column("name", verbose_name="Name")
    hs_instance_host = tables.Column("hs_instance_host", verbose_name="Hyperstash Host")
    size = tables.Column("size", verbose_name="Size(MB)")
    objects = tables.Column("objects", verbose_name="Objects")
    order = tables.Column("order", verbose_name="Order")
    format = tables.Column("format", verbose_name="Format")

    class Meta:
        name = "rbds"
        verbose_name = "RBDs"
        # status_columns = ["status"]
        # row_class = UpdateRow
        row_actions = (MonitorRbdAction, ShowRBDCacheConfigAction,
                       UpdateCacheConfigAction)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
