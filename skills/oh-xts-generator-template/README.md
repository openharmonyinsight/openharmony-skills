# oh-xts-generator-template

> **OpenHarmony XTS 测试用例通用生成模板**

## 快速开始

```bash
请使用 oh-xts-generator-template 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
```

## 核心功能

- **API 解析**：解析 `.d.ts` 文件，提取接口、方法、参数信息
- **智能测试生成**：根据测试策略自动生成符合 XTS 规范的测试用例
- **测试设计文档生成**：同步生成结构化的测试设计文档
- **测试覆盖分析**：分析现有测试文件，识别已覆盖和未覆盖的API

## 使用场景

- 为新 API 生成完整的测试套件
- 分析现有测试的覆盖情况
- 各子系统定制化测试生成

> 📖 **详细使用方式**: [docs/USAGE.md](./docs/USAGE.md)

## 模块架构

四层模块化设计，可根据任务需求按需加载：
- **L1_Framework**: 框架和规范层
- **L2_Analysis**: 分析层（API解析、覆盖率分析）
- **L3_Generation**: 生成层（测试用例、设计文档生成）
- **L4_Build**: 构建层（编译指南）

```
oh-xts-generator-template/
├── modules/
│   ├── L1_Framework/            # 框架层（必须加载）
│   │   ├── hypium_framework.md  # Hypium框架知识
│   │   ├── arkts_standards.md   # ArkTS语法规范
│   │   ├── test_conventions.md  # 测试约定
│   │   └── uitest_framework.md  # UiTest框架（可选）
│   ├── L2_Analysis/             # 分析层（按需加载）
│   │   ├── api_parser.md        # API定义解析
│   │   ├── project_parser.md    # 工程配置解析
│   │   ├── coverage_analyzer.md # 测试覆盖分析
│   │   └── doc_reader.md        # 文档阅读
│   ├── L3_Generation/           # 生成层（按需加载）
│   │   ├── test_generator.md    # 测试生成策略
│   │   ├── design_doc_generator.md # 测试设计文档生成
│   │   ├── templates.md         # 代码模板库
│   │   └── examples/           # 示例文件
│   └── L4_Build/                # 构建层（按需加载）
│       ├── build_workflow_linux.md    # Linux编译工作流
│       ├── build_workflow_windows.md  # Windows编译工作流
│       ├── linux_compile_env_setup.md  # Linux环境准备
│       ├── linux_prebuild_cleanup.md   # 预编译清理
│       └── linux_compile_troubleshooting.md # 问题排查
├── scripts/                     # 辅助工具集
│   └── read_excel.py          # Excel文件读取工具
└── references/
    └── subsystems/              # 子系统配置 ⭐
        ├── _common.md           # 通用配置
        └── {SubsystemName}/   # 子系统配置
```

## 子系统支持

| 子系统 | Kit 包 | 状态 |
|--------|--------|------|
| ArkUI | @kit.ArkUI | ✅ 完整 |
| ArkWeb | @kit.ArkWeb | ✅ 完整 |
| testfwk | @kit.TestKit | ✅ 完整 |
| Storage | @kit.CoreFileKit | ✅ 完整 |

## 触发关键词

- `XTS`
- `测试生成`
- `用例生成`
- `测试用例`
- `用例生成`
- `测试用例`
- `测试设计`

**次要关键词**：
- `API测试`
- `测试设计文档`
- `测试覆盖分析`
- `OpenHarmony测试`

**平台关键词**：
- `OpenHarmony`
- `ArkTS`
- `ArkUI`
- `ArkWeb`

## 文档

- **完整技能说明**: [SKILL.md](./SKILL.md)
- **详细使用指南**: [docs/USAGE.md](./docs/USAGE.md)
- **配置说明**: [docs/CONFIG.md](./docs/CONFIG.md)
- **故障排除**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

## 辅助工具

### Excel文件读取工具 (scripts/read_excel.py)

用于读取覆盖率报告Excel文件并转换为可处理的格式。

**功能特性**：
- 读取Excel文件所有行数据
- 转换为CSV格式输出
- 转换为JSON格式输出
- 命令行接口支持
- 支持输出到文件或控制台

**使用示例**：

```bash
# 读取并打印为表格格式（默认）
python3 scripts/read_excel.py Book1.xlsx

# 读取并输出为CSV格式
python3 scripts/read_excel.py Book1.xlsx -f csv

# 读取并输出为JSON格式，保存到文件
python3 scripts/read_excel.py Book1.xlsx -f json -o output.json
```

**命令行参数**：
- `-f, --format`: 输出格式 (table/csv/json, 默认: table)
- `-o, --output`: 输出文件路径 (可选，默认输出到控制台)

**依赖要求**：
- Python >= 3.6
- openpyxl 库

**安装依赖**：
```bash
pip3 install openpyxl
```

### Group清理工具 (scripts/cleanup_group.sh)

用于清理测试套的编译缓存，支持Group和单个测试套清理。

**功能特性**：
- 解析BUILD.gn获取测试套列表
- 逐个清理测试套缓存
- 清理.hvigor, build, entry/build, oh_modules
- 清理oh-package-lock.json5, local.properties
- 清理OH_ROOT/out目录
- 提供清理统计信息
- 支持Group和单个测试套清理

**使用示例**：

```bash
# 清理testfwk子系统的所有测试套
~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh /mnt/data/c00810129/oh_0130 testfwk

# 清理arkui子系统的所有测试套
~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh /mnt/data/c00810129/oh_0130 arkui

# 使用默认参数（清理testfwk）
~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh
```

**命令行参数**：
- `OH_ROOT`: OpenHarmony工程根目录路径（默认: /mnt/data/c00810129/oh_0130）
- `subsystem`: 子系统名称（默认: testfwk），可选值: testfwk, arkui等

**清理的目录和文件**：
- `.hvigor` - Hvigor构建缓存
- `build/` - 模块编译缓存
- `entry/build/` - Entry模块构建缓存
- `oh_modules/` - OHPM依赖模块缓存
- `oh-package-lock.json5` - OHPM依赖锁文件
- `local.properties` - 本地配置文件
- `out/` - 编译输出目录（OH_ROOT下）

**注意事项**：
- ⚠️ 重要：严格按照脚本执行，避免误删系统编译环境
- 清理前确认当前工作目录
- 清理后验证`OH_ROOT/build`目录仍然存在

**依赖要求**：
- bash
- grep, sed, cut, sort, uniq

**相关文档**：
- [预编译清理指南](./modules/L4_Build/linux_prebuild_cleanup.md)
- [Linux编译工作流](./modules/L4_Build/build_workflow_linux.md)

**命令行参数**：
- `-f, --format`: 输出格式 (table/csv/json, 默认: table)
- `-o, --output`: 输出文件路径 (可选，默认输出到控制台)

**依赖要求**：
- Python >= 3.6
- openpyxl 库

**安装依赖**：
```bash
pip3 install openpyxl
```

## 版本

- **当前版本**: 3.0.0 (2026-02-28)
- **完整版本历史**: [CHANGELOG.md](./CHANGELOG.md)
