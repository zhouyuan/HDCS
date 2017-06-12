
import horizon

from hsm_dashboard.dashboards.hsm import dashboard

class User(horizon.Panel):
    name = "User"
    slug = 'user'

dashboard.VizDash.register(User)
