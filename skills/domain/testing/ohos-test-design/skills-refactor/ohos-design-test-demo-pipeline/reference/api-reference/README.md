# api-reference 外部数据依赖（不随仓发布）

`reference/api-reference/` 是 ohos-design-test-demo-pipeline 的**外部、可安装、可探测**数据依赖，**不在本仓发布**（体积大、由上游维护、随 SDK 版本演进）。本文件是其安装 / 探测 / 降级契约。

## 数据布局与 schema

每个声明领域（见 `reference/domains.yaml`）一个子目录：

```
reference/api-reference/<domain>/
  index.json          # 索引：modules[].files[]{name,type,file}
  <api>.json          # index 引用的 API 详情（importPath/参数签名/examples）
  ...
```

`index.json` schema：`{ "modules": [{ "files": [{ "name": "<api>", "type": "...", "file": "<api>.json" }] }] }`

## 安装（可安装）

将上游取得的 `<domain>/index.json` 及其引用的 API JSON 文件放入 `reference/api-reference/<domain>/`。用探测脚本确认：

```bash
bash reference/api-reference/install.sh <domain>
```

未提供官方下载源前，数据由使用方自行取得并放置；`install.sh` 只做探测与指引，**不联网、不臆造、不修改用户环境**。

## 探测（可探测）

- 启动时探测 `reference/api-reference/<domain>/index.json` 是否存在。
- **存在** → 该领域运行于**完整模式**：API 验证走 index.json 索引（NEVER 凭记忆、NEVER Grep/Glob 兜底）。
- **不存在** → 该领域运行于**降级模式**：跳过 index 查找，所有 API 标注 `⚠️ 无 API 参考`，代码生成采用最佳努力 + 显式 ⚠️ 标记，由门禁决定是否继续。

## 降级路径与「不宣称可独立运行」

- 在 `api-reference` 未安装时，Demo Pipeline **不宣称可独立运行**；它以降级模式工作：API 准确性不保证，产物中相关 API 标 `⚠️ 无 API 参考`，validation/timing 写入 `api_reference=degraded`。
- 降级状态必须写入结果（`demo_design.md` API 清单 + 返回摘要 + timing），不得静默降质。
- 完整模式（API 准确性受 index 约束）仅在对应领域 `index.json` 已安装后启用。
