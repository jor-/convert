import pathlib

import convert.universal


# *** constants *** #

GZIP_FILE_EXTENSION = '.gz'
BZ2_FILE_EXTENSION = '.bz2'
LZMA_FILE_EXTENSION = '.xz'

FILE_EXTENSIONS = (GZIP_FILE_EXTENSION,
                   BZ2_FILE_EXTENSION,
                   LZMA_FILE_EXTENSION)


# *** load and save functions *** #

def compress_file_object(file, mode='r'):
    file = pathlib.Path(file)
    file_extension = file.suffix
    if file_extension == GZIP_FILE_EXTENSION:
        import gzip
        return gzip.open(file, mode=mode, compresslevel=9)
    elif file_extension == BZ2_FILE_EXTENSION:
        import bz2
        return bz2.open(file, mode=mode, compresslevel=9)
    elif file_extension == LZMA_FILE_EXTENSION:
        import lzma
        if mode.startswith('w'):
            preset = 9
        else:
            preset = None
        return lzma.open(file, mode=mode, preset=preset)
    else:
        assert file_extension not in FILE_EXTENSIONS
        raise convert.universal.UnsupportedFileExtensionError(file, supported_file_extensions=FILE_EXTENSIONS)


def compress_file_extension(file):
    file = str(file)
    for file_extension in FILE_EXTENSIONS:
        if file.endswith(file_extension):
            return file_extension
    raise convert.universal.UnsupportedFileExtensionError(file, supported_file_extensions=FILE_EXTENSIONS)
