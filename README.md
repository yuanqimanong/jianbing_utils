# jianbing_utils（煎饼 Util）

> 开箱即用的爬虫/数据工具库 —— 取材 **feapder 工具类**（请求/解析/去重/管道）+ **hutool 风格**（小而全、静态方法、开箱即用）。发布到 PyPI，供 `payipa` 等项目复用。

## 状态

M0 骨架。首个模块：**S3 分片上传/下载工具** `jianbing_utils.s3`。

- `multipart`：分片规划（纯函数，已实现）+ multipart 上传编排（断点续传，M1 落地）
- `presign`：presigned URL 签发/消费（M1 落地）
- `constants` / `types`：S3 协议常量与数据类型

网络动作在 M0 为 `NotImplementedError` 占位，随 payipa M1 storage 落地（惰性导入 `boto3`）。

## 安装

```bash
pip install jianbing-utils          # 轻量本体（零运行期硬依赖）
pip install 'jianbing-utils[s3]'    # 含 boto3（presigned 签发 / multipart 生命周期）
```

## 开发

```bash
uv sync                 # 安装 dev 依赖（pytest / ruff）
uv run pytest
uv run ruff check
uv build --no-sources   # 验证可脱离本机构建（依赖须全部来自公开 index）
```

- `requires-python >= 3.11`；代码须保持 3.11 语法兼容（CI 矩阵 3.11–3.14）。
- 构建后端：`uv_build`（src layout）。

## License

MIT
