"""jianbing_utils（煎饼 Util）

开箱即用的爬虫/数据工具库：取材 feapder 工具类（请求/解析/去重/管道）+ hutool 风格
（小而全、静态方法、开箱即用）。首个模块为 S3 分片上传/下载工具（见 :mod:`jianbing_utils.s3`）。

设计纪律（见 payipa 新方案/决策记录）：
- ``requires-python >= 3.11``，代码须保持 3.11 语法兼容（供多项目复用，CI 矩阵 3.11–3.14）。
- 依赖全部来自公开 index；发布前 ``uv build --no-sources`` 验证可脱离本机构建。
- 重量级/可选客户端（如 boto3）走 extra + 惰性导入，保持库本体轻量。
"""

from __future__ import annotations

from jianbing_utils.__about__ import __version__

__all__ = ["__version__"]
