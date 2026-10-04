"""S3 分片规划纯函数：整数运算，不依赖客户端、凭证或网络适配器。"""

from __future__ import annotations

from jianbing_utils.s3.constants import DEFAULT_PART_SIZE, MAX_PARTS, MIN_PART_SIZE


def plan_part_size(total_size: int, *, preferred_part_size: int = DEFAULT_PART_SIZE) -> int:
    """每块至少 MIN_PART_SIZE（末块除外），分片数最多 MAX_PARTS。

    分片数超限时放大到 MIN_PART_SIZE 的整数倍。所有除法使用整数上取整，避免大整数浮点舍入。
    """
    if total_size < 0:
        raise ValueError("total_size 不能为负")
    part_size = max(preferred_part_size, MIN_PART_SIZE)
    min_needed = (total_size + MAX_PARTS - 1) // MAX_PARTS
    if min_needed > part_size:
        part_size = ((min_needed + MIN_PART_SIZE - 1) // MIN_PART_SIZE) * MIN_PART_SIZE
    return part_size


def count_parts(total_size: int, part_size: int) -> int:
    """计算分片数；零字节对象不需要分片。"""
    if part_size <= 0:
        raise ValueError("part_size 必须为正")
    if total_size < 0:
        raise ValueError("total_size 不能为负")
    return (total_size + part_size - 1) // part_size
