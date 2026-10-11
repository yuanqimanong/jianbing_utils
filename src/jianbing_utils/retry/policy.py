"""无 I/O 的指数退避策略，可独立预览、复用与测试。"""

from __future__ import annotations

import math
import random
import sys
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
        exponent = max(0, attempt - 1)
        if self.factor == 1 or exponent == 0:
            exp = self.base
        else:
            try:
                power = float(self.factor) ** exponent
            except OverflowError:
                power = math.inf if self.factor > 1 else 0.0
            if not math.isfinite(power) or power < sys.float_info.min:
                # 中间幂溢出或丢失精度不代表乘上 base 后仍不可表示。
                # 仅在该边界使用对数域，普通退避保留原有计算结果。
                try:
                    log_delay = math.log(self.base) + exponent * math.log(self.factor)
                except OverflowError:
                    exp = self.cap if self.factor > 1 else 0.0
                else:
                    exp = self.cap if log_delay >= math.log(self.cap) else math.exp(log_delay)
            else:
                exp = self.base * power
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
