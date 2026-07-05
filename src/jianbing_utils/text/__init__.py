"""text —— 字符串工具（自研，纯函数/静态方法）。

小而全的常用字符串处理：空白判定/清理、截断、脱敏、命名风格转换、slug 生成。
"""

from __future__ import annotations

import re
import unicodedata

__all__ = [
    "camel_case",
    "collapse_ws",
    "default_if_blank",
    "is_blank",
    "kebab_case",
    "mask",
    "slugify",
    "snake_case",
    "truncate",
]

_WS = re.compile(r"\s+")
_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_WORD_SPLIT = re.compile(r"[^0-9A-Za-z]+")
_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def is_blank(s: str | None) -> bool:
    """None 或去空白后为空 → True。"""
    return s is None or s.strip() == ""


def default_if_blank(s: str | None, default: str) -> str:
    """空白则返回默认值。"""
    return default if is_blank(s) else s  # type: ignore[return-value]


def collapse_ws(s: str) -> str:
    """连续空白折叠为单个空格并去首尾。"""
    return _WS.sub(" ", s).strip()


def truncate(s: str, length: int, *, suffix: str = "…") -> str:
    """超长截断并加省略后缀（length 含后缀长度）。"""
    if len(s) <= length:
        return s
    if length <= len(suffix):
        return s[:length]
    return s[: length - len(suffix)] + suffix


def mask(s: str, *, keep_start: int = 0, keep_end: int = 0, mask_char: str = "*") -> str:
    """脱敏：保留首尾若干字符，中间用掩码字符替换。"""
    n = len(s)
    if n <= keep_start + keep_end:
        return mask_char * n
    tail = s[-keep_end:] if keep_end else ""
    return s[:keep_start] + mask_char * (n - keep_start - keep_end) + tail


def _words(s: str) -> list[str]:
    parts = _WORD_SPLIT.sub(" ", _CAMEL_BOUNDARY.sub(" ", s)).split()
    return [p for p in parts if p]


def snake_case(s: str) -> str:
    return "_".join(w.lower() for w in _words(s))


def kebab_case(s: str) -> str:
    return "-".join(w.lower() for w in _words(s))


def camel_case(s: str, *, upper_first: bool = False) -> str:
    words = _words(s)
    if not words:
        return ""
    head = words[0].capitalize() if upper_first else words[0].lower()
    return head + "".join(w.capitalize() for w in words[1:])


def slugify(s: str) -> str:
    """转 URL 友好 slug（ASCII 化 + 小写 + 连字符）。"""
    normalized = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return _SLUG_STRIP.sub("-", normalized.lower()).strip("-")
