"""retry —— 重试/退避（自研，指数退避 + 可选满抖动）。

``backoff_delay`` 为纯函数（可测；无抖动时确定性）；``retry_async`` 为通用异步重试包装，
sleep 可注入（默认 asyncio.sleep，也可传 anyio.sleep）便于测试与不同事件循环。
"""

from __future__ import annotations

import random
from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

__all__ = ["backoff_delay", "backoff_delays", "retry_async"]

T = TypeVar("T")


def backoff_delay(
    attempt: int, *, base: float = 0.5, factor: float = 2.0, cap: float = 30.0, jitter: bool = False
) -> float:
    """第 ``attempt`` 次（从 1 起）重试前的退避秒数：min(cap, base*factor**(attempt-1))；jitter=满抖动。"""
    exp = base * (factor ** max(0, attempt - 1))
    delay = min(cap, exp)
    return random.uniform(0, delay) if jitter else delay


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    base: float = 0.5,
    factor: float = 2.0,
    cap: float = 30.0,
    jitter: bool = True,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], Awaitable[None]] | None = None,
) -> T:
    """调用 ``fn``，失败按指数退避重试至多 ``attempts`` 次；耗尽后抛最后一次异常。"""
    import asyncio

    do_sleep = sleep or asyncio.sleep
    last: BaseException | None = None
    for i in range(1, attempts + 1):
        try:
            return await fn()
        except exceptions as exc:
            last = exc
            if i >= attempts:
                raise
            await do_sleep(backoff_delay(i, base=base, factor=factor, cap=cap, jitter=jitter))
    raise last  # pragma: no cover - 逻辑上不可达


def backoff_delays(attempts: int, **kwargs: float | bool) -> Iterable[float]:
    """便捷：生成前 ``attempts`` 次的退避序列（无抖动时用于预览/测试）。"""
    return [backoff_delay(i, **kwargs) for i in range(1, attempts + 1)]  # type: ignore[arg-type]
