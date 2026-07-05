"""S3 工具的数据类型（纯数据，无 I/O）。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

# 进度回调：(已传字节数, 总字节数) -> None
ProgressCallback = Callable[[int, int], None]


@dataclass(slots=True)
class PartInfo:
    """一个已上传分片的元数据（Complete 时按 part_number 升序提交）。"""

    part_number: int  # 1-based，1..MAX_PARTS
    etag: str  # 上传该分片后 S3 返回的 ETag
    size: int  # 该分片字节数


@dataclass(slots=True)
class MultipartSession:
    """可持久化的 multipart 会话，用于断点续传。

    持久化本对象（如落盘/落库）即可在进程重启后 ``ListParts`` 查已传分片 → 补传 → Complete。
    """

    bucket: str
    key: str
    upload_id: str
    part_size: int
    total_size: int | None = None
    parts: list[PartInfo] = field(default_factory=list)
    completed: bool = False

    @property
    def uploaded_bytes(self) -> int:
        return sum(p.size for p in self.parts)


@dataclass(slots=True)
class PresignedTarget:
    """一次上传的目标描述（storage 抽象对 agent 屏蔽后端差异）。

    - s3 后端：``method="PUT"`` + presigned ``url``（可含一组 multipart 分片 URL）。
    - local 兜底：``url`` 指向主控流式分块上传端点 + 一次性 ``headers`` token。
    """

    url: str
    method: str = "PUT"
    headers: dict[str, str] = field(default_factory=dict)
    expires_at: float | None = None  # epoch 秒；None 表示不过期/未知
