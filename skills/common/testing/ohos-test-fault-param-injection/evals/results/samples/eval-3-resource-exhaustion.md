# 基于系统参数的故障注入手工测试用例集 — OOM 保护降级验证

> 方法来源：`fault-inject-param` skill 第 5 节（用例字段表 + 骨架 + 产出后自检清单）+ 第 4 节范式 D。
> 故障类型：**资源耗尽**（范式 D）。
> 目标服务：OS Account 子系统 SA 200（`accountmgr`）。
>
> **背景**：OS Account 服务在真实内存耗尽场景下应走 OOM 保护降级（返回错误码 + 清理中间态，而非崩溃或写出脏数据）。但整机低内存环境难造且不稳定，故用系统参数控制注入"多少 1MB 内存占用"，把目标函数运行时的可用内存压低到分配失败，从而稳定、可量化地验证 OOM 保护降级路径。参数默认 0、`#ifdef FAULT_INJECT_TEST` 包裹、生产零开销；测试完务必复位。
>
> **本样本的关键约束（回应检视）**：
> 1. **RAII 回收**：用 `std::vector<std::unique_ptr<char[]>>` 持有分配块，作用域结束自动释放，不丢失指针、不残留。
> 2. **硬上限**：`GetIntParameter(key, 0, 0, 1024)` 第 4 参数限 1024 块（≤1GB），按设备物理内存调整，禁止无上限耗尽整机资源。
> 3. **不在业务锁内执行**：压力分配循环（`malloc`+`memset`）放在 `createOsAccountMutex_`/`subscribeRecordMutex_` 等 `lock_guard` **之前**；held 缓冲区仅以指针形式带入锁内，不持锁做慢分配。
> 4. **throwing allocation 语义正确**：`std::make_shared`/`new` 失败**抛 `std::bad_alloc`**（禁异常构建下 `terminate`），**不返回 nullptr**；既有 `make_shared` 后的 nullptr 校验对 throwing 分配是死代码。要测 nullptr 分支须改用 `new (std::nothrow)`（见用例 3）。

---

## 公共依赖与约定

- 注入代码统一使用范式 D（资源耗尽），`OHOS::system::GetIntParameter<int>` 读参，默认 0，`#ifdef FAULT_INJECT_TEST` 包裹。
- 头文件：`#include "parameters.h"`（`OHOS::system::GetIntParameter`）；BUILD.gn 依赖 `init:libbegetutil`（accountmgr 已有该依赖，因已使用 `bootevent.account.ready` 参数）。
- 日志宏：`ACCOUNT_LOGI`（各目标文件已 include `account_log_wrapper.h`）。
- RAII：`#include <memory>` + `#include <vector>`（`std::unique_ptr` / `std::vector`）。
- 参数命名前缀：`account.faultinject.<func>_leak`（**非持久默认**，重启自动清除）；后缀长度 < `PARAM_NAME_LEN_MAX`（96）；DAC 统一 `account:account:644`（沿用仓内 `services/accountmgr/param/account.para.dac` 既有约定）。
- 上限语义：`GetIntParameter(key, default, min, max)` 中第 4 参数为单次最大块数；测试值按设备物理内存调整（1–2GB 设备建议 512–1024 块 = 512MB–1GB），**不得超 1024**。
- 压力分配用 `new (std::nothrow) char[1024*1024]`（nothrow 版本返回 nullptr 而非抛异常，便于在注入点检测失败并 break）；`memset` 触发真实物理页提交以规避 overcommit 误判。
- leak 缓冲区**故意持有至作用域结束**以构造低内存窗口；离开作用域 RAII 自动释放，**不残留**——故无需依赖 reboot 清理（但参数仍复位）。

---

### FI-account-CreateOsAccount-001  内存耗尽下创建 OS 账户应走 OOM 保护降级（错误码返回 + 中间态清理，不崩溃不脏写）

- 注入目标: `IInnerOsAccountManager::CreateOsAccount` @ `services/accountmgr/src/osaccount/inner_os_account_manager.cpp:907`, 故障类型=耗尽
  - 锚点：**函数入口（line 908，`createOsAccountMutex_` 持锁前）**、`CheckAndCleanOsAccounts` 早返校验后（line 918–920）、`PrepareOsAccountInfo` 调用前（line 922）。leak 把可用内存压低，使 `PrepareOsAccountInfo` / `SendMsgForAccountCreate` 内部分配失败，验证其 OOM 保护路径：返回 errCode + `RemoveLocalIdToOperating` 清理（line 924、928），而非崩溃。
  - **压力分配在锁外**：`held` 的构造（`malloc`+`memset` 循环）在 `createOsAccountMutex_` 持锁**之前**完成；`held` 仅以指针形式带入锁内，锁内不做慢分配。
- 前置条件:
  - 记录原始 selinux 状态：`ORIG=$(hdc shell getenforce)`；`hdc shell "setenforce 0"`（accountmgr 域读新参数需放行；首选定向 allow，setenforce 0 仅兜底）
  - 已编译并推送 `libaccountmgr.z.so`（含注入代码，临时路径 + 校验 + 备份 + 原子替换 + reboot）
  - 设备可用内存 ≥512MB（保证 leak 值可压到低内存）
  - ACM 可用：`hdc shell "acm dump -a"` 正常
- 注入代码: 范式D, `#ifdef FAULT_INJECT_TEST` 包裹, @ `inner_os_account_manager.cpp:908`（函数入口、`createOsAccountMutex_` 持锁前）
  ```cpp
  // === faultinject: OOM 保护降级验证（CreateOsAccount）===
  // 头部 include: #include "parameters.h"  #include <memory>  #include <vector>
  // @ 插入位置: CreateOsAccount 函数入口、createOsAccountMutex_ lock_guard 之前
  #ifdef FAULT_INJECT_TEST
      std::vector<std::unique_ptr<char[]>> fiHeld;   // RAII：作用域结束自动释放，不残留
      {
          int leakCount = OHOS::system::GetIntParameter<int>(
              "account.faultinject.createacct_leak", 0, 0, 1024);   // 硬上限 1024 块
          if (leakCount > 0) {
              ACCOUNT_LOGI("faultinject: leak %{public}d * 1MB before CreateOsAccount prepare", leakCount);
              fiHeld.reserve(leakCount);
              for (int i = 0; i < leakCount; ++i) {
                  std::unique_ptr<char[]> block(new (std::nothrow) char[1024 * 1024]);
                  if (!block) {
                      ACCOUNT_LOGI("faultinject: alloc OOM at i=%{public}d", i);
                      break;
                  }
                  memset(block.get(), 0x5a, 1024 * 1024);  // 真实物理页提交，规避 overcommit 误判
                  fiHeld.push_back(std::move(block));
              }
          }
      }
      // fiHeld 在本作用域内持续占用内存，使下游 PrepareOsAccountInfo 内部分配失败
      // 离开 CreateOsAccount 作用域：fiHeld 自动释放，不残留
  #endif
  // === faultinject end ===
  ErrCode errCode = PrepareOsAccountInfo(name, type, domainInfo, osAccountInfo);
  ```
  > 注意：`fiHeld` 声明在函数入口（锁外），其构造循环在锁外完成；后续 `createOsAccountMutex_` 持锁段内仅持有 `fiHeld` 指针，**不在锁内做慢分配**。
- 参数注册:
  - `services/accountmgr/param/account.para`: `account.faultinject.createacct_leak=0`
  - `services/accountmgr/param/account.para.dac`: `account.faultinject.createacct_leak="account:account:644"`
- 执行步骤:
  1. `hdc shell "param set account.faultinject.createacct_leak 512"`  （1–2GB 设备；若未触发分配失败则上调到 768/1024，**不得超 1024**）
  2. 触发 `CreateOsAccount`：`hdc shell "acm create -n fi_oom_test -t normal"`
  3. `hdc shell "hilog | grep -E 'faultinject|CreateOsAccount|PrepareOsAccountInfo|OPERATION_CREATE'"`
  4. `hdc shell "ps -ef | grep accountmgr"`  （验证服务未崩溃）
  5. `hdc shell "acm dump -a"`  （验证无名为 fi_oom_test 的半成品账号残留）
- 预期结果:
  - accountmgr 进程存活（`ps` 仍可见 accountmgr PID，未被 OOM killer 杀掉；若被杀则 init 按 `.cfg` critical 重拉，但**预期走降级**而非被杀）
  - `acm create` 返回非 0 错误码（OOM 保护降级生效），不产生新账号
  - 日志关键字：先见 `faultinject: leak 512 * 1MB`、可能见 `faultinject: alloc OOM at i=...`；继而见 `CreateOsAccount`/`PrepareOsAccountInfo` 失败日志与 `RemoveLocalIdToOperating` 清理路径
  - 功能恢复判据：`acm dump -a` 不存在 `fi_oom_test` 账号（无脏数据/半成品）；`fiHeld` 离开作用域已 RAII 释放，复位参数后 `acm create -n normal_test -t normal` 可成功
- 清理步骤:
  - `hdc shell "param set account.faultinject.createacct_leak 0"`
  - `hdc shell "setenforce $ORIG"`（按记录恢复）
  - `hdc shell "reboot"`

---

### FI-account-AddAppAccount-001  内存耗尽下添加应用账号应走 OOM 保护降级（错误码返回 + 数据存储一致，不脏写不崩溃）

- 注入目标: `InnerAppAccountManager::AddAccount` @ `services/accountmgr/src/appaccount/inner_app_account_manager.cpp:43`, 故障类型=耗尽
  - 锚点：**函数入口（line 45，无业务锁）**、`AppAccountInfo` 构造（line 46）与向 `controlManager_.AddAccount`（line 48，含数据存储/KV 写入）委派之前。leak 压低可用内存，使下游 `AppAccountControlManager::AddAccount`（`app_account_control_manager.cpp:240`）内 `AppAccountInfo` 分配 / `AppAccountDataStorage` 写入失败，验证 OOM 保护：返回 `ERR_APPACCOUNT_*` 错误码且**不产生半条账号、不破坏既有存储一致性**。
  - AddAccount 入口本身不持业务锁，压力分配在入口完成，`fiHeld` 跨下游调用持续占用直至函数返回 RAII 释放。
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`
  - 已编译并推送 `libaccountmgr.z.so`（含注入代码，临时路径 + 校验 + 备份 + 原子替换 + reboot）
  - 存在可触发 `addAccount` 的测试应用或模块测试套件已编译推送
  - 设备可用内存 ≥512MB
- 注入代码: 范式D, `#ifdef FAULT_INJECT_TEST` 包裹, @ `inner_app_account_manager.cpp:45`（函数入口、`AppAccountInfo` 构造前）
  ```cpp
  ErrCode InnerAppAccountManager::AddAccount(const std::string &name, const std::string &extraInfo,
      const uid_t &uid, const std::string &bundleName, const uint32_t &appIndex)
  {
      // === faultinject: OOM 保护降级验证（AddAccount）===
      // 头部 include: #include "parameters.h"  #include <memory>  #include <vector>
      #ifdef FAULT_INJECT_TEST
          std::vector<std::unique_ptr<char[]>> fiHeld;
          {
              int leakCount = OHOS::system::GetIntParameter<int>(
                  "account.faultinject.addappacct_leak", 0, 0, 1024);
              if (leakCount > 0) {
                  ACCOUNT_LOGI("faultinject: leak %{public}d * 1MB before AddAccount", leakCount);
                  fiHeld.reserve(leakCount);
                  for (int i = 0; i < leakCount; ++i) {
                      std::unique_ptr<char[]> block(new (std::nothrow) char[1024 * 1024]);
                      if (!block) {
                          ACCOUNT_LOGI("faultinject: alloc OOM at i=%{public}d", i);
                          break;
                      }
                      memset(block.get(), 0x5a, 1024 * 1024);
                      fiHeld.push_back(std::move(block));
                  }
              }
          }
          // fiHeld 持续占用至函数返回（跨下游 controlManager_.AddAccount），返回时 RAII 释放
      #endif
      // === faultinject end ===
      AppAccountInfo appAccountInfo(name, bundleName);
      appAccountInfo.SetAppIndex(appIndex);
      return controlManager_.AddAccount(name, extraInfo, uid, bundleName, appAccountInfo);
  }
  ```
- 参数注册:
  - `services/accountmgr/param/account.para`: `account.faultinject.addappacct_leak=0`
  - `services/accountmgr/param/account.para.dac`: `account.faultinject.addappacct_leak="account:account:644"`
- 执行步骤:
  1. `hdc shell "param set account.faultinject.addappacct_leak 768"`  （1–2GB 设备；无分配失败则上调到 1024，**不得超 1024**）
  2. 触发 `AddAccount`（二选一）：
     - 主机跑覆盖 AddAccount 的模块测试：`cd {OpenHarmonyRootFolder}/test/testfwk/developer_test && ./start.sh run -p rk3568 -t MST -tp os_account -ts AppAccountManagerServiceModuleTest`
     - 或推送测试应用，调用 `appAccount.addAccount('fi_oom_app','extra')`
  3. `hdc shell "hilog | grep -E 'faultinject|AddAccount|AppAccountControl|APP_ACCOUNT_FAILED'"`
  4. `hdc shell "ps -ef | grep accountmgr"`
  5. `hdc shell "hisysevent -l -o ACCOUNT | grep APP_ACCOUNT_FAILED"`  （验证有失败事件但服务未崩）
- 预期结果:
  - accountmgr 进程存活（`ps` 仍可见），未被 OOM killer 杀掉
  - `AddAccount` 返回非 0 错误码（OOM 保护降级生效，不抛异常不崩溃）
  - 数据存储一致：用同名账号再次正常 add（复位后）应成功，说明未残留半条 `fi_oom_app` 账号
  - 日志关键字：先见 `faultinject: leak 768 * 1MB`、可能见 `faultinject: alloc OOM at i=...`；继而见 `AddAccount`/`AppAccountControl` 失败日志或 `APP_ACCOUNT_FAILED` 事件
  - 功能恢复判据：`fiHeld` RAII 释放 + 参数复位后，正常 `addAccount` 调用返回 `ERR_OK`，且既有账号数据无丢失/错乱
- 清理步骤:
  - `hdc shell "param set account.faultinject.addappacct_leak 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

### FI-account-SubscribeOsAccount-001  内存耗尽下订阅 OS 账号事件应走 OOM 保护降级（make_shared 抛 bad_alloc → 异常处理路径，不崩溃）

- 注入目标: `OsAccountSubscribeManager::SubscribeOsAccount` @ `services/accountmgr/src/osaccount/os_account_subscribe_manager.cpp:138`, 故障类型=耗尽
  - 锚点：两处 nullptr 入参校验后（line 141–149）、**`subscribeRecordMutex_` 持锁前**、`std::make_shared<OsSubscribeRecord>`（line 168）之前。leak 压低可用内存，使 line 168 `make_shared` **抛 `std::bad_alloc`**（`make_shared` 分配失败抛异常，**不返回 nullptr**），验证 OOM 保护路径。
  - **语义修正**：既有代码 line 169–171 若是 `if (subscribeRecord == nullptr)` 校验——对 throwing 的 `make_shared` 是**死代码**（`make_shared` 失败抛异常，永远不会到 nullptr 校验）。本用例验证的是 **`std::bad_alloc` 异常处理路径**：若既有代码未 try/catch 则 `terminate`（这正是要发现的缺陷，需补 try/catch 或改 `new(std::nothrow)`）；要测 nullptr 分支须将 `make_shared` 改为 `new(std::nothrow)` + 显式构造。
  - 压力分配在 `subscribeRecordMutex_` 持锁**之前**完成。
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`
  - 已编译并推送 `libaccountmgr.z.so`（含注入代码，临时路径 + 校验 + 备份 + 原子替换 + reboot）
  - 存在可触发 `SubscribeOsAccount` 的测试应用或模块测试套件已编译推送
  - 设备可用内存 ≥512MB
- 注入代码: 范式D, `#ifdef FAULT_INJECT_TEST` 包裹, @ `os_account_subscribe_manager.cpp:149`（两处 nullptr 校验后、`subscribeRecordMutex_` 持锁与 `make_shared` 前）
  ```cpp
      if (eventListener == nullptr) {
          ACCOUNT_LOGE("EventListener is nullptr");
          return ERR_ACCOUNT_COMMON_NULL_PTR_ERROR;
      }
      // === faultinject: OOM 保护降级验证（SubscribeOsAccount）===
      // 头部 include: #include "parameters.h"  #include <memory>  #include <vector>
      #ifdef FAULT_INJECT_TEST
          std::vector<std::unique_ptr<char[]>> fiHeld;
          {
              int leakCount = OHOS::system::GetIntParameter<int>(
                  "account.faultinject.subosacct_leak", 0, 0, 1024);
              if (leakCount > 0) {
                  ACCOUNT_LOGI("faultinject: leak %{public}d * 1MB before SubscribeOsAccount make_shared", leakCount);
                  fiHeld.reserve(leakCount);
                  for (int i = 0; i < leakCount; ++i) {
                      std::unique_ptr<char[]> block(new (std::nothrow) char[1024 * 1024]);
                      if (!block) {
                          ACCOUNT_LOGI("faultinject: alloc OOM at i=%{public}d", i);
                          break;
                      }
                      memset(block.get(), 0x5a, 1024 * 1024);
                      fiHeld.push_back(std::move(block));
                  }
              }
          }
          // fiHeld 持续占用至本作用域结束，使下游 make_shared 抛 std::bad_alloc
      #endif
      // === faultinject end ===
      std::lock_guard<std::mutex> lock(subscribeRecordMutex_);
      // ↓ line 168: std::make_shared<OsSubscribeRecord>(...) — 内存不足时抛 std::bad_alloc（不返回 nullptr）
  ```
- 参数注册:
  - `services/accountmgr/param/account.para`: `account.faultinject.subosacct_leak=0`
  - `services/accountmgr/param/account.para.dac`: `account.faultinject.subosacct_leak="account:account:644"`
- 执行步骤:
  1. `hdc shell "param set account.faultinject.subosacct_leak 1024"`  （订阅对象较小，需更激进压内存；**不得超 1024**）
  2. 触发 `SubscribeOsAccount`（二选一）：
     - 主机跑覆盖 Subscribe 的模块测试：`cd {OpenHarmonyRootFolder}/test/testfwk/developer_test && ./start.sh run -p rk3568 -t MST -tp os_account -ts OsAccountManagerServiceModuleTest`
     - 或推送测试应用，调用 `osAccount.on('activate' | 'stopping', ...)` 订阅
  3. `hdc shell "hilog | grep -E 'faultinject|SubscribeOsAccount|SubscribeRecordPtr is nullptr|bad_alloc|terminate'"`
  4. `hdc shell "ps -ef | grep accountmgr"`
  5. `hdc shell "hidumper -s AccountMgrService"`  （验证订阅记录表无脏条目）
- 预期结果:
  - accountmgr 进程存活（`ps` 仍可见），未被 OOM killer 杀掉
  - 若既有代码对 `make_shared` 有 try/catch `std::bad_alloc`：捕获异常并返回 `ERR_ACCOUNT_COMMON_NULL_PTR_ERROR`（或等价错误码），**不崩溃**
  - 若既有代码未捕获 `std::bad_alloc`：进程 `terminate`——**这是本用例要发现的缺陷**，修复方式：补 try/catch 处理 `std::bad_alloc`，或改用 `new(std::nothrow)` 显式构造再测 nullptr 分支
  - 日志关键字：先见 `faultinject: leak 1024 * 1MB`、可能见 `faultinject: alloc OOM at i=...`；继而见 `bad_alloc`/`terminate`（缺陷暴露）或 `SubscribeRecordPtr is nullptr`（若已改 nothrow）
  - `subscribeRecords_` 一致性判据：`hidumper` 订阅记录表未新增脏条目；`fiHeld` RAII 释放 + 参数复位后正常订阅应返回 `ERR_OK` 并收到账号状态事件
- 清理步骤:
  - `hdc shell "param set account.faultinject.subosacct_leak 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

## 产出后自检（validation）

逐项核对结果：

- [x] 9 个字段齐全：每用例均含 用例ID / 标题 / 注入目标 / 前置条件 / 注入代码 / 参数注册 / 执行步骤 / 预期结果 / 清理步骤（每项均有内容）
- [x] 注入代码默认值是 0 且 `#ifdef FAULT_INJECT_TEST` 包裹：三处 `GetIntParameter<int>(..., 0, 0, 1024)` 默认 0，`leakCount > 0` 才注入，生产路径零开销；release 不定义宏 → 不含注入符号
- [x] 清理步骤含三件套：每用例末尾均含 `param set <param> 0` + `setenforce 按记录恢复` + `reboot`
- [x] 参数名前缀 `account.faultinject.` 且长度 < 96：`account.faultinject.createacct_leak`(34)、`account.faultinject.addappacct_leak`(34)、`account.faultinject.subosacct_leak`(33) 均合规；非持久（无 `persist.`）；DAC 沿用 `account:account:644` 约定
- [x] 前置条件记录原始 `getenforce` 状态：三用例均含
- [x] 预期结果有可观察判据：每用例均给出 进程行为（accountmgr 存活）+ 日志关键字（`faultinject: leak` / `alloc OOM` / 各自下游失败关键字）+ 功能恢复判据（`fiHeld` RAII 释放 + 复位后正常调用恢复）
- [x] RAII 回收：用 `std::vector<std::unique_ptr<char[]>>` 持有，作用域结束自动释放，不丢失指针、不残留
- [x] 硬上限：`GetIntParameter` 第 4 参数限 1024 块（≤1GB），不无上限耗尽整机资源
- [x] 不在业务锁内执行：压力分配循环在 `createOsAccountMutex_`/`subscribeRecordMutex_` 持锁**之前**完成
- [x] throwing allocation 语义正确：`make_shared` 失败抛 `std::bad_alloc`（不返回 nullptr），用例 3 验证异常处理路径并指明测 nullptr 须用 `new(std::nothrow)`
- [x] release 隔离检查：注入代码 `#ifdef FAULT_INJECT_TEST` 包裹，release 不定义该宏 → release 二进制不含 `faultinject` 符号

补充说明：
- 注入点均位于业务锁外（压力分配在锁前完成，held 仅以指针带入锁内），不修改任何 SA 启动/首用户路径、不改持久化 schema、不改公开 API/错误码值、不弱化权限检查（符合 root/模块 AGENTS.md §3.1 Do-not 与 Pitfall 1/2/5/6）。
- `fiHeld` RAII 释放，离开作用域即回收，故无需依赖 reboot 清理内存；参数仍复位为 0，非持久参数重启自动清除。
- `setenforce 0` 仅开发态兜底，生产禁用；首选定向 `debug_only(allow ...)`。
