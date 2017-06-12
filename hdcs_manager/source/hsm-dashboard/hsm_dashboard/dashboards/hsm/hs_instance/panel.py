
import horizon

from hsm_dashboard.dashboards.hsm import dashboard

class HsInstance(horizon.Panel):
    name = "Hyperstash"
    slug = 'hs_instance'

dashboard.VizDash.register(HsInstance)
