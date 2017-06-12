
from pbr import version as pbr_version

HSM_VENDOR = "Intel"
HSM_PRODUCT = "Intel"
HSM_PACKAGE = None

loaded = False
version_info = pbr_version.VersionInfo('hsm')
version_string = version_info.version_string
