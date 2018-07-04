import numpy as np

import pathlib

NUMPY_UNCOMPRESSED_FILE_EXTENSION = '.npy'
NUMPY_COMPRESSED_FILE_EXTENSION = '.npz'
TXT_FILE_EXTENSION = '.txt'


def load(file):
    file = pathlib.Path(file)
    # txt file
    if file.suffix == TXT_FILE_EXTENSION:
        try:
            return np.loadtxt(file, dtype=np.float)
        except ValueError:
            return np.loadtxt(file, dtype=np.complex)
    # npy file
    elif file.suffix == NUMPY_UNCOMPRESSED_FILE_EXTENSION:
        return np.load(file, allow_pickle=False)
    # npz file
    elif file.suffix == NUMPY_COMPRESSED_FILE_EXTENSION:
        with np.load(file, allow_pickle=False) as npz_file:
            if len(npz_file.keys()) != 1:
                raise ValueError(f'Only files with a single array can be loaded.'
                                 ' Instead {len(npz_file.keys())} arrays are stored in {file}.')
            return npz_file[npz_file.keys()[0]]
    # unknown file
    else:
        raise ValueError(f'The file {file} has an unknown file extension.'
                         ' Only {NUMPY_UNCOMPRESSED_FILE_EXTENSION},'
                         ' {NUMPY_COMPRESSED_FILE_EXTENSION} and'
                         ' {TXT_FILE_EXTENSION} are supported.')


def save(file, array):
    file = pathlib.Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    # txt file
    if file.suffix == TXT_FILE_EXTENSION:
        if array.ndim not in (1, 2):
            raise ValueError(f'Only 1D or 2D array can be saved as {TXT_FILE_EXTENSION} file.'
                             ' Got {array.ndim}D array instead.')
        return np.savetxt(file, array)
    # npy file
    elif file.suffix == NUMPY_UNCOMPRESSED_FILE_EXTENSION:
        return np.save(file, array)
    # npz file
    elif file.suffix == NUMPY_COMPRESSED_FILE_EXTENSION:
        return np.savez_compressed(file, array)
    # unknown file
    else:
        raise ValueError(f'The file {file} has an unknown file extension.'
                         ' Only {NUMPY_UNCOMPRESSED_FILE_EXTENSION},'
                         ' {NUMPY_COMPRESSED_FILE_EXTENSION} and'
                         ' {TXT_FILE_EXTENSION} are supported.')


def convert(file_from, file_to):
    if file_from != file_to:
        array = load(file_from)
        save(file_to, array)
