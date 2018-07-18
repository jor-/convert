import numpy as np
import scipy.sparse as sp
import pytest

import convert.universal
import convert.tests.universal
from convert.scipy import FILE_EXTENSIONS, MATRIX_FORMATS


# *** random array *** #

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'
DATA_TYPE_COMPLEX = 'complex'
# DATA_TYPES = (DATA_TYPE_INT, DATA_TYPE_FLOAT, DATA_TYPE_COMPLEX)
# dtype which are not float is only supported in sp.random since SciPy 1.2
DATA_TYPES = (DATA_TYPE_FLOAT,)

MATRIX_TYPE_GENERAL = 'general'
MATRIX_TYPE_SYMMETRIC = 'symmetric'
MATRIX_TYPE_HERMITIAN = 'hermitian'
MATRIX_TYPES = (MATRIX_TYPE_GENERAL, MATRIX_TYPE_SYMMETRIC, MATRIX_TYPE_HERMITIAN)


def random_sparse_matrix(shape, data_type=DATA_TYPE_FLOAT, matrix_type=MATRIX_TYPE_GENERAL, matrix_format='csc'):
    # get data type
    if data_type == DATA_TYPE_INT:
        dtype = np.int
    elif data_type == DATA_TYPE_FLOAT:
        dtype = np.float
    elif data_type == DATA_TYPE_COMPLEX:
        dtype = np.complex
    else:
        raise ValueError('Data type {} unknown.'.format(data_type))
    # generate random matrix
    assert len(shape) == 2
    A = sp.random(*shape, density=0.5, dtype=dtype, format='coo')
    # apply matrix type
    if matrix_type == MATRIX_TYPE_HERMITIAN:
        assert shape[0] == shape[1]
        A = A + A.conj()
    elif matrix_type == MATRIX_TYPE_SYMMETRIC:
        assert shape[0] == shape[1]
        A = A + A.T
    else:
        assert matrix_type == MATRIX_TYPE_GENERAL
    # return
    return A.asformat(matrix_format, copy=False)


def is_close(A, B):
    if A.shape != B.shape:
        return False
    else:
        diff = A - B
        diff = diff.tocsc(copy=False)
        return np.allclose(diff.data, 0)


# *** tests *** #

test_save_load_setups = [
    (shape, data_type, MATRIX_TYPE_GENERAL, matrix_format, file_extension)
    for shape in ((10, 1), (2, 3))
    for data_type in DATA_TYPES
    for matrix_format in MATRIX_FORMATS
    for file_extension in FILE_EXTENSIONS
] + [
    (shape, data_type, matrix_type, matrix_format, file_extension)
    for shape in ((4, 4),)
    for data_type in DATA_TYPES
    for matrix_type in MATRIX_TYPES
    for matrix_format in MATRIX_FORMATS
    for file_extension in FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, matrix_type, matrix_format, file_extension', test_save_load_setups)
def test_save_load(shape, data_type, matrix_type, matrix_format, file_extension):
    value = random_sparse_matrix(shape, data_type=data_type, matrix_type=matrix_type, matrix_format=matrix_format)
    other_value = convert.tests.universal.test_save_load(value, file_extension)
    assert is_close(value, other_value)


test_convert_setups = [
    (shape, data_type, MATRIX_TYPE_GENERAL, matrix_format, file_extension, other_file_extension)
    for shape in ((10, 1), (2, 3))
    for data_type in DATA_TYPES
    for matrix_format in MATRIX_FORMATS
    for file_extension in FILE_EXTENSIONS
    for other_file_extension in FILE_EXTENSIONS
] + [
    (shape, data_type, matrix_type, matrix_format, file_extension, other_file_extension)
    for shape in ((4, 4),)
    for data_type in DATA_TYPES
    for matrix_type in MATRIX_TYPES
    for matrix_format in MATRIX_FORMATS
    for file_extension in FILE_EXTENSIONS
    for other_file_extension in FILE_EXTENSIONS
]


@pytest.mark.parametrize('shape, data_type, matrix_type, matrix_format, file_extension, other_file_extension', test_convert_setups)
def test_convert_file(shape, data_type, matrix_type, matrix_format, file_extension, other_file_extension):
    value = random_sparse_matrix(shape, data_type=data_type, matrix_type=matrix_type, matrix_format=matrix_format)
    other_value = convert.tests.universal.test_convert_file(value, file_extension, other_file_extension)
    assert is_close(value, other_value)


@pytest.mark.parametrize('shape, data_type, matrix_type, matrix_format, file_extension, other_file_extension', test_convert_setups)
def test_convert_file_extension(shape, data_type, matrix_type, matrix_format, file_extension, other_file_extension):
    value = random_sparse_matrix(shape, data_type=data_type, matrix_type=matrix_type, matrix_format=matrix_format)
    other_value = convert.tests.universal.test_convert_file_extension(value, file_extension, other_file_extension)
    assert is_close(value, other_value)
