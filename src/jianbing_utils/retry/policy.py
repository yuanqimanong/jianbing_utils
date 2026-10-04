"""无 I/O 的指数退避策略，可独立预览、复用与测试。"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BackoffPolicy:
    """不可变退避参数；jitter=True 使用 [0, delay] 范围内的满抖动。"""

    base: float = 0.5
    factor: float = 2.0
    cap: float = 30.0
    jitter: bool = False

    def __post_init__(self) -> None:
        for name, value in (("base", self.base), ("cap", self.cap)):
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} 必须是有限非负数")
        if not math.isfinite(self.factor) or self.factor <= 0:
            raise ValueError("factor 必须是有限正数")

    def delay(self, attempt: int) -> float:
        """attempt 从 1 起；为兼容旧接口，小于 1 时仍使用首次退避值。"""
        if self.base == 0 or self.cap == 0:
            return 0.0
        try:
            exp = self.base if self.factor == 1 else self.base * self.factor ** max(0, attempt - 1)
        except OverflowError:
            # 长期断连后仍返回封顶值，不能因先算指数再取 min 而让重试循环退出。
            exp = self.cap if self.factor > 1 else 0.0
        delay = min(self.cap, exp)
        return random.uniform(0, delay) if self.jitter else delay


def backoff_delay(
    attempt: int, *, base: float = 0.5, factor: float = 2.0, cap: float = 30.0, jitter: bool = False
) -> float:
    """兼容函数接口：计算一次退避，参数校验与溢出处理统一由策略对象负责。"""
    return BackoffPolicy(base=base, factor=factor, cap=cap, jitter=jitter).delay(attempt)


def backoff_delays(
    attempts: int, *, base: float = 0.5, factor: float = 2.0, cap: float = 30.0, jitter: bool = False
) -> list[float]:
    """返回前 attempts 次的退避序列；attempts=0 返回空列表。"""
    if attempts < 0:
        raise ValueError("attempts 不能为负")
    policy = BackoffPolicy(base=base, factor=factor, cap=cap, jitter=jitter)
    return [policy.delay(i) for i in range(1, attempts + 1)]
