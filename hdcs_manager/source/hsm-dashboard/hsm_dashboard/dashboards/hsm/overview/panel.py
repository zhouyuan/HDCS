
import horizon

from hsm_dashboard.dashboards.hsm import dashboard

class Overview(horizon.Panel):
    name = "Overview"
    slug = 'overview'

dashboard.VizDash.register(Overview)
