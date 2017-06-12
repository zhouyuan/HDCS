
import horizon

from hsm_dashboard.dashboards.hsm import dashboard

class Server(horizon.Panel):
    name = "Server"
    slug = 'server'

dashboard.VizDash.register(Server)
