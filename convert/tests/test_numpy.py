import pathlib
import tempfile

import numpy as np
import pytest

import convert.numpy
import convert.compress


# *** random array *** #

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'
DATA_TYPE_COMPLEX = 'complex'
DATA_TYPES = (DATA_TYPE_INT, DATA_TYPE_FLOAT, DATA_TYPE_COMPLEX)


def random_array(shape, data_type):
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
    return a


# *** tests *** #

test_numpy_save_load_setups = [
    (shape, data_type, file_extension)
    for shape in ((10,), (2, 3))
    for data_type in DATA_TYPES
    for file_extension in convert.numpy.NUMPY_FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, file_extension', test_numpy_save_load_setups)
def test_numpy_save_load(shape, data_type, file_extension):
    # generate test array
    a = random_array(shape, data_type)

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


test_numpy_convert_setups = [
    (shape, data_type, file_extension, other_file_extension)
    for shape in ((10,), (2, 3))
    for data_type in DATA_TYPES
    for file_extension in convert.numpy.NUMPY_FILE_EXTENSIONS
    for other_file_extension in convert.numpy.NUMPY_FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, file_extension, other_file_extension', test_numpy_convert_setups)
def test_numpy_convert(shape, data_type, file_extension, other_file_extension):
    # generate test array
    a = random_array(shape, data_type)

    # test save load and convert
    FILENAME = pathlib.Path('test_file')
    with tempfile.TemporaryDirectory() as tmp_dir:
        # save base file
        base_file = pathlib.Path(tmp_dir) / FILENAME
        file = base_file.with_suffix(file_extension)
        convert.numpy.save(file, a)
        # convert file
        other_file = base_file.with_suffix(other_file_extension)
        convert.numpy.convert(file, other_file)
        b = convert.numpy.load(other_file)
        # test
        assert file.exists()
        assert other_file.exists()
    assert np.allclose(a, b)
