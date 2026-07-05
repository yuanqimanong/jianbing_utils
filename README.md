# jianbing_utils（煎饼 Util）

> 自研通用工具库。设计理念：小而全、开箱即用、以静态方法/纯函数为主、低学习成本；聚焦爬虫/数据方向常用工具。**借鉴业界优秀库的设计经验/思路，代码完全自主实现——不依赖也不复制任何第三方库源码。** 发布到 PyPI，供 `payipa` 等项目复用。

## 状态

先建目录、按需实现，**当前以 `payipa` 用到的为主**（s3）；其余模块随其他项目引入时再开发（YAGNI）。

| 模块 | 说明 | 状态 |
|---|---|---|
| `s3` | S3 分片上传/下载（multipart / presigned / 断点续传） | 骨架（payipa agent 直传大对象用；网络动作随落地实现） |
| `net` | HTTP 请求辅助（重试/退避/会话/UA） | 规划中（目录占位，未实现） |
| `parse` | 解析辅助（选择器/文本清洗/日期） | 规划中 |
| `dedup` | 去重/指纹（URL 规范化指纹、数据指纹） | 规划中 |
| `pipeline` | 数据管道（批处理/落地） | 规划中 |

## 安装

```bash
pip install jianbing-utils          # 轻量本体（零运行期硬依赖）
pip install 'jianbing-utils[s3]'    # 含 boto3（presigned 签发 / multipart 生命周期）
```

## 开发

```bash
uv sync
uv run pytest
uv run ruff check
uv build --no-sources   # 验证可脱离本机构建（依赖须全部来自公开 index）
```

- `requires-python >= 3.11`；代码须保持 3.11 语法兼容（CI 矩阵 3.11–3.14）。
- 构建后端：`uv_build`（src layout）。

## License

MIT
