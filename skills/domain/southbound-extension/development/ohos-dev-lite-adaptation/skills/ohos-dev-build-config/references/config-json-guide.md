> **Scope**: config.json 产品定义——完整字段、子系统/部件清单、hb 发现机制
> **When**: 需要生成产品定义 `vendor/<device_company>/<board>/config.json` 时读取
> **Size**: ~230 lines

---

## 1. 文件定位与 hb 发现机制

`config.json` 是产品的**定义入口**，告诉构建系统（hb）这个产品叫什么、用什么板/内核、编哪些子系统与部件。

**位置约定（重要，纠正旧写法）**：

```
vendor/<device_company>/<board>/config.json
```

- 目录是 `<device_company>/<board>`（**不是** `<vendor>/<product>`）。
- `board` 既是板名，也是产品目录名；`product_name` 一般形如 `<device_company>_<board>`。
- 真机示例：`vendor/hisilicon/hispark_pegasus/config.json`，`product_name = "wifiiot_hispark_pegasus`。

**hb 如何发现产品**：

| 系统类型 | 发现方式 |
|---------|---------|
| mini / small（L0/L1） | hb 扫描 `vendor/<device_company>/<board>/config.json`，由其中的 `device_company`+`board`+`product_name` 定位 |
| standard | `productdefine/common/products/*.json`（**本 SKILL 不涉及**） |

> mini/small 产品**不写** `productdefine/common/products/`。只需把 config.json 放到正确的 vendor 目录即可被 hb 发现。

---

## 2. 完整字段定义

config.json 的顶层由**产品元数据**和 `subsystems[]` 两部分组成。缺产品元数据时 hb 找不到产品；缺 subsystems 时产品编不出内容。

### 2.1 产品元数据字段

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `product_name` | string | ✅ | 产品名，hb `--product` 的值；需与目录名约定一致 | `"wifiiot_hispark_pegasus"` |
| `type` | string | ✅ | 系统类型：`"mini"`=L0 轻量 / `"small"`=L1 小型 | `"mini"` |
| `version` | string | ✅ | 产品版本 | `"3.0"` |
| `ohos_version` | string | ✅ | OpenHarmony 版本 | `"OpenHarmony 1.0"` |
| `device_company` | string | ✅ | 芯片/设备厂商，对应 `device/board/<device_company>`、`device/soc/<device_company>` | `"hisilicon"` |
| `board` | string | ✅ | 板名，对应 `device/board/<device_company>/<board>` | `"hispark_pegasus"` |
| `device_build_path` | string | ✅ | hb 找 Board 级 BUILD.gn 的路径（相对源码根） | `"device/board/hisilicon/hispark_pegasus"` |
| `kernel_type` | string | ✅ | 内核类型：L0 `"liteos_m"`；L1 `"liteos_a"` 或 `"linux"` | `"liteos_m"` |
| `kernel_is_prebuilt` | bool | ⚠️ | 内核是否预编译。预编内核置 `true`，跳过内核源码构建 | `true` |
| `kernel_version` | string | ⚠️ | 内核版本，预编时可留空 `""` | `""` |
| `third_party_dir` | string | 可选 | 第三方库根目录（绝对路径 `//`） | `"//device/soc/.../third_party"` |
| `product_adapter_dir` | string | ✅ | HAL 适配目录，指向 `vendor/<device_company>/<board>/hals`（见 ohos-build-guide.md） | `"//vendor/hisilicon/hispark_pegasus/hals"` |

> ⚠️：`kernel_is_prebuilt` 决定编译链是否包含内核源码构建。新芯片若内核已移植并预编好，置 `true`；若需从源码编译内核，置 `false`（此时依赖内核裁剪能力提供的内核 BUILD.gn）。两种情况 `kernel_type` 必须与 Board 级 config.gni 一致。

### 2.2 subsystems[] 字段

顶层数组，每个元素描述一个子系统及其下的部件。

```json
"subsystems": [
  {
    "subsystem": "<子系统名>",
    "components": [
      {
        "component": "<部件名>",
        "features": ["<key>=<value>"]
      }
    ]
  }
]
```

- `subsystem`：子系统名，**必须与 OpenHarmony 仓库中的子系统目录名一致**
- `component`：部件名，**必须与仓库注册名完全一致**（仓库中对应 `lite_component("<component_name>")` 的名字）
- `features`：部件级功能开关，传键值对到部件 BUILD.gn；多数部件留空 `[]` 或省略

### 2.3 features 字段

```json
"features": ["key=value", "another_key=another_value"]
```

**何时需要填写**：部件 BUILD.gn 定义了 `feature_list` 并使用了某 feature key；需启用可选功能。
**何时可留空/省略**：大多数部件留空 `[]`，`{ "component": "utils_lite" }` 等价于 `{ "component": "utils_lite", "features": [] }`。

真实示例：
```json
{ "component": "hdf_core", "features": ["hdf_core_platform_test_support = true"] }
```

---

## 3. 部件名验证方法

部件名拼写错误会在 `gn gen` 阶段报 "component not found"。验证步骤：

1. 在子系统仓库找部件目录：`//<subsystem_path>/<component_name>/`
2. 该目录下有 `BUILD.gn` 且包含 `lite_component("<component_name>")` 定义
3. 目录名或 `lite_component` 名与你填写的不一致时，**以仓库实际名称为准**

常见易错部件名：
- `bounds_checking_function`（不是 `libsec`）
- `bootstrap_lite`（不是 `bootstrap`）
- `liteos_m`（不是 `liteos-m` 或 `kernel_liteos_m`）

---

## 4. 完整真实示例（Hi3861 wifiiot，L0 Mini）

```json
{
    "product_name": "wifiiot_hispark_pegasus",
    "type": "mini",
    "version": "3.0",
    "ohos_version": "OpenHarmony 1.0",
    "device_company": "hisilicon",
    "device_build_path": "device/board/hisilicon/hispark_pegasus",
    "board": "hispark_pegasus",
    "kernel_type": "liteos_m",
    "kernel_is_prebuilt": true,
    "kernel_version": "",
    "subsystems": [
      { "subsystem": "applications", "components": [
        { "component": "wifi_iot_sample_app", "features": [] }
      ]},
      { "subsystem": "iothardware", "components": [
        { "component": "peripheral", "features": [] }
      ]},
      { "subsystem": "hiviewdfx", "components": [
        { "component": "hilog_lite", "features": [] },
        { "component": "hievent_lite", "features": [] },
        { "component": "blackbox_lite", "features": [] },
        { "component": "hidumper_lite", "features": [] }
      ]},
      { "subsystem": "startup", "components": [
        { "component": "bootstrap_lite", "features": [] },
        { "component": "init", "features": [
          "init_feature_begetctl_liteos = true",
          "init_lite_use_thirdparty_mbedtls = true"
        ]}
      ]},
      { "subsystem": "commonlibrary", "components": [
        { "component": "utils_lite", "features": ["utils_lite_feature_file = true"] }
      ]}
    ],
    "third_party_dir": "//device/soc/hisilicon/hi3861v100/sdk_liteos/third_party",
    "product_adapter_dir": "//vendor/hisilicon/hispark_pegasus/hals"
}
```

> 上例为节选（省略 security/communication/xts 等）。完整产品请按目标功能从下方清单选取子系统/部件。

---

## 5. L0 (Mini) 子系统清单

L0 轻量系统（RAM < 1MB）可用子系统：

| 子系统 | 常用部件 | 说明 |
|--------|---------|------|
| `hiviewdfx` | hilog_lite, hievent_lite, blackbox_lite, hidumper_lite | 日志和诊断 |
| `startup` | bootstrap_lite, init | 启动引导 |
| `communication` | wifi_lite, dsoftbus, wifi_aware | 分布式通信 |
| `security` | device_auth, huks | 安全认证 |
| `systemabilitymgr` | samgr_lite | 系统服务管理 |
| `commonlibrary` | utils_lite | 公共工具库 |
| `updater` | sys_installer_lite | 系统升级 |
| `iothardware` | peripheral | IoT 外设子系统（L0 驱动入口） |
| `applications` | wifi_iot_sample_app | 示例应用 |
| `thirdparty` | mbedtls, bounds_checking_function | 第三方库 |
| `xts` | acts, tools, device_attest_lite | 兼容性测试 |

## 6. L1 (Small) 额外子系统

L1 小型系统（RAM ≥ 1MB）在 L0 基础上额外支持：

| 子系统 | 常用部件 | 说明 |
|--------|---------|------|
| `hdf` | hdf_core | HDF 驱动框架（精简版） |
| `kernel` | liteos_a | LiteOS-A 内核（本表为 L1-LiteOS 路线部件集；L1-Linux 路线的 kernel 部件为 Linux 内核组件，按目标产品实际配置） |
| `developtools` | syscap_codec | 系统能力编解码 |
| `ability` | dmsfwk_lite | 分布式能力框架 |
| `arkui` | ace_engine_lite | UI 引擎 |
| `multimedia` | media_lite | 多媒体 |

## 7. L0 vs L1 核心差异

| 维度 | L0 (Mini) | L1 (Small) |
|------|-----------|------------|
| `type` | `"mini"` | `"small"` |
| `kernel_type` | `"liteos_m"` | `"liteos_a"` 或 `"linux"` |
| 驱动框架 | IoT 外设子系统（`iothardware`） | 精简版 HDF（`hdf`） |
| 设备配置 | `board_config.h`（设备配置能力） | `.hcs`（设备配置能力） |

## 8. 查询官方子系统清单（ohos-lite-helper）

上方 §5/§6 是本 SKILL  curated 的常用子系统子集。`subsystems[]` 中的子系统名和 component 名必须与 OpenHarmony 官方注册一致，拼错或遗漏会导致 hb 装配失败。

**完整子系统清单**：上方 §5/§6 是常用子集。完整注册表需从 OpenHarmony 官方源码 `build/subsystem_config.json` 提取，或在项目中搜索已有芯片的 `config.json` 样本文件作为参考。

**校验方法**：生成 config.json 后，检查每个 `subsystem` 和 `component` 名是否与 ohos-lite-helper 返回的清单完全匹配（含大小写）。

---

## 9. 与其他文件的一致性约束（生成后必查）

- `product_name` 与 `vendor/<device_company>/<board>/ohos.build` 的 part 名前缀一致（见 `ohos-build-guide.md`）
- `device_build_path` 路径存在，且该目录下有 Board 级 `BUILD.gn`
- `product_adapter_dir` 指向的 `hals/` 目录真实存在
- `kernel_type` 与 Board 级 config.gni 的 `kernel_type` 完全一致
- `device_company`+`board` 与目录路径 `vendor/<device_company>/<board>/` 一致
