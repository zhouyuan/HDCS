
from horizon import tables

from hsm_dashboard import api


class EditUser(tables.LinkAction):
    name = "edit"
    verbose_name = "Change Password"
    url = "horizon:hsm:user:update"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, user):
        return api.keystone.keystone_can_edit_user()

class ListUserTable(tables.DataTable):

    user_id = tables.Column("id", verbose_name="ID")
    name = tables.Column("name", verbose_name="Name")

    class Meta:
        name = "user"
        verbose_name = "Users"
        row_actions = (EditUser,)
        multi_select = False

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]

    def get_object_display(self, datum):
        if hasattr(datum, "name"):
            return datum.id
        else:
            return datum["name"]