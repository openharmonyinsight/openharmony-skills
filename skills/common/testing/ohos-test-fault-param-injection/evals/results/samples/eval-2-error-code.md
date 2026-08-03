# 故障注入手工测试用例集 — SA 接口错误码 20900001 注入（验证调用方降级处理）

> 基于 `fault-inject-param` skill 第 5 节方法产出。注入方式：**范式 B（错误码注入）**。
> 场景说明：错误码 `20900001` 在正常路径下根本不会出现（不属于 os_account 错误空间，账号仓错误码基址从 `4194304` 起），调用方却为它预留了降级分支，长期无验证、易带病上线。通过系统参数在 SA 接口返回前强行注入 `20900001`，可稳定复现并验证调用方的降级/兜底逻辑。
> 默认值 `0`（`ERR_OK`）保证生产路径零影响；**参数默认非持久**（无 `persist.` 前缀），重启自动清除；**跨重启语义验证用 `persist.` 前缀（用例 2）**——错误码注入不杀进程，不与 critical 崩溃点组合，安全。

---

## 用例字段对照（按 skill 第 5 节用例字段表，9 项）

| 字段 | 内容 |
|------|------|
| 用例ID | `FI-<子系统>-<函数>-<序号>` |
| 标题 | 一句话描述故障场景 |
| 注入目标 | 函数名 + `file:line` + 故障类型 |
| 前置条件 | 记录 `getenforce`、selinux 放行、编译推送 so（原子替换）、测试环境就绪 |
| 注入代码 | C++ 片段（范式 B，`#ifdef FAULT_INJECT_TEST` 包裹）+ 插入位置 |
| 参数注册 | `.para` 行 + `.para.dac` 行（非持久默认） |
| 执行步骤 | `param set` → 触发接口 → 观察命令（bash 片段） |
| 预期结果 | 进程行为 + 日志关键字 + 功能恢复判据 |
| 清理步骤 | `param set 0` + `setenforce 按记录恢复` + `reboot` |

---

## 用例清单

| 用例ID | 标题 | 故障类型 | 参数持久性 |
|--------|------|----------|-----------|
| FI-sa-query-001 | 注入错误码 20900001，验证调用方触发降级/兜底分支 | 错误码 | 非持久 |
| FI-sa-query-002 | persist 持久注入 20900001 跨重启，验证降级稳定与复位恢复（非崩溃型，安全） | 错误码/降级 | persist（跨重启语义） |
| FI-sa-query-003 | 注入值=0（不注入）对照组，证明生产路径不受污染 | 错误码（基线） | 非持久 |

---

## 详细用例

### FI-sa-query-001  注入错误码 20900001，验证调用方触发降级/兜底分支

- 注入目标: `TargetSaStub::Query()` @ `services/<sa>/src/<sa>_service.cpp:<line>`, 故障类型=错误码
- 前置条件:
  - 记录原始 selinux 状态：`ORIG=$(hdc shell getenforce)`；`hdc shell "setenforce 0"`（关 selinux，否则 SA 进程读新参数 AVC denied）
  - `hdc shell "getenforce"` 应显示 `Permissive`
  - 已按范式 B 改源码并编译推送 `<sa_lib>.z.so`（临时路径 + 校验 + 备份 + 原子替换）
  - 调用方（系统应用 / 上游 SA）已就绪，调用方降级分支含可观察日志埋点
- 注入代码: 范式 B，`#ifdef FAULT_INJECT_TEST` 包裹，@ SA 接口 stub 实现入口处、参数校验之后、业务逻辑之前
  ```cpp
  #include "parameters.h"   // OHOS::system::GetIntParameter
  // BUILD.gn: deps += [ "init:libbegetutil" ]

  // @ 插入位置: TargetSaStub::Query(...) 入口、入参校验之后、真实业务逻辑之前
  #ifdef FAULT_INJECT_TEST
      int injectErr = OHOS::system::GetIntParameter<int>(
          "sa.faultinject.query_err", 0, 0, INT_MAX);
      if (injectErr != 0) {
          LOGI("faultinject: query return err %{public}d", injectErr);
          return injectErr;   // 直接返回 20900001，跳过正常业务逻辑
      }
  #endif
  ```
- 参数注册:
  - `param/sa.para`:    `sa.faultinject.query_err=0`
  - `param/sa.para.dac`: `sa.faultinject.query_err="<sa_uid>:<sa_gid>:644"`
- 执行步骤:
  1. `hdc shell "param set sa.faultinject.query_err 20900001"`
  2. 触发 `TargetSaStub::Query()`（调用方系统应用/上游 SA 调用，或 `hdc shell` 调 SA）
  3. `hdc shell "hilog | grep -E 'faultinject: query return err|20900001'"`
     - 预期命中 SA 侧 `faultinject: query return err 20900001`
  4. `hdc shell "hilog | grep -E '<调用方降级关键字>|degrade|fallback'"`
     - 预期命中调用方降级分支日志
  5. `hdc shell "ps -ef | grep <调用方进程名>"`
     - 预期调用方进程仍在（未被错误码击垮）
  6. 观察调用方对下游的输出（默认值/兜底结果/告警）
- 预期结果:
  - SA 接口直接返回 `20900001`，未执行正常业务逻辑
  - 调用方捕获 `20900001`，进入降级/兜底分支（返回默认值、重试达上限放弃、或上报告警）
  - 调用方进程不崩溃、不卡死（错误码注入不杀进程，安全）
  - 日志关键字: SA 侧 `faultinject: query return err 20900001`；调用方侧 `<降级关键字>`
  - 功能恢复判据: 复位参数后（见 FI-sa-query-002 / 003）调用方恢复正常路径
- 清理步骤:
  - `hdc shell "param set sa.faultinject.query_err 0"`
  - `hdc shell "setenforce $ORIG"`（按记录恢复）
  - `hdc shell "reboot"`

---

### FI-sa-query-002  persist 持久注入 20900001 跨重启，验证降级稳定与复位恢复

- 注入目标: `TargetSaStub::Query()` @ `services/<sa>/src/<sa>_service.cpp:<line>`, 故障类型=错误码/降级
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`
  - 已编译推送 `<sa_lib>.z.so`（含范式 B 注入点，代码读 `persist.sa.faultinject.query_err`，`#ifdef FAULT_INJECT_TEST` 包裹）
  - 用 FI-sa-query-001 已验证单次注入可触发降级；本例验证 `persist.` 跨重启稳定注入 + 复位后恢复
  - **安全前提**：错误码注入不杀进程，`persist.` 不与 critical 崩溃点组合——故跨重启持久化用错误码类验证，而非 RECOVERY 类
- 注入代码: 范式 B（`#ifdef FAULT_INJECT_TEST` 包裹），参数名改 `persist.` 前缀以验证跨重启语义，不再重复
- 参数注册:
  - `param/sa.para`:    `persist.sa.faultinject.query_err=0`
  - `param/sa.para.dac`: `persist.sa.faultinject.query_err="<sa_uid>:<sa_gid>:644"`
- 执行步骤:
  1. `hdc shell "param set persist.sa.faultinject.query_err 20900001"`
  2. `hdc shell "reboot"`（验证 persist 跨重启仍注入）
  3. 重启后触发 `TargetSaStub::Query()`
  4. `hdc shell "hilog | grep -E 'faultinject: query return err|20900001'"`
     - 预期重启后仍命中（证明 persist 注入稳定，可作回归基线）
  5. `hdc shell "hilog | grep -E '<调用方降级关键字>|degrade|fallback'"`
     - 预期调用方每次调用都稳定走降级分支
  6. **复位并验证恢复**：
     - `hdc shell "param set persist.sa.faultinject.query_err 0"`
     - `hdc shell "reboot"`
     - 重启后再次触发 `TargetSaStub::Query()`
     - `hdc shell "hilog | grep -E 'faultinject: query return err|20900001'"`
       - 预期**不再命中**注入日志
     - `hdc shell "hilog | grep -E '<调用方降级关键字>|degrade|fallback'"`
       - 预期**不再命中**降级日志，调用方走正常路径
- 预期结果:
  - persist 注入跨重启稳定生效：每次调用 SA 接口都返回 `20900001`，调用方每次都降级（进程不被杀，无 panic 风险）
  - 复位 `param set ... 0` + reboot 后，SA 接口恢复返回正常结果，调用方恢复主路径
  - 日志关键字: 注入期 `faultinject: query return err 20900001` + `<降级关键字>`；复位后均消失
  - 功能恢复判据: 复位后调用方降级日志消失、下游拿到正常结果
- 清理步骤:
  - `hdc shell "param set persist.sa.faultinject.query_err 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

### FI-sa-query-003  注入值=0（不注入）对照组，证明生产路径不受污染

- 注入目标: `TargetSaStub::Query()` @ `services/<sa>/src/<sa>_service.cpp:<line>`, 故障类型=错误码（基线）
- 前置条件:
  - 记录 `getenforce`；`setenforce 0`
  - 已编译推送 `<sa_lib>.z.so`（含范式 B 注入点，默认值 0，`#ifdef FAULT_INJECT_TEST` 包裹）
  - 用作 FI-sa-query-001/002 的对照基线，证明注入点对生产路径零影响
  - release 构建验证：`nm <sa_lib>.z.so | grep -i faultinject`（release 版应为空）
- 注入代码: 同 FI-sa-query-001（范式 B，默认值 0 → 不触发）
- 参数注册: 同 FI-sa-query-001
  - `param/sa.para`:    `sa.faultinject.query_err=0`
  - `param/sa.para.dac`: `sa.faultinject.query_err="<sa_uid>:<sa_gid>:644"`
- 执行步骤:
  1. `hdc shell "param set sa.faultinject.query_err 0"`（显式置 0）
  2. 触发 `TargetSaStub::Query()`
  3. `hdc shell "hilog | grep -E 'faultinject: query return err|20900001'"`
     - 预期**无命中**（injectErr=0 → 不进入 return 分支）
  4. `hdc shell "hilog | grep -E '<调用方降级关键字>|degrade|fallback'"`
     - 预期**无命中**（调用方走正常路径）
  5. `hdc shell "ps -ef | grep <调用方进程名>"`
     - 预期调用方进程正常
  6. 观察调用方对下游输出正常业务结果
- 预期结果:
  - `GetIntParameter` 读到默认值 0，不进入错误返回分支，SA 走正常业务逻辑
  - 调用方拿到正常结果，不触发降级
  - 日志关键字: 无 `faultinject` 注入日志、无降级关键字
  - 功能恢复判据: 与未改代码前行为一致（证明注入点默认 0 对生产零影响）
  - release 隔离判据: release 二进制不含 `faultinject` 符号（区分"默认不触发"与"release 零开销不含注入面"）
- 清理步骤:
  - `hdc shell "param set sa.faultinject.query_err 0"`
  - `hdc shell "setenforce $ORIG"`
  - `hdc shell "reboot"`

---

## 产出后自检清单（skill 第 5 节 validation）

- [x] 9 个字段齐全（用例ID / 标题 / 注入目标 / 前置条件 / 注入代码 / 参数注册 / 执行步骤 / 预期结果 / 清理步骤——注入代码与参数注册已分列，每项均有内容）
- [x] 注入代码默认值是 0 且 `#ifdef FAULT_INJECT_TEST` 包裹（`GetIntParameter(..., 0, 0, INT_MAX)`，`if (injectErr != 0)`，保证生产零影响）
- [x] 清理步骤含 `param set 0` + `setenforce 按记录恢复` + `reboot` 三件套（每例均含）
- [x] 参数名 < `PARAM_NAME_LEN_MAX`（96）、前缀 `sa.faultinject.`：`sa.faultinject.query_err` = 24 字节；跨重启语义用例 2 用 `persist.` 前缀（错误码类不杀进程，不与 critical 崩溃点组合）
- [x] 前置条件记录原始 `getenforce` 状态（每例均含，并附 `getenforce` 校验）
- [x] 预期结果有可观察判据（日志关键字 `faultinject: query return err 20900001` / `<降级关键字>`；进程行为 `ps -ef`；恢复信号 复位后日志消失）
- [x] release 隔离检查：注入代码 `#ifdef FAULT_INJECT_TEST` 包裹，release 不定义该宏 → release 二进制不含 `faultinject` 符号
