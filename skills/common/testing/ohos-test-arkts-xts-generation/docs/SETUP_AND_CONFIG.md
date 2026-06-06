# 安装配置与子系统配置体系

## 一、快速开始

### 前置条件

| 依赖 | 必需 | 说明 |
|------|:----:|------|
| XTS 测试仓库 | 是 | 如 `D:\xts_acts_0414` |
| SDK 接口定义 | 是 | 如 `D:\interface_sdk-js\ets` |
| DevEco Studio | 推荐 | 提供 Node.js、Java、hvigor |
| APICoverageDetector | 可选 | 覆盖率扫描工具，仅 Windows/WSL |

### 安装

将技能目录放到工具的 skills 路径下：

- opencode: `{用户主目录}\.opencode\skills\ohos-test-arkts-xts-generation\`
- Claude Code: `{用户主目录}\.claude\skills\ohos-test-arkts-xts-generation\`

### 首次使用

首次使用时技能会自动创建配置文件（`.oh-xts-config.json`）并询问路径。

**Windows 示例**：
```
用户：帮我为 media.createAVRecorder() 生成XTS测试用例，
     目标测试套是 D:\xts_acts_0414\multimedia\media\，语法类型是ets1.1动态语法

技能：我需要一些环境信息来配置工具：
      必填：
      1. XTS 测试仓库路径（如 D:\xts_acts_0414）          ← 从你的消息中自动提取
      2. SDK 接口定义路径（如 D:\interface_sdk-js\ets）
      可选（推荐填写）：
      3. DevEco Studio 安装路径
      4. APICoverageDetector 安装路径
      5. 静态编译 Hvigor 路径（仅 ArkTS-Sta 需要）

用户：SDK 在 D:\interface_sdk-js\ets，DevEco Studio 在 D:\DevEco Studio

技能：✅ 配置完成，已自动推导 hvigor/Java/Node.js 路径。
```

**Linux 示例**：
```
用户：帮我为 ability 模块生成XTS测试，OH 根目录是 /home/user/openharmony

技能：已从 OH_ROOT 自动推导 XTS/SDK/文档路径，配置完成。
```

也可以手动创建：将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json` 并填写路径。

### 常见配置问题

**没有 APICoverageDetector？** 不影响使用，技能会提示选择跳过扫描或提供扫描结果。

**如何使用覆盖率扫描功能？** 需要准备两样东西：
1. **APICoverageDetector 工具**：仅支持 Windows/WSL，配置 `scan_tool_root` 路径即可
2. **ohos-sdk-full SDK 包**：从日构建下载 `ohos-sdk-full_Dyn_Sta`，解压后将其 `ets` 目录配置为 `sdk_path`。下载地址：https://dcp.openharmony.cn/workbench/cicd/dailybuild/detail/component

> **注意**：日构建 SDK 解压后 `ets` 目录下为 `dynamic/` 和 `static/`，扫描环境搭建时 `manage_scan_env.py` 会自动将其重命名为 `ets1.1/` 和 `ets1.2/`。

**ets_version 怎么选？** 默认 `["ets1.1"]`（动态语法）。需要静态语法时改为 `["ets1.2"]`。

---

## 二、跨平台配置

### 配置文件结构

`.oh-xts-config.json` 使用扁平 JSON 结构：

```json
{
  "platform": "wsl",
  "OH_ROOT": "/path/to/ohos",
  "scan_tool_root": "/mnt/d/APICoverageDetector",
  "skill_root": "/path/to/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "xts_acts_path": "[auto-derived from OH_ROOT if not set]",
  "sdk_path": "[auto-derived from OH_ROOT if not set]",
  "sdk_local_path": "[wsl only] Linux local SDK path",
  "use_builtin_sdk": true,
  "deveco_studio_path": "[windows only]",
  "hvigor_path_1.1": "[windows only]",
  "hvigor_path_1.2": "[windows only]",
  "docs_path": "[auto-derived from OH_ROOT if not set]"
}
```

### 字段说明

| 字段 | 必需 | 适用平台 | 说明 |
|------|------|---------|------|
| **platform** | **必需** | 全部 | 运行环境：`"wsl"` / `"windows"` / `"linux"` |
| **OH_ROOT** | **必需** | 全部 | OpenHarmony 根目录 |
| **scan_tool_root** | **必需** | 全部 | APICoverageDetector 工具路径 |
| **skill_root** | **必需** | 全部 | 本 skill 的安装路径 |
| **ets_version** | **必需** | 全部 | ETS 版本列表，如 `["ets1.1"]` |
| **xts_acts_path** | 可选 | 全部 | 未设置时从 `OH_ROOT` 自动推导 |
| **sdk_path** | 可选 | 全部 | 未设置时从 `OH_ROOT` 自动推导 |
| **sdk_local_path** | 可选 | WSL | WSL 本地 SDK 路径（Linux 格式） |
| **deveco_studio_path** | 可选 | Windows | 自动推导 Java 和 Node.js 路径 |
| **hvigor_path_1.1** | 可选 | Windows | ArkTS-Dyn 构建工具路径 |
| **hvigor_path_1.2** | 可选 | Windows | ArkTS-Sta 构建工具路径 |

### 路径自动推导规则

| 字段 | 推导规则 | 示例 |
|------|---------|------|
| **xts_acts_path** | `${OH_ROOT}/xts/acts` | `/home/user/ohos/xts/acts` |
| **sdk_path** | `${OH_ROOT}/sdk` | `/home/user/ohos/sdk` |
| **docs_path** | `${OH_ROOT}/docs` | `/home/user/ohos/docs` |

优先级：显式配置 > 自动推导。

### 运行环境

| 环境 | `platform` 值 | APICoverageDetector | 路径格式 | 检测方式 |
|------|-------------|---------------------|---------|---------|
| **Windows 原生** | `windows` | 直接运行 `.exe` | `D:\path\to\...` | `sys.platform == 'win32'` |
| **WSL** | `wsl` | 通过 `/mnt/d/...` 调用 `.exe` | `/mnt/d/path/to/...` | `/proc/version` 含 `microsoft` |
| **纯 Linux** | `linux` | 不可用 | `/home/user/...` | `sys.platform == 'linux'` |

### hvigor 版本化配置

hvigor 是 DevEco Studio 的构建工具，ArkTS-Dyn 和 ArkTS-Sta 使用不同版本：
- `hvigor_path_1.1`：ArkTS-Dyn 动态语法编译
- `hvigor_path_1.2`：ArkTS-Sta 静态语法编译
- 两者包含相同可执行文件：`hvigorw.bat` (Windows) / `hvigorw.sh` (Linux)

查找路径：DevEco Studio → `File` → `Settings` → `Build Tools` → 查看 Hvigor Path。

### 平台配置示例

**Windows**：
```json
{
  "platform": "windows",
  "OH_ROOT": "D:\\path\\to\\ohos",
  "scan_tool_root": "D:\\path\\to\\APICoverageDetector",
  "skill_root": "D:\\path\\to\\skills\\ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "sdk_path": "D:\\path\\to\\sdk\\openharmony\\ets-windows-x64-26.0.0.20-Beta",
  "deveco_studio_path": "D:\\path\\to\\DevEco Studio",
  "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
  "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin",
  "use_builtin_sdk": true
}
```

**Linux**：
```json
{
  "platform": "linux",
  "OH_ROOT": "/home/user/openharmony",
  "scan_tool_root": "/home/user/APICoverageDetector",
  "skill_root": "/home/user/.opencode/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "use_builtin_sdk": true
}
```

**WSL**：
```json
{
  "platform": "wsl",
  "OH_ROOT": "/home/chen/ohos",
  "scan_tool_root": "/mnt/d/APICoverageDetector",
  "skill_root": "/home/chen/.opencode/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "sdk_local_path": "/home/chen/.sdk/ets",
  "use_builtin_sdk": true
}
```

WSL 路径解析规则（优先级从高到低）：显式配置 → `OH_ROOT` 推导 → `sdk_local_path`。

### 路径格式注意事项

1. **不要混合路径分隔符**：`"D:/work\\xts_acts"` ❌
2. **JSON 中反斜杠需双重转义**：`"D:\\work\\xts_acts"` ✅
3. **路径长度限制**：Windows 最大 260 字符（推荐 APICoverageDetector 放磁盘根目录如 `D:\APICoverageDetector`）

### 配置验证

```bash
python scripts/config_validator.py
```

验证器根据 `platform` 字段选择对应的验证逻辑，检查所有路径是否存在且可访问。

### WSL 专项故障排除

**WSL 下 .exe 无法执行**：
```bash
cat /proc/sys/fs/binfmt_misc/WSLInterop  # 确认 interop 启用
# 若未启用，检查 /etc/wsl.conf：
# [interop]
# enabled=true
# 重启 WSL：PowerShell 中运行 wsl.exe --shutdown
```

**WSL 下 /mnt/ 路径不可访问**：
```bash
ls /mnt/d/  # 检查挂载
# 手动挂载：sudo mkdir -p /mnt/d && sudo mount -t drvfs D: /mnt/d
```

---

## 三、子系统配置体系

### 设计理念

采用分层配置系统，从通用到特化多级继承：

```
通用配置 (_common.md)           — 所有子系统共享的基础规范
      ↓ 继承
子系统配置 ({Subsystem}/_common.md) — 子系统特有规则、模块映射
      ↓ 继承
模块配置 ({Subsystem}/{Module}.md)  — 模块特有规则、API 列表
```

### 配置优先级

```
用户自定义配置 > 模块配置 > 子系统配置 > 通用配置
```

### 已有子系统配置

| 子系统 | 配置路径 | 说明 |
|--------|---------|------|
| ArkUI | `references/subsystems/ArkUI/` | Component、Animator、Router 等模块 |
| ArkWeb | `references/subsystems/ArkWeb/` | Web、WebViewController 模块 |
| testfwk | `references/subsystems/testfwk/` | UiTest、JsUnit、PerfTest 模块 |
| ArkTS | `references/subsystems/ArkTS/` | 特殊规则：string 空字符串是合法参数 |

### 创建新子系统配置

#### 步骤 1：创建子系统目录

```bash
mkdir -p references/subsystems/{SubsystemName}
```

#### 步骤 2：创建子系统通用配置

文件：`references/subsystems/{SubsystemName}/_common.md`

```markdown
# {子系统名称} 子系统通用配置

> **子系统信息**
> - 名称: {子系统英文名}
> - Kit包: @kit.{KitName}
> - 测试路径: test/xts/acts/{子系统}/

## 一、子系统通用配置

### 1.1 API Kit 映射
\```typescript
import { APIName } from '@kit.{KitName}';
\```

### 1.2 模块映射配置
| 模块名称 | API 声明文件 | 说明 |
|---------|-------------|------|
| Module1 | @ohos.module1.d.ts | 模块1说明 |

## 二、子系统通用测试规则
[适用于该子系统所有模块的测试规则]
```

#### 步骤 3：创建模块配置（可选）

文件：`references/subsystems/{SubsystemName}/{ModuleName}.md`

```markdown
# {模块名称} 模块配置

> **模块信息**
> - 所属子系统: {子系统名称}
> - API 声明文件: @ohos.{模块}.d.ts

## 一、模块特有 API 列表
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| API1 | API说明 | LEVEL0 |
```
