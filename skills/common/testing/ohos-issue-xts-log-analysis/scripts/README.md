# scripts目录说明

> **脚本定位说明**：明确每个脚本的职责、定位和使用场景
> 
> **更新时间**：2026-07-10  
> **重要更新**：新增证据链强制脚本、自动化脚本、状态管理脚本、并行解密脚本

---

## 脚本分类总览

**实际脚本总数**：**16个**

| 分类 | 脚本数 | 说明 |
|------|--------|------|
| 前置检查 | 2 | 解密前必须执行（check_dict.sh、verify_dict_location.sh） |
| 证据链强制 | 3 | 证据链追溯必须使用（map_domain.py、extract_imports.py、explore_import_chain.py） |
| 核心辅助 | 3 | AI运行时可用的辅助脚本（query_db.py、detect_logs.py、locate_xts_source.py） |
| 自动化脚本 | 2 | 自动生成报告内容（generate_evidence_chain.py、recommend_template.py） |
| 状态管理 | 1 | 流程状态跟踪（state_manager.py） |
| 解密脚本 | 2 | hilog解密专用（parallel_decrypt.py、filter_hilog.py） |
| 可选分析 | 3 | 特定场景深度分析（analyze_source.py、analyze_crash_stack.py、dependency_tree_parser.py） |

---

## 1. 前置检查脚本（解密前必须执行）

### dict文件检测（强制）

**脚本**: `check_dict.sh`

**用途**：
- 自动检测hilog目录中的dict文件
- 验证dict文件可用性
- 检查hilog与dict时间戳匹配度
- 输出推荐解密命令

**用法**：
```bash
bash scripts/check_dict.sh <hilog日志目录>
```

**强制要求**：
- ⚠️ 解密hilog前**必须**运行此脚本检查dict文件
- 如果找不到dict文件，不应执行hilogtool（会超时）

---

### dict位置验证（强制，2026-07-10新增）

**脚本**: `verify_dict_location.sh`

**用途**：
- 验证dict文件是否在正确位置（用户路径下）
- 检测skill目录下是否有dict污染
- 支持自动清理错误位置的dict

**用法**：
```bash
# 验证dict位置（解密后必须执行）
bash scripts/verify_dict_location.sh <日志目录>

# 自动清理错误位置的dict
bash scripts/verify_dict_location.sh <日志目录> --clean
```

**强制要求**：
- ⚠️ 解密完成后**必须**执行验证，防止dict污染skill目录
- 发现污染应立即清理（`--clean`参数）

---

## 2. 证据链强制脚本（必须使用，禁止AI推断）

### 🔒 API→Domain映射（强制）

**脚本**: `map_domain.py`

**用途**：
- 查询@ohos/@kit模块对应的domain和子系统
- 固化常量映射（零db依赖，最稳定）
- 区分被测方domain vs 测试运行时domain

**用法**：
```bash
# 查单个 @ohos 模块
python3 scripts/map_domain.py @ohos.arkui.inspector  # → 0xD003900 / ArkUI

# 展开 @kit 并逐个映射
python3 scripts/map_domain.py @kit.ArkTS             # → [@ohos.util.stream=0xD003F00, ...]

# 区分被测方 vs 测试运行时
python3 scripts/map_domain.py --list-runtime         # → 测试运行时domain（非被测方）
```

**强制要求**：
- ⚠️ 证据链的"@ohos/@kit → domain"映射**必须**使用此脚本
- ❌ 禁止AI自行推断（避免把测试运行时domain误当被测方domain）

---

### 🔒 源码import提取（强制，2026-07-09新增）

**脚本**: `extract_imports.py`

**用途**：
- 自动提取源码文件的import语句
- 自动分类import类型（api_module / kit_module / internal_module / test_framework）
- 识别被测API（过滤测试框架）

**用法**：
```bash
python3 scripts/extract_imports.py <测试源码文件>
```

**强制要求**：
- ⚠️ 提取import语句**必须**使用此脚本
- ❌ 禁止AI猜测import语句（如：猜测`import stream from '@ohos.stream'`）

---

### 🔒 引用链探索（可选增强，2026-07-09新增）

**脚本**: `explore_import_chain.py`

**用途**：
- 探索内部模块的引用链（最多3层）
- 递归解析依赖树
- 避免遗漏间接引用的API

**用法**：
```bash
# 探索引用链（最多3层）
python3 scripts/explore_import_chain.py <测试源码文件> --max-depth 3
```

**适用场景**：
- 测试文件引用了内部模块（如：`import Utils from '../common/Utils'`）
- 内部模块可能封装了OpenHarmony API

---

## 3. 核心辅助脚本（AI运行时可用）

### DB查询统一入口（优先使用）

**脚本**: `query_db.py`

**用途**：
- 替代文档SQL抄写
- 参数化查询（字段名已校正）
- 支持多表查询：rules/contacts/so_mapping/commands等

**用法**：
```bash
# rules 表
python3 scripts/query_db.py rules --keyword "App died"
python3 scripts/query_db.py rules --domain 元能力
python3 scripts/query_db.py rules --high

# contacts 表（责任人）
python3 scripts/query_db.py contacts 元能力

# so_mapping 表（SO库归属）
python3 scripts/query_db.py so libace.z.so

# JSON 输出
python3 scripts/query_db.py -f json rules --high
```

---

### 日志检测（AI必须使用）

**脚本**: `detect_logs.py`

**用途**：
- 检测加密文件（hilog.*.gz）
- 检测日志状态
- 输出文件状态提示

**用法**：
```bash
python3 scripts/detect_logs.py <日志目录>
```

---

### 源码工程定位（新增）

**脚本**: `locate_xts_source.py`

**用途**：
- 根据testcase/testsuite/hap定位源码文件
- 自动搜索源码工程

**用法**：
```bash
python3 scripts/locate_xts_source.py --testcase "textAreaLetterSpacing001"
python3 scripts/locate_xts_source.py --testsuite "TextAreaLetterSpacing"
python3 scripts/locate_xts_source.py --hap "ActsAceCArkUI16Test"
```

---

## 4. 自动化脚本（自动生成报告内容）

### 自动生成证据链（新增）

**脚本**: `generate_evidence_chain.py`

**用途**：
- 自动提取import语句
- 自动探索引用链
- 自动查询domain和subsystem
- 生成标准Markdown格式的证据链追溯

**用法**：
```bash
python3 scripts/generate_evidence_chain.py <测试文件> --test-case <用例名>
```

**输出**：可直接粘贴到报告的"源码→领域证据链"段落

---

### 模板推荐（新增）

**脚本**: `recommend_template.py`

**用途**：
- 根据测试文件自动推荐报告模板
- 提供必填段落建议
- 支持多种测试场景（Stream API、ArkUI组件、元能力等）

**用法**：
```bash
python3 scripts/recommend_template.py <测试文件> --subsystem <子系统名>
```

---

## 5. 状态管理脚本（2026-07-09新增）

**脚本**: `state_manager.py`

**用途**：
- 跟踪当前执行阶段
- 记录已完成步骤，避免重复执行
- 缓存执行结果，提升效率

**用法**：
```bash
# 检查流程状态
python3 scripts/state_manager.py show <日志目录>

# 检查步骤是否已完成
python3 scripts/state_manager.py check <日志目录> L1_Decrypt

# 重置状态（重新分析）
python3 scripts/state_manager.py reset <日志目录>
```

**状态文件**：`<日志目录>/.xts_analysis_state.json`

---

## 6. 解密脚本（hilog专用）

### 并行解密（推荐，2026-07-10新增）

**脚本**: `parallel_decrypt.py`

**用途**：
- 并行解密多个hilog.gz文件（提升10倍效率）
- 检查解密缓存（避免重复解密）
- 验证解密结果（确保解密成功）
- 验证dict位置（防止污染）

**用法**：
```bash
python3 scripts/parallel_decrypt.py <日志目录>
python3 scripts/parallel_decrypt.py <日志目录> <输出目录> <线程数>
```

**强制要求**：
- ⚠️ 使用此脚本代替手动hilogtool命令
- ✅ 自动验证dict位置，防止污染skill目录

---

### 分层过滤（可选）

**脚本**: `filter_hilog.py`

**用途**：
- 精准过滤hilog（domain过滤）
- 时间窗过滤
- AI可自己实现，但脚本更高效

**用法**：
```bash
python3 scripts/filter_hilog.py -i hilog.txt -d 00310 0013X
python3 scripts/filter_hilog.py -i hilog.txt -d 00310 --time-start "06-26 15:53:48"
```

---

## 7. 可选分析脚本（特定场景）

### 源码解析（可选）

**脚本**: `analyze_source.py`

**用途**：
- 解析.ets源码，提取API→Domain链路
- 源码驱动领域精准定界

**用法**：
```bash
python3 scripts/analyze_source.py test.ets
python3 scripts/analyze_source.py test.ets --format summary
```

---

### 崩溃栈分析（可选）

**脚本**: `analyze_crash_stack.py`

**用途**：
- 深度分析SO崩溃栈
- 自动定位SO库归属

**用法**：
```bash
python3 scripts/analyze_crash_stack.py cppcrash.log
```

---

### 递归import解析（可选）

**脚本**: `dependency_tree_parser.py`

**用途**：
- 递归解析多层import依赖（深度≤5）
- 复杂依赖链路追溯

**用法**：
```bash
python3 scripts/dependency_tree_parser.py <源码文件> --max-depth 5
```

---

## 性能对比

| 脚本 | 执行时间 | 内存消耗 | AI自己实现耗时 | 建议 |
|------|---------|---------|---------------|------|
| map_domain.py | <1s | <10MB | 5-10s | 🔒 **强制使用** |
| extract_imports.py | <1s | <10MB | 10-15s | 🔒 **强制使用** |
| query_db.py | <1s | <10MB | 5-10s | ✅ **优先使用** |
| detect_logs.py | <1s | <10MB | 10-15s | ✅ **必须使用** |
| parallel_decrypt.py | 20-60s/文件 | <50MB | 120-300s | ✅ **推荐使用** |
| filter_hilog.py | 1-5s | <50MB | 30-60s | ⭐ 可选使用 |
| analyze_source.py | 1-3s | <20MB | 60-120s | ⭐ 可选使用 |

---

## 脚本依赖说明

### 数据库依赖

所有查询脚本都依赖 `data/xts_rules.db`（**map_domain.py 例外：关键映射零 db 依赖**）：

```
map_domain.py       → 固化常量（零 db 依赖）+ expand_kit 查 kit_module 表
query_db.py         → data/xts_rules.db (rules/contacts/so_mapping等全表)
extract_imports.py  → 无db依赖（纯源码解析）
```

---

## 已废弃脚本（不要再使用）

以下脚本已被新脚本替代，**不要在README中提及**：

| 废弃脚本 | 替代方案 | 说明 |
|---------|---------|------|
| `query_rules.py` | `query_db.py rules` | 已被query_db.py收录 |
| `query_so_mapping.py` | `query_db.py so` | 已被query_db.py收录 |
| `query_api_domain.py` | `map_domain.py` | 功能重复，已移除 |

---

## 脚本定位原则

**核心原则**：
1. AI主导判断，脚本辅助查询
2. 脚本只做辅助查询，不做分析判断
3. AI可以选择使用脚本辅助，也可以自己实现
4. 脚本输出结果，AI需要验证和应用

**禁止行为**：
- ❌ 不要用脚本替代AI判断
- ❌ 不要用脚本自动化全流程
- ❌ 不要跳过文档阅读直接使用脚本

---

**更新时间**：2026-07-10  
**设计理念**：AI主导判断，脚本辅助查询  
**脚本总数**：**16个**（前置检查2 + 证据链强制3 + 核心辅助3 + 自动化2 + 状态管理1 + 解密2 + 可选分析3）