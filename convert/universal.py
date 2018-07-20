import importlib
import warnings

import convert.compress


class UnsupportedFileExtensionError(ValueError):
    """ The file extension is not supported. """

    def __init__(self, file, supported_file_extensions=None):
        self.file = file
        message = f'The file {file} has an unsupported file extension.'
        if supported_file_extensions is not None:
            self.supported_file_extensions = supported_file_extensions
            message += f' Only {supported_file_extensions} are supported.'
        self.message = message
        super().__init__(message)


class UnsupportedConversionError(ValueError):
    """ The file extension is not supported. """

    def __init__(self, file_from, file_to, supported_file_extension_combinations=None):
        self.file_from = file_from
        self.file_to = file_to
        message = f'The file {file_from} can not be converted to file {file_to}.'
        if supported_file_extension_combinations is not None:
            self.supported_file_extension_combinations = supported_file_extension_combinations
            message += (f' Only {supported_file_extension_combinations} as file extension'
                        f' conversions are supported.')
        self.message = message
        super().__init__(message)


SUPPORTED_MODULES = []
for module_string in ('convert.scipy', 'convert.numpy'):
    try:
        module = importlib.import_module(module_string)
    except ImportError:
        warnings.warn(f'Model {module_string} could not be imported. '
                      f'Thus the related functions are not available.',
                      category=ImportWarning)
    else:
        SUPPORTED_MODULES.append(module)

SUPPORTED_FILE_EXTENSIONS = [file_extension
                             for module in SUPPORTED_MODULES
                             for file_extension in module.FILE_EXTENSIONS]

SUPPORTED_FILE_EXTENSION_COMBINATIONS = [(file_extension_1, file_extension_2)
                                         for module in SUPPORTED_MODULES
                                         for file_extension_1 in module.FILE_EXTENSIONS
                                         for file_extension_2 in module.FILE_EXTENSIONS]


def _module_and_file_extension(file):
    file = str(file)
    for module in SUPPORTED_MODULES:
        for file_extension in module.FILE_EXTENSIONS:
            if file.endswith(file_extension):
                return module, file_extension
    raise UnsupportedFileExtensionError(file, supported_file_extensions=SUPPORTED_FILE_EXTENSIONS)


def _io_function(file, mode, module, file_extension):
    assert mode in ('r', 'w')

    # check if compress file extension
    try:
        compress_file_extension = convert.compress.compress_file_extension(file_extension)
    except UnsupportedFileExtensionError:
        compress_file_extension = None
    else:
        file_extension = file_extension[: len(file_extension) - len(compress_file_extension)]

    # apply binary or text mode
    binary_mode = module.BINARY_MODE_DICT[file_extension]
    if binary_mode:
        mode += 'b'
    else:
        mode += 't'

    # open function
    if compress_file_extension is None:
        def open_function():
            return open(file, mode=mode)
    else:
        def open_function():
            return convert.compress.compress_file_object(file, mode=mode)

    #
    if mode.startswith('r'):
        def io_function():
            with open_function() as file_object:
                return module.load(file_object, file_extension)
    else:
        def io_function(value):
            with open_function() as file_object:
                return module.save(file_object, file_extension, value)

    # return
    return io_function


def _load(file, module, file_extension):
    io_function = _io_function(file, 'r', module, file_extension)
    return io_function()


def load(file):
    """
    Loads a value.

    Parameters
    ----------
    file : str or pathlib.Path
        The file that should be loaded.

    Returns
    -------
    object
        The value stored in `file`.
    """

    module, file_extension = _module_and_file_extension(file)
    return _load(file, module, file_extension)


def _save(file, module, file_extension, value):
    io_function = _io_function(file, 'w', module, file_extension)
    return io_function(value)


def save(file, value):
    """
    Saves a value.

    Parameters
    ----------
    file : str or pathlib.Path
        The file where `value` should be saved.
    value : object
        The value that should be saved.
    """

    module, file_extension = _module_and_file_extension(file)
    return _save(file, module, file_extension, value)


def convert_file(file_from, file_to):
    """
    Converts a file into another file.

    Parameters
    ----------
    file_from : str or pathlib.Path
        The file that should be converted.
    file_to : str or pathlib.Path
        The file to which `file_from` should be converted.
    """

    if file_from != file_to:
        module_from, file_extension_from = _module_and_file_extension(file_from)
        module_to, file_extension_to = _module_and_file_extension(file_to)

        if (file_extension_from, file_extension_to) not in SUPPORTED_FILE_EXTENSION_COMBINATIONS:
            raise UnsupportedConversionError(
                file_from, file_to,
                supported_file_extension_combinations=SUPPORTED_FILE_EXTENSION_COMBINATIONS)

        array = _load(file_from, module_from, file_extension_from)
        _save(file_to, module_to, file_extension_to, array)
    return file_to


def convert_file_extension(file, file_extension):
    """
    Converts a file into another file.

    Parameters
    ----------
    file : str or pathlib.Path
        The file that should be converted.
    file_extension : str
        The new file extension that the converted file should have. The new file has the same
        filename as `file` only its file extension is replaced by `file_extension`.
    """

    file = str(file)
    _, old_file_extension = _module_and_file_extension(file)
    file_to = file[: len(file) - len(old_file_extension)] + file_extension

    convert_file(file, file_to)
    return file_to
