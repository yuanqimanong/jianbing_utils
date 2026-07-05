"""S3 分片上传/下载工具（jianbing_utils 首个模块）。

提供 multipart（5 MiB–5 GiB/块、断点续传）、presigned URL 签发/消费、进度回调、重试退避。
主控侧用于签发 presigned / 管理 multipart 生命周期；agent 侧只做 HTTP PUT（零密钥）。

M0 为骨架：分片规划为纯函数（已实现、可测），网络动作为 ``NotImplementedError`` 占位，
随 M1 storage 落地（惰性导入 boto3，走可选 extra ``jianbing-utils[s3]``）。
"""

from __future__ import annotations

from jianbing_utils.s3 import constants
from jianbing_utils.s3.constants import (
    DEFAULT_PART_SIZE,
    MAX_PART_SIZE,
    MAX_PARTS,
    MIN_PART_SIZE,
    MULTIPART_THRESHOLD,
)
from jianbing_utils.s3.multipart import (
    MultipartUploader,
    count_parts,
    plan_part_size,
)
from jianbing_utils.s3.presign import presign_get, presign_put, presign_upload_part
from jianbing_utils.s3.types import (
    MultipartSession,
    PartInfo,
    PresignedTarget,
    ProgressCallback,
)

__all__ = [
    "DEFAULT_PART_SIZE",
    "MAX_PARTS",
    "MAX_PART_SIZE",
    "MIN_PART_SIZE",
    "MULTIPART_THRESHOLD",
    "MultipartSession",
    "MultipartUploader",
    "PartInfo",
    "PresignedTarget",
    "ProgressCallback",
    "constants",
    "count_parts",
    "plan_part_size",
    "presign_get",
    "presign_put",
    "presign_upload_part",
]
