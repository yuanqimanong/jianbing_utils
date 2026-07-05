"""presigned URL 签发（主控侧：持 S3 密钥本地 HMAC 签名，密钥不出主控）。

骨架：定义接口与契约，具体实现（惰性导入 boto3）随 M1 storage 落地。
agent 侧只拿到 :class:`~jianbing_utils.s3.types.PresignedTarget` 做 HTTP PUT，永不接触密钥。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from jianbing_utils.s3.constants import DEFAULT_PRESIGN_TTL_SECONDS
from jianbing_utils.s3.types import PresignedTarget

if TYPE_CHECKING:  # 仅类型检查期引用，避免运行期硬依赖 boto3
    from botocore.client import BaseClient


def _require_boto3_client(client: BaseClient | None) -> BaseClient:
    """惰性获取 boto3 S3 client；未安装 extra 时给出清晰错误。"""
    if client is not None:
        return client
    try:
        import boto3  # noqa: PLC0415  惰性导入：boto3 走可选 extra
    except ImportError as exc:  # pragma: no cover - 依赖缺失路径
        raise RuntimeError("presign 需要 boto3，请安装可选依赖：pip install 'jianbing-utils[s3]'") from exc
    return boto3.client("s3")


def presign_put(
    bucket: str,
    key: str,
    *,
    ttl_seconds: int = DEFAULT_PRESIGN_TTL_SECONDS,
    content_type: str | None = None,
    client: BaseClient | None = None,
) -> PresignedTarget:
    """签发单对象 PUT 的 presigned URL（用于 ≤5 GiB 的整体上传）。"""
    raise NotImplementedError("M1 storage 落地：generate_presigned_url('put_object', ...)")


def presign_get(
    bucket: str,
    key: str,
    *,
    ttl_seconds: int = DEFAULT_PRESIGN_TTL_SECONDS,
    client: BaseClient | None = None,
) -> PresignedTarget:
    """签发 GET 的 presigned URL（UI 下载/重解析随用随签，秒级）。"""
    raise NotImplementedError("M1 storage 落地：generate_presigned_url('get_object', ...)")


def presign_upload_part(
    bucket: str,
    key: str,
    upload_id: str,
    part_number: int,
    *,
    ttl_seconds: int = DEFAULT_PRESIGN_TTL_SECONDS,
    client: BaseClient | None = None,
) -> PresignedTarget:
    """签发某个 multipart 分片的 presigned URL（可随任务握手批量签一组）。"""
    raise NotImplementedError("M1 storage 落地：generate_presigned_url('upload_part', ...)")
