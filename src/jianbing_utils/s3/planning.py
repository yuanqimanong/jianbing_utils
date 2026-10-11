"""S3 分片规划纯函数：整数运算，不依赖客户端、凭证或网络适配器。"""

from __future__ import annotations

from jianbing_utils.s3.constants import DEFAULT_PART_SIZE, MAX_PART_SIZE, MAX_PARTS, MIN_PART_SIZE


def plan_part_size(total_size: int, *, preferred_part_size: int = DEFAULT_PART_SIZE) -> int:
    """每块 MIN_PART_SIZE–MAX_PART_SIZE（末块可更小），分片数最多 MAX_PARTS。

    分片数超限时放大到 MIN_PART_SIZE 的整数倍。所有除法使用整数上取整，避免大整数浮点舍入。
    """
    _require_integer(total_size, "total_size")
    _require_integer(preferred_part_size, "preferred_part_size")
    if total_size < 0:
        raise ValueError("total_size 不能为负")
    if preferred_part_size > MAX_PART_SIZE:
        raise ValueError("preferred_part_size 不能超过 MAX_PART_SIZE")
    part_size = max(preferred_part_size, MIN_PART_SIZE)
    min_needed = (total_size + MAX_PARTS - 1) // MAX_PARTS
    if min_needed > part_size:
        part_size = ((min_needed + MIN_PART_SIZE - 1) // MIN_PART_SIZE) * MIN_PART_SIZE
    if part_size > MAX_PART_SIZE:
        raise ValueError("无法在 MAX_PART_SIZE 和 MAX_PARTS 限制内规划分片")
    return part_size


def count_parts(total_size: int, part_size: int) -> int:
    """计算分片数；零字节对象不需要分片。"""
    _require_integer(total_size, "total_size")
    _require_integer(part_size, "part_size")
    if part_size <= 0:
        raise ValueError("part_size 必须为正")
    if part_size > MAX_PART_SIZE:
        raise ValueError("part_size 不能超过 MAX_PART_SIZE")
    if total_size < 0:
        raise ValueError("total_size 不能为负")
    return (total_size + part_size - 1) // part_size


def _require_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} 必须是整数")
