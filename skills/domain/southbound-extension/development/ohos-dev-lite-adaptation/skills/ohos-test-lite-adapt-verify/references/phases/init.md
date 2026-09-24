# 阶段 0 · init — 环境初始化

本阶段是验证工作流的入口。设计目标：**任何人换台机器/换芯片，跑一遍即可就绪**。

核心手段：**探测候选值 → 确认 → 写入 config**。能自动探测的给真实候选作选项，
不能探测的用现有配置值或引导用户输入。

完成后产出：有效的连接配置、选定的设备 profile、`xts_test/` 产物目录、
校准好的 `ohos-ci-lite-deploy-burn/config.json`。

**前置**：无。本阶段是整个工作流的起点。

**约定路径**：

- **项目根**：agent 当前工作目录 `<PROJECT_ROOT>`
- **产物目录**：`<PROJECT_ROOT>/xts_test/`（默认，可由用户改为外部路径）
- **ohos-ci-lite-deploy-burn**：`skills/ohos-ci-lite-deploy-burn/`
- **config 文件**：`ohos-ci-lite-deploy-burn/config.json`
- **config 模板**：`ohos-ci-lite-deploy-burn/config.example.json`

## 执行步骤

### Step 1 · 检查本地工具链

- `python --version`（需 ≥ 3.7）
- `python -c "import serial; print(serial.__version__)"`（本地烧录模式需要）
- 可选：`node --version`、`openspec --version`（有则记录，无也不阻塞）

任一缺失：给安装命令提示，等用户装好再继续。

**已知坑**：
- Python 3.8 自带 pip 过旧，后续 `pip install paramiko` 等可能报 TomlError。
  遇到先 `python -m pip install --upgrade pip` 升级再装。

### Step 2 · 选择连接方式

询问用户本次验证使用的连接方式：

| 方式 | 适用场景 | 需要的信息 |
|------|---------|-----------|
| **SSH** | 远程编译服务器 | host / port / user / code_dir |
| **Local** | 本地 / WSL2 编译 | code_dir 本地路径 |
| **Custom** | 其他方式 | 用户自述 |

根据用户选择，进入对应子流程：

#### SSH 模式
1. 读现有 `config.json`（若存在），取 `remote.host/port/user/code_dir` 作为推荐默认值
2. 探测本地 COM 口 + USB 芯片（用于后续烧录）：
   ```bash
   python -c "from serial.tools import list_ports; [print(f'{p.device}\t{p.description}\t{p.hwid}') for p in list_ports.comports()]"
   ```
3. 多轮确认：host / port / user / code_dir / com_port / usb_chip
4. 配置 SSH 免密（测试连通性）：
   ```bash
   ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=8 -p <port> <user>@<host> echo ok
   ```

#### Local 模式
1. 确认本地 code_dir 路径
2. 探测 COM 口（同上）
3. 确认编译环境（hb / python / gcc 在 PATH 中）

#### Custom 模式
1. 请用户描述连接方式和可用操作
2. 记录到 config 的 `connection.custom` 字段

### Step 3 · 选择目标芯片 / 设备

列出 `ohos-ci-lite-deploy-burn/references/devices/` 下可用的设备 profile：

```bash
# 列出所有可用设备
ls skills/ohos-ci-lite-deploy-burn/references/devices/*.json
```

请用户选择：
- 有匹配的 profile → 直接使用
- 无匹配 → 引导用户基于 `config.example.json` 创建新 profile

确认后，将 `device.profile` 写入 config.json。

从设备 profile 读取硬件上限（RAM / Flash 大小），记录备用。

### Step 4 · 选择测试策略

**这是本 skill 的核心差异化点——用户决定怎么验证。**

询问用户本次验证使用的测试策略：

| 策略 | 说明 | 产出 |
|------|------|------|
| **XTS** | OpenHarmony XTS 测试套件 | PASS/FAIL 统计 + 测试日志 |
| **Unit Test** | 模块级单元测试 | 测试通过率 |
| **Integration** | 集成测试（多模块联动） | 功能验证结果 |
| **Manual** | 手动测试 checklist | 人工确认结果 |
| **Custom** | 用户自定义测试方案 | 用户定义的格式 |

用户选择后：
- 写入 config.json 的 `test.strategy` 字段
- 若选择 XTS，额外确认 XTS 子集范围（acts / dcts / 全量 / 指定模块）
- 若选择 Custom，请用户描述测试方案要点

> **重要**：此选择可在后续 `verify` 阶段重新调整。初始选择不影响已完成的 init/explore/analyze/implement 工作。

### Step 4.5 · XTS 验证环境配置（仅 XTS 策略触发）

> 当 Step 4 选了 **XTS** 策略时执行。这是验证前的环境准备——解压 acts + 配 COM + 备 HiBurn.exe，做完让用户确认才进 verify。

#### 4.5.1 解压 acts（用户交互）

向用户问询：

> 已有 `acts.zip`（XTS 测试套件）。要不要帮你解压？
> - 要 → 我解压到 `<产物目录>/acts/`（或你指定目录）
> - 不要 → 跳过（你已解压或自行处理）

用户选"要" → 解压 `acts.zip` 到产物目录下的 `acts/`，记录解压路径（后续 `user_config.xml` 在 `acts/config/user_config.xml`）。

#### 4.5.2 验证环境配置协助（用户交互）

向用户问询：

> 要不要让工作流协助处理验证环境配置（COM 端口写入 user_config.xml + 备 HiBurn.exe 到 tools）？
> - 要 → 我来检测+配置
> - 不要 → 跳过，你自行配置

用户选"要" → 执行下面 (a)(b)：

**(a) 检测板子 COM 端口 → 写入 user_config.xml**

```bash
# 探测当前连接的 COM 口
python -c "from serial.tools import list_ports; [print(f'{p.device}\t{p.description}') for p in list_ports.comports()]"
```

- 单端口 → 直接用，写入 `acts/config/user_config.xml` 的设备 COM 字段
- 多端口 → 列出给用户选，选完写入
- 写入后回显 user_config.xml 的 COM 配置让用户确认

**(b) 备 HiBurn.exe 到 tools/**

检查 `<产物目录>/tools/`（或 acts 的 tools 目录）是否有 `HiBurn.exe`：
- 检测系统里 HiBurn.exe 的位置（不随 plugin 分发；全盘搜 `where HiBurn.exe` / 常见路径）
- **检测到** → 复制一份到 tools 目录
- **检测不到** → 提示用户："找不到 HiBurn.exe，请给路径，我复制一份进去"
- 复制完确认 tools/HiBurn.exe 就位

#### 4.5.3 汇报 + 用户确认

把 4.5.1/4.5.2 的操作结果汇报给用户：

```
XTS 验证环境配置完成：
- acts 解压：<路径>（或"未解压，用户自行处理"）
- COM 端口：<COMx>（已写入 user_config.xml）
- HiBurn.exe：已复制到 <tools路径>（或"未找到，待用户提供"）
```

请用户确认配置是否正确：
- **正确** → 进下一步 verify 阶段（跑 XTS）
- **不对** → 按用户指正重新配置（重跑 4.5.2 的对应项）

> 用户确认前**不进 verify**。这一步是验证前的最后一道环境校准。

### Step 5 · 校准 config.json & 初始化产物目录

1. 将 Step 2~4 的确认值写入 `ohos-ci-lite-deploy-burn/config.json`
2. 用 `config.example.json` 作模板对照，确保必填字段齐全
3. 创建 `xts_test/` 目录结构：
   ```
   xts_test/
   ├── reports/          # 基线、验证结果、MAP 对比
   ├── proposals/        # 分析提案（若有 openspec 或手动提案）
   └── lessons.md        # 经验沉淀（追加式）
   ```
4. 若使用 openspec：初始化 `xts_test/openspec/` 工程（可选）

### Step 6 · 连通性验证

执行一次最小化验证，确认配置可用：

- **SSH 模式**：`ssh <user>@<host> -p <port> "ls <code_dir>"` 确认远程代码可达
- **Local 模式**：`ls <code_dir>` 确认本地代码可达
- **烧录相关**：若选择了需要烧录的测试策略，确认 COM 口可访问

## 阶段收尾

确认清单：
- [ ] 工具链满足最低要求（Python ≥ 3.7）
- [ ] 连接方式已配置且连通性验证通过
- [ ] 目标设备 profile 已选定（含硬件上限信息）
- [ ] 测试策略已选定（写入 config）
- [ ] **若 XTS 策略**：Step 4.5 环境配置完成且用户确认（acts 解压 + COM→user_config.xml + HiBurn.exe 就位）
- [ ] `config.json` 校准完毕（与 config.example.json 对照无缺失字段）
- [ ] `xts_test/` 产物目录已创建

回显当前配置摘要，提示用户下一阶段（explore，见 `references/phases/explore.md`）。
