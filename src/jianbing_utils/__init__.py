"""jianbing_utils（煎饼 Util）—— 自研通用工具库。

设计理念：小而全、开箱即用、以静态方法/纯函数为主、低学习成本；聚焦爬虫/数据方向的常用工具。
借鉴业界优秀库的**设计经验/思路**，代码完全自主实现——不依赖、也不复制任何第三方库源码。

模块（先建目录、按需实现，当前以 payipa 用到的为主）：
- ``s3``       —— S3 分片上传/下载（首个模块；payipa agent 直传大对象用）
- ``net``      —— HTTP 请求辅助（规划中）
- ``parse``    —— 解析辅助（规划中）
- ``dedup``    —— 去重/指纹（规划中）
- ``pipeline`` —— 数据管道（规划中）

设计纪律（见 payipa 新方案/决策记录）：
- ``requires-python >= 3.11``，代码须保持 3.11 语法兼容（供多项目复用，CI 矩阵 3.11–3.14）。
- 依赖全部来自公开 index；发布前 ``uv build --no-sources`` 验证可脱离本机构建。
- 重量级/可选客户端（如 boto3）走 extra + 惰性导入，保持库本体轻量。
"""

from __future__ import annotations

from jianbing_utils.__about__ import __version__

__all__ = ["__version__"]
