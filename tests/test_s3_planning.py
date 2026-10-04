"""整数分片规划与旧 multipart 导入路径兼容。"""

from __future__ import annotations

import pytest

from jianbing_utils.s3 import MAX_PARTS, MIN_PART_SIZE, count_parts, multipart, plan_part_size, planning


def test_legacy_exports_forward_to_pure_planning() -> None:
    assert count_parts is planning.count_parts is multipart.count_parts
    assert plan_part_size is planning.plan_part_size is multipart.plan_part_size


def test_integer_division_has_no_float_rounding() -> None:
    total = 2**53 + 1
    assert count_parts(total, 1) == total
    assert count_parts(total, 2) == 2**52 + 1


@pytest.mark.parametrize("extra", [-1, 0, 1])
def test_part_count_boundary(extra: int) -> None:
    total = MIN_PART_SIZE * MAX_PARTS + extra
    size = plan_part_size(total, preferred_part_size=MIN_PART_SIZE)
    assert count_parts(total, size) <= MAX_PARTS
    assert size >= MIN_PART_SIZE
    if extra <= 0:
        assert size == MIN_PART_SIZE
    else:
        assert size == 2 * MIN_PART_SIZE


def test_negative_object_sizes_are_rejected_consistently() -> None:
    with pytest.raises(ValueError):
        plan_part_size(-1)
    with pytest.raises(ValueError):
        count_parts(-1, MIN_PART_SIZE)
