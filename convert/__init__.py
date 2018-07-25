from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from convert.universal import load, save, convert_file, convert_file_extension, UnsupportedFileExtensionError, UnsupportedConversionError
