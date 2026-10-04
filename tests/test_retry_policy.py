"""策略与执行器的边界：长期运行、非法参数、指定异常和取消传播。"""

from __future__ import annotations

import asyncio
from dataclasses import FrozenInstanceError

import pytest

from jianbing_utils.retry import BackoffPolicy, backoff_delay, backoff_delays, retry_async


def test_policy_is_immutable_and_reusable() -> None:
    policy = BackoffPolicy(base=1.0, cap=3.0)
    assert [policy.delay(i) for i in range(1, 5)] == [1.0, 2.0, 3.0, 3.0]
    with pytest.raises(FrozenInstanceError):
        policy.base = 2.0


@pytest.mark.parametrize("attempt", [1025, 10_000, 10**1000])
def test_long_running_backoff_never_overflows(attempt: int) -> None:
    assert backoff_delay(attempt, base=1.0, cap=30.0) == 30.0
    assert backoff_delay(attempt, base=0.0) == 0.0
    assert backoff_delay(attempt, factor=1.0) == 0.5
    assert 0.0 <= backoff_delay(attempt, factor=0.5) < 1e-308


@pytest.mark.parametrize(
    "kwargs",
    [
        {"base": -1.0},
        {"base": float("nan")},
        {"base": float("inf")},
        {"factor": 0.0},
        {"factor": -1.0},
        {"factor": float("inf")},
        {"cap": -1.0},
        {"cap": float("nan")},
    ],
)
def test_invalid_policy_fails_before_execution(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        BackoffPolicy(**kwargs)


def test_delay_sequence_preserves_empty_and_legacy_first_attempt() -> None:
    assert backoff_delays(0) == []
    assert backoff_delay(0) == backoff_delay(1)
    with pytest.raises(ValueError):
        backoff_delays(-1)


@pytest.mark.parametrize("attempts", [0, -1])
def test_retry_rejects_invalid_budget_without_calling_operation(attempts: int) -> None:
    calls = []

    async def operation():
        calls.append("called")

    with pytest.raises(ValueError, match="attempts"):
        asyncio.run(retry_async(operation, attempts=attempts))
    assert calls == []


@pytest.mark.parametrize("attempts", [1.5, float("inf"), "3"])
def test_retry_rejects_non_integer_budget_without_calling_operation(attempts) -> None:
    async def operation():
        pytest.fail("non-integer budgets must be rejected before I/O")

    with pytest.raises(TypeError, match="attempts"):
        asyncio.run(retry_async(operation, attempts=attempts))


@pytest.mark.parametrize("exceptions", [(), (str,), [ValueError]])
def test_retry_rejects_invalid_exception_filter(exceptions) -> None:
    async def operation():
        pytest.fail("invalid exception filter must be rejected before I/O")

    with pytest.raises(TypeError, match="exceptions"):
        asyncio.run(retry_async(operation, exceptions=exceptions))


def test_unselected_error_is_not_retried() -> None:
    error = ValueError("permanent")
    calls = []

    async def operation():
        calls.append("called")
        raise error

    with pytest.raises(ValueError) as raised:
        asyncio.run(retry_async(operation, exceptions=(OSError,)))
    assert raised.value is error
    assert calls == ["called"]


def test_cancellation_is_never_retried_even_with_base_exception_filter() -> None:
    calls = []

    async def operation():
        calls.append("called")
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(retry_async(operation, exceptions=(BaseException,)))
    assert calls == ["called"]


def test_cancellation_during_backoff_propagates() -> None:
    calls = []

    async def operation():
        calls.append("called")
        raise OSError("transient")

    async def sleep(_delay):
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(retry_async(operation, sleep=sleep))
    assert calls == ["called"]
