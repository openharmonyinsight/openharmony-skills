---
name: ohos-test-fault-param-injection
description: 当用户需要用系统参数向 OpenHarmony 服务注入故障以验证异常/错误路径与恢复能力时使用本 skill。适用所有 openharmony 仓库(SA/进程/模块)。触发:做故障注入、覆盖异常或错误路径、复现某接口超时/崩溃/错误码、模拟内存或资源耗尽、构造时序竞争、验证服务崩溃重拉或降级重试、测试高频接口故障分支、性能卡顿边界。不适用:能用 UT/TDD 直接覆盖的正常路径或硬件级故障。
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: fault
  capability: param-injection
  version: "1.5.0"
  status: draft
---

# 基于系统参数的故障注入测试方法（通用）

> 适用**整个 openharmony 仓库**，所有仓的 watchdog/参数/selinux/critical 机制一致，非某仓特例。参考文件路径见 `references/paths.md`。
> **前置依赖**：hdc 工具 + OpenHarmony 设备（Linux 主机 + USB/SSH 隧道连设备）。

## 1. 方法概述

核心思想：

```
param set <参数> <值>           ← 测试时注入故障开关（默认非持久，重启自动清除）
      ↓
代码 OHOS::system::GetIntParameter 读参（默认 0 → 不注入）
      ↓
按值决定执行路径（sleep / 返回错误码 / 走异常分支 / 耗尽资源 / 错开时序）
      ↓
触发待验证的故障路径（watchdog 杀进程 / 错误码返回 / 分支命中 / OOM / 竞态）
      ↓
观察恢复行为（调用方降级重试 / 告警 / 进程被杀后 init 重拉 / 状态恢复）
```

解决以下痛点：
1. **异常/错误路径覆盖率低**——错误码返回、空指针、边界、资源耗尽、异常分支等故障路径，常规 TDD/XTS 只跑 happy path，长期无验证，易带病上线
2. **高频接口硬编码故障拖垮整机**——订阅类/IPC 高频接口写死 sleep/错误会让整机卡死或持续异常；参数开关默认 0，按需注入；**注入代码必须用 `#ifdef FAULT_INJECT_TEST` 包裹**，release 构建不定义该宏、不安装 `.para/.para.dac`，确保 release 零开销、二进制不含注入面（见第 4 节）
3. **环境依赖型故障难构造且需稳定复现**——网络异常、时序竞争、内存/句柄耗尽、磁盘满真实环境难造；**默认用非持久参数**（不带 `persist.` 前缀），重启自动清除避免故障残留；能精确量化故障边界（sleep 毫秒/错误码值/资源配额）。仅专门验证跨重启语义时才用 `persist.`，且**不得与 critical 崩溃点组合**（见第 7 节 panic 重启风险）
4. **需验证系统容错与恢复能力**——服务崩溃后调用方降级、重试、告警链路，正常跑测不到，需主动注入触发

## 2. 适用场景与限制

| 场景 | 注入方式 | 验证目标 |
|------|---------|---------|
| watchdog 超时恢复 | sleep 超阈值 | XCOLLIE_FLAG_RECOVERY 杀进程 + init 重拉（critical 服务 N 次内重复崩溃会触发整机 panic 重启，见第 7 节） |
| 错误码返回路径 | 返回指定 err | 调用方容错/重试/降级 |
| 异常分支覆盖 | 走边界/空指针分支 | 分支逻辑正确性 |
| 时序竞争/临界条件 | sleep 错开时序 | 竞态保护/锁正确性 |
| 内存/资源耗尽 | 确定性 allocator/failpoint 注入（或隔离压力法） | OOM 保护/降级/回收 |
| 服务崩溃恢复 | 触发崩溃/超时杀进程 | init 重拉/状态恢复（注意 panic 阈值） |
| IPC 超时/失败 | sleep 或返回错误 | 调用方超时/重试 |
| 性能卡顿边界 | sleep 注入延时 | SLA/超时阈值/降级触发 |
| 配置/数据异常 | 参数注入非法值 | 校验/默认值/告警 |
| 降级/重试验证 | 触发失败路径 | 降级开关/重试上限 |

**不适用**：能用 UT/TDD 直接覆盖的正常路径；需要硬件级故障（断电、外设掉线）；已有专用故障注入框架的子系统；release 版（注入代码须默认 0 + `#ifdef FAULT_INJECT_TEST` 强制隔离，release 不含）。

## 3. 通用流程（7 步）

### Step 1：确定注入目标
- 选函数 + 故障类型（超时 / 错误码 / 异常分支 / 资源耗尽 / 时序竞争 / 降级）
- 确认该函数是否已有 watchdog：`grep -n "SetTimer\|XCOLLIE_FLAG" <service>.cpp`，看 flag 是否含 `XCOLLIE_FLAG_RECOVERY`（超时杀进程）。若已有，注入 sleep 即可触发；若无，可自加 watchdog 或只验证错误码/分支
- **若目标进程的 `.cfg` 含 `critical:[1,N,T]`，注入 RECOVERY 类（杀进程）故障前必须评估 panic 重启风险**：critical 服务在 N 次内重复崩溃会触发 `ExecReboot("panic")` 整机重启（见第 7 节）。对 critical 崩溃点优先用错误码/分支类非杀进程注入，必须杀进程时用非持久参数 + 单次消费（Step 2）

### Step 2：参数命名与注册
- **命名约定**：`<subsystem>.faultinject.<func>_<action>`（如 `account.faultinject.<func>_sleep_ms`）
  - **默认非持久**（不带 `persist.` 前缀）：重启自动清除，故障不跨重启残留；测试中断/崩溃后重启即恢复安全态
  - **参数名长度**必须小于目标版本的 `PARAM_NAME_LEN_MAX`（当前标准配置为 96，最大 95 字节）；允许字母、数字及 `.` `-` `@` `:` `_`
  - **参数值约束按故障类型定义**（sleep 毫秒整数、err 错误码整数、branch 布尔、leak 块数整数），不与参数名规则混写
  - **仅当专门验证跨重启语义时**才加 `persist.` 前缀，且**禁止与 critical 崩溃点组合**：`persist.` + RECOVERY + critical 会导致每次重启重复崩溃 → `ExecReboot("panic")` 整机重启循环（见第 7 节）。跨重启语义请优先用错误码/分支类（不杀进程）注入来验证持久化
- **退出类注入的单次消费**：对会杀进程/触发重启的注入（范式 A 的 RECOVERY），读参命中后应**立即 `OHOS::system::SetParameter(key, "0")` 自清零**，防止 init 重拉后再次命中同一参数反复崩溃（critical 服务尤甚）
- **注册**：在仓内 `param/*.para` 加默认值 0，`param/*.para.dac` 加权限
  ```
  # param/<subsystem>.para
  <subsystem>.faultinject.<func>_<action>=0

  # param/<subsystem>.para.dac
  <subsystem>.faultinject.<func>_<action>="<ownerUid>:<ownerGid>:644"
  ```
  BUILD.gn 的 `ohos_prebuilt_para` 模板会自动包含同目录 `.para`/`.para.dac`；**release 版不得安装这些文件**

### Step 3：代码注入点
见第 4 节通用模板。**全部模板必须用 `#ifdef FAULT_INJECT_TEST` 整体包裹**，读参默认 0；release 构建不定义 `FAULT_INJECT_TEST`（注入代码不编译、零开销、release 不含注入符号，见第 5 节自检）。

### Step 4：selinux 放行（首选定向 allow，setenforce 0 仅兜底）
- **首选**：定向放行单参数——改 `.te` 用 `debug_only(allow ...)` + `parameter_contexts` 打 label（见 `references/paths.md`），生产态可关闭 `debug_only` 不影响其他规则
- **兜底**（仅一次性隔离开发设备）：`setenforce 0` 切 permissive，所有进程都能读新参数。**必须先记录原始 `getenforce`，结束时按记录恢复（不无条件写 1，原始可能非 Enforcing）**
```bash
ORIG=$(hdc shell getenforce)     # 先记录原始状态
hdc shell "setenforce 0"          # 仅隔离开发设备兜底用
hdc shell "getenforce"            # 应显示 Permissive
# ... 测试 ...
# 任何中断路径（崩溃/OOM/连接中断）后也必须恢复：用 trap/finally 保证
hdc shell "setenforce $ORIG"     # 按记录恢复
hdc shell "getenforce"           # 断言恢复成功
```
> 服务进程运行在各自 selinux 域（如 samgr 域 / foundation 域 / 各 SA 自有域），读新参数需对应 label 放行（见 `references/paths.md` 的 selinux 映射）。新增参数若无 allow 规则，服务进程读不到（AVC denied）。`setenforce 0` 整体切 permissive 最简但风险最大（所有域放行）；定向 allow 更安全且可回归。**生产禁用 setenforce 0**。

### Step 5：编译推送（原子替换 + 失败回滚）
- 编译：`hb build <模块>`（账号仓细节见 `os-account-compile` skill）
- 推送：**禁止先删再用库**，必须临时路径 + 校验 + 备份 + 原子替换（复用 `os-account-device-test` skill 已验证的部署/回滚流程）：
  ```bash
  hdc shell "mount -o rw,remount /"
  # 1. 新库先发到同分区临时路径
  hdc file send out/<product>/account/os_account/libaccountmgr.z.so /system/lib64/libaccountmgr.z.so.new
  # 2. 校验大小/哈希和权限
  hdc shell "ls -l /system/lib64/libaccountmgr.z.so.new"
  hdc shell "sha256sum /system/lib64/libaccountmgr.z.so.new"
  # 3. 备份旧库并原子替换
  hdc shell "cp /system/lib64/libaccountmgr.z.so /system/lib64/libaccountmgr.z.so.bak"
  hdc shell "mv -f /system/lib64/libaccountmgr.z.so.new /system/lib64/libaccountmgr.z.so"
  # 任一步失败：mv -f ...bak ...so 恢复旧库，且禁止重启
  hdc shell "reboot"
  ```
  > 传输中断或校验失败时，必须先 `mv -f ...bak ...so` 恢复旧库，**禁止重启**——缺失关键库启动会变砖。

### Step 6：执行测试
```bash
# 注入故障（默认非持久参数，重启自动清除）
hdc shell "param set <subsystem>.faultinject.<func>_<action> <值>"
# 触发目标接口（测试用例/应用调用/hdc shell 调 SA）
# 观察
hdc shell "hilog | grep -E '<关键字>|XCOLLIE'"
hdc shell "ps -ef | grep <进程名>"   # 看是否被杀+init重拉
```

### Step 7：清理复位（必须）
```bash
hdc shell "param set <subsystem>.faultinject.<func>_<action> 0"   # 或 param delete
hdc shell "setenforce $ORIG"                                       # 按记录恢复
hdc shell "reboot"                                                 # 非持久参数重启即清
```
> 非持久参数重启自动清除；`persist.` 参数重启仍生效，不复位会跨重启持续注入，整机表现异常。

## 4. 通用代码注入模板（4 范式，强制 `#ifdef FAULT_INJECT_TEST` 包裹）

头文件与依赖：
```cpp
#include "parameters.h"   // OHOS::system::GetIntParameter / GetBoolParameter / SetParameter
// BUILD.gn: deps += [ "init:libbegetutil" ]
```
> **强制要求**：以下每段注入代码必须整体包在 `#ifdef FAULT_INJECT_TEST ... #endif` 内。release 构建不定义 `FAULT_INJECT_TEST` → 注入代码不编译、零开销、release 二进制不含注入符号（自检见第 5 节）。参数名默认非持久（无 `persist.` 前缀）。

### 范式 A：超时注入（配合 watchdog，触发 RECOVERY）
在已有 `XCollie::SetTimer(...)` 之后、业务逻辑之前插入：
```cpp
#ifdef FAULT_INJECT_TEST
    int fiSleepMs = OHOS::system::GetIntParameter<int>(
        "<sub>.faultinject.<func>_sleep_ms", 0, 0, 60000);
    if (fiSleepMs > 0) {
        // 单次消费：读后立即清零，防止 init 重拉后再次命中反复崩溃（critical 服务尤甚，见第 7 节）
        OHOS::system::SetParameter("<sub>.faultinject.<func>_sleep_ms", "0");
        LOGI("faultinject: sleep %{public}d ms", fiSleepMs);
        std::this_thread::sleep_for(std::chrono::milliseconds(fiSleepMs));
    }
#endif
```
watchdog 超时阈值（如 6s）< sleep 时长 → 触发 `XCOLLIE_FLAG_RECOVERY` 杀进程。**sleep 也可用于"错开时序"暴露竞态**（放在持锁/释放前后）。**注意**：RECOVERY 类（杀进程）注入**不得用 `persist.` 前缀**，且对 critical 进程须评估 panic 重启风险（Step 2 / 第 7 节）。

### 范式 B：错误码注入
```cpp
#ifdef FAULT_INJECT_TEST
    int injectErr = OHOS::system::GetIntParameter<int>(
        "<sub>.faultinject.<func>_err", ERR_OK, ERR_OK, INT_MAX);
    if (injectErr != ERR_OK) {
        LOGI("faultinject: return err %{public}d", injectErr);
        return injectErr;
    }
#endif
```
> 错误码注入不杀进程，是验证 `persist.` 跨重启语义的安全选择（见 eval-2 用例 2）。

### 范式 C：异常分支注入
```cpp
#ifdef FAULT_INJECT_TEST
    if (OHOS::system::GetBoolParameter(
            "<sub>.faultinject.<func>_branch", false)) {
        // 走异常/边界分支（空指针、越界、配置非法）
    }
#endif
```

### 范式 D：资源耗尽注入（优先确定性注入，压力法为辅）
```cpp
#ifdef FAULT_INJECT_TEST
    {   // held 在本作用域内持续占用，离开作用域 RAII 自动释放（不残留）
        int leakCount = OHOS::system::GetIntParameter<int>(
            "<sub>.faultinject.<func>_leak", 0, 0, 1024);   // 硬上限，按设备物理内存调整
        std::vector<std::unique_ptr<char[]>> held;
        if (leakCount > 0) {
            held.reserve(leakCount);
            for (int i = 0; i < leakCount; ++i) {
                std::unique_ptr<char[]> block(new (std::nothrow) char[1024 * 1024]);
                if (!block) {
                    LOGI("faultinject: alloc OOM at i=%{public}d", i);
                    break;
                }
                memset(block.get(), 0x5a, 1024 * 1024);   // 触发真实物理页提交，规避 overcommit 误判
                held.push_back(std::move(block));
            }
        }
        // ↓ 被施压的下游分配在此调用（held 仍持有内存，使其分配失败）
        // 离开作用域：held 自动释放，不残留
    }
#endif
```
> 范式 D 要点：
> - **优先确定性注入**：用可替换 allocator / failpoint 在目标分配点直接返回失败，不耗整机资源、不影响其他进程——这是首选
> - **压力法（次选）**：仅在隔离进程/cgroup + 硬上限 + RAII 回收时使用；**禁止在业务锁内执行**（持锁长占资源致死锁/线程耗尽，见第 7 节）
> - **throwing allocation 语义**：`std::make_shared` / `new` 分配失败**抛 `std::bad_alloc`**（禁异常构建下 `terminate`），**不会返回 nullptr**。既有代码中 `make_shared` 后的 nullptr 校验对 throwing 分配是死代码；要测 nullptr 分支须改用 `new (std::nothrow)`
> - `GetIntParameter` 带 min/max 边界校验，越界返回默认值

## 5. 输出形式：结构化手工测试用例集

skill 调用后，agent 交付**结构化手工测试用例集**（markdown），每用例按以下字段填写。执行/清理步骤以可复制的 bash 命令片段呈现（非 bat；OpenHarmony 开发以 Linux 主机 + hdc 为主）。注入点改源码、编译推送、触发接口、预期判断需人工，故用例化而非纯脚本。

### 用例字段（9 项）

| 字段 | 内容 |
|------|------|
| 用例ID | `FI-<子系统>-<函数>-<序号>`，如 `FI-account-Subscribe-001` |
| 标题 | 一句话描述故障场景 |
| 注入目标 | 函数名 + `file:line` + 故障类型（超时/错误码/分支/耗尽/竞争/降级） |
| 前置条件 | 记录原始 `getenforce` 状态、selinux 放行、编译推送 so（原子替换）、测试环境就绪 |
| 注入代码 | C++ 片段（`#ifdef FAULT_INJECT_TEST` 包裹）+ 插入位置（SetTimer 后/函数入口/分支前） |
| 参数注册 | `.para` 行 + `.para.dac` 行（非持久默认；仅跨重启语义用例才 `persist.`） |
| 执行步骤 | `param set` → 触发接口 → 观察命令（bash 片段） |
| 预期结果 | 进程行为 + 日志关键字 + 功能恢复判据 |
| 清理步骤 | `param set 0` + `setenforce <原始状态>` + `reboot` |

### 用例骨架（复制填写）

外层用四反引号 fence，避免与内层三反引号代码块冲突：

````markdown
### FI-<sub>-<func>-001  <场景一句话>
- 注入目标: <func> @ <file:line>, 故障类型=<超时/错误码/分支/耗尽/竞争/降级>
- 前置条件: 记录 getenforce; setenforce 0(或定向 allow); 已编译推送 <lib>.z.so(原子替换)
- 注入代码:
  ```cpp
  // @ 插入位置: <SetTimer后/函数入口/...>，#ifdef FAULT_INJECT_TEST 包裹
  <范式A/B/C/D 代码>
  ```
- 参数注册:
  - param/<sub>.para:    <sub>.faultinject.<func>_<action>=0
  - param/<sub>.para.dac: <sub>.faultinject.<func>_<action>="<uid>:<gid>:644"
- 执行步骤:
  1. hdc shell "param set <sub>.faultinject.<func>_<action> <值>"
  2. 触发 <func>（<测试用例/应用调用/hdc shell>）
  3. hdc shell "hilog | grep -E '<关键字>|XCOLLIE'"
  4. hdc shell "ps -ef | grep <进程名>"
- 预期结果:
  - <进程被杀/init重拉/错误码返回/分支命中/OOM降级/...>
  - 日志关键字: <...>
  - 功能恢复判据: <...>
- 清理步骤:
  - hdc shell "param set <sub>.faultinject.<func>_<action> 0"
  - hdc shell "setenforce <原始状态>"
  - hdc shell "reboot"
````

### 填好的样例（通用占位，watchdog 超时触发恢复）

````markdown
### FI-<sub>-<func>-001  watchdog 超时触发 critical 服务恢复
- 注入目标: `<Service>::<Method>` @ `<path/to/service>.cpp:<line>`, 故障类型=超时
- 前置条件: 记录 `getenforce`; `setenforce 0`(或定向 allow); 已编译推送 `<lib>.z.so`
- 注入代码: 范式A, @ SetTimer 之后、业务逻辑之前（`#ifdef FAULT_INJECT_TEST` 包裹，单次消费）
  （该函数已有 `flag = XCOLLIE_FLAG_LOG | XCOLLIE_FLAG_RECOVERY`、`SetTimer(name, <超时阈值s>, ...)`）
- 参数注册:
  - param/<sub>.para: `<sub>.faultinject.<func>_sleep_ms=0`
  - param/<sub>.para.dac: `<sub>.faultinject.<func>_sleep_ms="<uid>:<gid>:644"`
- 执行步骤:
  1. `hdc shell "param set <sub>.faultinject.<func>_sleep_ms <超阈值ms>"`
  2. 触发 `<Method>`（测试用例/应用调用/hdc shell 调 SA）
  3. `hdc shell "hilog | grep -E '<超时关键字>|XCOLLIE'"`
  4. `hdc shell "ps -ef | grep <进程名>"`
- 预期结果:
  - 超阈值后 watchdog 回调打印超时关键字
  - `XCOLLIE_FLAG_RECOVERY` 杀 <进程名>
  - init 按 `.cfg` 的 `critical:[1,N,T]` 重拉 <进程名>；注意 N 次内重复崩溃会触发 `ExecReboot("panic")` 整机重启——故本类注入用非持久参数 + 单次消费，不得跨重启持续命中
  - 功能恢复判据: <就绪参数/bootevent 重新 true>
- 清理步骤:
  - `hdc shell "param set <sub>.faultinject.<func>_sleep_ms 0"`
  - `hdc shell "setenforce <原始状态>"`
  - `hdc shell "reboot"`
````

### 产出后自检（validation）
交付用例前，agent 逐项核对，不全则补齐再交付：
- [ ] 9 个字段齐全（用例ID/标题/注入目标/前置条件/注入代码/参数注册/执行步骤/预期结果/清理步骤，每项均有内容）
- [ ] 注入代码默认值是 0/false，且整体被 `#ifdef FAULT_INJECT_TEST` 包裹
- [ ] 清理步骤含 `param set 0` + `setenforce <原始状态>` + `reboot` 三件套
- [ ] 参数名长度 < `PARAM_NAME_LEN_MAX`（当前 96，最大 95 字节）、前缀 `<sub>.faultinject.`；仅跨重启语义用例才 `persist.` 且不与 critical 崩溃点组合
- [ ] 前置条件记录了原始 `getenforce` 状态
- [ ] 预期结果有可观察判据（日志关键字 / 进程行为 / 恢复信号）
- [ ] release 隔离检查：注入符号不出现在 release 二进制（`nm`/`readelf` 查 `faultinject` 相关符号为空），区分"默认不触发"与"release 零开销、二进制不含注入面"

## 6. selinux 处理（首选定向 allow，setenforce 0 仅兜底）

```bash
ORIG=$(hdc shell getenforce)   # 记录原始状态
hdc shell "setenforce 0"        # 兜底，仅隔离开发设备
hdc shell "getenforce"          # Permissive
# 测试完按记录恢复（不无条件写 1，原始可能非 Enforcing）
hdc shell "setenforce $ORIG"
hdc shell "getenforce"          # 断言恢复
```

- 服务进程运行在各自 selinux 域（如 samgr / foundation / 各 SA 自有域），读新参数需对应 label 放行
- **首选**定向放行单参数：改 `.te` 用 `debug_only(allow ...)` + `parameter_contexts` 打 label（见 `references/paths.md`），生产态可关闭 `debug_only`
- `setenforce 0` 整体切 permissive，所有进程都能读新参数，最简但风险最大；**仅一次性隔离开发设备兜底用**
- **生产禁用**；任何中断路径（崩溃/OOM/连接中断）后也必须恢复，用 trap/finally 保证

## 7. 注意事项

| 项 | 要点 |
|----|------|
| 高频接口 | 绝不硬编码 sleep，必须参数开关默认 0；否则整机卡死 |
| 参数持久性 | 默认非持久（无 `persist.`），重启自动清除；`persist.` 仅跨重启语义用例，且**禁止与 critical 崩溃点组合** |
| panic 重启风险 | critical 服务（`.cfg` `critical:[1,N,T]`）在 N 次内重复崩溃，`startup_init` 的 `ServiceReap` 会 `ExecReboot("panic")` 整机重启。RECOVERY 类注入须用非持久参数 + 单次消费（读后 `SetParameter` 清 0），不得跨重启持续命中 critical 崩溃点 |
| 参数名 | 长度 < `PARAM_NAME_LEN_MAX`（当前 96，最大 95 字节），允许字母数字及 `.` `-` `@` `:` `_`；参数值约束按 fault 类型定义，不与参数名规则混写 |
| selinux | 首选定向 allow；`setenforce 0` 仅隔离开发设备兜底，生产禁用；记录原始状态并按记录恢复 |
| 推送替换 | 禁止先删再用库；临时路径 + 校验大小/哈希/权限 + 备份旧库 + 原子替换，失败回滚旧库且禁止重启 |
| watchdog flag | `XCOLLIE_FLAG_LOG` 只打日志，`XCOLLIE_FLAG_RECOVERY` 杀进程；注入前确认目标 flag（见 `references/paths.md` flag 速查表） |
| critical 服务 | 被杀后 init 按 `.cfg` `critical:[1,N,T]` 重拉，但**非无限重拉**——N 次内重复崩溃触发 panic 整机重启 |
| 注入代码 | 强制 `#ifdef FAULT_INJECT_TEST` 包裹全部模板；release 不定义该宏、不安装 `.para/.para.dac`，确保 release 零开销不含注入面 |
| DAC 权限 | `.para.dac` 用 644（owner 可写、其他只读），避免任意进程改参数 |
| 资源耗尽 | 优先确定性 allocator/failpoint 注入；压力法须隔离进程/cgroup + 硬上限 + RAII 回收，**禁止在业务锁内执行**；throwing allocation（`make_shared`/`new`）抛 `std::bad_alloc` 不返回 nullptr，测 nullptr 须用 `new (std::nothrow)` |

## 8. 参考文件

通用机制、API 路径、selinux 映射、watchdog flag 速查表详见 [`references/paths.md`](references/paths.md)（按需加载，节省主上下文）。
