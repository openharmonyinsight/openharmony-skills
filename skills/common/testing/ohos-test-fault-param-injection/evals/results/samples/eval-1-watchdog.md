# 故障注入手工测试用例集：watchdog 超时恢复链路验证

## 背景

**用户需求**：accountmgr（SA 200）的高频 IPC 接口注册了 watchdog，超时 6s 触发
`XCOLLIE_FLAG_RECOVERY` 杀进程；需验证"超时 → 杀进程 → init 重拉"恢复链路，
但该接口业务逻辑极快（微秒级返回），平时无法稳定复现超时。

**方案**：按 fault-inject-param skill 范式 A（超时注入），在 `SetTimer` 之后、业务逻辑
之前插入参数可控的 `sleep`。**参数默认非持久**（`account.faultinject.proc_sleep_ms`，无
`persist.` 前缀），重启自动清除；**读后立即 `SetParameter` 清零做单次消费**，防止 init
重拉后再次命中同一参数反复崩溃（accountmgr 是 critical 服务，N 次内重复崩溃会触发
`ExecReboot("panic")` 整机重启）。`param set` 一个 >6s 的值即可稳定触发 watchdog RECOVERY
杀进程，配合 `accountmgr.cfg` 的 `critical:[1,4,240]` 验证 init 重拉。

> **不使用 `persist.` 前缀**：RECOVERY 类（杀进程）注入 + `persist.` + critical 会跨重启
> 持续命中崩溃点 → 反复崩溃 → panic 整机重启循环。跨重启语义的持久化验证改用错误码类
> 注入（见 eval-2 用例 2，不杀进程，安全）。

**注入目标函数**：`OsAccountManagerService::GetOsAccountLocalIdFromProcess`
@ `services/accountmgr/src/osaccount/os_account_manager_service.cpp:817`
- 已有 watchdog：`SetTimer(TIMER_NAME, RECOVERY_TIMEOUT=6, ..., XCOLLIE_FLAG_LOG|XCOLLIE_FLAG_RECOVERY)` @ line 827-828
- 业务逻辑仅 `uid / UID_TRANSFORM_DIVISOR`（line 830-831，微秒级）→ 生产永不超时，正是"无法稳定复现"根因
- `CancelTimer` @ line 833

**环境事实**（已核实源码）：
- 进程名 `accountmgr`，库 `libaccountmgr.z.so`（`services/accountmgr/BUILD.gn:153 ohos_shared_library("accountmgr")`）
- `init:libbegetutil` 已在 `services/accountmgr/BUILD.gn:280` → `OHOS::system::GetIntParameter`/`SetParameter` 可用，无需新增依赖
- `accountmgr.cfg`：`"critical" : [1, 4, 240]`（init 240s 内最多重拉 4 次，**4 次内重复崩溃触发 panic 整机重启**）、`"uid":"account"`、`"secon":"u:r:accountmgr:s0"`
- `bootevent.account.ready` 为就绪信号
- 现有参数 DAC 格式参考 `param/account.para.dac`：`persist.account.login_name_max="account:account:644"`

**注入点**：`os_account_manager_service.cpp:829`（`#endif // HICOLLIE_ENABLE`）之后、
line 830（`const std::int32_t uid = ...`）之前 —— 即 `SetTimer` 之后、`CancelTimer` 之前。

**参数**：`account.faultinject.proc_sleep_ms`（func=`proc` 取自 GetOsAccountLocalIdFrom**Proc**ess）
- 后缀 `faultinject.proc_sleep_ms` = 25 字节 < `PARAM_NAME_LEN_MAX`（96）；默认 0；范围 [0, 60000]；值 >6000 即超 6s 阈值触发 RECOVERY；非持久，重启自动清除

> 同类可替换目标（同为 6s + RECOVERY，注入方式一致）：
> `SubscribeOsAccount` @ line 1491、`QueryActiveOsAccountIds` @ line 1859、
> `QueryOhosAccountInfo` @ `account_mgr_service.cpp:273`。

---

## 公共：注入代码与参数注册（4 个用例共用）

### 注入代码（范式 A：超时注入，`#ifdef FAULT_INJECT_TEST` 包裹 + 单次消费）

```cpp
// 头部新增 include（os_account_manager_service.cpp 顶部 include 区）
#include "parameters.h"   // OHOS::system::GetIntParameter / SetParameter; init:libbegetutil 已在 BUILD.gn:280
#include <thread>
#include <chrono>

// @ 插入位置: os_account_manager_service.cpp
//   第 829 行 "#endif // HICOLLIE_ENABLE" 之后、第 830 行 "const std::int32_t uid" 之前
//   （SetTimer 已注册 6s watchdog + RECOVERY flag；此处 sleep 超阈值即触发杀进程）
#ifdef FAULT_INJECT_TEST
    int fiSleepMs = OHOS::system::GetIntParameter<int>(
        "account.faultinject.proc_sleep_ms", 0, 0, 60000);
    if (fiSleepMs > 0) {
        // 单次消费：读后立即清零，防止 init 重拉后再次命中反复崩溃（critical 4 次内重复崩溃 → panic 整机重启）
        OHOS::system::SetParameter("account.faultinject.proc_sleep_ms", "0");
        ACCOUNT_LOGI("faultinject: GetOsAccountLocalIdFromProcess sleep %{public}d ms", fiSleepMs);
        std::this_thread::sleep_for(std::chrono::milliseconds(fiSleepMs));
    }
#endif
```

> 生产隔离：注入代码整体包在 `#ifdef FAULT_INJECT_TEST` 内，release 构建不定义该宏 → 不编译、零开销、release 不含注入符号。

### 参数注册

`services/accountmgr/param/account.para` 追加：
```
account.faultinject.proc_sleep_ms=0
```

`services/accountmgr/param/account.para.dac` 追加：
```
account.faultinject.proc_sleep_ms="account:account:644"
```

> `ohos_prebuilt_para` 模板自动包含同目录 `.para`/`.para.dac`，无需改 BUILD.gn。release 版不得安装这些文件。

### 编译推送（公共前置，原子替换 + 失败回滚）

```bash
# 编译 accountmgr（账号仓细节见 os-account-compile skill）
hb build accountmgr
# 推送：临时路径 + 校验 + 备份 + 原子替换（细节见 os-account-device-test skill）
hdc shell "mount -o rw,remount /"
hdc file send out/<product>/account/os_account/libaccountmgr.z.so /system/lib64/libaccountmgr.z.so.new
hdc shell "ls -l /system/lib64/libaccountmgr.z.so.new"          # 校验大小
hdc shell "sha256sum /system/lib64/libaccountmgr.z.so.new"      # 校验哈希
hdc shell "cp /system/lib64/libaccountmgr.z.so /system/lib64/libaccountmgr.z.so.bak"
hdc shell "mv -f /system/lib64/libaccountmgr.z.so.new /system/lib64/libaccountmgr.z.so"
hdc shell "reboot"
# 任一步失败：mv -f ...bak ...so 恢复旧库，禁止重启
```

### 触发方式说明

`GetOsAccountLocalIdFromProcess` 由调用方经 inner API `OsAccountManager::GetOsAccountLocalIdProcess()`
发起 IPC，账号子系统内部多处路径会调用它。可靠触发方式：
1. 跑 account 模块测试用例（如 `OsAccountManagerServiceModuleTest` 相关 case）；
2. 系统应用经 inner API 显式调用 `OsAccountManager::GetOsAccountLocalIdProcess()`；
3. `hdc shell "acm dump -a"` 等账号操作间接触发（概率较高但不保证命中目标方法）。

---

## 用例 1（核心）：注入超阈值 sleep 触发 RECOVERY 杀进程 + init 重拉

### FI-account-proc-001  watchdog 超时触发 critical 服务恢复

- 注入目标: `OsAccountManagerService::GetOsAccountLocalIdFromProcess`
  @ `services/accountmgr/src/osaccount/os_account_manager_service.cpp:817`, 故障类型=超时
- 前置条件:
  - 记录原始 selinux 状态：`ORIG=$(hdc shell getenforce)`；`hdc shell "setenforce 0"`；`hdc shell "getenforce"` 应显示 Permissive
  - 已按"公共"节注入代码、注册参数、编译推送 `libaccountmgr.z.so` 并重启就绪
  - `hdc shell "ps -ef | grep accountmgr"` 记录旧 PID
  - `hdc shell "param get bootevent.account.ready"` 应为 true
- 注入代码: 见"公共"节（范式 A，`#ifdef FAULT_INJECT_TEST` 包裹，单次消费，@ SetTimer 后 / 业务逻辑前）
- 参数注册: 见"公共"节
- 执行步骤:
  1. `hdc shell "param set account.faultinject.proc_sleep_ms 8000"`（8000ms > 6000ms 阈值）
  2. 触发 `GetOsAccountLocalIdFromProcess`（见上方"触发方式说明"，推荐跑一个 account 模块测试 case）
  3. `hdc shell "hilog | grep -E 'faultinject:|ProcGetOsAccountLocalIdFromProcess failed|watchDog|Get osaccount local id time out|XCOLLIE'"`
  4. `hdc shell "ps -ef | grep accountmgr"`（对比 PID 是否变化 = 被杀重拉）
  5. `hdc shell "param get account.faultinject.proc_sleep_ms"`（应已被单次消费清零为 0，重拉后不再重复崩溃）
  6. `hdc shell "param get bootevent.account.ready"`（重拉后应重新 true）
  7. `hdc shell "hisysevent -l -o ACCOUNT | grep -i watchDog"`（应有 watchDog 故障事件）
- 预期结果:
  - 进程行为: accountmgr 在 sleep 第 6s 被 `XCOLLIE_FLAG_RECOVERY` kill；init 按 `critical:[1,4,240]` 重拉，`ps` 出现新 PID
  - 单次消费生效: `param get` 显示已清零为 0；重拉后再次调用不会重复崩溃（避免 panic 风险）
  - 日志关键字: `faultinject: GetOsAccountLocalIdFromProcess sleep 8000 ms` → `ProcGetOsAccountLocalIdFromProcess failed, callingPid:...` → `Get osaccount local id time out` → `XCOLLIE` RECOVERY
  - 功能恢复判据: `bootevent.account.ready` 重新为 true；重拉后接口可正常响应（再次触发 `acm dump -a` 成功输出账号列表）
  - 注意: accountmgr 为 critical 服务，4 次内重复崩溃会触发 `ExecReboot("panic")` 整机重启——故本注入用非持久参数 + 单次消费，绝不与 `persist.` 组合
- 清理步骤:
  - `hdc shell "param set account.faultinject.proc_sleep_ms 0"`
  - `hdc shell "setenforce $ORIG"`（按记录恢复，不无条件写 1）
  - `hdc shell "reboot"`

---

## 用例 2（负向）：低于阈值 sleep 不触发杀进程（不误杀）

### FI-account-proc-002  低于阈值 sleep 不触发 RECOVERY

- 注入目标: `OsAccountManagerService::GetOsAccountLocalIdFromProcess`
  @ `services/accountmgr/src/osaccount/os_account_manager_service.cpp:817`, 故障类型=超时（负向）
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`；`getenforce` 应显示 Permissive
  - 已编译推送 `libaccountmgr.z.so`；确认 `account.faultinject.proc_sleep_ms` 已复位为 0
  - 记录当前 accountmgr PID
- 注入代码: 见"公共"节
- 参数注册: 见"公共"节
- 执行步骤:
  1. `hdc shell "param set account.faultinject.proc_sleep_ms 3000"`（3000ms < 6000ms 阈值）
  2. 触发 `GetOsAccountLocalIdFromProcess`（见"触发方式说明"）
  3. `hdc shell "hilog | grep -E 'faultinject:|XCOLLIE|ProcGetOsAccountLocalIdFromProcess failed|watchDog'"`
  4. `hdc shell "ps -ef | grep accountmgr"`（PID 应不变）
  5. 确认接口返回正常（`hdc shell "acm dump -a"` 正常输出账号列表）
- 预期结果:
  - 进程行为: sleep 3s 后 `CancelTimer` 正常取消定时器，进程不被杀；PID 不变
  - 日志关键字: 仅出现 `faultinject: ... sleep 3000 ms`；不出现 `ProcGetOsAccountLocalIdFromProcess failed` / `XCOLLIE` RECOVERY / `watchDog`
  - 功能恢复判据: 接口正常返回，accountmgr 持续存活
- 清理步骤:
  - `hdc shell "param set account.faultinject.proc_sleep_ms 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

## 用例 3（边界）：阈值临界值精确性

### FI-account-proc-003  阈值边界：6100ms 杀 / 5900ms 不杀

- 注入目标: `OsAccountManagerService::GetOsAccountLocalIdFromProcess`
  @ `services/accountmgr/src/osaccount/os_account_manager_service.cpp:817`, 故障类型=超时（边界）
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`；`getenforce` 应显示 Permissive
  - 已编译推送 `libaccountmgr.z.so`；每轮执行前确认参数已复位为 0、accountmgr 存活
- 注入代码: 见"公共"节
- 参数注册: 见"公共"节
- 执行步骤:
  1. `hdc shell "param set account.faultinject.proc_sleep_ms 6100"`（略超阈值）
  2. 触发 `GetOsAccountLocalIdFromProcess`（见"触发方式说明"）
  3. `hdc shell "hilog | grep -E 'faultinject:|XCOLLIE|ProcGetOsAccountLocalIdFromProcess failed|watchDog'"`
  4. `hdc shell "ps -ef | grep accountmgr"`（预期 PID 变化 = 被杀重拉）
  5. 等 init 重拉就绪后复位：`hdc shell "param set account.faultinject.proc_sleep_ms 0"`
  6. `hdc shell "param set account.faultinject.proc_sleep_ms 5900"`（略低于阈值）
  7. 再次触发 `GetOsAccountLocalIdFromProcess`（见"触发方式说明"）
  8. `hdc shell "hilog | grep -E 'faultinject:|XCOLLIE|ProcGetOsAccountLocalIdFromProcess failed|watchDog'"`
  9. `hdc shell "ps -ef | grep accountmgr"`（预期 PID 不变）
- 预期结果:
  - 6100ms 轮: sleep 超过 6s 阈值 → `XCOLLIE_FLAG_RECOVERY` 杀进程，PID 变化，出现 `ProcGetOsAccountLocalIdFromProcess failed` + `XCOLLIE` RECOVERY + `watchDog`
  - 5900ms 轮: sleep 未超阈值 → `CancelTimer` 正常取消，进程存活，PID 不变，不出现 RECOVERY/watchDog 日志
  - 边界判据: 阈值两侧行为明确翻转，确认 6000ms 为精确触发点
- 清理步骤:
  - `hdc shell "param set account.faultinject.proc_sleep_ms 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

## 用例 4（生产安全）：参数默认 0 生产路径不受影响

### FI-account-proc-004  默认参数 0 不注入、生产路径零影响

- 注入目标: `OsAccountManagerService::GetOsAccountLocalIdFromProcess`
  @ `services/accountmgr/src/osaccount/os_account_manager_service.cpp:817`, 故障类型=超时（生产安全验证）
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`；`getenforce` 应显示 Permissive
  - 已编译推送含注入代码的 `libaccountmgr.z.so`；参数为默认值 0（未执行过 param set，或已 `param set ... 0`）
  - release 构建验证：确认 `libaccountmgr.z.so` 的 release 版本不含 `faultinject` 符号（`nm`/`readelf` 查为空）
- 注入代码: 见"公共"节（默认 0 → `fiSleepMs=0` → 跳过 sleep）
- 参数注册: 见"公共"节（`.para` 默认 `=0`）
- 执行步骤:
  1. `hdc shell "param get account.faultinject.proc_sleep_ms"`（应为 0）
  2. 连续触发 `GetOsAccountLocalIdFromProcess` 多次（`hdc shell "acm dump -a"` 连续 5 次）
  3. `hdc shell "hilog | grep -E 'faultinject:|XCOLLIE|ProcGetOsAccountLocalIdFromProcess failed|watchDog'"`
  4. `hdc shell "ps -ef | grep accountmgr"`（PID 不变）
  5. 计时 `hdc shell "acm dump -a"` 响应耗时（应与无注入代码版本一致，毫秒级）
  6. `nm libaccountmgr.z.so | grep -i faultinject`（release 版应为空，证明零开销不含注入面）
- 预期结果:
  - 进程行为: 参数=0 → 不 sleep → 业务逻辑瞬间返回；进程持续存活，PID 不变
  - 日志关键字: 不出现任何 `faultinject:` / `XCOLLIE` RECOVERY / `watchDog` 日志
  - 功能恢复判据: 接口响应耗时与未注入版本无差异（生产零影响）
  - release 隔离判据: release 二进制不含 `faultinject` 符号，区分"默认不触发"与"release 零开销不含注入面"
- 清理步骤:
  - 参数已为 0，无需复位
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

## 产出后自检清单

- [x] 9 个字段齐全：每用例含 用例ID / 标题 / 注入目标 / 前置条件 / 注入代码 / 参数注册 / 执行步骤 / 预期结果 / 清理步骤（注入代码与参数注册提取为"公共"节，各用例引用，确保每项有内容）
- [x] 注入代码默认值是 0 且 `#ifdef FAULT_INJECT_TEST` 包裹：`GetIntParameter("...", 0, 0, 60000)`，默认 0 → 跳过 sleep，生产零影响（用例 4 验证）
- [x] 清理步骤含 `param set 0` + `setenforce 按记录恢复` + `reboot` 三件套（每用例均有）
- [x] 参数名 < `PARAM_NAME_LEN_MAX`（96）、前缀 `account.faultinject.`：`account.faultinject.proc_sleep_ms` 后缀 `faultinject.proc_sleep_ms` = 25 字节；非持久（无 `persist.`），RECOVERY 类不与 persist 组合
- [x] 前置条件记录原始 `getenforce` 状态（每用例均有，并要求 `getenforce` 验证 Permissive）
- [x] 预期结果有可观察判据：日志关键字（`ProcGetOsAccountLocalIdFromProcess failed` / `XCOLLIE` / `watchDog` / `Get osaccount local id time out`）+ 进程行为（PID 变化 = 被杀重拉）+ 恢复信号（`bootevent.account.ready` 重新 true）
- [x] release 隔离检查：注入代码 `#ifdef FAULT_INJECT_TEST` 包裹，release 不定义该宏 → release 二进制不含 `faultinject` 符号（用例 4 验证）
- [x] 单次消费：RECOVERY 类读后 `SetParameter` 清 0，避免 init 重拉后反复崩溃触发 panic（用例 1 验证）
