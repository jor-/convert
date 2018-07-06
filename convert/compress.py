import pathlib

GZIP_FILE_EXTENSION = '.gz'
BZ2_FILE_EXTENSION = '.bz2'
LZMA_FILE_EXTENSION = '.xz'

COMPRESS_FILE_EXTENSIONS = (GZIP_FILE_EXTENSION,
                            BZ2_FILE_EXTENSION,
                            LZMA_FILE_EXTENSION)


def compressed_file(file, mode='r'):
    file = pathlib.Path(file)
    file_extension = file.suffix
    if file_extension == GZIP_FILE_EXTENSION:
        import gzip
        return gzip.GzipFile(file, mode=mode, compresslevel=9)
    elif file_extension == BZ2_FILE_EXTENSION:
        import bz2
        return bz2.BZ2File(file, mode=mode, compresslevel=9)
    elif file_extension == LZMA_FILE_EXTENSION:
        import lzma
        if mode.startswith('w'):
            preset = 6
        else:
            preset = None
        return lzma.LZMAFile(file, mode=mode, preset=preset)
    else:
        assert file_extension not in COMPRESS_FILE_EXTENSIONS
        raise ValueError(f'File {file} has an unsupported file extension. '
                         f'Only {COMPRESS_FILE_EXTENSIONS} are supported.')


def is_compressed_file(file):
    file = pathlib.Path(file)
    return file.suffix in COMPRESS_FILE_EXTENSIONS


def _read_write(file, mode):
    if is_compressed_file(file):
        return compressed_file(file, mode=mode)
    else:
        raise ValueError(f'File {file} has an unsupported file extension. '
                         f'Only {COMPRESS_FILE_EXTENSIONS} are supported.')


def read(file):
    return _read_write(file, mode='r')


def write(file):
    return _read_write(file, mode='w')
