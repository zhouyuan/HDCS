
import horizon

from hsm_dashboard.dashboards.hsm import dashboard

class Rbd(horizon.Panel):
    name = "RBD"
    slug = 'rbd'

dashboard.VizDash.register(Rbd)
