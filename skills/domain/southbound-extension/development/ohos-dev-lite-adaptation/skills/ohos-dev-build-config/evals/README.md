# ohos-dev-build-config evals

5 个评估用例，判据全部来自 SR-04 交付件真实验证数据（自验证说明-补做.md：装配咬合 5/5 + 配置一致性 12/12 实测值 + build-config-output/ 实例文件），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l1_config_json_ohos_build_generation` | L1 产品定义生成（config.json + ohos.build） | product_name/type/kernel_type 正确 + part 名 `product_` 前缀推导 + 咬合字段指向真实路径 | SR-04 4.1/4.2 实测值（Hi3516CV610 L1，咬合 5/5 + 一致性 12/12） |
| `part_name_derivation_and_generation_order` | part 名推导 + 生成顺序约束 | part = product_ + product_name；ohos.build 必须晚于 config.json | SR-04 实测 part=product_hi3516cv610_dmeb_liteos_a + SKILL Step 3 顺序 |
| `soc_buildgn_hardcoded_sdk_path_antipattern` | 反模式识别（SoC BUILD.gn 写死猜测的 SDK 路径） | 拒绝写死厂商 SDK 路径，留 deps 接入点 + TODO | SR-04 验收判据 3 + 配置一致性 #7（实测仅 deps + TODO 占位） |
| `assembly_mating_check_mismatch` | 咬合校验（5 条逐条判定，注入 module_list↔group 断裂） | 5 条全查 + 精确定位唯一断裂项 + 修复方向 | SR-04 装配咬合 5 条实测清单 |
| `formal_build_vs_gn_smoke` | 编译方式选择 | 裸 gn+ninja 仅语法冒烟；正式编译 build.sh --product | SKILL Step 5 禁止项 + SR-04 4.3 编译命令实测 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：

- part 名 `product_` 前缀推导（基线常给裸 product_name 或 board 名）
- 生成顺序约束（基线不知道 ohos.build 依赖 config.json 的 product_name）
- SoC BUILD.gn SDK 接入点规则（基线倾向保留/修补给出的路径而不是拒写）
- 咬合 5 条全量清单（基线常只查 JSON 语法或个别字段，漏 module_list↔group、product_adapter_dir 等装配级检查）
- build.sh vs 裸 gn+ninja 区别（基线可能直接给 gn gen + ninja 当正式编译）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **咬合完整性**：with skill 逐条跑 5 条装配咬合（part 名/module_list/device_build_path/product_adapter_dir/目录约定）；基线通常只做 JSON 语法检查
2. **命名推导**：with skill 的 part 名 100% 带 `product_` 前缀且与 product_name 严格拼接；基线命名随机性强
3. **反模式拦截**：写死 SDK 路径场景，with skill 明确拒绝并给 TODO 接入点写法；基线常顺水推舟
4. **编译入口**：with skill 一律引导 `./build.sh --product`；基线倾向直接 gn/ninja
