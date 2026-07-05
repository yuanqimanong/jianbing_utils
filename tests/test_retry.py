"""retry 模块测试（确定性：无抖动 + 注入 sleep）。"""

from __future__ import annotations

import asyncio

import pytest

from jianbing_utils import retry


def test_backoff_delay_deterministic() -> None:
    assert retry.backoff_delay(1, base=0.5, factor=2.0) == 0.5
    assert retry.backoff_delay(2, base=0.5, factor=2.0) == 1.0
    assert retry.backoff_delay(3, base=0.5, factor=2.0) == 2.0
    assert retry.backoff_delay(10, base=0.5, factor=2.0, cap=5.0) == 5.0  # 封顶


def test_backoff_delay_jitter_within_bounds() -> None:
    for _ in range(50):
        d = retry.backoff_delay(3, base=1.0, factor=2.0, cap=100.0, jitter=True)
        assert 0.0 <= d <= 4.0


def test_backoff_delays_sequence() -> None:
    assert retry.backoff_delays(3, base=1.0, factor=2.0) == [1.0, 2.0, 4.0]


def test_retry_async_succeeds_after_failures() -> None:
    async def main() -> None:
        calls = {"n": 0}
        slept: list[float] = []

        async def sleeper(d: float) -> None:
            slept.append(d)

        async def flaky() -> str:
            calls["n"] += 1
            if calls["n"] < 3:
                raise ValueError("transient")
            return "ok"

        result = await retry.retry_async(flaky, attempts=5, jitter=False, sleep=sleeper)
        assert result == "ok"
        assert calls["n"] == 3
        assert len(slept) == 2  # 两次失败 → 两次退避

    asyncio.run(main())


def test_retry_async_exhausts_and_raises() -> None:
    async def main() -> None:
        async def always() -> str:
            raise ValueError("boom")

        with pytest.raises(ValueError):
            await retry.retry_async(always, attempts=2, jitter=False, sleep=lambda _d: asyncio.sleep(0))

    asyncio.run(main())
