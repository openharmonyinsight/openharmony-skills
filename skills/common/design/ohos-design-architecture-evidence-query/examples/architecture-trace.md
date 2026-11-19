# CLI 查询示例：从镜像文件到 SDK 接口

这是 **CLI 查询示例**；运行时下载与安装见 `references/usage.md`。假设 skill 已完成
运行时安装。先设置：

```bash
CLI="$HOME/.oskm/oskm-cli.pyz"
DB="$HOME/.oskm/knowledge.db"
```

本示例示范**怎么问、怎么读返回**，不冻结任何产品数量；换库或重扫后，字段含义
不变，具体值以当前快照为准。

## 1. 确认快照边界

```bash
python3.12 "$CLI" --db "$DB" ask get_scan_info
```

先核对 `product`、`scan_id`、`cpu_arch`、`status` 与每个采集器的
`status`/`record_count`。`degraded` 表示证据覆盖不足，不等于整库失败；但对应
采集器计数为 0 时，依赖该域的结论不可用。

## 2. 查看产品规模与入口

```bash
python3.12 "$CLI" --db "$DB" arch overview
```

读取 `counts` 与 `top_subsystems` 时同时记住：这些是当前快照的扫描结果，不是
产品常量。后续某个宽搜索返回 0 或明显偏小时，先回到这里检查对应采集器是否降级。

## 3. 先宽搜索，再追踪真实路径

```bash
python3.12 "$CLI" --db "$DB" ask search_elf_modules --query <文件名>
```

从返回的 `results[].dest` 里选真实安装路径；不要只凭 `cpu_arch` 猜
`system/lib/` 或 `system/lib64/`。确认路径后执行：

```bash
python3.12 "$CLI" --db "$DB" arch trace <dest>
```

返回中的 `install_module`、`component`、`subsystem`、`repo`、`repo_url` 和
`sdk_modules` 给出归属链路；`direct_dependencies` 只表示 DB 中记录的直接依赖数，
无 ELF 证据时为 `null`。

## 4. 依赖从 1 跳起

```bash
python3.12 "$CLI" --db "$DB" ask elf_dependencies \
  --dest <dest> --max_distance 1
```

同时报告 `total` 与 `truncated`。需要更深闭包时显式提高 `max_distance`；不要把
截断后的 `reachable` 条数当作闭包规模。

## 5. 核对 Native SDK 证据

```bash
python3.12 "$CLI" --db "$DB" ask search_native_headers --query <文件名>
```

Native SDK 映射按具体库建立。`get_native_headers` 对非 Native SDK 库返回 `NOT_FOUND` 时，只能说明
该库没有 Native SDK 头文件映射，不能推断 Native SDK 采集整体缺失；改查宽搜索命中的 Native SDK 库。

## 6. 反向影响与能力边界

```bash
python3.12 "$CLI" --db "$DB" arch impact <部件名>
python3.12 "$CLI" --db "$DB" arch provides <部件名>
python3.12 "$CLI" --db "$DB" arch runtime <服务名>
```

- `impact` 返回 DB 记录的部件依赖，不等于运行时 ABI 或设备影响面。
- `provides` 中 SDK 模块为空只说明本库没有关联记录，不能推导“不提供任何能力”。
- `runtime` 的 `cfg` 是扫描时声明；`component=null`、`sas=[]`、`hdis=[]` 表示
  未解析出宿主或托管设备，不要补猜。
