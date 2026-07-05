"""text 模块测试。"""

from __future__ import annotations

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


def test_case_conversions() -> None:
    assert text.snake_case("helloWorld foo-bar") == "hello_world_foo_bar"
    assert text.kebab_case("helloWorld foo-bar") == "hello-world-foo-bar"
    assert text.camel_case("hello_world foo") == "helloWorldFoo"
    assert text.camel_case("hello_world", upper_first=True) == "HelloWorld"


def test_slugify() -> None:
    assert text.slugify("Héllo, World!") == "hello-world"
    assert text.slugify("  a  b  ") == "a-b"
