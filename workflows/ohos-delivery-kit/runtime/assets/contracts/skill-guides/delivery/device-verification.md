# 实现阶段的设备与模拟器运行时验证

本指南负责 `odk-implement` Build & Verify 中运行时验证的执行细节：范围与确认的分离、
Task 命令形态的判定，以及设备准备（b）与模拟器启动（c）两个子步骤。编译（a）与测试（d）
仍由主流程执行。子步骤的选择由计划快照中的验证范围控制，不由编译产品名推断。

## 范围与确认分离

`验证范围`、`验证产品` 和 `验证目标确认` 与 `编译产品` 分开读取。具体或抽象的编译名
不选择运行时目标。旧计划缺少确认时，先补齐实际确认或询问，再执行运行时验证。
编译名、验证目标或范围变更时，先按 [build-products.md](build-products.md) 更新计划和受影响的
命令。验证产品或设备 ID 变更后，设备准备、部署和运行时测试证据全部失效。

先读取并遵循 [device-version.md](device-version.md) 的确认规则，再按已记录的版本策略执行：`host-only`/`build-only`
不询问 daily；`emulator` 使用已确认的验证目标，不准备物理镜像；仅 `device` 在验证产品上
选择 daily/existing。准备结果只对同一确认产品和实际设备复用。全自动模式仍须遵守
产品、验证目标、实际目标设备及刷机覆盖的显式确认要求。

## 命令形态与子步骤选择

先确定 Task 命令形态，再仅在显式验证范围要求时应用 a–d：

- **Test-only Task**（`验证命令` 仅为测试运行器）：跳过 a 和产物推送。`device` 范围仍通过 b 选择并准备设备；`emulator` 范围执行 c，再执行 d。build-only 计划可运行 host 检查，但不得包含设备/模拟器命令。
- **Build+test Task**（`验证命令` 含 `&&` 分隔的编译与测试命令）：先执行 a，再按范围选择运行时步骤，最后执行 d。
- **Build-only Task**（`验证命令` 仅含编译命令、无 `&&` 测试步骤）：先执行 a，再按范围选择运行时步骤；如 `## 构建与验证环境` 记录了适用的 `测试命令`，将其用于 d。

选择运行时步骤时，`device` 只用 b，`emulator` 只用 c。`host-only` 和 `build-only` 跳过 b/c，
仅运行各自适用的主机检查或编译。无适用测试时跳过 d；若计划要求测试却缺少可运行命令，
记录待验证，按反馈流程补齐命令或明确处置。禁止通过比较编译名与 arm64_virt、rk3568 等设备名选择 b/c。

所有依赖运行时的测试（包括 Red、步骤 d 和最终集成验证）必须绑定到 b 或 c 确认的设备 ID。
HDC 命令使用 `hdc -t <实际设备 ID>`；
其他测试工具使用其支持的目标选择方式。目标未准备就绪、已跳过或无法可靠绑定时，不运行依赖
该目标的命令。在 Actual Result 记录运行时未执行及原因；连接或准备失败不能作为预期 Red 证据。
独立主机检查可继续，结果单独记录。
计划要求的运行时验证仍未完成时，按反馈流程处理，不得仅据主机结果标 Task Done。

已确认且明确适用的刷机在调用其配置 skill 前，先阅读
[configured-skills.md](../router/configured-skills.md)；当前 Agent 缺失该 skill 时，从匹配
配置注释的安装链接安装、确认可用后再继续。安装未完成阻塞设备准备。

## 运行时 Red 与通过验证

1. 写好失败测试后，使用尚未加入本 Task 实现修复的源码准备 Red 基线。按计划编译 Red
   所依赖的测试和目标产物。已有产物须核实基线来源及目标兼容性才能复用。用 QEMU 时，
   按 c 的启动前检查核实所需镜像属于 Red 基线。Test-only Task 跳过 a 和 Task 产物推送，
   仍需准备运行环境所需的镜像。
2. 按范围执行 b 或 c，部署 Red 所需且已核验的基线产物，绑定实际设备 ID 后再运行失败测试。
   记录基线、产物、设备 ID 和失败证据。基线构建、启动、连接或部署不成功时，记录待验证并走
   反馈流程。
3. 实现修复后，重新编译本 Task 的适用产物，核验其来源和兼容性，再部署到仍就绪且适用的
   同一已确认目标并运行 d。可用推包和服务重启加载修复时，复用已确认的模拟器实例并从 c
   的产物部署步骤继续。实例已退出、目标变化，或必须重新引导才会加载修复时，按 c 先
   核验修复后的启动镜像，再启动并确认新实例。重建或部署未成功时，不运行依赖新产物的
   测试，按反馈流程记录待验证。通过验证的证据须对应修复后的实际产物和实际设备。

## b. 设备准备（仅验证范围=device）

- **刷机适用条件（所有入口共用）**：automatic daily flashing requires scope `device`, confirmed `验证产品=rk3568`, and non-empty `device_flash_skill`. The concrete or abstract build name is not part of this test. Keep the selected-device and explicit overwrite confirmation requirements. Other validation products need a confirmed supported manual preparation method. Reuse successful preparation only for the same validation product and actual device.
- **设备选择与准备（含 test-only）**：运行 `hdc list targets` 获取候选。排除已知模拟器，并核实候选是与
  `验证产品` 匹配的实体设备。复用该验证产品下用户已经确认且仍然匹配的实际设备 ID；否则询问并等待用户
  确认。列表只有一个候选时同样执行这个规则。身份不明、产品不匹配或设备变更时，在确认前不准备、不推包。
  - `existing`：使用设备现有版本，记录实际设备 ID。不要再次询问 daily，也不要声称现有版本是今日 daily。
  - `daily`：复用同一目标设备已经成功的准备证据；否则按计划的 `设备版本准备方式` 执行。自动刷机前复核
    rk3568 和配置条件，传入已确认的设备 ID，并取得覆盖确认。不能自动刷机时，先确认受支持的手动准备方案
    并更新计划；手动准备必须等待用户确认完成。准备失败或未完成时保持待验证，不能自动改用现有版本。
    刷机后重新检测并确认设备身份，记录准备结果和实际设备 ID。
  - 没有可用实体设备或查询失败时，询问是输入设备地址还是跳过设备验证。若用户提供地址，使用
    `hdc tconn <ip>:<port>`（端口缺省为 7777）连接，重新枚举后沿用同一身份和策略确认流程。
    连接失败时说明结果并询问重试或跳过。选择跳过时结束 b，并按上文规则记录未验证，只允许
    d 中独立于设备的主机检查。
- **产物检查（有编译产物时）**：从配置的 `device_so_dirs` 或 `out/<编译产品>/` 查找该 Task 的
  `.so` 文件。结合编译日志、输出清单或已确认的目录结构核对来源、组件及架构，确认与实际目标兼容；
  产物有歧义时先确认。记录实际路径、构建证据及目标绑定。
- **部署与服务重启（有编译产物时）**：对已确认设备使用 `hdc -t <device-id>` 运行 `shell mount -o rw,remount /` 后用
  `file send <local> /system/lib/<name>` 推包（按目标布局选择 `/system/lib64/`），再重启服务。优先用配置的 `device_service_restart` 并替换 `{service}`，从组件 init 配置或 systemd
  单元解析服务名，始终绑定已确认设备。仅在推送成功且无法确定服务名时，才用
  `hdc -t <device-id> shell reboot` 重启该设备，等待并核实同一目标恢复，记录回退原因。
  Test-only Task 跳过产物检查、remount、推包与服务重启。

## c. 模拟器启动与 hdc 推包（仅验证范围=emulator）

使用独立确认的验证产品。需要启动实例时执行步骤 1–4；符合上文复用条件的实例继续使用
其已确认 ID，直接执行适用的部署步骤。

**启动前检查**：每次启动或重启前，按计划的 `模拟器命令` 核对实际加载的内核、ramdisk
等启动镜像及其构建证据。Red 使用基线镜像；实现后的验证须确保镜像包含需要在启动时加载
的修复。单模块编译完成不代表已更新镜像。若所需镜像缺失或无法证实其适用于本轮验证，
用环境表中已确认的全量编译或打包命令生成镜像，再核对启动命令所用路径和产物来源。
在 Actual Result 记录实际镜像路径和构建证据。仍无法生成或核验时，按反馈流程记录
待验证，暂停启动和依赖该镜像的测试。

1. 按启动方式记录 `hdc list targets` 中的在线 ID 作为基线。开始重启时，旧绑定失效。
   - **冷启动**：在启动前记录基线。
   - **分步重启**：用本流程记录的进程或托管实例标识定位已确认的旧模拟器，只停止该实例。
     核实旧实例已退出，再用成功的 HDC 枚举确认其端点已离线，然后记录基线。
   - **脚本一键重启**：仅在计划的 `模拟器命令` 明确支持停启并能提供可核验记录时使用。
     运行前记录基线及已确认的旧实例标识、HDC ID。
2. 运行计划的 `模拟器命令` 启动 QEMU 或执行脚本重启。核对并记录新实例的启动证据和
   实际使用的已核验镜像。重启还须核实旧实例已退出，并能把新实例关联到实际 HDC 端点，
   例如通过受管进程的退出与启动记录，或含实例标识、镜像和端点的托管日志。
3. 每 10 秒成功枚举后，把本轮启动的在线端点列为候选。冷启动只从基线外选择；重启时，
   新实例对应的在线端点可以沿用旧 HDC ID，其他基线 ID 即使重连也不算候选。HDC 枚举
   只用于确认连接就绪，离线再上线不能证明实例已重启。停启证据缺失或 3 分钟内没有可信
   候选时，按反馈流程记录待验证，不执行依赖该目标的命令。
4. 列出候选并等待用户明确确认，即使只有一个候选或沿用了旧 ID：
   ```
   本次模拟器启动或重启检测到以下候选设备：
     1) <device-id-1>
     2) <device-id-2>  （如有）
   请确认哪个是本次启动的模拟器？输入序号：
   ```
   在 Actual Result 记录启动或重启证据及用户确认的 ID。后续 hdc 命令只绑定该
   `<emulator-id>`。
5. For Tasks with build outputs, run `hdc -t <emulator-id> shell mount -o rw,remount /` first to make the filesystem writable.
6. For Tasks with build outputs, apply b's artifact checks only (provenance, path and architecture) against this validation product, record actual paths and emulator ID, then push the confirmed files with `hdc -t <emulator-id> file send <local> /system/lib/<name>` (or `/system/lib64/`). Test-only Tasks skip pushing and service restarts.
7. After pushing build outputs, restart the relevant service: `hdc -t <emulator-id> shell <restart-command>`.

Only `emulator` uses this step; the build product name never selects this branch.
