"""通用异步重试执行器；等待函数可注入，取消与进程退出信号始终向上传播。"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from jianbing_utils.retry.policy import BackoffPolicy

T = TypeVar("T")


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
    """至多执行 attempts 次；只重试指定异常，耗尽后保留最后一次异常的 traceback。"""
    if not isinstance(attempts, int):
        raise TypeError("attempts 必须是整数")
    if attempts < 1:
        raise ValueError("attempts 必须至少为 1")
    if (
        not isinstance(exceptions, tuple)
        or not exceptions
        or any(not isinstance(cls, type) or not issubclass(cls, BaseException) for cls in exceptions)
    ):
        raise TypeError("exceptions 必须是非空异常类型 tuple")
    policy = BackoffPolicy(base=base, factor=factor, cap=cap, jitter=jitter)
    do_sleep = sleep if sleep is not None else asyncio.sleep
    attempt = 1
    while True:
        try:
            return await fn()
        except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
            raise
        except exceptions:
            if attempt >= attempts:
                raise
            await do_sleep(policy.delay(attempt))
            attempt += 1
