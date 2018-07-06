import pathlib
import tempfile

import numpy as np
import pytest

import convert.numpy


# *** save and load *** #

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'
DATA_TYPE_COMPLEX = 'complex'
DATA_TYPES = (DATA_TYPE_INT, DATA_TYPE_FLOAT, DATA_TYPE_COMPLEX)

FILE_EXTENSIONS = (convert.numpy.NUMPY_FILE_EXTENSION,
                   convert.numpy.NUMPY_COMPRESSED_FILE_EXTENSION,
                   convert.numpy.TXT_FILE_EXTENSION)

test_numpy_setups = [
    (shape, data_type, file_extension)
    for shape in ((10,), (2, 3))
    for data_type in DATA_TYPES
    for file_extension in FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, file_extension', test_numpy_setups)
def test_numpy(shape, data_type, file_extension):
    # generate test array
    n = np.prod(shape)
    if data_type == DATA_TYPE_INT:
        a = np.random.randint(-n, n, n)
    elif data_type == DATA_TYPE_FLOAT:
        a = np.random.rand(n)
    elif data_type == DATA_TYPE_COMPLEX:
        a = np.random.rand(n) + np.random.rand(n) * 1j
    else:
        raise ValueError('Data type {} unknown.'.format(data_type))
    a = a.reshape(*shape)

    # test save load and convert
    FILENAME = pathlib.Path('test_file')
    with tempfile.TemporaryDirectory() as tmp_dir:
        base_file = pathlib.Path(tmp_dir) / FILENAME
        file = base_file.with_suffix(file_extension)

        # test save and load
        convert.numpy.save(file, a)
        assert file.exists()
        b = convert.numpy.load(file)
        assert file.exists()
        assert np.allclose(a, b)

        # test convert
        for other_file_extension in FILE_EXTENSIONS:
            other_file = base_file.with_suffix(other_file_extension)
            convert.numpy.convert(file, other_file)
            assert file.exists()
            assert other_file.exists()
            b = convert.numpy.load(other_file)
            assert np.allclose(a, b)
