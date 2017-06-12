
import json
import logging

from horizon import exceptions
from horizon import forms
from horizon import tables

from django.core.urlresolvers import reverse, reverse_lazy
from django import http
from django.http import HttpResponse
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from .forms import UpdateUserForm
from .tables import ListUserTable
from hsm_dashboard import api

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    """"""

    table_class = ListUserTable
    template_name = "hsm/user/index.html"

    def get_data(self):
        tenants = api.keystone.tenant_list(self.request)
        tenants_dict = SortedDict([t.name, t] for t in tenants)
        admin_tenant = tenants_dict.get("admin", None)

        users_list = api.keystone.user_list(self.request, admin_tenant.id)

        if self.request.user.username != "admin":
            users_list = [user for user in users_list if user.id == self.request.user.id]

        result = []
        for user in users_list:
            user = {
                "id": user.id,
                "name": user.name,
            }
            result.append(user)
        LOG.info("Users list is %s" % str(result))

        return result

class UpdateView(forms.ModalFormView):
    form_class = UpdateUserForm
    template_name = 'hsm/user/update.html'
    success_url = reverse_lazy('horizon:hsm:user:index')

    @method_decorator(sensitive_post_parameters('password',
                                                'confirm_password'))
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = api.keystone.user_get(self.request,
                                                     self.kwargs['user_id'],
                                                     admin=True)
            except:
                redirect = reverse("horizon:hsm:user:index")
                exceptions.handle(self.request,
                                  'Unable to update user.',
                                  redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def get_initial(self):
        user = self.get_object()
        return {'id': user.id,
                'name': user.name,
                'tenant_id': getattr(user, 'tenantId', None)}

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception:
            handled = None
            exceptions.handle(self.request)

        if handled:
            if "HTTP_X_HORIZON_ADD_TO_FIELD" in self.request.META:
                field_id = self.request.META["HTTP_X_HORIZON_ADD_TO_FIELD"]
                data = [self.get_object_id(handled),
                        self.get_object_display(handled)]
                response = http.HttpResponse(json.dumps(data))
                response["X-Horizon-Add-To-Field"] = field_id
            elif isinstance(handled, http.HttpResponse):
                return handled
            else:
                success_url = self.get_success_url()
                response = http.HttpResponseRedirect(success_url)
                # AJAX should be handled, but it's an expedient solution
                # until the blueprint for AJAX handling is architected
                # and implemented.
                response['X-Horizon-Location'] = success_url
            return response
        else:
            # If handled didn't return, we can assume something went
            # wrong, and we should send back the form as-is.
            return self.form_invalid(form)

def update_pwd(request):
    data = json.loads(request.body)

    api.keystone.user_update_password(request, data["id"], data["pwd"])
    resp = dict(message="Update User", status="OK", data="")
    resp = json.dumps(resp)
    return HttpResponse(resp)
