"""crypto —— 哈希 / HMAC / 编码（自研薄封装 stdlib hashlib/hmac/base64）。

统一入参（str 自动按 utf-8 编码），返回 hexdigest；base64 默认 urlsafe、可去 padding。
注：md5/sha1 仅用于内容指纹/去重等**非安全**场景。
"""

from __future__ import annotations

import base64
import hashlib
import hmac

__all__ = [
    "b64decode",
    "b64encode",
    "hmac_sha256",
    "md5",
    "sha1",
    "sha256",
]


def _to_bytes(data: str | bytes) -> bytes:
    return data.encode("utf-8") if isinstance(data, str) else data


def md5(data: str | bytes) -> str:
    return hashlib.md5(_to_bytes(data)).hexdigest()


def sha1(data: str | bytes) -> str:
    return hashlib.sha1(_to_bytes(data)).hexdigest()


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(_to_bytes(data)).hexdigest()


def hmac_sha256(key: str | bytes, msg: str | bytes, *, hexdigest: bool = True) -> str | bytes:
    """HMAC-SHA256。hexdigest=True 返回十六进制串，否则返回原始 bytes。"""
    mac = hmac.new(_to_bytes(key), _to_bytes(msg), hashlib.sha256)
    return mac.hexdigest() if hexdigest else mac.digest()


def b64encode(data: str | bytes, *, urlsafe: bool = True, padding: bool = False) -> str:
    raw = _to_bytes(data)
    encoded = base64.urlsafe_b64encode(raw) if urlsafe else base64.b64encode(raw)
    text = encoded.decode("ascii")
    return text if padding else text.rstrip("=")


def b64decode(s: str, *, urlsafe: bool = True) -> bytes:
    padded = s + "=" * (-len(s) % 4)  # 补回 padding，兼容去 padding 的输入
    return base64.urlsafe_b64decode(padded) if urlsafe else base64.b64decode(padded)
