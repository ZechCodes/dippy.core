import pkg_resources as _pkg_resources
import sys as _sys


__version__ = _pkg_resources.get_distribution("dippy.core").version
__python_version__, *_ = _sys.version.split()
__aiohttp_version__ = _pkg_resources.get_distribution("aiohttp").version
