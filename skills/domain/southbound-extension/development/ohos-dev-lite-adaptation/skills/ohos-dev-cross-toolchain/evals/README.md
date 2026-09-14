# ohos-dev-cross-toolchain evals

4 个评估用例，判据来自 skill 自身方法论（探测/配置/校验/wrapper/兜底规则）+ 真实环境样例（Hi3516CV610_L1_适配指南.md §2.2 记载的 musl 工具链真实路径），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 来源 |
|----|------|--------------|------|
| `cross_toolchain_auto_detect_and_verify` | ①交叉工具链探测（auto 模式） | PATH 探测记录 prefix/path/version + 测试编译校验（不止 --version） | SKILL.md 流程 §2 + Initial Checks §5 |
| `user_mode_prefix_path_config_generation` | ②前缀/路径配置生成（user 模式） | 全路径拆 prefix/path 正确 + 配置块 schema 完整 | SKILL.md 配置位置 yaml 模板 + 真实 musl 工具链样例 |
| `version_incompatibility_zicsr_detection_wrapper_fix` | ③版本不兼容检出 + wrapper 修复 | zicsr 拆分根因识别 + wrapper 注入 flag 方案 + config 落盘 | SKILL.md wrapper 模式 + compiler_fix_playbook §4 recipe |
| `no_toolchain_found_install_guidance_not_silent_substitute` | 探测不到工具链的兜底 | 不静默用本机 gcc 顶替、引导安装/转 user 模式 | SKILL.md 禁止操作表 + Exceptions 表 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent。预期基线在以下断言上显著弱于 with skill：

- `auto_detect`：基线常只跑 `--version` 即判可用，不跑测试编译
- `user_mode`：基线拆前缀/路径易错（漏尾杠/整串塞 path），配置块字段不全
- `zicsr`：基线倾向建议"改源码用内联汇编"或"升级 gcc"（可行但不合题设约束），不知道 wrapper 注入方案
- `no_toolchain_found`：基线可能直接拿本机 gcc 顶替（编不出目标架构）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **校验深度**：with skill 测试编译为准；基线 --version 即判可用
2. **配置规范化**：with skill 输出 schema 完整的 toolchain 块；基线自由格式
3. **wrapper 方案**：with skill 直给 exec 包装 + flag 注入 recipe；基线绕路（改源码/换工具链）
4. **兜底纪律**：with skill 缺工具链不静默顶替；基线可能用本机 gcc 硬上
