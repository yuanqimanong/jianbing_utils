"""text 模块测试。"""

from __future__ import annotations

import pytest

from jianbing_utils import text


def test_blank() -> None:
    assert text.is_blank(None)
    assert text.is_blank("   ")
    assert not text.is_blank(" x ")
    assert text.default_if_blank("  ", "d") == "d"
    assert text.default_if_blank("v", "d") == "v"


def test_collapse_ws() -> None:
    assert text.collapse_ws("  a\t b\n c ") == "a b c"


def test_truncate() -> None:
    assert text.truncate("hello", 10) == "hello"
    assert text.truncate("hello world", 8) == "hello w…"
    assert text.truncate("hello", 1) == "h"  # length<=suffix


def test_mask() -> None:
    assert text.mask("13800001234", keep_start=3, keep_end=4) == "138****1234"
    assert text.mask("ab", keep_start=3, keep_end=3) == "**"


@pytest.mark.parametrize("value", [-1, 1.5, "1", True])
@pytest.mark.parametrize("s", ["", "secret"])
def test_text_lengths_reject_invalid_values_before_returning(s: str, value) -> None:
    error = ValueError if value == -1 else TypeError
    with pytest.raises(error, match="length"):
        text.truncate(s, value)
    with pytest.raises(error, match="keep_start"):
        text.mask(s, keep_start=value)
    with pytest.raises(error, match="keep_end"):
        text.mask(s, keep_end=value)


def test_zero_text_lengths_keep_existing_behavior() -> None:
    assert text.truncate("secret", 0) == ""
    assert text.mask("secret", keep_start=0, keep_end=0) == "******"
    assert text.mask("") == ""


def test_case_conversions() -> None:
    assert text.snake_case("helloWorld foo-bar") == "hello_world_foo_bar"
    assert text.kebab_case("helloWorld foo-bar") == "hello-world-foo-bar"
    assert text.camel_case("hello_world foo") == "helloWorldFoo"
    assert text.camel_case("hello_world", upper_first=True) == "HelloWorld"


def test_slugify() -> None:
    assert text.slugify("Héllo, World!") == "hello-world"
    assert text.slugify("  a  b  ") == "a-b"
