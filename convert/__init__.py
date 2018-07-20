from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import sys
if sys.version_info.major < 3 or sys.version_info.minor < 6:
    raise NotImplementedError('This modules needs at least Python 3.6.')
del sys

from convert.universal import load, save, convert_file, convert_file_extension, UnsupportedFileExtensionError
