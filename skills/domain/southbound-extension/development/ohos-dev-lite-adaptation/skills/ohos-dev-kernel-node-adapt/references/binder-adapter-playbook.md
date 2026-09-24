# binder 内核适配 playbook

> binder `ioctl c0186201 returned -22 EINVAL` ×400 → samgr `Goto next boot step return code:-9` 卡死，各 service（foundation/appspawn/各 sa）起不来反复重启。来源：hi3516cv610 实战（案例 OH001）。

## 症状

rootfs 起来，内核 boot 完进 OHOS init，串口狂刷：
```
binder: 83: 83 ioctl c0186201 returned -22       ← -EINVAL，~400 次
binder: 84: 84 ioctl c0186201 returned -22
...
samgr: Goto next boot step return code:-9         ← samgr 走不到下一步，启动卡死
```
各 service 起不来，反复重启。

## 根因

`c0186201` 是 binder ioctl 命令码（`BINDER_WRITE_READ`），`-22` = `-EINVAL`。binder ioctl 拒绝请求 = binder 协议层参数校验失败。**根因是 32 位 vs 64 位 binder 协议位宽错配**：

- Hi3516CV610 是 32 位 ARM（`arm-linux-ohos`），user 态 binder 库按 32 位 binder 协议编译，结构体 24B。
- 内核 binder.h 默认走 64 位协议，结构体 48B，`BINDER_IPC_32BIT` 宏未定义。
- `ioctl(BINDER_WRITE_READ)` 时内核按 64 位结构体拷贝，与 user 态 32 位结构体大小不匹配 → `-EINVAL`（-22）。

对照 OHOS 官方 `hispark_taurus_cv610_small.patch`（hi3516dv300 同系 CV610 小型系统参考适配）：patch 第 9 行明示内核 binder.h 需加 `#define BINDER_IPC_32BIT 1` 对齐 32 位协议。

## 适配操作

### 1. defconfig 开 CONFIG

```
CONFIG_ANDROID=y
CONFIG_ANDROID_BINDER_IPC=y
```

关 BINDERFS（32 位 OH 小系统用 misc_register/devtmpfs 出 `/dev/binder`，不走 binderfs）：

```
# 不开 CONFIG_ANDROID_BINDERFS（或 =n）
```

### 2. drivers/Kconfig source uncomment

binder 驱动要在 `drivers/Kconfig` 有 `source "drivers/android/Kconfig"`，被注释掉则驱动不编入：

```
# drivers/Kconfig
source "drivers/android/Kconfig"     # ← 不能被注释
```

### 3. 内核 binder.h 加 BINDER_IPC_32BIT（32 位 OH 小系统关键）

```c
// drivers/android/binder.h（或 vendor binder 头，按实际路径）
#ifndef BINDER_IPC_32BIT
#define BINDER_IPC_32BIT 1        /* ← 加这一行：32 位 ARM 对齐 OHOS user 态 binder 库（24B 结构体） */
#endif
```

> **64 位系统不加**：64 位 OH（L2 标准系统）user 态 binder 库按 64 位协议编译（48B），内核默认 64 位即可，不加 `BINDER_IPC_32BIT`。32 位 OH 小系统才加。

### 4. 关联 /dev/binder 节点

`/dev/binder`、`/dev/hwbinder`、`/dev/vndbinder` 依赖 `CONFIG_ANDROID_BINDER_IPC` + 禁 binderfs（用 misc_register/devtmpfs 自动建节点）。init.cfg pre-init 通常有 `chmod 0666 /dev/binder`（节点由驱动建，只需放权限）。

### 5. 重编 + 烧后验证

重编内核，重烧 kernel 分区：
```
binder ioctl 不再 -22       → 协议位宽对齐
samgr 走到下一步             → boot step 不卡 -9
foundation/appspawn/各 sa 起来
```

## 32 位 vs 64 位协议对照

| 维度 | 32 位 OH 小系统（如 hi3516cv610） | 64 位 OH 标准系统（L2） |
|------|-------------------------------|----------------------|
| user 态 binder 结构体 | 24B | 48B |
| 内核 binder.h | 加 `#define BINDER_IPC_32BIT 1` | 默认 64 位，不加 |
| 错配症状 | `ioctl -22 EINVAL` ×400 + samgr `boot step -9` | （不错配） |
| BINDERFS | 关（misc_register/devtmpfs） | 可开 |

## 原则

- **binder ioctl returned -22 EINVAL + samgr boot step 卡死 → 优先怀疑内核/user 态 binder 协议位宽错配**（32 位 vs 64 位结构体大小不一致）。`-22` = `-EINVAL` 是协议/参数校验失败通用码，常是结构体 sizeof 错配，不是权限/路径问题。
- **同 SoC 系列参考适配的 patch 是权威**：hi3516cv610 与 hispark_taurus_cv610 同系，官方 patch（如 `BINDER_IPC_32BIT` 一行）直接照打，别从零排查 binder 协议位宽。
- **先联网搜再查源码**：搜「binder ioctl returned -22 EINVAL openharmony」命中社区线索（32/64 位错配），再查参考仓 patch 确认。关联 memory `search-then-verify-in-source`、`opencode-websearch-fallback`。

## 关联

- `../ohos-issue-lite-diagnose/references/diagnostic-cases.md` §9 案例OH001（binder -22 完整诊断）
- `{{ASSET_ROOT}}/workflow/steps/02-kernel-port/SKILL.md` §binderfs（关 binderfs 用 misc_register/devtmpfs）
- `config-devnode-map.md`（binder 行：CONFIG_ANDROID_BINDER_IPC → /dev/binder → samgr/foundation 依赖）
