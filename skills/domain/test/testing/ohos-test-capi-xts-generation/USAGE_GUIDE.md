# ohos-test-capi-xts-generation 用户输入内容指导

## 一、首次配置（一次性输入）

编辑 `{skill_root}/.oh-capi-xts-config.json`，仅需一个字段：

```json
{
  "OH_ROOT": "/home/chen/openharmony"
}
```

`OH_ROOT` 指向 OpenHarmony 源码根目录。CAPI 头文件路径默认解析为 `{OH_ROOT}/interface/sdk_c/`。

---

## 二、对话触发输入（自然语言）

### 1. 触发技能的最低输入

只需在对话中提及以下关键词之一即可激活技能：
```
CAPI / N-API / napi / .h文件 / 头文件解析 / Native测试 / C测试 / 原生测试
编译 / build / compile / 覆盖率报告 / 未覆盖API / 测试套编译 / XTS
async_build / cleanup_group / N-API封装 / 三重校验 / 新增接口 / new API
```

### 2. 完整生成任务（推荐模板）

提供以下信息（缺项技能会反问）：

| 字段 | 必需 | 示例输入 |
|------|------|---------|
| 子系统名称 | 必需 | "为 **multimedia** 子系统生成测试" |
| 目标 .h 头文件路径 | 必需 | "头文件在 `interface/sdk_c/multimedia/image/native_image.h`" |
| Flow 标识 | 可选 | "新增接口" → Flow C；或附带覆盖率报告文件 → Flow A |
| 目标测试套路径 | 可选 | "目标测试套：`test/xts/acts/multimedia/ActsCameraManagerCapiTest`"（已存在则补充，未指定则从模板新建） |
| 具体 API 名称 | 可选 | "针对 `OH_NativeImage_Create` 接口" |

**示例完整输入**：
```
为 multimedia 子系统的 OH_NativeImage_Create 接口生成 N-API 封装测试，
头文件位于 interface/sdk_c/multimedia/image/native_image.h，
目标测试套路径 test/xts/acts/multimedia/ActsNativeImageCapiTest
```

### 3. 补充已有测试套（Flow A 输入）

必须附带覆盖率报告文件：
```
根据覆盖率报告 /path/to/coverage_report.csv，
为 ActsHiLogCapiTest 测试套补充未覆盖的 API 测试
```

支持报告格式：CSV / XLSX / JSON / MD。

### 4. 仅编译模式输入

触发关键词"编译/build/compile/重新编译"即可，技能跳过 Phase 1-6：
```
编译 ActsCameraManagerCapiTest 测试套
```
或编译失败后重试：
```
ActsCameraManagerCapiTest 编译失败，帮我重新编译
```

### 5. 编译环境参数输入（Phase 7 可选）

如需指定产品，附带：
```
产品名称 rk3568
```
默认产品为 `rk3568`，不指定即用默认值。

---

## 三、脚本手动调用输入

技能执行时会自动调用脚本，但用户也可手动运行。参数如下：

| 脚本 | 必需参数 | 示例 |
|------|---------|------|
| `verify_napi_triple.sh` | 测试套路径 | `bash scripts/verify_napi_triple.sh test/xts/acts/multimedia/ActsNativeImageCapiTest` |
| `check_test_suite_structure.sh` | 测试套路径 | `bash scripts/check_test_suite_structure.sh <测试套路径>` |
| `auto_fix_napi_triple.sh` | 测试套路径 | `bash scripts/auto_fix_napi_triple.sh <测试套路径>` |
| `async_build.sh` | OH_ROOT + 测试套名 [+ 产品] [+ 动作] | `bash scripts/async_build.sh /home/chen/openharmony ActsNativeImageCapiTest` |
| `cleanup_group.sh` | OH_ROOT + 测试套名 | `bash scripts/cleanup_group.sh <OH_ROOT> <测试套名>` |
| `run_xts_test.py` | 见脚本内帮助 | `python scripts/run_xts_test.py --help` |

`async_build.sh` 的动作参数：`start`（默认）/ `status` / `stop` / `tail` / `wait`。

---

## 四、交互式反问时的回答

当信息不完整时，技能会反问，对应回答模板：

- **"子系统无法确定"** → 回答子系统名：`multimedia` / `hilog` / `bundlemanager` / `ability` 等
- **"目标测试套路径"** → 回答已有工程路径 或 `新建`
- **"OH_ROOT 路径无效"** → 修正 `.oh-capi-xts-config.json` 中的路径
- **"是否创建新工程"** → `是`（从模板复制）/ `否`（指定已有路径）
- **"是否执行真机测试（Phase 8）"** → `是`（需连接设备）/ `否`（跳过）

---

## 五、最小可用输入

如果只想最快跑通，三句话即可：

```
1. OH_ROOT 已配置在 .oh-capi-xts-config.json
2. 为 <子系统> 的 <API名> 生成 N-API 测试，头文件 <.h 路径>
3.（编译时追加）编译 <测试套名>
```

技能会自动补全其余决策（默认 Flow C、产品 rk3568、从模板创建工程）。
