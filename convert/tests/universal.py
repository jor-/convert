import pathlib
import tempfile

import convert.universal


def test_save_load(value, file_extension):
    FILENAME = pathlib.Path('test_file')
    with tempfile.TemporaryDirectory() as tmp_dir:
        # save file
        base_file = pathlib.Path(tmp_dir) / FILENAME
        file = base_file.with_suffix(file_extension)
        convert.universal.save(file, value)
        assert file.exists()
        # load file
        value_loaded = convert.universal.load(file)
        assert file.exists()
    return value_loaded


def test_convert_file(value, file_extension, other_file_extension):
    FILENAME_FROM = pathlib.Path('test_file')
    FILENAME_TO = pathlib.Path('test_file_converted')
    with tempfile.TemporaryDirectory() as tmp_dir:
        # save base file
        base_file_from = pathlib.Path(tmp_dir) / FILENAME_FROM
        file = base_file_from.with_suffix(file_extension)
        convert.universal.save(file, value)
        assert file.exists()
        # convert file
        base_file_to = pathlib.Path(tmp_dir) / FILENAME_TO
        other_file = base_file_to.with_suffix(other_file_extension)
        convert.universal.convert_file(file, other_file)
        assert file.exists()
        assert other_file.exists()
        # load converted file
        value_loaded = convert.universal.load(other_file)
    return value_loaded


def test_convert_file_extension(value, file_extension, other_file_extension):
    FILENAME = pathlib.Path('test_file')
    with tempfile.TemporaryDirectory() as tmp_dir:
        # save base file
        base_file = pathlib.Path(tmp_dir) / FILENAME
        file = base_file.with_suffix(file_extension)
        convert.universal.save(file, value)
        assert file.exists()
        # convert file
        other_file = convert.universal.convert_file_extension(file, other_file_extension)
        assert file.exists()
        other_file = pathlib.Path(other_file)
        assert other_file.exists()
        # load converted file
        value_loaded = convert.universal.load(other_file)
    return value_loaded
