
__all__ = ['__version__']

import pbr.version

version_info = pbr.version.VersionInfo('python-hsmclient')

try:
    __version__ = version_info.version_string()
except AttributeError:
    __version__ = None
