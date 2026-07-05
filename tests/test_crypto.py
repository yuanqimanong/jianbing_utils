"""crypto 模块测试（已知向量）。"""

from __future__ import annotations

from jianbing_utils import crypto


def test_hashes_known_vectors() -> None:
    assert crypto.md5("abc") == "900150983cd24fb0d6963f7d28e17f72"
    assert crypto.sha1("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d"
    assert crypto.sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_hash_accepts_bytes() -> None:
    assert crypto.sha256(b"abc") == crypto.sha256("abc")


def test_hmac_sha256_known_vector() -> None:
    got = crypto.hmac_sha256("key", "The quick brown fox jumps over the lazy dog")
    assert got == "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
    assert isinstance(crypto.hmac_sha256("k", "m", hexdigest=False), bytes)


def test_base64_roundtrip() -> None:
    token = crypto.b64encode("hello/world+data", urlsafe=True, padding=False)
    assert "=" not in token
    assert crypto.b64decode(token) == b"hello/world+data"
    # 带 padding 也能解
    assert crypto.b64decode(crypto.b64encode("x", padding=True)) == b"x"
