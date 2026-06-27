## Phase 0: 初始化配置文件

---

### 触发条件

读取 `{skill_root}/.oh-xts-config.json`：

| 状态 | 操作 |
|------|------|
| 文件存在且可读取 | ✅ 跳过 Phase 0，直接进入 Phase 1 |
| 文件不存在 | ❌ 执行 Phase 0 |
| 用户要求修改配置 | ❌ 执行 Phase 0 |

---

### 步骤 1: 创建配置文件

将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json`：

```bash
cp {skill_root}/.oh-xts-config.example.json {skill_root}/.oh-xts-config.json
```

---

### 步骤 2: 检测平台

使用 `platform.system()` 或 `uname` 判断当前环境：

| 检测结果 | `platform` 字段 | 说明 |
|---------|-----------------|------|
| Windows 原生 | `"windows"` | 直接使用 Windows 路径 |
| WSL（Linux 内核含 microsoft） | `"wsl"` | 通过 `/mnt/d/...` 访问 Windows 文件 |
| 纯 Linux（计算云/远程服务器） | `"linux"` | 无 Windows 工具支持 |

---

### 步骤 3: 交互式获取路径

根据步骤 2 检测到的平台，向用户询问必要路径信息。

#### Linux / WSL 环境

```
我需要一些环境信息来配置工具：

必填：
1. OpenHarmony 根目录（如 /home/user/openharmony）

其他路径将从根目录自动推导，无需手动配置。

注意：APICoverageDetector 支持 Windows 原生和 WSL 环境（通过 /mnt/d/... 路径调用 .exe）。仅 Linux 计算云/远程服务器不可用，可提供已有扫描结果。
```

**自动推导规则**（Linux/WSL，从 `OH_ROOT` 推导）：

| 字段 | 推导路径 | 说明 |
|------|---------|------|
| `xts_acts_path` | `{OH_ROOT}/test/xts/acts` | XTS 测试仓库 |
| `interface_path` | `{OH_ROOT}/interface/sdk-js` | 源接口声明目录 |
| `sdk_local_path` | `{OH_ROOT}/prebuilts/ohos-sdk/linux/{ver}/ets` | 编译后 SDK 产物 |
| `docs_path` | `{OH_ROOT}/docs` | 文档目录 |

推导路径不存在时向用户确认实际位置。

#### Windows 环境

```
我需要一些环境信息来配置工具：

必填：
1. XTS 测试仓库路径（如 D:\xts_acts_0414）
2. SDK 接口定义路径（如 D:\interface_sdk-js\ets）

可选（推荐填写，可解锁编译验证和覆盖率扫描功能）：
3. DevEco Studio 安装路径（如 D:\DevEco Studio，填后自动配置 Java/Node.js/hvigor）
4. APICoverageDetector 安装路径（如 D:\APICoverageDetector，用于覆盖率扫描）
5. ArkTS-Sta 静态编译 Hvigor 路径（仅做静态语法项目编译时需要）
6. 文档路径（如 D:\docs）

请提供以上路径，我会自动完成配置。不确定的可以跳过，后续再补充。
```

**自动推导规则**（Windows，从 `deveco_studio_path` 推导）：

| 字段 | 推导路径 | 说明 |
|------|---------|------|
| `hvigor_path_1.1` | `{deveco_studio_path}\{DevEco Studio}\tools\hvigor\bin` | 自动检测子目录 |
| Java | `{deveco_studio_path}\{DevEco Studio}\jbr` | — |
| Node.js | `{deveco_studio_path}\{DevEco Studio}\tools\node\node.exe` | — |

无法推导的保持占位符，不阻断流程。

---

### 步骤 4: 写入配置并验证

1. 将所有路径（用户提供的 + 自动推导的）写入 `.oh-xts-config.json`
2. 验证必填路径存在且可访问：

| 平台 | 必须存在 | 建议存在 | 可选 |
|------|---------|---------|------|
| Windows | `xts_acts_path`、`interface_path` | `deveco_studio_path`、`hvigor_path_1.1` | `scan_tool_root`、`hvigor_path_1.2`、`docs_path` |
| Linux/WSL | `OH_ROOT` | — | 其他所有路径（从 `OH_ROOT` 自动推导） |

3. 无效路径给出警告但不阻断流程（用户可能只需要用例生成，不需要编译验证）

完成后执行步骤 5（依赖安装校验），然后自动进入 Phase 1。

---

### 步骤 5: 依赖 Skill 安装与兼容性校验

> 在首次配置完成后，校验依赖 skill 的版本和能力兼容性。

1. 检查 `{skill_root}/.probe_results` 是否存在且修改时间 < 24 小时：
   ```bash
   test -f {skill_root}/.probe_results && find {skill_root}/.probe_results -mmin -1440 | grep -q .
   ```
2. 如果文件不存在或已过期，执行：
   ```bash
   bash {skill_root}/scripts/install_related_skills.sh --check-probes
   ```
3. 读取 `{skill_root}/.probe_results`，根据每行的 status 列采取行动：

| status | 含义 | 行动 |
|--------|------|------|
| `OK` | 版本和探测均通过 | 继续 |
| `WARN_VERSION` | 版本未知但探测通过 | 警告，继续 |
| `MISSING_OPTIONAL` | 可选 skill 未安装 | 警告，相关 Phase 自动降级 |
| `MISSING` | 必选 skill 未安装 | **阻断**：提示运行 `install_related_skills.sh` |
| `VERSION_LOW` | 版本低于 min_version | **阻断**：提示运行 `install_related_skills.sh --force` |
| `FAIL_PROBES` | 探测失败（接口不兼容） | **阻断**：提示运行 `install_related_skills.sh --force` |

4. 阻断时向用户展示具体失败项和建议命令，**不自动执行安装**
5. 将校验结果追加到 `session_issues_{日期}.md`（如已存在）或记录到配置摘要中

完成后自动进入 Phase 1。
