import importlib
import warnings

import convert.compress


class UnsupportedFileExtension(ValueError):
    """ The file extension is not supported. """

    def __init__(self, file, supported_file_extensions=None):
        self.file = file
        message = f'The file {file} has an unsupported file extension.'
        if supported_file_extensions is not None:
            self.supported_file_extensions = supported_file_extensions
            message += f' Only {supported_file_extensions} are supported.'
        self.message = message
        super().__init__(message)


SUPPORTED_MODULES = []
for module_string in ('convert.numpy',):
    try:
        module = importlib.import_module(module_string)
    except ImportError:
        warnings.warn(f'Model {module_string} could not be imported. '
                      f'Thus the related functions are not available.',
                      category=ImportWarning)
    else:
        SUPPORTED_MODULES.append(module)


def _module_and_file_extension(file):
    file = str(file)
    for module in SUPPORTED_MODULES:
        for file_extension in module.FILE_EXTENSIONS:
            if file.endswith(file_extension):
                return module, file_extension

    supported_file_extensions = tuple(file_extension for module in SUPPORTED_MODULES for file_extension in module.FILE_EXTENSIONS)
    raise UnsupportedFileExtension(file, supported_file_extensions=supported_file_extensions)


def _prepare_load_save(file, mode):
    assert mode in ('r', 'w')

    # get model and file extension
    module, file_extension = _module_and_file_extension(file)

    # check if compress file extension
    try:
        compress_file_extension = convert.compress.compress_file_extension(file_extension)
    except UnsupportedFileExtension:
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

    # return
    return open_function, module, file_extension


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

    open_function, module, file_extension = _prepare_load_save(file, 'r')

    with open_function() as file_object:
        return module.load(file_object, file_extension)


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

    open_function, module, file_extension = _prepare_load_save(file, 'w')

    with open_function() as file_object:
        return module.save(file_object, file_extension, value)


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
        array = load(file_from)
        save(file_to, array)
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
