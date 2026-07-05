# jianbing_utils（煎饼 Util）

> 自研通用工具库。设计理念：小而全、开箱即用、以静态方法/纯函数为主、低学习成本；聚焦爬虫/数据方向常用工具。**借鉴业界优秀库的设计经验/思路，代码完全自主实现——不依赖也不复制任何第三方库源码。** 发布到 PyPI，供 `payipa` 等项目复用。

## 状态

**先建目录、按需实现**：当前仅 `s3` 有骨架（payipa 在用），其余为占位（`规划中`），随其他项目引入时再开发（YAGNI）。

### 采集 / 爬虫向

| 模块 | 说明 | 状态 |
|---|---|---|
| `s3` | S3 分片上传/下载（multipart / presigned / 断点续传） | 骨架 |
| `net` | HTTP 请求辅助（会话/重试/超时/UA 轮换/下载） | 规划中 |
| `parse` | 解析辅助（xpath/css/jsonpath/正则/文本抽取） | 规划中 |
| `dedup` | 去重/指纹（URL 规范化指纹、数据指纹、布隆/布谷鸟） | 规划中 |
| `pipeline` | 数据管道（批处理/落地/去重管道） | 规划中 |
| `proxy` | 代理辅助（代理池/选路/健康检查/溯源） | 规划中 |
| `render` | 浏览器渲染/自动化辅助（Playwright 兼容封装） | 规划中 |
| `ua` | User-Agent 池（随机/按平台） | 规划中 |
| `cookies` | Cookie 管理（解析/序列化/持久化） | 规划中 |
| `robots` | robots.txt / sitemap 辅助 | 规划中 |

### 通用工具向

| 模块 | 说明 | 状态 |
|---|---|---|
| `text` | 字符串工具（空白/截断/脱敏/命名风格/slug） | ✅ 已实现 |
| `datetime` | 日期时间（解析/格式化/时区/相对时间） | 规划中 |
| `collection` | 集合/字典工具（分组/扁平化/深合并/切片） | 规划中 |
| `number` | 数值/金额/单位换算/精度 | 规划中 |
| `crypto` | 哈希/HMAC/编码（md5/sha1/sha256/hmac_sha256/base64） | ✅ 已实现 |
| `codec` | 编码转换（base64/hex/url/百分号） | 规划中 |
| `fs` | 文件/路径/流工具（读写/遍历/临时文件） | 规划中 |
| `jsonx` | JSON 读写/路径取值/安全解析 | 规划中 |
| `cache` | 本地缓存（TTL/LRU） | 规划中 |
| `retry` | 重试/退避（backoff_delay / retry_async，指数退避 + 抖动） | ✅ 已实现 |
| `ratelimit` | 限流原语（令牌桶/漏桶） | 规划中 |
| `validate` | 数据校验（类型/正则/范围/schema） | 规划中 |
| `idgen` | ID 生成（uuid/雪花/短码） | 规划中 |
| `config` | 配置加载（env/文件/合并/校验） | 规划中 |
| `logx` | 结构化日志辅助 | 规划中 |
| `compress` | 压缩（zstd/gzip/zip 辅助） | 规划中 |
| `notify` | 通知（邮件/webhook/飞书 等） | 规划中 |
| `db` | 数据库薄封装（连接/分页/批量/游标） | 规划中 |
| `concurrency` | 并发辅助（协程池/信号量/超时） | 规划中 |

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
