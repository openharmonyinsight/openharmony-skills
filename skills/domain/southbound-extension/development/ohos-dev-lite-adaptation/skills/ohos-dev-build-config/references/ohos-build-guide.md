> **Scope**: 产品注册三件套——ohos.build、vendor BUILD.gn、hals/ 目录
> **When**: 生成产品装配文件时读取（config.json 生成后、编译验证前）
> **Size**: ~170 lines

---

## 1. 为什么需要这三件套

`config.json` 告诉 hb "这个产品编哪些子系统/部件"，但要让 hb 把**本产品的 Board 级构建**拉进编译图，还需要三个文件咬合：

| 文件 | 作用 |
|------|------|
| `ohos.build` | 注册产品级 part（部件），声明 module_list 指向产品构建 target |
| `BUILD.gn`（vendor 目录） | 定义 ohos.build module_list 指向的 target（产品构建入口） |
| `hals/` | HAL 适配目录，config.json 的 `product_adapter_dir` 指向它 |

缺 `ohos.build` → 产品的 part 不被注册，Board 级构建不会被 hb 拉进依赖图，编译产物为空。
`ohos.build` 的 module_list 指向不存在的 target → `gn gen` 报 "no such target"。

---

## 2. ohos.build 格式

位置：`vendor/<device_company>/<board>/ohos.build`

```json
{
  "parts": {
    "product_<product_name>": {
      "module_list": [
        "//vendor/<device_company>/<board>:<board>"
      ]
    }
  },
  "subsystem": "product_<product_name>"
}
```

### 字段说明

- `subsystem`：产品子系统名，约定为 `product_<product_name>`
- `parts.<part_name>`：part 名 = `product_<product_name>`，与 subsystem 同名
- `module_list`：该 part 包含的构建 target 列表，格式 `//<路径>:<target名>`
  - 默认指向本 vendor 目录的 `<board>` target：`//vendor/<device_company>/<board>:<board>`

### 真实示例（Hi3861 wifiiot）

```json
{
  "parts": {
    "product_wifiiot_hispark_pegasus": {
      "module_list": [
        "//vendor/hisilicon/hispark_pegasus:hispark_pegasus"
      ]
    }
  },
  "subsystem": "product_wifiiot_hispark_pegasus"
}
```

> `product_name` 来自 config.json。ohos.build 的 part 名 / subsystem 名都以 `product_` 前缀 + product_name 构成，三者必须保持一致。

---

## 3. vendor BUILD.gn 模板

位置：`vendor/<device_company>/<board>/BUILD.gn`

定义 ohos.build `module_list` 指向的 target。最简形式是一个 `group()`：

```gn
# vendor/<device_company>/<board>/BUILD.gn
group("<board>") {
  deps = [
    # 产品需要拉进编译的本地目标（通常为空，子系统/部件由 config.json 驱动）
    # 如有 vendor 自有 demo/应用模块，在此引用：
    # "//vendor/<device_company>/<board>/demo/led_demo:led_demo",
  ]
}
```

### 关键约束

- target 名（`group("<board>")`）**必须**等于 ohos.build `module_list` 冒号后的部分
- target 名约定用 `<board>`（与板名一致）
- `group()` 是虚拟目标，不编译文件，仅聚合依赖；产品实际编译内容由 config.json 的 subsystems 驱动，不在这里重复

### 真实示例（Hi3861 hispark_pegasus）

```gn
# vendor/hisilicon/hispark_pegasus/BUILD.gn
group("hispark_pegasus") {
  deps = []
}
```

ohos.build 中 `//vendor/hisilicon/hispark_pegasus:hispark_pegasus` 的 `hispark_pegasus` 即此 group 名。

---

## 4. hals/ 适配目录

位置：`vendor/<device_company>/<board>/hals/`

config.json 的 `product_adapter_dir` 指向此目录。它承载产品级 HAL 适配（audio/utils 等接口的厂商实现占位）。

### 目录结构

```
vendor/<device_company>/<board>/
├── config.json              ← 产品定义（本 SKILL）
├── ohos.build               ← 部件注册（本 SKILL）
├── BUILD.gn                 ← 产品构建 target（本 SKILL）
└── hals/                    ← HAL 适配目录（本 SKILL 生成目录骨架与占位 BUILD.gn）
    ├── BUILD.gn             ← 最小构建占位
    ├── audio/               ← 音频 HAL 适配（占位）
    └── utils/               ← 工具 HAL 适配（占位）
```

### 最小 BUILD.gn 占位

```gn
# vendor/<device_company>/<board>/hals/BUILD.gn
group("hals") {
  deps = []
}
```

> 本 SKILL 只生成 `hals/` 目录骨架与占位 BUILD.gn。config.json 的 `product_adapter_dir` 必须指向这个真实存在的目录，否则 hb 装配阶段报路径缺失。

---

## 5. 三者咬合关系（生成后必查）

```
config.json
  ├─ product_name ──────────────┐
  │                              ├─→ ohos.build: part/subsystem 名 = "product_" + product_name
  ├─ product_adapter_dir ────────┼─→ hals/ 目录必须存在
  └─ device_build_path ─────────→ Board 级 BUILD.gn 必须存在（见 build-gn-templates.md）

ohos.build
  └─ module_list ["//vendor/<dc>/<board>:<board>"]
                              └─→ vendor/<dc>/<board>/BUILD.gn 中 group("<board>") 必须存在
```

交叉校验清单：
- [ ] ohos.build 的 `subsystem`/`parts` key = `product_` + config.json 的 `product_name`
- [ ] ohos.build `module_list` 的 target 名 == vendor BUILD.gn 的 `group("<board>")` 名
- [ ] config.json `product_adapter_dir` 指向的 `hals/` 目录存在且含 BUILD.gn
- [ ] `hals/BUILD.gn` 有合法 target（即使是空 group）

---

## 6. 与 config.json / 其他文件的协作

- **生成顺序**：先 config.json（确定 product_name、device_company、board）→ 再 ohos.build（用 product_name 构造 part 名）→ 再 vendor BUILD.gn（用 board 构造 target 名）→ 最后 hals/ 占位
- ohos.build 的 part 名依赖 config.json 的 `product_name`，**不可先于 config.json 生成**
- 这三个文件加上 config.json，构成 hb 能完整发现并装配的产品骨架
