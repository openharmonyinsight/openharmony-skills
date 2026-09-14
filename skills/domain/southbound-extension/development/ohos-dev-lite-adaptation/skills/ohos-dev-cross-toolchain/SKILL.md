---
name: ohos-dev-cross-toolchain
description: OpenHarmony Lite 交叉编译工具链配置器——探测/选择/校验工具链，生成 wrapper 注入 flag，保存工具链 profile 到 workflow_config.yaml，同步 chip-basics.yaml。支持 4 种模式：auto-detect / user-provided / wrapper / docker。Use when a cross toolchain must be selected, verified, or fixed for an OpenHarmony Lite build; triggers include 配置工具链、用自己的工具链、工具链缺失、工具链探测、gcc/riscv 版本查不到、交叉编译器前缀是什么、换 GCC 版本、wrapper 注入 flag、zicsr 指令集扩展缺失、prebuilt gcc 报未知指令、用 docker 编译。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: cross
  capability: toolchain
  version: 0.1.0
  status: trial
---

# 工具链配置器

管理交叉编译工具链的选择、配置、wrapper 生成、profile 保存、校验。
**主动询问用户用哪种工具链**（不只缺失才问），按选择配置并写入 `workflow_config.yaml`。

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 明确配置任务 | "配置工具链"、"用我的工具链编译"、"生成工具链配置" |
| 症状词（隐性需求） | "交叉编译器找不到"、"riscv gcc 在哪"、"报 unrecognized command-line option / unknown instruction"（zicsr 类指令集扩展缺失 → wrapper 模式）、"换 GCC 版本" |
| 流程链式调用 | workflow P1 Step 2c 工具链安装 / P4 Step 0d 工具链检查读本 skill 写入的配置；ohos-dev-build-config 编译前环境确认 |
| 同义表达 | toolchain profile / 交叉编译环境 / 编译器前缀 / cross gcc |

**不触发**（明确排除）：整个编译环境从零搭建含源码同步等（走 ohos-dev-build-config / workflow env-prep）；编译报错的诊断定位（走 ohos-issue-lite-diagnose，除非确诊是工具链问题回来配置）。

## Scope

本 skill 负责 OpenHarmony Lite（L0/L1）**交叉编译工具链**的选择、配置、wrapper 生成、profile 保存、校验。**主动询问用户用哪种工具链**（不只缺失才问），按选择配置并写入 `workflow_config.yaml` 的 `toolchain:` 块，并同步到 `chip-basics.yaml` 的 toolchain 字段（P1 输出）。

**任务边界**：本 skill 只管工具链这一层——产出是 `toolchain:` 配置块（mode/prefix/path/version/special_flags/wrapper/docker_image）。**不负责**：用该工具链执行完整编译（ohos-dev-build-config / ohos-ci-lite-deploy-burn）、编译错误的根因诊断（ohos-issue-lite-diagnose）、SDK/源码环境搭建（workflow env-prep）。

### 4 种模式

| mode | 含义 | 何时用 |
|---|---|---|
| `auto` | auto-detect PATH 里的 `{prefix}gcc` | 默认，用户无偏好 |
| `user` | 用用户提供的 `path`/`prefix` | 用户有自己的工具链，不想用环境里的 |
| `wrapper` | wrapper 脚本包装二进制注入 flag | prebuilt 缺指令集扩展（如 zicsr），见 `references/wrapper-recipes.md` |
| `docker` | 预配置编译容器镜像 | 用户想用容器化环境 |

## Initial Checks

配置前按以下顺序先做判断：

1. **用户偏好询问**：主动问用户用哪种（auto/user/wrapper/docker 四选一），不只工具链缺失才问——用户有自己的工具链时不问会用错环境里的。
2. **现有配置探测**：`workflow_config.yaml` 是否已有 `toolchain:` 块？有且校验通过 → 直接复用（profile 复用），不重复问。
3. **PATH 探测（auto 模式）**：`which {prefix}gcc` → 找到几个？多个不同版本 → 让用户选，不默认取第一个。
4. **目标架构判定**：从 chip_spec.json 的 cpu.coreType 或用户目标取架构，前缀跟架构走（L0 Cortex-M→arm-none-eabi-、RISC-V→riscv32-unknown-elf-；L1 musl 系→arm-linux-musleabi- 等）。
5. **可用性测试编译**（校验必做，不只查 `--version`）：`echo 'int main(){return 0;}' | {prefix}gcc -x c {special_flags} - -o /dev/null`——`--version` 能跑不代表能编目标代码（缺指令集扩展/头文件时只在真编译暴露）。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 只查 `--version` 就判定工具链可用 | 必须跑测试编译（`int main(){return 0;}` 真编过才算可用）——缺指令集扩展/头文件只在真编译暴露 |
| PATH 里有多个 gcc 时默认取第一个 | 列出版本让用户选，并记录选定项的 path/prefix/version |
| 未问用户偏好就自作主张选模式 | 主动询问四选一（auto/user/wrapper/docker），用户有自己的工具链时优先 user |
| 编造工具链前缀/路径（凭记忆写 `/opt/...`） | 前缀/路径必须来自探测结果（which）或用户提供的真实路径；探测不到 → 走异常兜底（安装引导或问用户） |
| 把 special_flags 硬编进每条编译命令 | 统一配到 `toolchain.special_flags`（或 wrapper），下游读 config 注入，不散落各处 |
| 改了配置不写回 workflow_config.yaml | 配置必须落盘（toolchain: 块 + chip-basics.yaml 同步），后续 P1/P4 直接读，不重复问 |
| wrapper 修 zicsr 类缺失时直接改 prebuilt 二进制 | wrapper 只做透明包装注入 flag（`exec 原gcc "$@" flags`），不patch二进制本身 |

## ① 文件路由表

| 用户意图 | Agent 读取 |
|---------|-----------|
| 查 toolchain 配置块字段定义与模板 | 项目根 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml` §1 |
| 生成 wrapper 脚本（注入 flag recipe / GCC 版本兼容要点） | 本 skill `references/wrapper-recipes.md` |
| 工具链适配 patch 深入案例（GT patch 全集，可选深读） | `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` §4 |
| 工具链安装步骤（读本 skill 配置） | `{{ASSET_ROOT}}/workflow/steps/01-env-prep/SKILL.md` Step 2c |
| 编译前工具链检查（读本 skill 配置） | `{{ASSET_ROOT}}/workflow/steps/04-build-verify/SKILL.md` Step 0d |

## ② 工作流

### 1. 主动询问用户工具链偏好（不只缺失才问）

> 你想用哪种工具链编译？
> - [ ] **auto** — 用环境 PATH 里的（默认，工作流 auto-detect）
> - [ ] **user** — 我有自己的，提供 path + prefix（不用环境里的）
> - [ ] **wrapper** — 包装现有二进制注入 flag（如 prebuilt 缺 zicsr）
> - [ ] **docker** — 用预配置编译容器

### 2. 按 mode 配置 + 校验

```bash
# auto / user:
{path}/{prefix}gcc --version                      # path 空则查 PATH
echo 'int main(){return 0;}' | {path}/{prefix}gcc -x c {special_flags} - -o /dev/null  # 测试编译

# wrapper（必须用 wrapper 真跑测试编译，不只查 --version）:
echo 'int main(){return 0;}' | {wrapper} -x c - -o /dev/null

# docker（测试编译进容器跑，不只查 --version）:
echo 'int main(){return 0;}' | docker run -i --rm {docker_image} {prefix}gcc -x c {special_flags} - -o /dev/null
```

- `auto`：查 PATH，记录 prefix/path/version 到 config。
- `user`：让用户提供 path + prefix，校验 `{path}/{prefix}gcc` 可编译，记录。
- `wrapper`：按 `references/wrapper-recipes.md` 生成 wrapper 脚本注入 `special_flags`，**用 wrapper 跑测试编译通过后**才记录 wrapper 路径。
- `docker`：让用户提供镜像名，**容器内测试编译**通过才算镜像可用，记录 `docker_image`。

#### 测试编译失败分类（校验失败时按此路由）

```
测试编译失败（--version 正常）?
    ├── unknown instruction / unrecognized option（csrrw、-march 类）
    │       → 指令集扩展缺失（如 zicsr）→ wrapper 模式注入扩展 flag（版本兼容见 references/wrapper-recipes.md §5）
    ├── No such file / cannot find header
    │       → 头文件/sysroot 缺失 → wrapper 解不了；检查工具链是否带 newlib/sysroot，或换带 sysroot 的工具链
    └── cannot find -lgcc / libgcc 版本报错
            → libgcc 与 GCC 版本不匹配 → 对齐参考仓/官方 prebuilt 版本换工具链
```

### 3. 写入配置

把结果写回 `workflow_config.yaml` 的 `toolchain:` 块 + `chip-basics.yaml` 的 toolchain 字段（prefix/path/version/special_flags/wrapper）。后续 P1 Step 2c / P4 Step 0d 直接读 config，不再重复问。

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **PATH 里探测不到任何交叉 gcc** | 不静默换本机 gcc（编不出目标架构）——引导安装：读 `{{ASSET_ROOT}}/workflow/steps/01-env-prep/SKILL.md` Step 2c 安装步骤 + compiler_fix_playbook 工具链获取章节；装不了（无网/无权限）→ 问用户提供现成工具链路径转 user 模式 |
| **测试编译失败但 `--version` 正常** | 大概率缺指令集扩展/头文件——先跑 `echo 'int main(){return 0;}' | {prefix}gcc -x c -march=<target> -` 复现定位；属 march 指令集缺失（如 zicsr）→ 转 wrapper 模式注入扩展 flag |
| **PATH 里有多个版本工具链** | 全部列出（path + version），让用户选；选定后写死 path 不再依赖 PATH 顺序 |
| **用户给的 path/prefix 校验失败**（路径不存在/前缀拼不出 gcc） | 原样告知失败原因（哪个路径/哪个二进制缺失），让用户修正后再配；不擅自改用 PATH 里的替代品 |
| **wrapper 也解不了（flag 注入后仍编不过）** | 说明不是简单缺扩展——升级方向：换正确版本的工具链（对齐参考仓/官方 prebuilt 版本）或转 docker 模式用预配置镜像；记录已试过的 flag 组合避免重复试错 |
| **docker 镜像不可用**（本地无镜像且拉取失败） | 降级：回到 auto/user 模式先跑通本地工具链，docker 待网络/镜像就绪再切（config 留 user/auto 配置，不空着） |
| **目标架构未知导致前缀没法定** | 从 chip_spec.json 的 cpu.coreType / metadata 取架构；仍未知 → 追问用户目标板，不猜前缀 |

## 配置位置

工具链配置在 `workflow_config.yaml` 的 `toolchain:` 块（见项目根 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml` §1）。本 skill 帮用户填这块 + 同步到 `chip-basics.yaml` 的 toolchain 字段（P1 输出）。

```yaml
toolchain:
  mode: auto              # auto | user | wrapper | docker
  prefix: ""              # mode=user: "riscv32-unknown-elf-"
  path: ""                # mode=user: "<TOOLCHAIN_ROOT>/bin"
  version: ""             # 可选: "13.2.0"
  special_flags: []       # ["-march=rv32imac_zicsr"]
  wrapper: ""             # mode=wrapper: wrapper 脚本路径
  docker_image: ""        # mode=docker: 镜像名
```

## wrapper 生成（mode=wrapper）

Read `references/wrapper-recipes.md`（简单 wrapper / 参数感知 wrapper v3 / as+ld 包装 / GCC 版本兼容要点）。典型：prebuilt GCC 不暴露 zicsr 到 march，wrapper 动态注入：

```bash
#!/bin/sh
# wrapper: 注入 -march=rv32imac_zicsr
exec {path}/{prefix}gcc.real "$@" -march=rv32imac_zicsr
```

生成后用 wrapper 跑测试编译，通过才把 wrapper 路径填到 `toolchain.wrapper`，编译命令用 wrapper 替代原 gcc。

## profile 复用

工具链配置持久存 `workflow_config.yaml`。跨项目复用时拷贝 `toolchain:` 块到新项目 config。

## 引用

- `references/wrapper-recipes.md` — wrapper 配方（透明包装原则 / v3 脚本 / as+ld 包装 / GCC 版本兼容实测要点）
- `compiler_fix_playbook.md §4`（ohos-dev-build-config，可选深读）— 工具链适配 patch 完整案例
- `{{ASSET_ROOT}}/workflow/steps/01-env-prep/SKILL.md` Step 2c — 工具链安装（读本 skill 的配置）
- `{{ASSET_ROOT}}/workflow/steps/04-build-verify/SKILL.md` Step 0d — 工具链检查（读本 skill 的配置）
