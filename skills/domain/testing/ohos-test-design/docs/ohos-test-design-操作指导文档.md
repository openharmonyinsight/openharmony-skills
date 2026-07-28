# OpenHarmony 测试设计工具(ohos-test-design)操作指导

> **适用对象**:零基础用户,无需编程经验也能按本文档完成操作。同时为进阶用户提供深入的技术原理说明。
>
> **最后更新**:2026-07-15

---

## 目录

1. [工具简介](#1-工具简介)
2. [环境准备](#2-环境准备)
3. [快速开始](#3-快速开始)
4. [执行流程详解](#4-执行流程详解)
5. [XTS测试用例生成](#5-xts测试用例生成)
6. [术语表](#6-术语表)
7. [输出文件与经验库](#7-输出文件与经验库)
8. [常见问题 FAQ](#8-常见问题-faq)
9. [高级用法](#9-高级用法)

---

## 1. 工具简介

### 1.1 这是什么?

`ohos-test-design` 是一个 **AI 驱动的 OpenHarmony 测试设计自动化工具**。它能:

- 自动解析需求文档(Markdown/Word/PDF等) → 生成测试点设计和测试用例
- 一键导出Excel文件
- 为非XTS测试点生成可运行的HarmonyOS Demo应用
- 为XTS测试点生成符合Hypium框架的ArkTS测试用例

### 1.2 工作流程概览

**测试设计流程**:
```
需求文档 ──→ 需求解析 ──→ 测试点生成 ──→ 测试点对抗 ──→ Demo流水线 ──→ 用例细化 ──→ 用例对抗 ──→ 验证导出
  (你提供)     阶段1        阶段2         阶段2Adv       阶段3         阶段4        阶段4Adv      阶段5
```

**XTS测试用例生成流程**:
```
.d.ts API ──→ 配置加载 ──→ 覆盖率扫描 ──→ API解析 ──→ 测试设计 ──→ 用例生成 ──→ 注册 ──→ 验证 ──→ 编译 ──→ 覆盖率验证 ──→ 输出
               Phase1      Phase2      Phase3     Phase4    Phase5/5A/5B  Phase6  Phase7  Phase8  Phase10       Phase11
```

### 1.3 核心原则与架构特点

- **IBO原则**:只提取外部可触发且可验证的行为（Input-Black-box-Output）
- **零推导**:仅提取文档明确描述，不进行业务逻辑推导
- **场景风险驱动**:从场景出发定向生成，高风险(P0)深覆盖，低风险(P2)浅覆盖
- **交付推断**:Phase1区分**测试对象**(变更内容重点测试P0-P3)与**回归对象**(已交付功能回归验证P0+P1)
- **三层知识层级隔离**:domain-knowledge(Phase1)/test-experience(Phase2)/case-refinement(Phase4)各阶段仅读取对应层级
- **验证完整性**:预期结果必须验证到外部可观测效果，不能仅依赖"接口返回成功"
- **脚本固化检查**:覆盖率、对抗评估等关键检查由Python脚本执行，避免AI主观判断

### 1.4 模块架构

| 模块 | 职责 | 位置 |
|------|------|------|
| **ohos-design-test-coordinator** | 主编排器，7阶段测试设计流程 | `skills-refactor/ohos-design-test-coordinator/` |
| **adversary** | 对抗评估规则和策略 | `skills-refactor/ohos-design-test-coordinator/adversary/` |
| **ohos-design-test-demo-pipeline** | Demo生成和编译验证 | `skills-refactor/ohos-design-test-demo-pipeline/` |
| **ohos-design-test-task-manager** | 计时协议和检查点保存恢复 | `skills-refactor/ohos-design-test-task-manager/` |
| **ohos-test-arkts-xts-generation** | XTS测试用例生成器 | `skills-refactor/ohos-test-arkts-xts-generation/` |

**关键架构机制**:
- 规划Agent+执行Agent两轮模式:Phase2/Phase4先由规划Agent匹配经验库+分批规划，再由协调器多轮并行spawn执行Agent(≤4)
- knowledge_match.md三段式:§1领域知识(Phase1创建)+§2测试经验(Phase2追加)+§3用例细化(Phase4追加)
- 17个门控检查点确保流程质量和数据完整性
- Phase3拆分为3个子步骤独立计时，支持检查点中断恢复

---

## 2. 环境准备

| 条件 | 说明 |
|------|------|
| opencode CLI | 已安装opencode命令行工具 |
| AI 模型配置 | opencode已配置可用AI模型 |
| Python 3 + openpyxl + allpairspy | `pip3 install openpyxl allpairspy` |
| Command Line Tools | HarmonyOS NEXT命令行编译工具（Demo编译需要） |
| ohos-test-xts-code-quality | XTS代码质量扫描依赖技能（XTS生成时需要） |

---

## 3. 快速开始

### 第 1 步：准备需求文档

将需求文档放在一个目录中，支持 `.md`（推荐）/ `.docx` / `.pdf` / `.json` / `.yaml`

### 第 2 步：启动 opencode

```bash
cd /Users/yourname/project/req/  # 进入需求文档目录
opencode
```

在opencode对话框中输入 `/ohos-test-design`

### 第 3 步：回答 4 个问题

| 序号 | 问题 | 选项 |
|------|------|------|
| 1 | 输入路径 | ① 当前工作目录 ② 自定义 |
| 2 | 输出路径 | ① 与输入相同 ② 自定义 |
| 3 | 领域选择 | ① 默认（仅通用） ② 领域（通用+领域，AI自动匹配） ③ 自定义 |
| 4 | 用例编号起始值 | ① 默认case_id_temp_001 ② 自定义 |

**第3题分支**：
- **①默认** → 仅加载general/下三层知识目录，无需确认
- **②领域** → 通用固定加载 + AI自动匹配领域层级 + AskUserQuestion确认

**AI领域匹配确认（选择②时）**：

| 选项 | 说明 |
|------|------|
| ① 确认匹配 | 使用AI匹配的领域层级 |
| ② 调整层级 | 选择该领域不同层级深度 |
| ③ 仅通用 | 回退，不加载领域经验库 |
| ④ 自定义路径 | 用户输入路径 |

**检索路径限定**：各阶段仅读取对应知识层级目录（domain-knowledge/Phase1、test-experience/Phase2、case-refinement/Phase4），禁止跨层读取。

---

## 4. 执行流程详解

### 4.1 阶段总览

| 阶段 | 名称 | 需确认？ | 关键特点 |
|------|------|---------|---------|
| 1 | 需求解析(IBO) | **需确认** | IBO解析+交付推断+三层知识匹配domain-knowledge |
| 2 | 测试点生成 | 不达标时确认 | 规划Agent匹配test-experience→协调器多轮并行→脚本合并 |
| 2Adv | 测试点对抗 | **不达标时确认** | 脚本固化+AI语义校验，总分≥80分达标 |
| 3 | Demo流水线 | 编译异常时确认 | 委托ohos-design-test-demo-pipeline，非XTS时执行，XTS全量跳过 |
| 4 | 用例细化 | 不达标时确认 | 规划Agent匹配case-refinement→协调器多轮并行→脚本合并 |
| 4Adv | 用例对抗 | **不达标时确认** | 充分性≥95%/≥98% + AI质量评分≥18分 |
| 5 | 验证与导出 | 自动 | 四维评分≥80 + P0门禁 + Excel导出 + 清理 |

### 4.2 Phase1：需求解析

**做什么**:IBO原则解析需求文档，提取功能需求/业务规则/异常流程/API接口/验收标准/约束条件/非功能需求/可测试性手段/输入条件规格/耦合分析/前置依赖，并执行**交付推断**(区分测试对象与回归对象)。

**知识库调用**:读取domain-knowledge目录，生成knowledge_match.md骨架+§1(交付推断结果+领域知识匹配详情)。

**输出**: `requirement_analysis.md` + `knowledge_match.md`

**确认机制**:自检 → 待确认项答疑(每批≤10个) → 最终确认 → 用户可选"需要优化"则spawn增量修改Agent

**详细规则**:phase1_rules.md(IBO原则、正交判定、ID角色边界、待确认项生成)、phase1_clarify_rules.md(澄清交互)

### 4.3 Phase2：测试点生成

**执行流程**(规划Agent+执行Agent两轮模式):

1. **测试技术预处理**(协调器):调用phase2_testing_technology.py
2. **规划Agent**:Read knowledge_match.md §1.1交付推断 → 匹配test-experience → 追加§2到knowledge_match.md → 分批规划(一个测试对象主单元一个batch)
3. **协调器**:确认knowledge_match.md已更新 → 多轮并行spawn执行Agent(≤4)
4. **执行Agent**:Read knowledge_match.md §1.1+§2 → 每Agent处理一个测试对象主单元 → 生成batch_{id}.md
5. **脚本合并**:merge_batch_mds → test_point_design.md
6. **对抗**:phase2_adversary.py + Agent评分 → 达标进入Phase3 / 不达标循环补充(≤3轮)

**测试对象/回归对象差异化采纳**:

| 对象 | 最深层级-无标注 | 最深层级-[选测] | 父层级-[选测]/无标注 | 优先级 |
|------|----------------|----------------|---------------------|--------|
| 测试对象 | 直接采纳(全部) | 语义匹配(score≥0.6) | 语义匹配 | P0-P3全量 |
| 回归对象 | 直接采纳(全部) | **跳过** | **跳过** | 仅P0+P1 |

**详细规则**:phase2_rules.md(风险分级P0-P3、测试类型判定、执行方式判定、防重复、验证完整性)

### 4.4 Phase2Adv：测试点对抗评估

**三维度评分**(总分≥80达标):

| 维度 | 权重 | 计算 |
|------|------|------|
| 需求覆盖率 | 40分 | (场景覆盖率×0.7 + API覆盖率×0.3) × 40 |
| 关键场景 | 45分 | (脚本基础+深度 + AI补充-AI移除) / 有效满分 × 45 |
| 变异杀死率 | 15分 | (脚本杀死+AI语义杀死) / 变异体总数 × 15 |

**关键场景类型评分**:边界/异常/竞态/特殊/数据持久化各10分(基础5+深度5)，状态转换/组合各5分(仅基础)

**固定值变异过滤**:权限2750、属组3823等固定常量不生成±1变异

**循环规则**:总分<80 → 补充TP-ADD-{NNN} → 重新调用脚本(最多3轮)

**输出**: `phase2_adversary.json` + `adversarial_report.md`(第一部分)

### 4.5 Phase3：Demo流水线

**做什么**:委托ohos-design-test-demo-pipeline为非XTS测试点生成可运行HarmonyOS Demo应用。

| 子阶段 | 输出 | 说明 |
|--------|------|------|
| 子阶段1: UI设计 | demo_design.md | 页面布局+控件设计 |
| 子阶段2: 代码生成 | TestDemo/ + demo_code_manifest.md | ArkUI工程代码，MCP编排器前置查询 |
| 子阶段3: 编译验证 | demo_code_manifest.md(更新) | 自动编译+修复(≤5轮) |

**跳过条件**:所有测试点为XTS → 直接进入Phase4

**编译异常处理**:SDK缺失API/hvigorw未安装 → 独立调用暂停问用户；协调器调用写入摘要由协调器转达

**输出**: `demo_design.md`(主输出) + `TestDemo/` + `demo_code_manifest.md`

### 4.6 Phase4：测试用例细化

**执行流程**(规划Agent+执行Agent两轮模式):

1. **规划Agent**:匹配case-refinement → 追加§3到knowledge_match.md → 分批规划(一个US一个batch)
2. **协调器**:确认knowledge_match.md已更新 → 多轮并行spawn(≤4)
3. **执行Agent**:Read knowledge_match.md §3 → 按测试点范围生成batch_{id}.md
4. **脚本合并**:merge_batch_mds → test_cases.md
5. **对抗**:phase4_adversary.py + Agent评分

**执行方式分流**:XTS→白盒风格(调用接口/验证返回值)；非XTS→黑盒/Demo风格(页面操作/界面验证)

**Demo关联**(非XTS且demo_design.md存在):预置条件"Demo已安装启动，导航至[页面]"；步骤格式"在{区域}的「{控件}」{类型}(id:{ID})中{动作}"

**详细规则**:phase4_rules.md(白盒规范、Demo关联、验证完整性、TP-ADD处理、继承规则)

### 4.7 Phase4Adv：用例对抗评估

**充分性评分**:测试点覆盖率≥95%，关键测试点覆盖率≥98%

**重复检测**:精确重复(≥95%)自动删除；潜在重复(≥80%)AI语义判断合并

**质量评分**(AI评分，≥18分达标):步骤清晰性10分 + 预期明确性10分 + 验证完整性(扣分项:仅依赖"接口返回成功"扣5分)

**循环规则**:不达标 → 补充TC-{NNN}(顺延，禁止TC-ADD) → 重新合并(最多3轮)

**输出**: `phase4_adversary.json` + `adversarial_report.md`(追加第二部分)

### 4.8 Phase5：验证与导出

**四维评分**(综合≥80 + P0=0 通过):

| 维度 | 权重 | 达标 |
|------|------|------|
| 完整性 | 30% | ≥25分 |
| 正确性 | 25% | ≥22分 |
| 可执行性 | 20% | ≥18分 |
| 覆盖率 | 25% | ≥22分 |

**导出**:phase5_export.py生成Excel(18列) → 一致性检查 → 清理临时文件

**输出**: `validation_report.md` + `test_cases.xlsx`

---

## 5. XTS测试用例生成

### 5.1 概述

`ohos-test-arkts-xts-generation` 解析.d.ts API定义，生成符合Hypium框架的XTS测试用例。支持ArkTS-Dyn(ets1.1)和ArkTS-Sta(ets1.2)两种语法模式。

### 5.2 12-Phase工作流概览

| Phase | 名称 | 说明 |
|-------|------|------|
| 0 | Init Config | 仅首次使用，交互式配置引导 |
| 1 | Config & Subsystem | 配置加载、子系统确定 |
| 2 | Coverage Scan | APICoverageDetector扫描未覆盖API |
| 3 | API Parsing | 解析.d.ts获取API详情 |
| **4** | **Test Design** | **强制Phase**，生成.design.md |
| 5A | Demo (UI类) | 仅UI类用例，委托ohos-design-test-demo-pipeline |
| 5 | Cases (非UI类) | 非UI类测试代码生成 |
| 5B | UiTest (UI类) | UiTest代码生成 |
| 6 | Registration | List.test.ets注册 |
| **7** | **Validate** | **强制Phase**，格式验证+代码质量扫描 |
| 8 | Build | 编译验证（支持独立编译模式） |
| 9-11 | Coverage/Output | 可选设备测试、覆盖率验证、输出 |

**Flow判定**:用户说"新API"→Flow C(跳过before扫描)；用户提供覆盖率报告→Flow A；否则→Flow B

### 5.3 Dyn vs Sta 关键差异

| 差异 | ArkTS-Dyn(ets1.1) | ArkTS-Sta(ets1.2) |
|------|-------------------|-------------------|
| hypium导入 | `from "@ohos/hypium"` | `from "{相对路径}/hypium/index"` |
| 401测试 | 生成 | **不生成**(编译时拦截) |
| as any | 可用(不推荐) | **禁止** |
| 测试目录 | `entry/src/ohosTest/` | `entry/src/main/src/test/` |

### 5.4 Anti-Patterns(关键NEVER规则)

- NEVER使用未在.d.ts中声明的接口
- NEVER修改BUILD.gn等项目配置文件
- NEVER跳过Phase 7验证
- NEVER省略@tc注解
- NEVER为@throws声明以外的错误码构造测试(Dyn生成401，Sta不生成)
- NEVER跳过Phase 4测试设计文档
- NEVER为已废弃接口生成测试
- NEVER在Sta项目中使用as any
- NEVER在多版本模式下并行编译Dyn和Sta

### 5.5 依赖技能

| 技能 | 用途 | 必需 |
|------|------|------|
| ohos-test-xts-code-quality | 17条规则代码质量扫描 | Phase7必选 |
| ohos-design-test-demo-pipeline | UI类Demo生成 | 仅UI类用例时 |

---

## 6. 术语表

### 6.1 核心概念

| 术语 | 定义 |
|------|------|
| IBO原则 | 只提取外部可触发且可验证的行为(Input-Black-box-Output) |
| 零推导 | 仅提取文档明确描述，不推导 |
| 场景风险驱动 | 从场景出发定向生成，P0深覆盖P2浅覆盖 |
| 交付推断 | Phase1区分测试对象(变更重点测试)与回归对象(已交付回归验证) |
| 三层知识层级 | domain-knowledge(Phase1)/test-experience(Phase2)/case-refinement(Phase4)，层级隔离 |
| knowledge_match.md | 三段式Markdown:§1领域知识+§2测试经验+§3用例细化 |
| 规划Agent | Phase2/4中负责经验库匹配+分批规划的Agent |
| 验证完整性 | 预期结果必须验证到外部可观测效果 |
| 脚本固化 | 关键检查由Python脚本执行，避免AI主观判断 |

### 6.2 测试设计

| 术语 | 定义 |
|------|------|
| 风险分级 | P0(安全/权限/核心逻辑)→P3(参数校验)，决定测试深度 |
| 测试类型判定 | 由影响后果决定：崩溃→稳定性，权限绕过→安全，默认→功能 |
| 正交/非正交 | 正交=各输入独立影响输出；非正交=依赖其他条件取值 |
| 必测/选测 | 必测=核心每次回归必验证；选测=扩展按需验证 |

### 6.3 执行方式与知识层级ID

| 术语 | 说明 |
|------|------|
| XTS | OpenHarmony接口/组件白盒自动化 |
| 黑盒自动化 | 非XTS默认方式，UI操作+界面验证 |
| DK/TE/CR | 领域知识/测试经验/用例细化条目ID前缀 |
| GK/GE/GR | 通用领域知识/通用测试经验/通用用例细化ID前缀 |

---

## 7. 输出文件与经验库

### 7.1 输出文件清单

| 文件 | 说明 | 需检视 |
|------|------|--------|
| requirement_analysis.md | 需求分析报告 | 是 |
| knowledge_match.md | 知识库匹配结果(三段式，Phase5清理) | 否 |
| test_point_design.md | 测试点设计 | 是 |
| adversarial_report.md | 对抗评估报告(§1+§2) | 否 |
| demo_design.md | Demo UI设计(非XTS) | 否 |
| TestDemo/ + demo_code_manifest.md | Demo工程(非XTS) | 否 |
| test_cases.md | 完整测试用例 | 是 |
| validation_report.md + test_cases.xlsx | 验证报告+Excel | 否 |

### 7.2 三层知识层级目录架构

| 目录名 | 适用阶段 | 内容 | Phase读取路径 |
|--------|---------|------|--------------|
| domain-knowledge | Phase1 | 特性名称与规格 | domain/{domain}/domain-knowledge/**/*.md |
| test-experience | Phase2 | 应该测什么 | domain/{domain}/test-experience/**/*.md |
| case-refinement | Phase4 | 步骤特殊要求 | domain/{domain}/case-refinement/**/*.md |

**层级发现流程(各阶段统一)**:选择知识层级→glob扫描→沿层级从深到浅读取层级名.md→语义匹配(阈值≥0.6)

**领域特性关联**:需求关键词含领域特性名称且条目以该名称为前缀时，score取max(综合score, 0.6)自动达标

**优先级**:需求指定 > 子层级条目 > 父层级 > 通用 > 默认

**知识库继承**:
```
Phase1 → 创建knowledge_match.md骨架+§1(交付推断+领域知识)
Phase2 → 规划Agent追加§2(测试经验匹配结果)
Phase4 → 规划Agent追加§3(用例细化匹配结果)
Phase5 → 删除knowledge_match.md
```

### 7.3 当前支持的领域

| 领域 | 关键词 |
|------|--------|
| ArkUI | ArkUI, arkui |
| 包管理 | 包管理, BundleManager |

### 7.4 经验库条目格式

**domain-knowledge层**:
```
## DK-{领域缩写}-{层级缩写}-{序号}: {特性名称简述}
**特性名称**: {名称及说明}
**规格信息**: {约束、枚举值、取值范围}
```

**test-experience层**:
```
## TE-{领域缩写}-{层级缩写}-{序号}: {涉及特征简述}
**涉及特征**: {关键词}
**需要测试**: [必测]{验证点}(可观测:{方式}) / [选测]{验证点}
**推荐测试技术**: {技术名}
```

**case-refinement层**:
```
## CR-{领域缩写}-{层级缩写}-{序号}: {动作因子简述}
**动作因子**: {触发关键词}
**特殊步骤要求**: {细化要求}
**预期结果细化**: {细化内容}
```

**添加自定义领域**:在domain/下创建三层目录(domain-knowledge/test-experience/case-refinement) → 编写条目 → 编辑config.yaml → 运行experience_library/SKILL.md更新编号和配置

---

## 8. 常见问题 FAQ

**Q1: 需求文档格式要求？** 无严格要求，建议含功能描述、参数范围、错误码、验收标准。

**Q2: 执行出错怎么办？** 自动重试(≤3次指数退避) + 17个门控检查点 + 检查点中断恢复 + P0门禁自动修复(≤1轮)。

**Q3: Demo编译失败？** 自动修复(≤5轮)；SDK缺失/hvigorw未安装→协调器模式下由协调器转达用户。

**Q4: 验证通过条件？** P0=0 且 综合评分≥80/100。

**Q5: 交付推断是什么？** Phase1区分测试对象(spec标注变更的主单元，P0-P3全量)与回归对象(DK匹配的已交付领域功能，仅P0+P1)。

**Q6: 规划Agent和执行Agent区别？** 规划Agent负责经验库匹配+分批规划(不生成内容)；执行Agent按分配范围生成测试点/用例；协调器在规划后接管多轮并行spawn。

**Q7: XTS生成和测试设计区别？** 测试设计从需求文档→Excel；XTS生成从.d.ts API→ArkTS代码。两者独立技能模块。

---

## 9. 高级用法

### 9.1 模块目录结构

**ohos-design-test-coordinator**: SKILL.md + phases/(7骨架) + rules/(11规则) + assets/(6脚本) + experience_library/(三层知识层级) + templates/ + adversary/(对抗评估规则和策略)

**adversary**（ohos-design-test-coordinator子目录）: adversary_rules.md + strategies/(requirement_omission_check + testcase_quality_check) + templates/adversarial_report.md

**ohos-design-test-demo-pipeline**: SKILL.md + phases/(3子阶段) + reference/(api-reference含index.json索引、domains.yaml、template/)

**ohos-design-test-task-manager**: SKILL.md(计时与检查点协议) + templates/ui-templates.md

**ohos-test-arkts-xts-generation**: SKILL.md + prompts/(16个Phase prompt) + docs/(4个参考文档) + references/ + modules/ + scripts/ + .oh-xts-config.example.json

### 9.2 门控检查(17个检查点)

| 检查点 | 触发时机 | 未通过处理 |
|--------|---------|-----------|
| 启动流程缺失 | Phase1前 | 告警终止，重新启动 |
| 输出文档缺失 | 各Phase后 | 重试或终止 |
| 需求澄清未完成 | Phase1→Phase2前 | 执行答疑交互 |
| 数据空值 | Phase1→Phase2前 | 确认文档格式 |
| 规划步骤缺失 | Phase2/4规划后 | 告警终止spawn |
| 质量不达标 | Phase2→Phase4前 | 用户选择继续/优化 |
| 对抗评分不达标 | Phase2Adv/4Adv后 | 自动循环(≤3轮) |
| 编译状态异常 | Phase3后 | AskUserQuestion |
| 导出空字段 | Phase5导出后 | 重新调用脚本 |
| 清理门控 | Phase5完成后 | 告警重试清理 |

### 9.3 计时协议(T1-T6)

| 时机 | 写入字段 |
|------|---------|
| T1 Agent启动前 | phase_started_at |
| T2 Agent返回后 | agent_completed_at |
| T3 确认开始前 | confirmation_started_at |
| T4 用户回复后 | confirmation_completed_at |
| T5 优化轮次 | optimization_rounds累加 |
| T6 阶段完成 | phase_completed_at |

**确认策略**:Phase1/2Adv/4Adv需确认(T3/T4正常记录)；Phase2/3/4/5不确认(T3/T4=T2)；Phase3编译异常时确认

**Phase3子步骤拆分**:子阶段1/2/3各自独立条目记录

### 9.4 检查点协议

文件位置:`{输出目录}/tasks/task_checkpoints/` 下5个checkpoint JSON文件

保存前检查:①确认状态已完成 ②输出文件ls验证 ③timing数据phase_started_at>0 ④前序checkpoint存在

恢复规则:扫描所有checkpoint → 按phase排序找最后completed → 下一个阶段为恢复起点 → 验证outputs文件存在 → 缺失降级前一checkpoint

### 9.5 脚本调用方式

| 脚本 | 调用时机 | 命令 |
|------|---------|------|
| phase2_testing_technology.py | Phase2前 | `--technique generate_all --requirement {md} --output {json}` |
| phase2_testpoint_utils.py | Phase2合并 | `--action merge_batch_mds --batch-dir {dir} --output {md}` |
| phase2_adversary.py | Phase2Adv | `--testpoint {md} --requirement {md} --output {json}` |
| phase4_testcase_utils.py | Phase4合并 | `--action merge_batch_mds --batch-dir {dir} --testpoint {md} --output {md}` |
| phase4_adversary.py | Phase4Adv | `--testcases {md} --testpoint {md} --output {json}` |
| phase5_export.py | Phase5导出 | `--output {dir} --start-id {id} --testpoint {path}` |

### 9.6 清理临时文件

Phase5导出成功后删除: batches_phase2/、batches_phase4/、temp/、testing_technology.json、knowledge_match.md、coverage_result.json、phase2_*.json、phase4_*.json、validate_result.json

---

> 本文档基于 skills-refactor 目录全量更新（2026-07-15）。
> 4个核心模块：ohos-design-test-coordinator（含adversary子模块）、ohos-design-test-demo-pipeline、ohos-design-test-task-manager、ohos-test-arkts-xts-generation。
> 三层知识层级目录架构：domain-knowledge/Phase1、test-experience/Phase2、case-refinement/Phase4。
> knowledge_match.md三段式：§1领域知识+§2测试经验+§3用例细化。
> 17个门控检查点。XTS生成12-Phase工作流。