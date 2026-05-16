import pytest

from exceptions import EmptyFileError, UnsupportedFileError
from core.parser import validate_extension, validate_text


def test_empty_file():
    with pytest.raises(EmptyFileError):
        validate_text("")


def test_valid_txt():
    validate_extension("test.txt")


def test_invalid_extension():
    with pytest.raises(UnsupportedFileError):
        validate_extension("test.pdf")