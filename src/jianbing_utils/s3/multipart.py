"""S3 multipart 上传编排（分片规划 + 断点续传 + 完整性）。

网络接口仍为骨架；纯分片规划在 planning 模块实现，此处保留旧导入路径。
断点续传用 multipart 原生机制（持久化 UploadId → ListParts 查已传 → 补传 → Complete），
无需引入 tus；生产须配 ``AbortIncompleteMultipartUpload`` lifecycle 清理孤儿分块。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from jianbing_utils.s3.constants import (
    DEFAULT_PART_SIZE,
)
from jianbing_utils.s3.planning import count_parts as count_parts
from jianbing_utils.s3.planning import plan_part_size as plan_part_size
from jianbing_utils.s3.types import MultipartSession, PartInfo, ProgressCallback

if TYPE_CHECKING:
    from pathlib import Path

    from botocore.client import BaseClient


class MultipartUploader:
    """multipart 上传编排器（骨架）。

    典型用法（M1 落地后）::

        up = MultipartUploader(bucket, key, client=s3)
        session = up.initiate(total_size=size)
        # ...逐块 upload_part（失败重试/退避）...
        up.complete(session)

    断点续传：持久化 ``session``，重启后 :meth:`resume` → :meth:`list_parts` 补传缺口。
    """

    def __init__(
        self,
        bucket: str,
        key: str,
        *,
        part_size: int = DEFAULT_PART_SIZE,
        client: BaseClient | None = None,
    ) -> None:
        self.bucket = bucket
        self.key = key
        self.part_size = part_size
        self._client = client

    def initiate(self, *, total_size: int | None = None) -> MultipartSession:
        """CreateMultipartUpload，返回可持久化的会话。"""
        raise NotImplementedError("M1 storage 落地：create_multipart_upload")

    def upload_part(
        self,
        session: MultipartSession,
        part_number: int,
        data: bytes,
    ) -> PartInfo:
        """UploadPart（带重试退避），返回分片 ETag。"""
        raise NotImplementedError("M1 storage 落地：upload_part + 重试退避")

    def list_parts(self, session: MultipartSession) -> list[PartInfo]:
        """ListParts：查询服务端已存在的分片（断点续传用）。"""
        raise NotImplementedError("M1 storage 落地：list_parts")

    def complete(self, session: MultipartSession) -> str:
        """CompleteMultipartUpload，返回对象最终 ETag。"""
        raise NotImplementedError("M1 storage 落地：complete_multipart_upload")

    def abort(self, session: MultipartSession) -> None:
        """AbortMultipartUpload：清理未完成上传（防孤儿分块计费）。"""
        raise NotImplementedError("M1 storage 落地：abort_multipart_upload")

    def resume(self, session: MultipartSession) -> MultipartSession:
        """从持久化的会话恢复：核对 ListParts，补齐 ``session.parts``。"""
        raise NotImplementedError("M1 storage 落地：基于 list_parts 恢复进度")

    def upload_file(
        self,
        path: Path,
        *,
        progress: ProgressCallback | None = None,
    ) -> str:
        """一站式：规划分片 → initiate → 逐块传（可续传）→ complete。"""
        raise NotImplementedError("M1 storage 落地：整合分片规划 + 逐块上传 + 进度回调")
