# 工具库架构

日期：2026-10-04。目标是让通用策略与执行器独立于 payipa、数据库、Web 框架和可选 SDK，同时保留已有导入入口。

## 模块边界

```text
retry/__init__.py       公共 facade，保留 backoff_delay/backoff_delays/retry_async
  ├─ policy.py         BackoffPolicy：不可变参数、校验、指数计算、抖动、封顶
  └─ runner.py         异步调用、异常选择、预算控制、可注入等待与取消传播

s3/__init__.py          公共 facade
  ├─ constants.py      项目协议常量
  ├─ planning.py       分片大小与分片数；纯整数计算
  ├─ types.py          纯数据对象
  ├─ multipart.py      网络编排骨架，继续导出旧规划函数
  └─ presign.py        可选 SDK 适配骨架
```

`runner → policy`、`planning → constants` 为单向依赖。策略层不得导入网络适配器或任何应用包。
`text` / `crypto` 继续是 stdlib 薄封装；未使用的规划目录保留兼容命名空间。
运行期硬依赖仍为零，可选 boto3 保持惰性导入。

## 修复的根因

| 问题 | 根因 | 修复与验证 |
|---|---|---|
| 长时间断连时退避反而退出 | `base * factor ** attempt` 在取 cap 前就可能 `OverflowError` | `BackoffPolicy` 保证封顶；测试覆盖 1,025 / 10,000 / 超大 attempt、零 base、恒定及衰减 factor |
| 无效重试预算报错不清晰 | 旧执行器保存最后异常，attempts=0 时实际上尝试抛出 None | 执行前验证正整数预算和异常类型，保证非法配置不调用操作 |
| 广泛异常过滤可能吞取消 | `exceptions=(BaseException,)` 包含任务取消 | asyncio cancellation、KeyboardInterrupt 和 SystemExit 始终传播；验证操作期间和等待期间取消 |
| 规划函数与网络骨架混在一起 | 纯计算与客户端编排位于同一模块 | 独立 `planning`，旧 facade / multipart 路径指向同一实现 |
| 分片计数存在浮点舍入 | 先用 `/` 转 float 再 `math.ceil` | 使用整数上取整；覆盖分片数边界和大整数精度 |
| README 的已实现状态不准确 | 工具模块演进后状态文字未同步 | 明确纯函数已实现、S3 网络接口未实现 |

## 公共 API 与兼容

已有 `from jianbing_utils.retry import backoff_delay, backoff_delays, retry_async` 保持有效。
新增 `BackoffPolicy` 供需要复用参数的调用方使用；facade 函数保持原有默认参数。
`backoff_delays` 仍返回 list；attempts=0 返回空列表。单次 `backoff_delay` 的 attempt≤0 继续采用首次退避值。
`from jianbing_utils.s3.multipart import plan_part_size, count_parts` 仍有效。

正常输入行为保持兼容。以下非法或控制流输入有意修正：

- base/cap 负数或非有限数、factor≤0 或非有限数：`ValueError`。
- retry_async 的非整数预算：`TypeError`；预算≤0：`ValueError`；空或非法异常过滤：`TypeError`。
- 取消与进程退出异常：即使调用方选择 BaseException，也不重试。
- count_parts 的负 total_size：`ValueError`，与 plan_part_size 一致。

S3 的实际上传、分片续传和 presigned 签发仍未实现；本次不改变协议常量，不宣称新增网络能力。
首次架构重构发布为 `v0.1.4`；2026-10-11 的边界修正发布为 `v0.1.5`。先合并并发布工具库 Git tag，再更新 payipa 的固定 tag 源和 lock。两个仓库联用时可通过 payipa 的 `scripts/verify_sibling_utils.py` 检查，不把本地 editable path 源写进提交。

## 2026-10-11 边界修正

- `truncate` 的 length、`mask` 的 keep_start / keep_end 必须是非负整数；非整数（包括 bool）抛出 `TypeError`，负数抛出 `ValueError`。校验先于空文本等快速返回，避免负切片意外保留待脱敏原文；有效输入行为不变。
- 重试执行器向上传播含取消或退出信号的嵌套 `BaseExceptionGroup`，保留原异常组；普通 `ExceptionGroup` 仍按调用方的异常过滤配置重试。
- 指数退避仅在中间幂溢出或落入低精度范围时回退到对数域，防止乘上 base 后本可表示的结果被提前封顶或清零。极端结果按浮点精度比较，cap 和抖动范围保持不变。
- S3 规划的字节数必须是整数，显式或自动计算的分片大小不能超过既有 `MAX_PART_SIZE`。较小的 preferred_part_size 继续自动抬升，`count_parts` 保留大整数精确计数；协议常量和网络骨架未变。

## 验证与回滚

运行 `uv run pytest`、`uv run ruff check`、`uv run ruff format --check`、`uv build --no-sources`。
架构测试用 `python -S` 验证无第三方运行时依赖，并静态检查纯策略的导入边界；CI 的 Python 3.11–3.14 矩阵继续保留。

`v0.1.5` 无数据库或用户数据迁移。需要回滚时，将使用方依赖 tag 改回 `v0.1.4` 并重新生成 lock、运行回归；库仓库通过 revert 本次合并提交恢复，保留已发布 tag。
