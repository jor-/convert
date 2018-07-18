import numpy as np

import convert.compress


# *** constants *** #

NUMPY_FILE_EXTENSION = '.npy'
NUMPY_COMPRESSED_FILE_EXTENSION = '.npz'
TXT_FILE_EXTENSION = '.txt'

NATIVE_FILE_EXTENSIONS = (NUMPY_FILE_EXTENSION,
                          NUMPY_COMPRESSED_FILE_EXTENSION,
                          TXT_FILE_EXTENSION)

BINARY_MODE_DICT = {native_file_extension: True for native_file_extension in NATIVE_FILE_EXTENSIONS}

COMPRESSED_FILE_EXTENSIONS = tuple(
    (native_file_extension + compression_file_extension
     for native_file_extension in (NUMPY_FILE_EXTENSION, TXT_FILE_EXTENSION)
     for compression_file_extension in convert.compress.FILE_EXTENSIONS))

FILE_EXTENSIONS = NATIVE_FILE_EXTENSIONS + COMPRESSED_FILE_EXTENSIONS


# *** load and save functions *** #

def load(file_object, file_extension):
    # txt file
    if file_extension == TXT_FILE_EXTENSION:
        try:
            return np.loadtxt(file_object, dtype=np.float)
        except ValueError:
            file_object.seek(0)
            return np.loadtxt(file_object, dtype=np.complex)
    # npy file
    elif file_extension == NUMPY_FILE_EXTENSION:
        return np.load(file_object, allow_pickle=False)
    # npz file
    elif file_extension == NUMPY_COMPRESSED_FILE_EXTENSION:
        with np.load(file_object, allow_pickle=False) as npz_file:
            if len(npz_file.keys()) != 1:
                raise ValueError(f'Only files with a single array can be loaded. Instead '
                                 f'{len(npz_file.keys())} arrays are stored in the file.')
            return npz_file[npz_file.keys()[0]]
    # unknown file
    else:
        assert False


def save(file_object, file_extension, value):
    array = np.asanyarray(value)
    # txt file
    if file_extension == TXT_FILE_EXTENSION:
        if array.ndim not in (1, 2):
            raise ValueError(f'Only 1D or 2D array can be saved as {TXT_FILE_EXTENSION} file. '
                             f'Got {array.ndim}D array instead.')
        np.savetxt(file_object, array)
    # npy file
    elif file_extension == NUMPY_FILE_EXTENSION:
        np.save(file_object, array, allow_pickle=False)
    # npz file
    elif file_extension == NUMPY_COMPRESSED_FILE_EXTENSION:
        np.savez_compressed(file_object, array)
    # unknown file
    else:
        assert False
