"""jianbing_utils.s3 骨架测试：验证纯函数正确、常量符合 S3 约束、网络动作为占位。"""

from __future__ import annotations

import pytest

import jianbing_utils
from jianbing_utils import s3
from jianbing_utils.s3 import (
    MAX_PARTS,
    MIN_PART_SIZE,
    MultipartSession,
    MultipartUploader,
    PartInfo,
    count_parts,
    plan_part_size,
)


def test_version_exposed() -> None:
    assert jianbing_utils.__version__ == "0.1.0"


def test_constants_match_s3_limits() -> None:
    assert MIN_PART_SIZE == 5 * 1024 * 1024
    assert MAX_PARTS == 10_000
    assert s3.MAX_PART_SIZE == 5 * 1024 * 1024 * 1024


@pytest.mark.parametrize(
    ("total", "part", "expected"),
    [
        (0, MIN_PART_SIZE, 0),
        (1, MIN_PART_SIZE, 1),
        (MIN_PART_SIZE, MIN_PART_SIZE, 1),
        (MIN_PART_SIZE + 1, MIN_PART_SIZE, 2),
        (10 * MIN_PART_SIZE, MIN_PART_SIZE, 10),
    ],
)
def test_count_parts(total: int, part: int, expected: int) -> None:
    assert count_parts(total, part) == expected


def test_plan_part_size_respects_min() -> None:
    # 小于 MIN 的 preferred 会被抬到 MIN
    assert plan_part_size(1, preferred_part_size=1) == MIN_PART_SIZE


def test_plan_part_size_scales_to_stay_under_max_parts() -> None:
    # 巨大对象：用 MIN 分片会超过 MAX_PARTS，规划须放大分片
    huge = MIN_PART_SIZE * MAX_PARTS * 3
    part_size = plan_part_size(huge, preferred_part_size=MIN_PART_SIZE)
    assert count_parts(huge, part_size) <= MAX_PARTS
    assert part_size % MIN_PART_SIZE == 0


def test_count_parts_rejects_bad_part_size() -> None:
    with pytest.raises(ValueError):
        count_parts(100, 0)


def test_multipart_session_uploaded_bytes() -> None:
    session = MultipartSession(bucket="b", key="k", upload_id="u", part_size=MIN_PART_SIZE)
    session.parts.append(PartInfo(part_number=1, etag="e1", size=100))
    session.parts.append(PartInfo(part_number=2, etag="e2", size=50))
    assert session.uploaded_bytes == 150


def test_network_actions_are_placeholders() -> None:
    # 骨架阶段：网络动作明确 NotImplementedError，避免"看起来已支持"的错觉
    up = MultipartUploader(bucket="b", key="k")
    with pytest.raises(NotImplementedError):
        up.initiate(total_size=1)
