
import horizon


class Dashboard(horizon.PanelGroup):
    slug = "dashboard"
    name = "Dashboard"
    panels = ("overview",)


class ServerManage(horizon.PanelGroup):
    slug = "server_manage"
    name = "Server Manage"
    panels = ("server",)


class HyperstashManage(horizon.PanelGroup):
    slug = "hyperstash_manage"
    name = "Hyperstash Manage"
    panels = ("hs_instance", "rbd")


class GlobalManage(horizon.PanelGroup):
    slug = "global_manage"
    name = "Global Manage"
    panels = ("user",)


class VizDash(horizon.Dashboard):
    name = "HSM"
    slug = "hsm"
    panels = (Dashboard, ServerManage, HyperstashManage, GlobalManage)
    default_panel = "overview"
    roles = ("admin",)

horizon.register(VizDash)
