import pytest

from apirouter.utils import removeprefix


@pytest.mark.parametrize(
    "string,prefix,expected",
    [
        ("", "/", ""),
        ("/path", "", "/path"),
        ("/path", "/", "path"),
        ("//string", "//", "string"),
    ],
)
def test_removeprefix(string: str, prefix: str, expected: str):
    assert removeprefix(string, prefix=prefix) == expected
