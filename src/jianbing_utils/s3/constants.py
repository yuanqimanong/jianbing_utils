"""S3 / S3 兼容对象存储的协议级常量。

数值依据 AWS 官方 multipart / presigned 限制（新方案 01 §2.1 已核验）：
单 PUT ≤ 5 GiB；multipart 每块 5 MiB–5 GiB、最多 10000 块、单对象上限约 5 TiB；
presigned URL 用 IAM 长期凭证签最长 7 天（临时凭证签则随凭证过期提前失效）。
"""

from __future__ import annotations

# ── 分片大小限制 ────────────────────────────────────────────────────────────
MIN_PART_SIZE: int = 5 * 1024 * 1024  # 5 MiB（最后一块可小于此值）
MAX_PART_SIZE: int = 5 * 1024 * 1024 * 1024  # 5 GiB
MAX_PARTS: int = 10_000  # 单对象最多分片数

# ── 对象大小限制 ────────────────────────────────────────────────────────────
MAX_SINGLE_PUT_SIZE: int = 5 * 1024 * 1024 * 1024  # 单次 PUT 上限 5 GiB
MAX_OBJECT_SIZE: int = 5 * 1024 * 1024 * 1024 * 1024  # 单对象上限 ~5 TiB

# ── 默认策略（骨架初值，可被调用方覆盖；最终默认档随 POC 定，见 SDD §14）──────
DEFAULT_PART_SIZE: int = 16 * 1024 * 1024  # 默认分片 16 MiB
MULTIPART_THRESHOLD: int = 100 * 1024 * 1024  # 超过 100 MiB 建议走 multipart

# ── presigned URL 有效期 ───────────────────────────────────────────────────
PRESIGN_MAX_TTL_SECONDS: int = 7 * 24 * 3600  # IAM 长期凭证签发上限 7 天
DEFAULT_PRESIGN_TTL_SECONDS: int = 3600  # 默认 1 小时

# ── 重试退避（骨架初值）────────────────────────────────────────────────────
DEFAULT_MAX_RETRIES: int = 5
DEFAULT_BACKOFF_BASE_SECONDS: float = 0.5
