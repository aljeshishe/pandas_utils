from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pandas_utils")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version
