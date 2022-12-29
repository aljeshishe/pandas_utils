from importlib.metadata import PackageNotFoundError, version

from pandas_utils.utils import *

try:
    __version__ = version("pandas_utils")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version
