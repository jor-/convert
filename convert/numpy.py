import numpy as np

import pathlib

import convert.compress as compress

NUMPY_FILE_EXTENSION = '.npy'
NUMPY_COMPRESSED_FILE_EXTENSION = '.npz'
TXT_FILE_EXTENSION = '.txt'

NATIVE_NUMPY_FILE_EXTENSIONS = (NUMPY_FILE_EXTENSION,
                                NUMPY_COMPRESSED_FILE_EXTENSION,
                                TXT_FILE_EXTENSION)

COMPRESSED_NUMPY_FILE_EXTENSIONS = tuple(
    (numpy_file_extension + compression_file_extension
     for numpy_file_extension in (NUMPY_FILE_EXTENSION, TXT_FILE_EXTENSION)
     for compression_file_extension in compress.COMPRESS_FILE_EXTENSIONS))

NUMPY_FILE_EXTENSIONS = NATIVE_NUMPY_FILE_EXTENSIONS + COMPRESSED_NUMPY_FILE_EXTENSIONS


def load(file):
    """
    Loads a NumPy array.

    Parameters
    ----------
    file : str or pathlib.Path
        The file that should be loaded.

    Returns
    -------
    numpy.ndarray
        The array stored in `file`.
    """

    file = pathlib.Path(file)

    if compress.is_compressed_file(file):
        file_extension = pathlib.Path(file.stem).suffix

        # txt file
        if file_extension == TXT_FILE_EXTENSION:
            with compress.read(file) as file_descriptor:
                try:
                    return np.loadtxt(file_descriptor, dtype=np.float)
                except ValueError:
                    file_descriptor.seek(0)
                    return np.loadtxt(file_descriptor, dtype=np.complex)
        # npy file
        elif file_extension == NUMPY_FILE_EXTENSION:
            with compress.read(file) as file_descriptor:
                return np.load(file_descriptor, allow_pickle=False)
        # npz or unknown file
        else:
            raise ValueError(f'The file {file} has an unsupported file extension '
                             f'{file_extension+file.suffix}. '
                             f'Only {NUMPY_FILE_EXTENSIONS} are supported.')

    else:
        file_extension = file.suffix

        # txt file
        if file_extension == TXT_FILE_EXTENSION:
            try:
                return np.loadtxt(file, dtype=np.float)
            except ValueError:
                return np.loadtxt(file, dtype=np.complex)
        # npy file
        elif file_extension == NUMPY_FILE_EXTENSION:
            return np.load(file, allow_pickle=False)
        # npz file
        elif file_extension == NUMPY_COMPRESSED_FILE_EXTENSION:
            with np.load(file, allow_pickle=False) as npz_file:
                if len(npz_file.keys()) != 1:
                    raise ValueError(f'Only files with a single array can be loaded. Instead '
                                     f'{len(npz_file.keys())} arrays are stored in {file}.')
                return npz_file[npz_file.keys()[0]]
        # unknown file
        else:
            raise ValueError(f'The file {file} has an unsupported file extension '
                             f'{file_extension+file.suffix}. '
                             f'Only {NUMPY_FILE_EXTENSIONS} are supported.')


def save(file, array):
    """
    Saves a NumPy array.

    Parameters
    ----------
    file : str or pathlib.Path
        The file where `array` should be saved.
    array : numpy.ndarray
        The array that should be saved.
    """

    file = pathlib.Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)

    if compress.is_compressed_file(file):
        file_extension = pathlib.Path(file.stem).suffix

        # txt file
        if file_extension == TXT_FILE_EXTENSION:
            if array.ndim not in (1, 2):
                raise ValueError(f'Only 1D or 2D array can be saved as {TXT_FILE_EXTENSION} file. '
                                 f'Got {array.ndim}D array instead.')
            with compress.write(file) as file_descriptor:
                np.savetxt(file_descriptor, array)
        # npy file
        elif file_extension == NUMPY_FILE_EXTENSION:
            with compress.write(file) as file_descriptor:
                np.save(file_descriptor, array, allow_pickle=False)
        # npz or unknown file
        else:
            raise ValueError(f'The file {file} has an unsupported file extension '
                             f'{file_extension+file.suffix}. '
                             f'Only {NUMPY_FILE_EXTENSIONS} are supported.')

    else:
        file_extension = file.suffix

        # txt file
        if file_extension == TXT_FILE_EXTENSION:
            if array.ndim not in (1, 2):
                raise ValueError(f'Only 1D or 2D array can be saved as {TXT_FILE_EXTENSION} file. '
                                 f'Got {array.ndim}D array instead.')
            np.savetxt(file, array)
        # npy file
        elif file_extension == NUMPY_FILE_EXTENSION:
            np.save(file, array, allow_pickle=False)
        # npz file
        elif file_extension == NUMPY_COMPRESSED_FILE_EXTENSION:
            np.savez_compressed(file, array)
        # unknown file
        else:
            raise ValueError(f'The file {file} has an unsupported file extension '
                             f'{file_extension+file.suffix}. '
                             f'Only {NUMPY_FILE_EXTENSIONS} are supported.')


def convert(file_from, file_to):
    """
    Converts a file containing a NumPy array into another file.

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
