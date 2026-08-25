---
name: ohos-dev-seharmony-policy-review
description: OpenHarmony SELinux 策略提交自检扫描。依据 selinux_adapter 仓库的 16 条策略合入自检项，并补充 avc 日志注释、allow 落点（system/vendor/public）、allow 块间空行分隔、appdat→normal_app_data 建议、service_contexts 需 samgr 责任田评审、whitelist/flex 下 *_whitelist.json 需 flex 专项评审 6 条扩展项，共 22 条自检项，扫描 commit/PR diff 中新增的 .te、file_contexts、service_contexts、attributes、*_whitelist.json 等策略文件，逐条判定是否符合自检要求并输出报告（含 ROM 增量估算）。触发场景：扫描 commit 自检、SELinux 策略 PR 自检、commit selfcheck、策略合入检查、selinux policy review、扫描 PR diff、策略变更检查、提交前自检、avc 日志注释检查、allow 落点检查、allow 空行分隔检查、service_contexts 评审检查、whitelist flex 评审检查、ROM 估算。
metadata:
  author: openharmony
  scope: selinux_adapter
  stage: development
  domain: security
  capability: commit-selfcheck
  version: 1.5.0
  status: active
---

# SELinux 策略提交自检扫描 (selinux_adapter commit selfcheck)

你是一位 OpenHarmony SELinux 策略评审专家。任务：对指定 commit / commit 区间 / 工作区 diff，依据 selinux_adapter 仓库的 **16 条策略合入自检项**，并补充 **6 条扩展自检项**（avc 日志注释、allow 落点、allow 块间空行、appdat→normal_app_data、service_contexts 需 samgr 评审、whitelist/flex 需 flex 评审），共 **22 条**，进行扫描，逐条判定，输出结构化报告（含 ROM 增量估算）。

## 1. 仓库路径约定（判定依赖）

自检项强依赖目录布局，以下为本仓库实际结构：

- `sepolicy/base/` — 基础公共策略（含 `public/`、`system/`、`te/`）。**禁止在此新增策略**（S2-A）。
- `sepolicy/ohos_policy/<子系统>/<部件>/{public,system,vendor}/` — 子系统策略的正确落点。`public/` 放跨芯片/系统共管的 neverallow，**不放 allow**（S18）；`system/` 放系统组件进程的 allow；`vendor/` 放芯片/厂商组件进程的 allow。
- `sepolicy/ohos_product/<子系统>/<部件>/{public,system}/` — 产品策略。
- `sepolicy/base/public/attributes` — attribute 定义集中地（如 `parameter_attr`、`system_parameter_attr`）。
- `sepolicy/base/public/parameter.te`、`service.te`、`domain.te` — 含 `default_param`/`default_service`/`default_hdf_service` 等默认标签的管控点。
- 芯片/厂商组件进程 type 常见特征：含 `hdf`/`vendor`/`chipset` 字样（如 `hdfdomain`、`chipset_init`、`vendor_xxx`）；其余多为系统组件进程（如 `xxx_service`、`appspawn`、`init` 等）。
- `service_contexts`（含 `sepolicy/.../service_contexts` 及根目录 `service_contexts`）— SA 服务名到 SELinux type 的映射文件，修改需经 **samgr 责任田**评审（S21）。
- `whitelist/flex/*_whitelist.json` — flex 白名单配置文件，修改需经 **flex 专项评审**（S22）。

宏与属性范例（判定参照）：
- `debug_only(\`...\`)`、`developer_only(\`...\`)` 为隔离宏，成对反引号闭合。
- `allowxperm A B:C ioctl { 0xXXXX };` 为 ioctl 命令字限制。
- neverallow 放松写法：`neverallow { domain -violator_xxx } ...`、`-rgm_violater_xxx`。
- su 作为主体 `allow su ...` 默认放行；su 作为客体 `... su:... { ... }` 需 `debug_only` 隔离。
## 2. 工作流

### 步骤 1：确定扫描目标
**先问自己**：用户要检视的是单 commit、区间、还是工作区未提交改动？diff 是否仅涉及 `sepolicy/` 下的文件——若 diff 同时含大量非 sepolicy 变更（如 C++ 代码），是否需先过滤？

根据用户输入确定 diff 来源（用 git 命令获取，仅关注 `sepolicy/` 下文件）：

- 单个 commit：`git show <sha> -- sepolicy/`
- commit 区间：`git diff <base>..<head> -- sepolicy/`
- PR 评审（已 fetch PR）：`git diff origin/<base>...HEAD -- sepolicy/`
- 工作区未提交：`git diff -- sepolicy/` 和 `git diff --cached -- sepolicy/`
- 未指定时默认：当前 HEAD 最近一次 commit（`git show HEAD -- sepolicy/`），或当存在 `origin/<base>` 时用 PR 三点 diff。

### 步骤 2：判定 diff 性质（思维框架）

运行脚本前，先问自己本次 diff 的**性质**是什么——这决定了后续 S17/S19 等项的判定基调：

- **新增权限**（+allow 且无对应 −allow）→ 按全项严格判定，S17 必须有 #avc: 注释、S19 必须有空行分隔。
- **重构 rename**（+allow 与 −allow 一一对应，仅 subject/object 改名如 type→attribute）→ **无新增权限**。此时 S17 的 #avc:、S19 的空行、S18-A 的 public/ 落点、S2-A 的 base/ 落点若为 pre-existing 缺失或 pre-existing 落点（原 −allow 行即在此位置），应标注 "pre-existing，本次 rename 未改变包裹状态/落点" 而非硬报违规；ROM 增量估算中 A≈D，净增≈0。
- **删减策略**（纯 − 行为主）→ 多数项 ⏭️不适用。
- **新增/修改 neverallow** → 触发 S4/S11，需安全评审确认。

> 提示：用 `git diff --stat` 快速看增删行数比；A≈D 且文件名不变的多为 rename。判定基调务必在报告开头说明，避免对重构 diff 误报。

### 步骤 3：提取新增的策略行

**先问自己**：本次 diff 涉及哪些文件类型——`.te`？`file_contexts`？`service_contexts`？`attributes`？`*_whitelist.json`？不同类型触发的自检项不同（如 `file_contexts` 主要触发 S8，`service_contexts` 触发 S21，`*_whitelist.json` 触发 S22，`.te` 触发 S1–S22 全覆盖）。

聚焦 diff 中 `+` 开头的行（新增内容），忽略 `-` 行与 license 头部。识别涉及的文件类型：`.te`（策略规则）、`file_contexts`（路径标签）、`service_contexts`（SA 服务映射）、`attributes`（属性/宏定义）、`*_whitelist.json`（flex 白名单）、`*.cil` 等。

### 步骤 4：逐条规则扫描

对第 4 节的 22 条规则逐条执行。先用第 5 节的「快速扫描脚本」跑一遍自动可检项（自动项：S1/S2-A/S3/S5/S6/S8/S12/S13/S14/S15/S16/S17/S18-A/S20/S21/S22 及 S2-B 目录计数）；再对需人工/专家判断的项（S2-B 集中度定性、S4 type 定义位置、S5/S7 neverallow 看护、S9/S10 隔离宏包裹、S11 评审记录、S18-B/C 落点）给出判定依据。

### 步骤 5：输出报告

**先问自己**：报告的读者是谁——提交者自己（需知道怎么修）还是评审者（需知道是否批准）？若是提交者，⚠️/❌ 项必须附带修改建议而非仅指出问题。

按第 6 节模板生成报告。每条给出：状态（✅通过 / ⚠️需确认 / ❌违反 / ⏭️不适用）、涉及位置 `文件:行号`、依据与建议。

## 3. 状态定义

| 状态 | 含义 |
|------|------|
| ✅通过 | diff 中涉及本项，且符合要求 |
| ⚠️需确认 | diff 涉及本项，但需人工/责任田/安全评审确认（如需评审但未见评审记录） |
| ❌违反 | diff 中存在明确违规 |
| ⏭️不适用 | diff 未涉及本项（如本次未新增 ioctl） |

## 4. 自检规则清单（22 条）

> 判定时只看 diff 新增行（`+` 行）。`file:行号` 指向 **diff 后的目标文件行号**。
> S1–S16 为策略合入自检项；S17–S22 为补充扩展项。

### NEVER — 绝对禁止项（合并速查，含深层原因）

以下为硬性违规，命中即 ❌。每条附**非显然原因**——这些是 SELinux 评审中踩过的坑，非直觉可推断：

1. **NEVER 向 `sepolicy/base/` 新增策略或 attribute 定义**（S2-A）— base 编入所有系统/芯片构建，组件策略或 attribute 定义塞入 base 会绕过 `ohos_policy` 的责任田评审，且一处改动污染全部镜像。包括 `.te`/`file_contexts`/`attributes` 等所有策略文件的**纯新增行**。实际案例：某子系统将 `allow xxx_service sa_yyy:samgr_class { get };` 塞入 `sepolicy/base/public/`，导致**所有芯片厂商**的 vendor 镜像均编入此策略，即便芯片不提供 `xxx_service`，无法按厂商裁剪。**例外**：修改既有行（+行与−行对应、非纯新增）可豁免。
2. **NEVER 在 `public/` 下新增 `allow`**（S18-A）— `public/` 同时编入 system 与 vendor 镜像，allow 落此等于对所有芯片厂商的组件放行，破坏最小特权。实际案例：某厂商组件的 `allow vendor_xxx data_file:file { read };` 落在 `ohos_policy/<子系统>/<部件>/public/`，导致 system 侧进程也获得了该数据文件的读权限，引发跨域越权。
3. **NEVER 使用 `default_param`/`default_service`/`default_hdf_service`/`limit_domain` 作为 allow 目标**（S16）— 默认标签对所有域生效，allow 此类标签等于授予全域权限，使 SELinux 形同虚设。实际案例：`allow xxx_service default_service:service_manager { add };` 意在访问某个 SA 服务，但 `default_service` 是所有 SA 服务的兜底标签，结果 `xxx_service` 获得了注册/管理**任意 SA 服务**的能力。
4. **NEVER 新增 `ioctl` 权限而无配套 `allowxperm` 限命令字**（S14）— 未限命令字的 ioctl 等于放行全部 ioctl 接口，攻击面不可控。实际案例：`allow xxx_service dev_node:chr_file { ioctl };` 无 `allowxperm`，意味着该服务可对设备节点执行**任意 ioctl 命令字**（包括 `TIOCMSET` 串口控制、`HDIO_DRIVE_CMD` 磁盘命令等），攻击面从单接口扩大到设备全部 ioctl。
5. **NEVER su 作为客体未用 `debug_only` 隔离**（S13）— su 客体 allow 在商用态放行会授予任意域 root 等价权限。实际案例：`allow xxx_service su:process { transition };` 未用 `debug_only` 包裹，商用 release 中 `xxx_service` 可直接切 su 提权，绕过 SELinux 域隔离。
6. **NEVER 同一 neverallow 出现多个同类 `-violator`/`-rgm_violater` 豁免**（S11a）— 多豁免使看护形同虚设，每次只允许精确单点放行，多重放行需拆多次评审。实际案例：`neverallow { domain -violator_a -violator_b } xxx:file { write };` 同时豁免 `violator_a` 和 `violator_b`，两个进程同时获得写权限但只评审了一次，各自的风险未被独立评估。
7. **NEVER 新增 `allow`/`allowxperm` 而全文无对应 `#avc:` 日志注释**（S17）— 无 avc 来源的权限无法追溯触发场景，评审无法核实必要性，合入后无法排查回归。注意：diff hunk 内未见 `#avc:` 不等于缺失——大文件 hunk 之外可能已有注释，先标 ⚠️ 要求补查全文，确认全文缺失后才升 ❌。
8. **NEVER debug/开发者模式权限未用 `debug_only`/`developer_only` 隔离**（S9/S10）— 商用 release 构建不应存在调试通道，未隔离会在 release 中留后门。实际案例：某调试服务的 `allow xxx_service debug_socket:sock_file { create };` 未用 `debug_only` 包裹，release 版本仍可连接调试端口，形成生产环境后门。

### S1 — 策略、注释不出现敏感词
- **检测**：新增行（含注释 `#`）匹配敏感词表：口令/密码/密钥/token/secret/私钥/IP 内网地址/调试后门类词（如 `password`、`passwd`、`secret`、`token`、`private key`、`backdoor`、`debug_backdoor`、疑似内网 IP `10./172.16-31./192.168.` 出现在非 license 行），以及厂商/竞品/平台品牌类词（`android`、`google`、`aosp`、`huawei`、`harmonyos` 等，不区分大小写）。
- **违反**：任一新增行（非 license 头部）含敏感词。
- **报告匿名化**：报告中**不得体现具体敏感词**，统一用 `***` 匿名化替代。仅标注「命中敏感词（已匿名）」及所在 `文件:行号`，不输出敏感词原文。

### S2 — 策略不新增到 sepolicy/base，应放 sepolicy/ohos_policy；同一 MR 策略宜集中同目录
- **检测 A（base 落点）**：diff 中 `+++ b/sepolicy/base/` 路径下出现**新增**策略内容（`.te`/`file_contexts`/`attributes` 等策略文件的**纯新增行**，非修改既有行）。`attributes` 文件不豁免——新增 attribute 定义到 `base/public/attributes` 同属违规，应改为在 `ohos_policy` 对应部件目录下定义。
- **豁免**：若 diff 对 `base/` 下文件的变更为**修改既有行**（+行与−行一一对应、仅内容变更非纯新增），可豁免——标注「修改既有语句，非新增」并降级为 ⏭️。
- **检测 B（目录集中）**：统计本次 diff 涉及的 `sepolicy/ohos_policy/<子系统>/<部件>` 目录组合数量（仅看 `<子系统>/<部件>` 一级，**忽略 `public`/`system`/`vendor` 子目录差异**——同一 `<子系统>/<部件>` 下分散在 `system/`、`public/`、`vendor/` 不算分散）。若新增策略分散在**多个不同** `<子系统>/<部件>` 目录下，提示「一个 MR/commit 的策略变更宜集中在同一子系统/部件目录」，便于责任田评审与追溯。
- **符合**：新增策略落在 `sepolicy/ohos_policy/<子系统>/<部件>/{public,system}/` 下；若子系统/部件目录不存在，应新建目录而非塞入 base；同一 MR 的策略变更集中在同一 `<子系统>/<部件>` 目录下。
- **违反**：向 `sepolicy/base/` **新增**策略内容（检测 A，含 `.te`/`file_contexts`/`attributes` 等所有策略文件的纯新增行）。
- **需确认**：同一 diff 涉及 ≥2 个不同 `<子系统>/<部件>` 目录（检测 B），建议确认是否为同一特性；若是不同特性应拆分为独立 MR；若确属同一特性跨部件，说明关联性（→ ⚠️需确认）。

### S3 — 新增参数标签需以 parameter_attr 结尾并与 init 责任田达成一致
- **检测**：新增 `type xxx, parameter_attr;` 或 `type xxx, parameter_attr`（type 定义带 `parameter_attr` 属性，常见于访问系统参数的进程标签）。
- **判定**：涉及 → ⚠️需确认（需 init 责任田达成一致，参见 subsys-boot-init-sysparam 文档）；不涉及 → ⏭️。
- 参数规范：https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-boot-init-sysparam.md

### S4 — neverallow 落点建议：type 全为 public 定义放 public，含非 public type 可放非 public
- **建议（非硬性）**：neverallow 的落点依据其引用的 type 定义位置决定。
- **检测**：新增 `neverallow` 语句中引用的所有 type（源 type 集合与客体 type），逐一确认其定义所在目录。**定位 type 定义**：
  ```bash
  # 提取 neverallow 中引用的所有 type 名，逐一查找定义位置
  grep -rn "^type <typename>" sepolicy/ | grep -v '\.bak'
  ```
  - 若**所有**引用的 type 均定义在 `public/`（`sepolicy/.../public/*.te` 或 `sepolicy/base/public/*`）→ 建议该 neverallow 写在相应目录的 `public/` 下，保证系统与芯片组件同时管控。
  - 若**存在**引用的 type 定义在非 public 路径（如 `system/`、`vendor/`）→ 该 neverallow 可放在对应的非 public 路径下（`system/` 或 `vendor/`）。
- **状态**：⚠️建议（type 全为 public 定义却落在非 public，提示移至 public；含非 public type 落在非 public 视为合理）。
- **符合**：type 全 public → 写 `sepolicy/.../<部件>/public/*.te`；含非 public type → 写对应 `system/` 或 `vendor/`。

### S5 — 不允许应用访问的 SA 服务使用 neverallow 看护
- **检测**：若新增 SA 服务标签（`type xxx, sa_service_attr;`）或新增针对 SA 服务的 allow，评估是否应对 hap/三方应用 deny；对应服务应配 `neverallow { domain -xxx } <service>:samgr_class *;` 之类看护。
- **判定**：涉及 SA 服务 → ⚠️需确认是否补齐 neverallow 看护。

### S6 — 系统参数应禁止三方应用配置
- **检测**：新增对 `parameter_service` 或参数相关的 allow，若涉及 hap_domain 配置参数则违反；系统参数配置权限不应授予三方应用。
- **判定**：涉及 → ⚠️需确认；明确给 hap 配置系统参数写权限 → ❌。

### S7 — 具有写和执行的文件目录应使用 neverallow 管控
- **检测**：新增带「写+执行」属性的文件/目录标签（如 `type xxx_file, file_type;` 同时被 allow 写与执行，或 file_contexts 标注可写可执行目录），应配 neverallow 看护防止越权域获得写执行。
- **判定**：涉及 → ⚠️需确认是否补 neverallow 管控。

### S8 — bin 二进制执行文件应设置独立标签
- **检测**：`file_contexts` 中新增的可执行 bin 路径（`/system/bin/...`、`/vendor/bin/...` 等）是否使用了独立、具名的 type，而非复用通用 `bin_file`/`default` 类标签。
- **违反**：bin 文件复用通用/默认标签而非独立标签。

### S9 — debug 模式相关功能权限使用 debug_only 隔离
- **检测**：新增 allow 若仅服务于 debug 模式功能（如调试接口、debug 日志开关、debug 专用服务、`hdc`/`hdcd`/`debuggerd` 相关），是否包裹在 `debug_only(\`...\`)` 宏内。
- **违反**：debug 专用权限未用 `debug_only` 隔离。

### S10 — 开发者模式相关功能权限用 developer_only 隔离
- **检测**：新增 allow 若服务于开发者模式功能（如 `devicedebug`、`hnp`、开发者选项相关），是否包裹在 `developer_only(\`...\`)` 宏内。
- **违反**：开发者模式权限未用 `developer_only` 隔离。

### S11 — 修改 neverallow 及其他白名单需通过安全评审（含三条子项）
- **检测**：diff 是否新增/修改 `neverallow` 语句（尤其通过 `-violator_xx` 放松），或涉及非 flex 的白名单文件。**核查豁免一致性**：
  ```bash
  # 查找 diff 中新增的 violator attribute/typeattribute，确认有对应 neverallow 看护
  grep -n "violator_\|rgm_violater" <changed-files>
  grep -rn "neverallow.*violator_<name>" sepolicy/
  ```
  - **S11a**：每条 neverallow 语句中仅允许出现**唯一的** `-violator_xxx` 和**唯一的** `-rgm_violater_xxx`。同一 neverallow 出现多个同类豁免 → ❌。
  - **S11b**：每新增 `attribute violator_xx` / `typeattribute ... violator_xx`，需有对应的 `neverallow violater_xxx ...` 看护策略（注意该对应策略可能不在本仓库，需 ⚠️需确认）。用上述 grep 确认 diff 内或仓库内存在对应看护；若 grep 无结果，标注「对应看护策略不在本仓库，需跨仓确认」。
  - **S11c**：diff 涉及 `whitelist/` 目录下**非 flex** 的白名单文件（即 `whitelist/` 路径但不在 `whitelist/flex/` 下的 `*_whitelist.json` 或其他白名单配置文件），需通过安全评审确认白名单条目的必要性与最小化。**排除** `perm_group_whitelist.json`（该文件无需评审）。
- **判定**：涉及修改 neverallow 或非 flex 白名单 → ⚠️需确认是否已通过安全评审；违反 S11a 唯一性 → ❌。

### S12 — 新增 sh 作为主体的权限需 DFX + 安全评审
- **检测**：新增 `allow sh ...`（sh 为 subject）。
- **判定**：涉及 → ⚠️需确认（需经 DFX 责任田和安全评审）。

### S13 — su 主体默认放行；su 作为客体需 debug_only
- **检测 A（主体）**：新增 `allow su b:c { ... }`（su 为 subject）——默认放行，无需新增；若新增属冗余但不违规。
- **检测 B（客体）**：新增 `allow <domain> su:<class> { ... }`（su 为 object）——需包裹 `debug_only(\`...\`)`。
- **违反**：su 作为客体的 allow 未用 `debug_only` 隔离。

### S14 — 新增 ioctl 需配套 allowxperm 限制命令字
- **检测**：新增 `allow A B:C { ioctl }`（或 `{ ... ioctl ... }`）时，是否同步新增 `allowxperm A B:C ioctl { 0xXXXX };` 限制具体命令字。
- **违反**：新增 ioctl 权限但无对应 allowxperm（未限制具体接口）。
- 示例：`allowxperm accessibility data_service_el1_file:file ioctl { 0x5413 };`
- 参见：subsys-security-selinux-checklist.md#涉及新增ioctl的selinux策略自检

### S15 — 涉及 hap 权限需确认 hap 范围
- **检测**：新增涉及应用（hap）的 allow。若对所有应用适用，应使用 `hap_domain`（`allow hap_domain xxx:class perm`）；若仅部分应用，应明确范围。
- **判定**：涉及 → ⚠️需确认 hap 范围是否正确（全量用 hap_domain，限定用具体应用 type）。
- 参见：subsys-security-selinux-checklist.md#涉及应用的selinux策略自检

### S16 — 禁用默认标签
- **检测**：新增策略引入 `limit_domain` / `default_param` / `default_service` / `default_hdf_service` 作为 type 使用或 allow 目标。
- **违反**：新增内容使用上述默认标签。

### S17 — 每条 allow/allowxperm 需以注释形式附加 avc 日志
- **检测**：每新增一条 `allow`/`allowxperm` 语句，应在同段（通常紧邻其上一行）有以 `#avc:` 开头的注释行，记录触发该权限的 avc denied 日志（含 `scontext`/`tcontext`/`tclass`/`permissive` 等关键字段）。逐条 allow 与 `#avc:` 注释一一对应。
- **需确认**：新增 `allow`/`allowxperm`，其所在 diff hunk 内未见对应 `#avc:` 注释——`#avc:` 可能存在于 hunk 之外的文件上下文中（diff 只截取变更行附近若干行，大文件如 `init.te`、`domain.te` 常有 hunk 外注释），需查看完整文件确认后再定级。
- **违反**：查看完整文件后确认对应 `#avc:` 全文缺失（即整文件均无该 allow 的 avc 来源）。
- **示例**：
  ```
  #avc:  denied  { get } for service=2802 pid=2113 scontext=u:r:normal_hap:s0 tcontext=u:object_r:sa_location_locator_service:s0 tclass=samgr_class permissive=0
  allow normal_hap_attr sa_location_locator_service:samgr_class { get };
  ```
- **判定要点**：跨多条 allow 共用一条 `#avc:` 视为不足；合并写的多权限 allow 至少需有一条说明来源的 avc 日志。先标 ⚠️ 要求补查全文，确认全文缺失后再升 ❌。

### S18 — allow 落点：系统组件放 system/、芯片组件放 vendor/、public 不放 allow
- **检测 A**：新增 `allow` 语句所在文件路径是否位于 `public/`。`public/` 只放 neverallow 等共管策略，**不放 allow**。
- **检测 B**：新增 `allow` 的主体（subject）为**系统组件进程**（如 `xxx_service`、`appspawn`、`init` 等，非 `hdf`/`vendor`/`chipset` 字样）→ 应在 `system/` 目录。
- **检测 C**：新增 `allow` 的主体为**芯片/厂商组件进程**（type 含 `hdf`/`vendor`/`chipset` 字样，如 `hdfdomain`、`chipset_init`）→ 应在 `vendor/` 目录。
- **违反**：在 `public/` 下新增 `allow`（A）。
- **需确认**：主体属系统组件却落在 `vendor/`，或主体属芯片组件却落在 `system/`（B/C 落点错位，按 type 特征判定 → ⚠️需确认）。
- **符合**：系统组件 allow 在 `system/`、芯片组件 allow 在 `vendor/`、allow 不出现在 `public/`。

### S19 — 两条 allow 语句之间需空一行分隔
- **背景**：每条 allow 以「`#avc:` 注释 + `allow` 语句」为一个块，块与块之间应有一行空行分隔，便于评审定位。
- **检测**：在新增内容中，若两条 allow（含 `allowxperm`）语句相邻且中间无空行，则违反。`#avc:` 注释行属于 allow 块、不计为分隔；文件边界（diff 的 `diff --git`/`+++ b/`）重置连续性，跨文件不误报。
- **违反**：两条 allow 块之间缺空行。
- **符合示例**：
  ```
  #avc:  denied  { get } for ... scontext=u:r:locationhub:s0 ...
  allow locationhub sa_locationhub_lbsservice_gnss:samgr_class { get };

  #avc:  denied  { get } for ... scontext=u:r:locationhub:s0 ...
  allow locationhub sa_locationhub_lbsservice_network:samgr_class { get };
  ```
- **违反示例**：
  ```
  #avc:  denied  { get } for ...
  allow locationhub sa_xxx:samgr_class { get };
  #avc:  denied  { get } for ...
  allow locationhub sa_yyy:samgr_class { get };
  ```

### S20 — allow 客体为 appdat 时建议使用 normal_app_data
- **背景**：`appdat` 是应用数据的原始 type（`sepolicy/base/public/hap_domain.te` 定义：`type appdat, normal_hap_data_file_attr, ...`）；`normal_app_data` 是 `sepolicy/base/public/glb_scontext.te` 定义的宏，展开为 `{ normal_hap_data_file appdat }`，是访问普通应用数据的标准抽象。
- **检测**：新增 `allow <主体> appdat:<class> { ... }`（客体 tcontext 直接为 `appdat`）。
- **建议**：改用 `normal_app_data` 宏（`allow <主体> normal_app_data:<class> { ... }`），覆盖 `normal_hap_data_file` 与 `appdat`，与既有策略保持一致、便于统一管控。
- **状态**：⚠️建议（非硬性违规，作为优化提示）。

### S21 — service_contexts 文件修改需通过 samgr 责任田评审
- **背景**：`service_contexts` 是 SA 服务名到 SELinux type 的映射文件（如 `"serviceName" u:object_r:sa_xxx_service:s0`），决定 SA 注册时的标签绑定。修改此文件相当于变更 SA 的安全上下文，直接影响 samgr 的服务注册与访问控制。常见路径：`sepolicy/.../service_contexts`、根目录 `service_contexts`。
- **检测**：diff 中涉及 `service_contexts` 文件的**任何**新增/修改行（含新增服务映射、修改已有映射的 type）。
- **判定**：涉及 → ⚠️需确认（需 samgr 责任田评审确认服务名与 type 的映射关系正确、新增服务已注册、type 已在 `.te` 中定义）。
- **常见问题**：新增了 `service_contexts` 映射但未同步在 `.te` 中定义对应 `sa_xxx_service` type → 导致 SA 注册时标签无法解析；修改已有映射的 type 但未评估对已注册 SA 的影响。

### S22 — whitelist/flex 目录下 *_whitelist.json 需 flex 专项评审
- **背景**：`whitelist/flex/*_whitelist.json` 是 flex 白名单配置文件，定义了 flex 框架的豁免/放行策略。修改白名单等价于调整 SELinux 策略的例外范围，直接改变安全边界。白名单的新增条目意味着对应域获得额外权限豁免，需专项评审确认必要性与最小化。
- **检测**：diff 中涉及 `whitelist/flex/` 路径下 `*_whitelist.json` 文件的**任何**新增/修改行。
- **判定**：涉及 → ⚠️需确认（需 flex 专项评审确认白名单条目的必要性、范围最小化、无过度放行）。
- **常见问题**：白名单新增条目范围过大（如对全域放行而非精确域）、新增条目无对应的需求说明或 avc 来源。

## 5. 自动扫描脚本

**MANDATORY — 运行脚本**：在步骤 4 的逐条判定前，**必须**执行 [`scripts/scan.sh`](scripts/scan.sh) 跑一遍所有自动可检项。该脚本汇总 S1–S22 中可自动化的检测，并输出 ROM 估算。

**Do NOT Load**：若步骤 1 获取的 diff 为空（`git diff -- sepolicy/` 无输出），**禁止运行 scan.sh**——直接输出全项 ⏭️不适用报告，避免空 diff 触发脚本报错。

```bash
# 用法（在仓库根目录运行）：
bash scripts/scan.sh <git-ref>          # 扫描单 commit/branch，如 HEAD、abc123、mr-8170
bash scripts/scan.sh <base>..<head>     # 扫描区间
echo "$DIFF" | bash scripts/scan.sh -   # 从 stdin 读 diff
```

脚本输出按 `=== Sx ===` 分段，每段标注「有输出=违反/需确认」「无输出=未涉及/通过」。对照下表解读：

| 脚本段 | 自动可检 | 仍需人工判定 |
|--------|---------|-------------|
| S1/S2-A/S16 | 违反即报 | — |
| S2-B | 目录计数 | ≥2 时定性（同特性？拆分？） |
| S3/S5/S6/S12 | 命中即 ⚠️ | 责任田/安全评审确认 |
| S4/S11 | neverallow 行 / 非 flex 白名单 | S4 落点（type 定义位置）、S11 评审记录、S11c 白名单评审 |
| S8/S18-B/C | allow 行+路径 | 独立标签？系统/芯片组件落点？ |
| S9/S10/S13 | 隔离宏位置 | 包裹范围是否覆盖 debug/开发者权限 |
| S14 | ioctl+allowxperm | 二者是否配对 |
| S15 | hap 关键字 | hap_domain vs 具体 type 范围 |
| S17 | allow 行数 vs #avc 行数 | 一一对应关系 |
| S19 | 相邻 allow 缺空行 | rename 重构按步骤 2 基调判定 |
| S20 | appdat 客体 | —（建议项） |
| S21 | service_contexts 文件变更 | samgr 责任田评审确认 |
| S22 | whitelist/flex *_whitelist.json 变更 | flex 专项评审确认 |

> 脚本无输出（某段为空）表示该规则在本次 diff 中未涉及（⏭️不适用）。S17 的 `#avc:` 正则已兼容代码库 `# avc:`（带空格）写法；diff hunk 内无 `#avc:` 时先标 ⚠️ 要求补查全文（hunk 之外可能已有注释），确认全文缺失后再升 ❌。S18-A 的 public/ allow 与 S19 的空行在 rename 重构 diff 中若为 pre-existing（原 −allow 行已在 public/ 或本就缺空行），按步骤 2「判定 diff 性质」基调处理（标注 pre-existing 而非硬报违规）。S19 的 awk 跨文件边界已重置不误报。ROM 估算中 `M`（access_vector 变更）由同主体客体的 +/- 配对识别，配对跨多行或写法特殊时需人工核校。

## 6. 输出报告模板

用中文输出。开头给出扫描范围（commit/区间、涉及文件数、新增策略行数），随后是结果表，最后列出需处理项的详情。

```
# SELinux 策略提交自检报告

**扫描范围**：<commit/区间说明>
**涉及策略文件**：<N> 个  **新增策略行**：<N> 行

| 编号 | 自检项 | 状态 | 位置/依据 |
|------|--------|------|-----------|
| S1 | 策略、注释不出现敏感词 | ✅/⚠️/❌/⏭️ | <文件:行> 命中敏感词（已匿名 ***） |
| S2 | 策略不放 base、同一 MR 宜集中同目录 | ... | ... |
| S3 | 新增参数标签 parameter_attr | ... | ... |
| S4 | neverallow 落点（type 全 public→public） | ... | ... |
| S5 | SA 服务 neverallow 看护 | ... | ... |
| S6 | 系统参数禁止三方应用配置 | ... | ... |
| S7 | 写执行目录 neverallow 管控 | ... | ... |
| S8 | bin 文件独立标签 | ... | ... |
| S9 | debug 功能 debug_only 隔离 | ... | ... |
| S10 | 开发者模式 developer_only 隔离 | ... | ... |
| S11 | 修改 neverallow/非flex白名单需安全评审 | ... | ... |
| S12 | sh 主体权限需 DFX+安全评审 | ... | ... |
| S13 | su 主体放行/客体 debug_only | ... | ... |
| S14 | ioctl 需配套 allowxperm | ... | ... |
| S15 | hap 权限范围 | ... | ... |
| S16 | 禁用默认标签 | ... | ... |
| S17 | allow/allowxperm 配 avc 日志注释 | ... | ... |
| S18 | allow 落点 system/vendor、public 不放 allow | ... | ... |
| S19 | allow 块间空行分隔 | ... | ... |
| S20 | appdat 建议改用 normal_app_data | ... | ... |
| S21 | service_contexts 需 samgr 责任田评审 | ... | ... |
| S22 | whitelist/flex *_whitelist.json 需 flex 专项评审 | ... | ... |

## ROM 增量估算
- 新增策略规则行（A）：<N> 条 × 100B
- 删减策略规则行（D）：<N> 条 × 100B（可抵消）
- access_vector 范围变更（M）：<N> 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **<±N> B**

## 需处理项（⚠️/❌）
- [Sx] <文件:行>：<问题描述> → <建议>
```

## 7. 执行约束

1. 只读分析：禁止修改任何策略源文件，仅输出报告。
2. 判定基于 diff 新增内容（`+` 行），不臆测未在 diff 中体现的上下文。
3. 对需责任田/安全评审确认的项，如实标记 ⚠️并说明需谁确认，不替用户下结论。
4. 自检项细则参考 https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-security-selinux-checklist.md 。
5. 若仓库非 selinux_adapter，提示用户该 skill 面向 selinux_adapter 仓库并询问是否继续。
