import numpy as np
import pytest

import convert.universal
import convert.tests.universal
from convert.numpy import FILE_EXTENSIONS


# *** random array *** #

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'
DATA_TYPE_COMPLEX = 'complex'
DATA_TYPES = (DATA_TYPE_INT, DATA_TYPE_FLOAT, DATA_TYPE_COMPLEX)


def random_array(shape, data_type=DATA_TYPE_FLOAT):
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

test_save_load_setups = [
    (shape, data_type, file_extension)
    for shape in ((10,), (2, 3))
    for data_type in DATA_TYPES
    for file_extension in FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, file_extension', test_save_load_setups)
def test_save_load(shape, data_type, file_extension):
    value = random_array(shape, data_type=data_type)
    other_value = convert.tests.universal.test_save_load(value, file_extension)
    assert np.allclose(value, other_value)


test_convert_setups = [
    (shape, data_type, file_extension, other_file_extension)
    for shape in ((10,), (2, 3))
    for data_type in DATA_TYPES
    for file_extension in FILE_EXTENSIONS
    for other_file_extension in FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, file_extension, other_file_extension', test_convert_setups)
def test_convert_file(shape, data_type, file_extension, other_file_extension):
    value = random_array(shape, data_type=data_type)
    other_value = convert.tests.universal.test_convert_file(value, file_extension, other_file_extension)
    assert np.allclose(value, other_value)


@pytest.mark.parametrize('shape, data_type, file_extension, other_file_extension', test_convert_setups)
def test_convert_file_extension(shape, data_type, file_extension, other_file_extension):
    value = random_array(shape, data_type=data_type)
    other_value = convert.tests.universal.test_convert_file_extension(value, file_extension, other_file_extension)
    assert np.allclose(value, other_value)
