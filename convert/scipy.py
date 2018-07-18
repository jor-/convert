import scipy.sparse
import scipy.io

import convert.compress


# *** constants *** #

MATRIX_FORMATS = ('csc', 'csr', 'bsr', 'dia', 'coo')
NPZ_FILE_EXTENSIONS = tuple(f'.{matrix_format}.npz' for matrix_format in MATRIX_FORMATS)
MATRIX_MARKET_FILE_EXTENSION = '.mtx'
HARWELL_BOEING_FILE_EXTENSION = '.rua'

NATIVE_FILE_EXTENSIONS = (MATRIX_MARKET_FILE_EXTENSION,
                          HARWELL_BOEING_FILE_EXTENSION) + NPZ_FILE_EXTENSIONS

BINARY_MODE_DICT = {npz_file_extension: True for npz_file_extension in NPZ_FILE_EXTENSIONS}
BINARY_MODE_DICT[MATRIX_MARKET_FILE_EXTENSION] = True
BINARY_MODE_DICT[HARWELL_BOEING_FILE_EXTENSION] = False

COMPRESSED_FILE_EXTENSIONS = tuple(
    (native_file_extension + compression_file_extension
     for native_file_extension in (MATRIX_MARKET_FILE_EXTENSION, HARWELL_BOEING_FILE_EXTENSION)
     for compression_file_extension in convert.compress.FILE_EXTENSIONS))

FILE_EXTENSIONS = NATIVE_FILE_EXTENSIONS + COMPRESSED_FILE_EXTENSIONS


# *** load and save functions *** #

def load(file_object, file_extension):
    # npz file
    if file_extension in NPZ_FILE_EXTENSIONS:
        return scipy.sparse.load_npz(file_object)
    # matrix market file
    elif file_extension == MATRIX_MARKET_FILE_EXTENSION:
        return scipy.io.mmread(file_object)
    # harwell boing file
    elif file_extension == HARWELL_BOEING_FILE_EXTENSION:
        return scipy.io.hb_read(file_object)
    # unknown file
    else:
        assert False


def save(file_object, file_extension, value):
    # npz file
    if file_extension in NPZ_FILE_EXTENSIONS:
        scipy.sparse.save_npz(file_object, value)
    # matrix market file
    elif file_extension == MATRIX_MARKET_FILE_EXTENSION:
        scipy.io.mmwrite(file_object, value)
    # harwell boing file
    elif file_extension == HARWELL_BOEING_FILE_EXTENSION:
        value = value.tocsc(copy=False)  # format which are not csc is not supported in scipy.io.hb_write for SciPy version <= 1.1
        scipy.io.hb_write(file_object, value)
    # unknown file
    else:
        assert False
