---
name: ohos-dev-sa-codegen
description: >
  Use when developing OpenHarmony SystemAbility (SA): generating IDL-based SA
  framework code from scratch, migrating hand-written Proxy/Stub to IDL mode,
  or modifying existing SA code (adding interfaces, updating configs, adding
  dependency listeners). Covers IDL definition, Proxy/Stub generation, SA
  registration, profile configuration, CFG process configuration, and SELinux
  rules. Triggers: "新建 SA", "创建 SA", "生成 SA", "迁移到 IDL", "修改 SA",
  "SystemAbility 开发", "SA 框架代码".
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: sa
  capability: sa-codegen
  version: 0.1.0
  status: draft
  tags:
    - sa
    - idl
    - cpp
    - code-generation
---

# OpenHarmony SystemAbility (SA) 开发指导

## 概述

SA (SystemAbility) 是系统元能力，本质是一个 binder 实体，运行在服务端进程中，对外提供服务。

本技能以**交互式问答**引导用户提供必需信息，然后根据用户选择的模式自动生成完整的 SA 框架代码。

**Use when**: 用户请求 SA/SystemAbility 开发、创建系统服务、生成 SA 框架代码、迁移 SA 到 IDL 模式、或修改已有 SA 代码。

## 模板文件

代码模板和变量定义已整合到 `references/` 中：

- 代码模板：`references/idl-sa-templates.md`（生成代码时必须严格参照）
- 变量定义：`references/variable-reference.md`

---

## 工作流程：首次交互（模式选择）

当用户请求 SA 开发相关帮助时，**根据用户意图自动判断工作模式**。

### 意图识别与模式路由

根据用户表述自动匹配对应模式，无需显式询问：

| 用户意图关键词 | 自动匹配模式 | 参考文件（相对于本文件所在目录） |
|---------------|-------------|-------------------------------|
| "新建 SA"、"创建 SA"、"生成 SA"、"从零开发"、"IDL 化 SA" | 生成 IDL 化 SA | `references/generate-idl-sa.md` |
| "迁移到 IDL"、"非 IDL 改 IDL"、"Proxy/Stub 改自动生成" | 非IDL 改 IDL 迁移 | `references/migrate-to-idl.md` |
| "修改 SA"、"添加接口"、"改配置"、"加依赖监听" | 修改已有 SA 代码 | `references/modify-existing-sa.md` |

**意图不明确时**，根据上下文推断最可能的模式；完全无法判断时，简要列出选项让用户确认。

### MANDATORY：加载详细指引

确认模式后，必须 Read 对应的参考文件获取完整执行流程。

| 模式 | 参考文件（相对于本文件所在目录） |
|------|-------------------------------|
| 生成 IDL 化 SA | `references/generate-idl-sa.md` |
| 非IDL 改 IDL 迁移 | `references/migrate-to-idl.md` |
| 修改已有 SA 代码 | `references/modify-existing-sa.md` |

**所有模式通用** — 执行前务必 Read `references/anti-patterns.md`，了解 NEVER 列表和常见失败模式。

---

## 目录结构总览

### IDL 化 SA 项目结构

参照 `references/idl-sa-templates.md` 中的模板：

```
{module}/
├── BUILD.gn                          # group() 汇总所有子目标
├── interfaces/
│   └── I{SaName}.idl                 # IDL 接口定义
├── services/
│   ├── BUILD.gn                      # idl_gen_interface + source_set + shared_library
│   ├── include/
│   │   └── {sa_name}.h              # SA 服务端头文件（继承 Stub）
│   └── src/
│       └── {sa_name}.cpp            # SA 服务端实现
├── sa_profile/
│   ├── {sa_id}.json                  # SA Profile
│   └── BUILD.gn                      # ohos_sa_profile
├── etc/
│   ├── {process_name}.cfg            # CFG 进程配置
│   └── BUILD.gn                      # ohos_prebuilt_etc
```

---

## 客户端获取 SA 的代码模板

无论哪种模式，客户端获取 SA 的方式相同：

```cpp
#include "iservice_registry.h"
#include "system_ability_definition.h"

auto samgr = SystemAbilityManagerClient::GetInstance().GetSystemAbilityManager();
if (samgr == nullptr) {
    return;
}
sptr<IRemoteObject> remote = samgr->GetSystemAbility({SA_ID});
if (remote == nullptr) {
    return;
}
auto proxy = iface_cast<I{SaName}>(remote);
```

---

## 服务端约束（务必遵守）

| 约束 | 说明 |
|------|------|
| 仅 native 进程可注册 SA | App 进程不能注册 |
| Publish 前必须完成初始化 | SA 注册前必须处于可用状态 |
| OnStart 不能耗时 | 同一进程 SA 共享线程池，耗时阻塞其他 SA 启动 |
| 构造函数不能耗时 | 影响 dlopen 耗时 |
| SA 服务端 so 做好隔离 | 不直接暴露给其他 SA 业务 |

**性能监控日志关键字**：`"OnStart-SA:"`、`"OpenSo"`

---

## Selinux 权限配置

| 操作 | 需要的权限 |
|------|-----------|
| 注册 SA | `add` |
| 注册远端 SA | `add_remote` |
| 获取 SA | `get` |
| 获取远端 SA | `get_remote` |

---

## SA ID 上库

- SA ID 定义：`foundation/systemabilitymgr/samgr/interfaces/innerkits/samgr_proxy/include/system_ability_definition.h`
- SA 服务名：`base/hiviewdfx/hidumper/frameworks/native/dump_utils.cpp`

---

## 调试方法

```bash
# push 配置到设备
hdc file send {process_name}.cfg /system/etc/init/
hdc file send {process_name}.json /system/profile/

# 重启设备
hdc shell reboot

# 检查进程
hdc shell ps -A | grep {process_name}

# 查看 SA 注册状态
hdc shell hidumper -ls
```

---

## Demo 代码参考

https://gitcode.com/openharmony/systemabilitymgr_safwk/tree/master/test/services/safwk/unittest/listen_ability

---

## Agent 工作检查清单

代码生成完成后，按此清单验证：

**信息完整性校验（在代码生成前执行）：**

- [ ] 全部 10 项必填字段已由用户明确提供（SA 类名、SA ID、进程名、子系统名、部件名、启动方式、分布式支持、HiLog domain、接口方法、生成路径）
- [ ] SA ID 为正整数（> 0），非临时值
- [ ] 未使用任何默认值或占位值填充必填字段

**代码生成质量校验：**

- [ ] 已读取对应模板文件，生成代码严格遵循模板结构和风格
- [ ] 所有必需文件已生成（按对应模式）
- [ ] 根 BUILD.gn 使用 `group()` 汇总所有子目标（services、etc、sa_profile）
- [ ] SA 类继承正确：`SystemAbility` + `Stub`（IDL 生成）
- [ ] `REGISTER_SYSTEM_ABILITY_BY_ID` 宏 3 个参数正确
- [ ] `DECLARE_SYSTEM_ABILITY` 宏已添加
- [ ] 构造函数接受 `int32_t saId, bool runOnCreate` 并传给基类
- [ ] `OnStart()` 中调用 `Publish(this)` 且无耗时操作
- [ ] services/BUILD.gn 包含 `idl_gen_interface`、两个 `ohos_source_set`（proxy/stub）、`ohos_shared_library`
- [ ] `idl_gen_interface` 的 `log_domainid` 和 `log_tag` 已配置
- [ ] SA Profile JSON 中 `name` 与代码注册的 SA ID 一致
- [ ] SA Profile JSON 中 `libpath` 指向正确的 so
- [ ] CFG 中进程名与 SA Profile 的 `process` 一致
- [ ] CFG 启动路径使用 `/system/bin/sa_main`
- [ ] sa_profile/BUILD.gn 使用 `import("//build/ohos/sa_profile/sa_profile.gni")`
- [ ] etc/BUILD.gn 使用 `ohos_prebuilt_etc`
- [ ] `HiLogLabel` 的 domain 和 tag 已配置
- [ ] 头文件 guard 宏正确

**编译验证（代码生成后执行）：**

生成代码后，使用以下命令进行编译验证：

```bash
./build.sh --product-name rk3568 --cache --build-target {sa_name}
```

- `{sa_name}` 对应根 BUILD.gn 中 `group()` 的目标名（即 snake_case 的 SA 名）
- 编译目标也可指定为子目录目标，如 `services:{sa_name}` 仅编译 so 库
- 验证步骤：
  1. 执行编译命令，确认退出码为 0（编译成功）
  2. 若编译失败，根据错误日志修复生成的代码，重新编译直到通过
  3. 编译通过后告知用户代码已通过编译验证
