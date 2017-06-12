
from django import shortcuts
from django.views.decorators import vary

import horizon

from openstack_auth.views import login


def get_user_home(user):
    return horizon.get_dashboard('hsm').get_absolute_url()

@vary.vary_on_cookie
def splash(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(get_user_home(request.user))
    form = login(request)
    request.session.clear()
    request.session.set_test_cookie()
    return shortcuts.render(request, 'splash.html', {'form': form})
