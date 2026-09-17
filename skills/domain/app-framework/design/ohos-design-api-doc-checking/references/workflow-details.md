# 工作流程详细说明

本文档包含 API 文档检查的详细工作流程与参考执行器实现。

文档中的 JavaScript 代码块是**可执行的参考实现**，按块顺序拼接后即可加载运行；`步骤 7` 给出必须通过的自检断言。任何改动都应先跑通步骤 7，再更新评测证据。

## 0. 数据契约与执行不变量

### 0.1 统一问题模型（唯一契约）

所有检查器（`automatic` 与 `agent`）只能产出下列结构，字段名不得各自发明。报告端（Markdown/Excel）只消费 `normalizeIssue()` 之后的记录，不得再从原始 issue 上读取自造字段。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ruleId` | string | 是 | 产出该问题的规则 ID |
| `dimension` | string | 是 | 7 大维度中文名 |
| `type` | string | 是 | 问题类型 |
| `subType` | string\|null | 否 | 子类型 |
| `priority` | string | 是 | `critical`/`high`/`medium`/`low` |
| `confidence` | number\|null | 否 | 0-100 |
| `filename` | string | 是 | 被检文档路径（由上下文注入，不得为 undefined） |
| `designer` | string | 是 | 文档设计人，取 `<!--Designer: xxx-->`，缺省 `-` |
| `line` / `lineEnd` | number\|null | 否 | 行号；无法定位时为 `null`，渲染为 `-` |
| `description` | string | 是 | 问题原因 |
| `suggestedFix` | string | 是 | 建议修改方案 |
| `autoFixable` | boolean | 否 | 是否可自动修复 |
| `evidence` | string\|null | 否 | 命中证据（原文片段或规则配置项） |
| `status` | string | 是 | 固定 `confirmed` |

### 0.2 执行不变量（fail-closed）

1. **禁止用空结果表示未实现或未执行。** 未实现的处理器必须抛错；无法执行的检查必须写入台账 `not-executed`/`failed` 并带 `reason`，不得折算成"0 个问题"。
2. **每条 `enabled: true` 的规则都必须留下一条执行台账记录**，`status ∈ executed | not-applicable | not-executed | failed`。`assertCompleteExecution()` 在报告生成前校验，缺失即中止。
3. **规则加载期即校验覆盖度与可构造性**：启用规则缺处理器、注册表存在未知 ID、`execution` 字段缺失或非法、正则无法构造、good/bad 样例断言失败，全部 fail-fast。
4. **带 `g` 标志的正则每次使用前必须重置 `lastIndex`**（或改用 `matchAll`）。同一 `RegExp` 对象复用时 `lastIndex` 残留会导致漏检。

### 0.3 `execution` 字段（规则 JSON 必填）

| 取值 | 判定依据 | 执行方 | 产出 |
|------|---------|--------|------|
| `automatic` | 规则 JSON 提供机器可判定的驱动配置（`pattern`/`patterns`/`keywords`/`requiredSections`/`indicators`/`extraction`/`validation`） | 执行器代码 | 问题记录 + 台账 `executed` |
| `agent` | 规则只有 `checkPoints` 语义描述，需人工/Agent 判定 | Agent | 必须回填 verdict，未回填即抛错 |

```javascript
// ===== 0.4 环境适配层 =====
// 执行器不直接依赖具体运行时：文件读取由调用方注入，便于自检时替换为 fixture。
const IO = {
  exists: null,   // (path) => boolean
  read: null,     // (path) => string
  readJson: null  // (path) => object
};

function setIO(impl) {
  for (const key of ['exists', 'read', 'readJson']) {
    if (typeof impl[key] !== 'function') {
      throw new Error(`setIO: 缺少实现 "${key}"`);
    }
  }
  Object.assign(IO, impl);
}

function requireIO(name) {
  if (typeof IO[name] !== 'function') {
    throw new Error(`IO.${name} 未注入：执行前必须调用 setIO({ exists, read, readJson })`);
  }
  return IO[name];
}

// ===== 0.5 统一问题模型 =====
const PRIORITY_SET = new Set(['critical', 'high', 'medium', 'low']);
const REQUIRED_ISSUE_FIELDS = ['type', 'priority', 'description', 'suggestedFix'];

function normalizeIssue(raw, context = {}) {
  const merged = { ...context, ...raw };

  for (const field of REQUIRED_ISSUE_FIELDS) {
    const value = merged[field];
    if (value === undefined || value === null || String(value).trim() === '') {
      throw new Error(`normalizeIssue: 问题记录缺少必填字段 "${field}"（ruleId=${merged.ruleId ?? 'unknown'}）`);
    }
  }
  if (!merged.ruleId) {
    throw new Error('normalizeIssue: 问题记录缺少 ruleId，无法追溯到规则');
  }
  if (!PRIORITY_SET.has(merged.priority)) {
    throw new Error(`normalizeIssue: 非法 priority "${merged.priority}"（ruleId=${merged.ruleId}）`);
  }
  if (merged.filename === undefined || merged.filename === null || merged.filename === '') {
    throw new Error(`normalizeIssue: 问题记录缺少 filename（ruleId=${merged.ruleId}）`);
  }

  const toLine = (v) => (v === undefined || v === null || v === '' || !Number.isFinite(Number(v)) ? null : Number(v));

  return {
    ruleId: merged.ruleId,
    dimension: merged.dimension ?? null,
    type: merged.type,
    subType: merged.subType ?? null,
    priority: merged.priority,
    confidence: Number.isFinite(Number(merged.confidence)) ? Number(merged.confidence) : null,
    filename: merged.filename,
    designer: merged.designer ?? '-',
    line: toLine(merged.line),
    lineEnd: toLine(merged.lineEnd),
    description: merged.description,
    suggestedFix: merged.suggestedFix ?? merged.explanation ?? '',
    autoFixable: Boolean(merged.autoFixable),
    evidence: merged.evidence ?? null,
    status: 'confirmed'
  };
}

// 检查器统一用它构造问题记录：rule 提供 ruleId/priority/confidence/message/suggestedFix，
// context 提供 filename/designer/dimension。
function makeIssue(rule, context, overrides = {}) {
  return normalizeIssue({
    ruleId: rule.id,
    dimension: context.dimension,
    type: context.dimension,
    subType: overrides.subType ?? rule.subType ?? rule.name ?? null,
    priority: overrides.priority ?? rule.priority,
    confidence: overrides.confidence ?? rule.confidence,
    description: overrides.description ?? rule.message,
    suggestedFix: overrides.suggestedFix ?? rule.suggestedFix ?? rule.explanation,
    autoFixable: overrides.autoFixable ?? rule.autoFixable ?? false,
    line: overrides.line,
    lineEnd: overrides.lineEnd,
    evidence: overrides.evidence ?? null
  }, { filename: context.filename, designer: context.designer });
}

// ===== 0.6 执行台账 =====
const LEDGER_STATUS = new Set(['executed', 'not-applicable', 'not-executed', 'failed']);

function ledgerRecord(entry) {
  if (!LEDGER_STATUS.has(entry.status)) {
    throw new Error(`非法台账状态 "${entry.status}"（ruleId=${entry.ruleId ?? entry.module}）`);
  }
  if ((entry.status === 'not-executed' || entry.status === 'failed') && !entry.reason) {
    throw new Error(`台账状态 ${entry.status} 必须给出 reason（ruleId=${entry.ruleId ?? entry.module}）`);
  }
  return {
    module: entry.module,
    ruleId: entry.ruleId ?? null,
    dimension: entry.dimension ?? null,
    execution: entry.execution ?? null,
    status: entry.status,
    issueCount: entry.issueCount ?? 0,
    reason: entry.reason ?? null,
    evidence: entry.evidence ?? null
  };
}

// 处理器可以用这两个哨兵值声明"本规则这次没执行/不适用"，由 executeChecks 写入台账。
// 这是"无法执行"的唯一合法表达方式——返回 [] 表示"查了，没问题"，二者不可混用。
function notExecuted(reason) {
  if (!reason) throw new Error('notExecuted 必须给出 reason');
  return { __ledger: 'not-executed', reason, issues: [] };
}

function notApplicable(reason) {
  if (!reason) throw new Error('notApplicable 必须给出 reason');
  return { __ledger: 'not-applicable', reason, issues: [] };
}
```

### 0.7 启动顺序（Agent 执行时的最小调用链）

```javascript
// 完整调用链（fs 为 Node 内置模块；Agent 也可用自身文件工具实现同样三个方法）
async function runApiDocCheck(docPath, options = {}) {
  // 1) 注入文件读取实现
  setIO({
    exists: (path) => fs.existsSync(path),
    read: (path) => fs.readFileSync(path, 'utf8'),
    readJson: (path) => JSON.parse(fs.readFileSync(path, 'utf8'))
  });

  // 2) 加载规则：内部自动执行覆盖校验 + 正则自检，任一失败即中止
  const loaded = loadRules(options.referencesDir ?? 'references');

  // 3) 解析文档：必须传 fileName（SDK 映射、报告列、模块范围都依赖它）
  const parsed = parseDocument(fs.readFileSync(docPath, 'utf8'), { fileName: docPath });

  // 4) 执行检查：agent 规则需要 verdicts；SDK 检查需要 sdkSourcePath/sdkFilePath
  const result = executeChecks(parsed, loaded, {
    sdkSourcePath: options.sdkSourcePath ?? process.env.INTERFACE_SDK_JS_PATH,  // 未提供 → sdk.state = not-executed
    sdkFilePath: options.sdkFilePath,                                          // 直接指定 .d.ts/.h
    projectRoot: options.projectRoot,                                          // 相对链接解析基准
    sampleData: options.sampleData,                                            // path-003 需要，未提供 → not-executed
    agentVerdicts: options.agentVerdicts ?? {},                                 // { [ruleId]: [{ checkPoint, status, evidence, ... }] }
    modules: options.modules                                                   // 可选：显式指定执行的模块集合
  });

  // 5) 生成报告：excelData 是报告端唯一数据源
  const report = generateReport(result, parsed.fileName);
  if (options.outputPath) {
    await generateExcelReport(report, options.outputPath);   // 见 references/excel-format.md
  }
  return report;
}
```

未注入 `IO`、未传 `fileName`、agent 规则未回填 verdict、启用规则缺处理器——这四种情况都会在对应步骤抛错，
而不是退化成"检查通过、0 问题"。

## 步骤 1：加载规则（按 7 大维度分类）

### 1.1 加载与分组

```javascript
const DIMENSION_BY_CATEGORY = {
  '资源易找性': 'findability',
  '资源丰富性/完整性': 'completeness',
  '资料正确性': 'correctness',
  '资源清晰易懂': 'clarity',
  '能力有效性/易用性/丰富性': 'capability',
  // index.json 中 semantics 模块的 category 是「能力易用性」，属于 capability 维度的子分类
  '能力有效性': 'capability',
  '能力易用性': 'capability',
  '能力丰富性': 'capability'
};

const DIMENSION_NAME = {
  findability: '资源易找性',
  completeness: '资源丰富性/完整性',
  correctness: '资料正确性',
  clarity: '资源清晰易懂',
  capability: '能力有效性/易用性/丰富性'
};

// 分类不在映射表中必须报错：静默回退到 correctness 会把语义类问题错误归档
function mapToDimension(category) {
  const dimension = DIMENSION_BY_CATEGORY[category];
  if (!dimension) {
    throw new Error(`mapToDimension: 未知规则分类 "${category}"，请在 DIMENSION_BY_CATEGORY 中登记`);
  }
  return dimension;
}

const EXECUTION_MODES = new Set(['automatic', 'agent']);
const VALID_PRIORITIES = new Set(['critical', 'high', 'medium', 'low']);
// 规则 JSON 的必填字段（与 references/rule-extensions.md 的字段说明一致）
const REQUIRED_RULE_FIELDS = ['id', 'name', 'description', 'type', 'priority', 'confidence', 'enabled', 'execution', 'message', 'suggestedFix'];

// index.json 声明模块级开关与 checkTypes，规则文件声明 mappingRules / sdkRepository，
// 两边必须合并；只取一边会丢掉映射规则（历史缺陷：SDK 检查因 mappingRules 缺失直接报错）
function mergeSdkSourceCheck(fromRuleFile, fromIndex) {
  if (!fromRuleFile && !fromIndex) return null;
  return { ...(fromRuleFile ?? {}), ...(fromIndex ?? {}) };
}

function loadRules(referencesDir = 'references') {
  const readJson = requireIO('readJson');
  const index = readJson(`${referencesDir}/index.json`);

  const byModule = {};
  const byDimension = { findability: [], completeness: [], correctness: [], clarity: [], capability: [] };

  for (const [moduleName, config] of Object.entries(index.rules)) {
    const ruleFile = readJson(`${referencesDir}/${config.file}`);
    byModule[moduleName] = {
      module: moduleName,
      enabled: config.enabled !== false,
      priority: config.priority,
      category: config.category,
      dimension: mapToDimension(config.category),
      file: config.file,
      sdkSourceCheck: mergeSdkSourceCheck(ruleFile.sdkSourceCheck, config.sdkSourceCheck),
      rules: ruleFile.rules ?? [],
      data: ruleFile
    };
    if (byModule[moduleName].enabled) {
      byDimension[byModule[moduleName].dimension].push(byModule[moduleName]);
    }
  }

  const loaded = { index, byModule, byDimension, classification: index.classification };

  // 加载期强制校验：覆盖度、execution 字段、正则可构造性、样例断言
  validateRuleCoverage(loaded, RULE_HANDLERS);
  validateRulePatterns(loaded);

  return loaded;
}
```

### 1.2 规则注册表与覆盖校验

分派不再使用「按维度写死 ID 的 switch」——那会让新增规则被静默跳过。改为**注册表驱动**：`RULE_HANDLERS` 必须为每一条启用规则登记一个处理器，并声明它处理的 `name`（规则英文名）与 `execution`；`validateRuleCoverage()` 双向校验，任何一侧不一致都 fail-fast。

```javascript
function validateRuleCoverage(loaded, registry) {
  const errors = [];
  const declared = new Map();

  for (const [moduleName, ruleFile] of Object.entries(loaded.byModule)) {
    for (const rule of ruleFile.rules) {
      if (!rule || typeof rule !== 'object' || !rule.id) {
        errors.push(`模块 ${moduleName} 存在缺少 id 的规则条目`);
        continue;
      }
      if (declared.has(rule.id)) {
        errors.push(`规则 ID 重复：${rule.id}（${declared.get(rule.id).module} 与 ${moduleName}）`);
      }
      declared.set(rule.id, {
        name: rule.name,
        module: moduleName,
        dimension: ruleFile.dimension,
        execution: rule.execution,
        enabled: rule.enabled !== false
      });
      if (!EXECUTION_MODES.has(rule.execution)) {
        errors.push(`规则 ${rule.id} 的 execution 字段缺失或非法（应为 automatic|agent）`);
      }
      for (const field of REQUIRED_RULE_FIELDS) {
        if (rule[field] === undefined || rule[field] === null || String(rule[field]).trim() === '') {
          errors.push(`规则 ${rule.id} 缺少必填字段 "${field}"（见 rule-extensions.md 字段说明）`);
        }
      }
      if (!VALID_PRIORITIES.has(rule.priority)) {
        errors.push(`规则 ${rule.id} 的 priority "${rule.priority}" 非法（应为 ${[...VALID_PRIORITIES].join('|')}）`);
      }
      if (!(Number.isFinite(rule.confidence) && rule.confidence >= 0 && rule.confidence <= 100)) {
        errors.push(`规则 ${rule.id} 的 confidence 必须是 0-100 的数字`);
      }
    }
  }

  // 1) 启用规则必须全部有处理器，且处理器的 name/execution 与规则文件一致
  for (const [id, meta] of declared) {
    if (!meta.enabled) continue;
    const entry = registry[id];
    if (!entry) {
      errors.push(`启用规则 ${id}（${meta.name}）没有注册处理器，会被静默跳过`);
      continue;
    }
    if (entry.name !== meta.name) {
      errors.push(`处理器 ${id} 声明处理 "${entry.name}"，但规则文件中该 ID 是 "${meta.name}"（处理器与规则错配）`);
    }
    if (entry.execution !== meta.execution) {
      errors.push(`处理器 ${id} 的 execution=${entry.execution} 与规则文件 ${meta.execution} 不一致`);
    }
    if (typeof entry.handler !== 'function') {
      errors.push(`处理器 ${id} 缺少 handler 函数`);
    }
  }

  // 2) 注册表不得登记规则文件里不存在的 ID（防止指向已删除/改名的规则）
  for (const id of Object.keys(registry)) {
    if (!declared.has(id)) {
      errors.push(`注册表存在未知规则 ID：${id}（规则文件中不存在）`);
    }
  }

  if (errors.length > 0) {
    throw new Error(`规则覆盖校验失败（${errors.length} 项）：\n- ${errors.join('\n- ')}`);
  }

  const enabledIds = [...declared.values()].filter(m => m.enabled).map(m => m.name);
  return { total: declared.size, enabled: enabledIds.length };
}
```

### 1.3 规则自检（正则可构造 + good/bad 样例断言）

规则 JSON 里的正则要经过 **JSON 转义 → RegExp 源码** 两层转义，写错时 `new RegExp` 直接抛 `SyntaxError`。加载期必须构造一遍全部启用正则，并对带 `examples` 的规则做正反例断言，否则错误会推迟到检查阶段甚至被静默忽略。

```javascript
function compileRuleRegex(patternValue, flags, ruleId, field) {
  try {
    return new RegExp(patternValue, flags);
  } catch (err) {
    throw new Error(`规则 ${ruleId} 的 ${field} 无法构造正则：${err.message}（value=${JSON.stringify(patternValue)}, flags=${JSON.stringify(flags ?? '')}）`);
  }
}

// 收集规则里所有正则型配置：pattern / fix.pattern / patterns / *Patterns / validation.*Patterns / requiredPattern
function collectRuleRegexes(rule) {
  const found = [];
  const push = (value, flags, field) => {
    if (typeof value === 'string' && value.length > 0) found.push({ value, flags, field });
  };

  if (rule.pattern?.type === 'regex') push(rule.pattern.value, rule.pattern.flags ?? '', 'pattern.value');
  if (typeof rule.pattern === 'string') push(rule.pattern, '', 'pattern');
  if (rule.fix?.pattern) push(rule.fix.pattern, rule.fix.flags ?? 'g', 'fix.pattern');
  if (rule.requiredPattern) push(rule.requiredPattern, '', 'requiredPattern');

  for (const key of ['patterns', 'ambiguousPatterns', 'deprecationIndicators']) {
    for (const [i, item] of (rule[key] ?? []).entries()) {
      if (item?.type === 'keyword') continue;              // 关键词型不是正则
      push(item?.pattern ?? (typeof item === 'string' ? item : null), item?.flags ?? '', `${key}[${i}].pattern`);
    }
  }
  for (const [i, item] of (rule.requiredPatterns ?? []).entries()) {
    push(item?.pattern, item?.flags ?? '', `requiredPatterns[${i}].pattern`);
  }
  for (const group of Object.values(rule.validation ?? {})) {
    if (!Array.isArray(group)) continue;
    group.forEach((value, i) => {
      if (typeof value === 'string' && /[\\^$.*+?()[\]{}|]/.test(value)) push(value, '', `validation 数组[${i}]`);
    });
  }
  for (const item of rule.validation?.warningPatterns ?? []) push(item?.pattern, item?.flags ?? '', 'validation.warningPatterns.pattern');
  for (const item of rule.linkPatterns?.required ?? []) push(item?.pattern, item?.flags ?? '', 'linkPatterns.required.pattern');
  for (const group of Object.values(rule.termMappings ?? {})) {
    // termMappings 的值是错误写法枚举，按字面量匹配，不当正则处理
    void group;
  }
  return found;
}

function validateRulePatterns(loaded) {
  const errors = [];

  // 退化正则探测：检测型正则若能把中性文档全部匹配，说明写成了通配（历史缺陷：
  // clarity-002 的 "等等|..." 中 `...` 被当成正则，任意 3 个字符即命中，每行都报问题）
  const NEUTRAL_SAMPLES = [
    'OpenHarmony 提供 createTask 接口，用于创建后台任务，起始版本为 10。',
    'import demoTaskManager from module; let taskId = 0;',
    '| 参数名 | 类型 | 必填 | 说明 |'
  ];

  for (const [moduleName, ruleFile] of Object.entries(loaded.byModule)) {
    for (const rule of ruleFile.rules) {
      if (rule.enabled === false) continue;

      // (1) 正则必须可构造
      for (const spec of collectRuleRegexes(rule)) {
        try {
          const compiled = compileRuleRegex(spec.value, spec.flags, rule.id, spec.field);
          const degenerate = NEUTRAL_SAMPLES.every(sample => {
            compiled.lastIndex = 0;                     // g 标志会残留 lastIndex，探测前必须复位
            return compiled.test(sample);
          });
          if (degenerate) {
            errors.push(`规则 ${rule.id}（${moduleName}）的 ${spec.field} 过于宽泛：中性样例全部命中，疑似把字面量当正则（value=${JSON.stringify(spec.value)}）；字面量请标注 "type": "keyword"`);
          }
        } catch (err) {
          errors.push(err.message);
        }
      }

      // (2) 正反例断言：good 全部不命中、bad 全部命中
      const examples = rule.examples;
      if (!examples) continue;
      const matcher = buildExampleMatcher(rule);
      if (!matcher) continue;   // 无可自动判定的驱动配置（纯 checkPoints 规则由 Agent 判定）

      for (const good of examples.good ?? []) {
        if (matcher(good)) errors.push(`规则 ${rule.id}（${moduleName}）误报：good 样例被命中 → ${JSON.stringify(good)}`);
      }
      for (const bad of examples.bad ?? []) {
        if (!matcher(bad)) errors.push(`规则 ${rule.id}（${moduleName}）漏报：bad 样例未命中 → ${JSON.stringify(bad)}`);
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`规则自检失败（${errors.length} 项）：\n- ${errors.join('\n- ')}`);
  }
  return true;
}

// 为样例断言构造判定函数：正则型规则用正则，函数型规则用对应处理器
function buildExampleMatcher(rule) {
  if (rule.pattern?.type === 'regex') {
    return (text) => countRegexMatches(text, rule.pattern.value, rule.pattern.flags ?? '') > 0;
  }
  if (rule.pattern?.type === 'function') {
    const fn = FUNCTION_HANDLERS[rule.pattern.name];
    if (!fn) throw new Error(`规则 ${rule.id} 引用的函数处理器 ${rule.pattern.name} 未实现`);
    return (text) => fn(text, rule).length > 0;
  }
  return null;
}

// g 标志的正则必须每次重置 lastIndex，否则复用同一对象会漏检
function countRegexMatches(text, value, flags) {
  const re = new RegExp(value, flags.includes('g') ? flags : flags + 'g');
  return [...text.matchAll(re)].length;
}
```

## 步骤 2：解析文档

`parseDocument` 必须产出后续步骤依赖的 `fileName`、`docType`、`designer`——SDK 映射、报告列（文件名/Designer）、模块范围判定都依赖它们。缺 `fileName` 时直接抛错，不允许后续以 `undefined` 继续。

```javascript
const API_DOC_NAME_PATTERNS = [/^js-apis.*\.md$/i, /^capi-.*\.md$/i];
const GUIDE_NAME_KEYWORDS = ['guide', 'tutorial', 'overview', 'getting-started'];

function detectDocType(fileName, doc) {
  const base = String(fileName ?? '').split('/').pop().toLowerCase();
  if (API_DOC_NAME_PATTERNS.some(re => re.test(base))) return 'api-doc';
  if (GUIDE_NAME_KEYWORDS.some(kw => base.includes(kw))) return 'dev-guide';

  // 文件名不足以判定时按内容特征判定
  const hasApiShape = /^#{2,3}\s+[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*\s*(?:<sup>\d+\+?<\/sup>|\d+\+)?\s*$/m.test(doc)
    && /\*\*(参数|返回值|错误码)\*\*/.test(doc);
  if (hasApiShape) return 'api-doc';
  if (/^#{2,3}\s*(概述|开发步骤|相关文档|约束限制)/m.test(doc)) return 'dev-guide';
  return 'unknown';
}

function extractDesigner(doc) {
  const match = doc.match(/<!--\s*Designer\s*[:：]\s*([^>]*?)\s*-->/i);
  const designer = match ? match[1].trim() : '';
  return designer === '' ? '-' : designer;
}

function parseDocument(doc, meta = {}) {
  if (!meta.fileName) {
    throw new Error('parseDocument: 必须通过 meta.fileName 传入被检文档路径，SDK 映射与报告列都依赖它');
  }
  const docType = meta.docType ?? detectDocType(meta.fileName, doc);

  return {
    fileName: meta.fileName,
    fileBaseName: String(meta.fileName).split('/').pop(),
    docType,
    designer: meta.designer ?? extractDesigner(doc),
    content: doc,
    lines: doc.split('\n'),
    codeBlocks: extractCodeBlocks(doc),
    tables: extractTables(doc),
    links: extractLinks(doc),
    headings: extractHeadings(doc),
    sections: identifySections(doc),
    methodSignatures: extractMethodSignatures(doc)
  };
}

// 代码块：返回内容首行行号（1-based）；支持被 blockquote（每行以 "> " 前缀）包裹的围栏
function extractCodeBlocks(doc) {
  const lines = doc.split('\n');
  const blocks = [];
  let current = null;

  lines.forEach((raw, idx) => {
    const line = raw.replace(/^\s*>\s?/, '');
    const fence = line.match(/^\s*(`{3,}|~{3,})\s*([\w+#-]*)\s*$/);
    if (!fence) {
      if (current) current.lines.push({ text: line, lineNo: idx + 1 });
      return;
    }
    if (!current) {
      current = { lang: fence[2] || 'text', fenceLine: idx + 1, startLine: idx + 2, lines: [] };
    } else {
      current.endLine = idx;                       // 闭合围栏所在行
      current.content = current.lines.map(l => l.text).join('\n');
      current.lineCount = current.lines.length;
      blocks.push(current);
      current = null;
    }
  });

  if (current) {                                   // 文档末尾围栏未闭合
    current.endLine = lines.length;
    current.content = current.lines.map(l => l.text).join('\n');
    current.lineCount = current.lines.length;
    current.unclosedFence = true;
    blocks.push(current);
  }
  return blocks;
}

function splitTableRow(line) {
  return line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map(cell => cell.trim());
}

function extractTables(doc) {
  const lines = doc.split('\n');
  const tables = [];
  let i = 0;
  while (i < lines.length) {
    if (!/^\s*\|.*\|\s*$/.test(lines[i])) { i++; continue; }
    const startLine = i + 1;
    const header = splitTableRow(lines[i]);
    const separator = lines[i + 1] && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1]);
    const rows = [];
    let j = separator ? i + 2 : i + 1;
    while (j < lines.length && /^\s*\|.*\|\s*$/.test(lines[j])) {
      rows.push({ cells: splitTableRow(lines[j]), lineNo: j + 1 });
      j++;
    }
    tables.push({ startLine, endLine: j, header, hasSeparator: Boolean(separator), rows });
    i = j;
  }
  return tables;
}

function extractLinks(doc) {
  const links = [];
  doc.split('\n').forEach((text, idx) => {
    const re = /\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;
    for (const m of text.matchAll(re)) {
      links.push({ text: m[1], target: m[2], line: idx + 1, external: /^(https?:)?\/\//.test(m[2]), anchor: m[2].startsWith('#') });
    }
  });
  return links;
}

function slugify(title) {
  return title.trim().toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/[^\w\u4e00-\u9fa5\s-]/g, '')
    .replace(/\s+/g, '-');
}

function extractHeadings(doc) {
  const headings = [];
  let inFence = false;
  doc.split('\n').forEach((raw, idx) => {
    const line = raw.replace(/^\s*>\s?/, '');
    if (/^\s*(`{3,}|~{3,})/.test(line)) { inFence = !inFence; return; }
    if (inFence) return;
    const m = line.match(/^(#{1,6})\s+(.*?)\s*#*\s*$/);
    if (m) {
      headings.push({ level: m[1].length, text: m[2], rawTitle: m[2], line: idx + 1, anchor: slugify(m[2]) });
    }
  });
  return headings;
}

// 章节：每个标题到下一个同级或更高级标题之前
function identifySections(doc) {
  const lines = doc.split('\n');
  const headings = extractHeadings(doc);
  return headings.map((h, i) => {
    const next = headings.slice(i + 1).find(x => x.level <= h.level);
    const endLine = next ? next.line - 1 : lines.length;
    return {
      title: h.text,
      rawTitle: h.rawTitle,
      level: h.level,
      anchor: h.anchor,
      startLine: h.line,
      endLine,
      body: lines.slice(h.line, endLine).join('\n'),
      bodyLines: lines.slice(h.line, endLine).map((text, k) => ({ text, lineNo: h.line + 1 + k }))
    };
  });
}

function extractMethodSignatures(doc) {
  const signatures = [];
  const re = /^#{2,3}\s+([A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\s*(?:<sup>(\d+)\s*\+?<\/sup>|(\d+)\s*\+)?\s*$/gm;
  for (const m of doc.matchAll(re)) {
    signatures.push({ fullName: m[1], name: m[1].split('.').pop(), since: Number(m[2] ?? m[3] ?? NaN) || null });
  }
  return signatures;
}
```

## 步骤 3：按 7 大维度执行检查

```javascript
// 模块执行范围（与 SKILL.md「检查项选择」一致）
const MODULE_SCOPE = {
  'api-doc': {
    required: ['spelling', 'syntax', 'path-consistency', 'semantics', 'project-structure',
               'findability', 'completeness', 'correctness', 'clarity', 'capability'],
    optional: [],
    sdkSourceCheck: true
  },
  'dev-guide': {
    required: ['spelling', 'syntax', 'path-consistency', 'clarity', 'semantics',
               'project-structure', 'findability', 'correctness'],
    optional: ['completeness', 'capability'],
    sdkSourceCheck: false
  },
  unknown: {
    required: ['spelling', 'syntax', 'path-consistency', 'clarity', 'findability', 'correctness'],
    optional: ['semantics', 'project-structure', 'completeness', 'capability'],
    sdkSourceCheck: false
  }
};

function resolveModuleScope(docType, options = {}) {
  const scope = MODULE_SCOPE[docType] ?? MODULE_SCOPE.unknown;
  const forced = options.modules;             // 调用方可显式指定模块集合（评测/复检场景）
  if (!forced) return scope;
  return {
    required: forced.filter(m => m !== 'sdk-source-check'),
    optional: [],
    sdkSourceCheck: forced.includes('sdk-source-check') ? true : scope.sdkSourceCheck
  };
}

function executeChecks(parsed, loaded, options = {}) {
  const ledger = [];
  const failures = [];
  const issuesByDimension = { findability: [], completeness: [], correctness: [], clarity: [], capability: [] };
  const scope = resolveModuleScope(parsed.docType, options);
  const sdk = { state: 'not-executed', reason: null, sdkFilePath: null, checkpoints: [], issues: [] };

  const context = {
    filename: parsed.fileName,
    designer: parsed.designer,
    options,
    parsed
  };

  for (const [moduleName, ruleFile] of Object.entries(loaded.byModule)) {
    const dimensionName = DIMENSION_NAME[ruleFile.dimension];

    if (!ruleFile.enabled) {
      ledger.push(ledgerRecord({ module: moduleName, dimension: dimensionName, status: 'not-executed', reason: 'index.json 中该模块 enabled=false' }));
      continue;
    }

    const isRequired = scope.required.includes(moduleName);
    const isOptional = scope.optional.includes(moduleName);
    if (!isRequired && !isOptional) {
      ledger.push(ledgerRecord({ module: moduleName, dimension: dimensionName, status: 'not-applicable', reason: `文档类型 ${parsed.docType} 不执行该模块` }));
      continue;
    }

    for (const rule of ruleFile.rules) {
      if (rule.enabled === false) {
        ledger.push(ledgerRecord({ module: moduleName, ruleId: rule.id, dimension: dimensionName, execution: rule.execution, status: 'not-executed', reason: '规则 enabled=false' }));
        continue;
      }

      const entry = RULE_HANDLERS[rule.id];
      if (!entry) {
        // 覆盖校验已在加载期拦截；此处兜底，绝不静默跳过
        failures.push(`启用规则 ${rule.id} 无处理器`);
        ledger.push(ledgerRecord({ module: moduleName, ruleId: rule.id, dimension: dimensionName, execution: rule.execution, status: 'failed', reason: '无注册处理器' }));
        continue;
      }

      const ruleContext = { ...context, dimension: dimensionName, module: moduleName, ruleFile };
      try {
        const produced = entry.handler(parsed, rule, ruleContext) ?? [];

        // 处理器声明"未执行/不适用"：写台账，不产生问题，也绝不当成"检查通过"
        if (produced.__ledger) {
          ledger.push(ledgerRecord({
            module: moduleName, ruleId: rule.id, dimension: dimensionName, execution: rule.execution,
            status: produced.__ledger, issueCount: 0, reason: produced.reason
          }));
          continue;
        }

        const normalized = produced.map(issue => normalizeIssue(issue, {
          ruleId: rule.id,
          dimension: dimensionName,
          filename: parsed.fileName,
          designer: parsed.designer,
          priority: rule.priority,
          confidence: rule.confidence
        }));
        issuesByDimension[ruleFile.dimension].push(...normalized);
        ledger.push(ledgerRecord({
          module: moduleName, ruleId: rule.id, dimension: dimensionName, execution: rule.execution,
          status: 'executed', issueCount: normalized.length,
          evidence: normalized.map(i => (i.line ? `L${i.line}` : 'no-line')).join(', ') || null
        }));
      } catch (err) {
        failures.push(`${rule.id}: ${err.message}`);
        ledger.push(ledgerRecord({ module: moduleName, ruleId: rule.id, dimension: dimensionName, execution: rule.execution, status: 'failed', reason: err.message }));
      }
    }
  }

  // SDK 源码一致性检查：状态必须显式区分 未执行 / 失败 / 通过
  if (scope.sdkSourceCheck) {
    const correctnessModule = loaded.byModule.correctness;
    const sdkConfig = correctnessModule?.sdkSourceCheck;
    if (!sdkConfig?.enabled) {
      sdk.state = 'not-executed';
      sdk.reason = 'correctness.sdkSourceCheck 未启用';
    } else if (!options.sdkSourcePath && !options.sdkFilePath) {
      sdk.state = 'not-executed';
      sdk.reason = '未提供 SDK 源码路径（options.sdkSourcePath / options.sdkFilePath / INTERFACE_SDK_JS_PATH）';
    } else {
      const result = checkSdkSourceConsistency(parsed, sdkConfig, options);
      Object.assign(sdk, result);
      issuesByDimension.correctness.push(...result.issues.map(issue => normalizeIssue(issue, {
        ruleId: issue.ruleId ?? 'correctness.sdkSourceCheck',
        dimension: DIMENSION_NAME.correctness,
        filename: parsed.fileName,
        designer: parsed.designer
      })));
      ledger.push(ledgerRecord({
        module: 'correctness', ruleId: 'sdk-source-check', dimension: DIMENSION_NAME.correctness,
        execution: 'automatic',
        status: sdk.state === 'passed' ? 'executed' : sdk.state,
        issueCount: result.issues.length,
        reason: sdk.state === 'passed' ? null : sdk.reason,
        evidence: sdk.sdkFilePath
      }));
    }
  } else {
    sdk.state = 'not-applicable';
    sdk.reason = `文档类型 ${parsed.docType} 不执行 SDK 源码一致性检查`;
    ledger.push(ledgerRecord({ module: 'correctness', ruleId: 'sdk-source-check', dimension: DIMENSION_NAME.correctness, status: 'not-applicable', reason: sdk.reason }));
  }

  if (failures.length > 0 && !options.tolerateFailures) {
    throw new Error(`规则执行失败（${failures.length} 项），不得按 0 问题继续：\n- ${failures.join('\n- ')}`);
  }

  assertCompleteExecution(ledger, loaded, scope);

  return { issuesByDimension, ledger, sdk, failures };
}

// 每条启用规则必须有且仅有一条台账记录，否则视为执行不完整
function assertCompleteExecution(ledger, loaded, scope) {
  const seen = new Map();
  for (const record of ledger) {
    const key = record.ruleId ?? `module:${record.module}`;
    seen.set(key, (seen.get(key) ?? 0) + 1);
  }

  const missing = [];
  for (const [moduleName, ruleFile] of Object.entries(loaded.byModule)) {
    const inScope = scope.required.includes(moduleName) || scope.optional.includes(moduleName);
    if (!ruleFile.enabled || !inScope) {
      if (!seen.has(`module:${moduleName}`)) missing.push(`模块 ${moduleName}（范围外/停用，应有模块级台账）`);
      continue;
    }
    for (const rule of ruleFile.rules) {
      if (!seen.has(rule.id)) missing.push(`${moduleName}/${rule.id}`);
    }
  }

  if (missing.length > 0) {
    throw new Error(`执行台账不完整，以下启用规则没有执行记录（禁止静默跳过）：${missing.join(', ')}`);
  }
  return true;
}
```

## 步骤 4：规则执行器实现（注册表驱动）

### 4.1 注册表

`RULE_HANDLERS` 覆盖 `references/` 下**全部启用规则**（47 条）。`def()` 登记的 `name` 必须与规则 JSON 的 `name` 一致——`validateRuleCoverage()` 用它拦截「ID 与处理器错配」（历史缺陷：`correctness-005` 在 JSON 中是 `sensitive-info-leak`，分派却调用链接有效性检查）。

```javascript
function def(name, execution, handler) {
  return { name, execution, handler };
}

// agent 规则：必须由调用方回填 verdict，未回填即抛错（禁止按 0 问题处理）
// 签名与其他处理器一致：(parsed, rule, context)
function agentRule(parsed, rule, context) {
  const verdicts = context.options?.agentVerdicts?.[rule.id];
  if (!Array.isArray(verdicts) || verdicts.length === 0) {
    const checkpoints = (rule.checkPoints ?? []).map(c => c.name).join(', ') || rule.id;
    throw new Error(`agent 规则 ${rule.id}（${rule.name}）未回填 verdict，需按 checkPoints 逐条判定：${checkpoints}`);
  }

  const covered = new Set(verdicts.map(v => v.checkPoint));
  for (const cp of rule.checkPoints ?? []) {
    if (!covered.has(cp.name)) {
      throw new Error(`agent 规则 ${rule.id} 的 checkPoint "${cp.name}" 缺少 verdict`);
    }
  }

  const issues = [];
  for (const verdict of verdicts) {
    if (!['pass', 'fail', 'not-applicable'].includes(verdict.status)) {
      throw new Error(`agent 规则 ${rule.id} 的 verdict.status 非法：${verdict.status}`);
    }
    if (verdict.status !== 'fail') continue;
    if (!verdict.evidence) {
      throw new Error(`agent 规则 ${rule.id} 判定 fail 时必须给出 evidence`);
    }
    issues.push(makeIssue(rule, context, {
      description: verdict.description ?? rule.message,
      suggestedFix: verdict.suggestedFix ?? rule.suggestedFix,
      priority: verdict.priority ?? rule.priority,
      confidence: verdict.confidence ?? rule.confidence,
      line: verdict.line,
      lineEnd: verdict.lineEnd,
      evidence: `[${verdict.checkPoint}] ${verdict.evidence}`
    }));
  }
  return issues;
}

const RULE_HANDLERS = {
  // ---- spelling（资料正确性）----
  'spelling-001': def('common-misspelling', 'automatic', checkCommonMisspelling),
  'spelling-002': def('harmonyos-glossary', 'automatic', checkHarmonyosGlossary),
  'spelling-003': def('unknown-decorator', 'automatic', checkUnknownDecorator),

  // ---- syntax（资料正确性）----
  'syntax-001': def('template-string-invalid-space', 'automatic', (parsed, rule, ctx) => regexRuleScan(parsed, rule, ctx)),
  'syntax-002': def('unclosed-brace', 'automatic', (parsed, rule, ctx) => functionRuleScan(parsed, rule, ctx)),
  'syntax-003': def('unclosed-parenthesis', 'automatic', (parsed, rule, ctx) => functionRuleScan(parsed, rule, ctx)),
  'syntax-004': def('unclosed-bracket', 'automatic', (parsed, rule, ctx) => functionRuleScan(parsed, rule, ctx)),
  'syntax-005': def('mismatched-quotes', 'automatic', (parsed, rule, ctx) => functionRuleScan(parsed, rule, ctx)),
  'syntax-006': def('missing-semicolon', 'automatic', (parsed, rule, ctx) => regexRuleScan(parsed, rule, ctx)),

  // ---- path-consistency（资料正确性）----
  'path-001': def('step-directory-mismatch', 'automatic', checkCreationReferenceConsistency),
  'path-002': def('step-file-mismatch', 'automatic', checkCreationReferenceConsistency),
  'path-003': def('sample-code-path-mismatch', 'automatic', checkSamplePathConsistency),
  'path-004': def('module-json5-srcentry-mismatch', 'automatic', checkSrcEntryConsistency),

  // ---- semantics（能力易用性 → capability 维度）----
  'semantics-001': def('bundlename-placeholder-clarity', 'automatic', checkPlaceholderClarity),
  'semantics-002': def('abilityname-unclear', 'automatic', checkPlaceholderClarity),
  'semantics-003': def('hardcoded-values-missing-note', 'automatic', checkPlaceholderClarity),
  'semantics-004': def('magic-number-missing-explanation', 'automatic', checkPlaceholderClarity),

  // ---- project-structure（资料正确性）----
  'structure-001': def('incorrect-directory-name', 'automatic', checkProjectStructure),
  'structure-002': def('incorrect-file-name', 'automatic', checkProjectStructure),
  'structure-003': def('wrong-file-extension', 'automatic', checkProjectStructure),

  // ---- findability（资源易找性）----
  'findability-001': def('keyword-accuracy', 'agent', agentRule),
  'findability-002': def('external-reference-completeness', 'automatic', checkExternalReference),
  'findability-003': def('document-discoverability', 'automatic', checkDiscoverability),

  // ---- completeness（资源丰富性/完整性）----
  'completeness-001': def('example-code-missing', 'automatic', checkExampleCompleteness),
  'completeness-002': def('critical-description-missing', 'automatic', checkRequiredSections),
  'completeness-003': def('constraint-missing', 'automatic', checkKeywordCoverage),
  'completeness-004': def('default-behavior-missing', 'automatic', checkDefaultBehavior),
  'completeness-005': def('related-info-missing', 'automatic', checkRequiredPatterns),

  // ---- correctness（资料正确性）----
  'correctness-001': def('version-update-lag', 'automatic', checkVersionSync),
  'correctness-002': def('example-code-broken', 'automatic', checkExampleValidity),
  'correctness-003': def('jsdoc-description-error', 'agent', agentRule),
  'correctness-004': def('path-consistency-across-doc', 'automatic', checkPathConsistency),
  'correctness-005': def('sensitive-info-leak', 'automatic', checkSensitiveInfoLeak),

  // ---- clarity（资源清晰易懂）----
  'clarity-001': def('title-content-mismatch', 'agent', agentRule),
  'clarity-002': def('description-accuracy', 'automatic', checkAmbiguousWording),
  'clarity-003': def('missing-related-links', 'automatic', checkConceptLinks),
  'clarity-004': def('mechanism-explanation-missing', 'automatic', checkRequiredSections),
  'clarity-005': def('terminology-consistency', 'automatic', checkTerminologyConsistency),

  // ---- capability（能力有效性/易用性/丰富性）----
  'capability-001': def('constraint-missing', 'automatic', checkKeywordCoverage),
  'capability-002': def('known-issues-missing', 'automatic', checkKeywordCoverage),
  'capability-003': def('outdated-documentation', 'automatic', checkDeprecationMarks),
  'capability-004': def('naming-ambiguity', 'automatic', checkAmbiguousWording),
  'capability-005': def('example-not-practical', 'agent', agentRule),
  'capability-006': def('alternative-missing', 'automatic', checkKeywordCoverage),
  'capability-007': def('system-capability-missing', 'automatic', checkRequiredPatternPresence),
  'capability-008': def('debugging-support-missing', 'automatic', checkKeywordCoverage),
  'capability-009': def('scenario-coverage', 'agent', agentRule),
  'capability-010': def('step-imperative-missing', 'agent', agentRule),
  'capability-011': def('missing-precautions', 'automatic', checkKeywordCoverage)
};
```

### 4.2 通用声明式驱动

规则的判定依据全部来自 JSON 配置，因此**新增同类规则只需编辑 JSON**；只有引入新的驱动类型或函数处理器时才需要改本文档，并同步在 `RULE_HANDLERS` 登记。

```javascript
// 正则型规则（pattern.type === 'regex'）：逐行扫描，报告命中行
function regexRuleScan(parsed, rule, context) {
  const issues = [];
  const scope = rule.checkInCodeBlocks === true ? 'code' : (rule.checkInCodeBlocks === false ? 'all' : 'all');
  const targets = scope === 'code'
    ? parsed.codeBlocks.flatMap(b => b.lines)
    : parsed.lines.map((text, i) => ({ text, lineNo: i + 1 }));

  for (const { text, lineNo } of targets) {
    const hits = countRegexMatches(text, rule.pattern.value, rule.pattern.flags ?? '');
    if (hits === 0) continue;
    issues.push(makeIssue(rule, context, {
      line: lineNo,
      description: `${rule.message}（命中 ${hits} 处）`,
      evidence: text.trim().slice(0, 160)
    }));
  }
  return issues;
}

// 函数型规则（pattern.type === 'function'）：调用 FUNCTION_HANDLERS 中登记的实现
const FUNCTION_HANDLERS = {
  checkUnclosedBraces: (code, rule) => balanceScan(code, rule, '{', '}'),
  checkUnclosedParentheses: (code, rule) => balanceScan(code, rule, '(', ')'),
  checkUnclosedBrackets: (code, rule) => balanceScan(code, rule, '[', ']'),
  checkUnbalancedQuotes: (code, rule) => quoteBalanceScan(code, rule)
};

function functionRuleScan(parsed, rule, context) {
  const handler = FUNCTION_HANDLERS[rule.pattern?.name];
  if (!handler) {
    throw new Error(`规则 ${rule.id} 引用的函数处理器 "${rule.pattern?.name}" 未实现（禁止返回空结果）`);
  }
  const issues = [];
  for (const block of parsed.codeBlocks) {
    for (const hit of handler(block.content, rule)) {
      issues.push(makeIssue(rule, context, {
        line: block.startLine + hit.offset,
        lineEnd: hit.offsetEnd === undefined ? undefined : block.startLine + hit.offsetEnd,
        description: hit.detail ? `${rule.message}：${hit.detail}` : rule.message,
        evidence: hit.evidence ?? null
      }));
    }
  }
  return issues;
}

// 关键词组的适用条件：只在文档确实涉及该主题时才要求对应说明，避免成片误报。
// 门禁只看文档形态特征，不能与该组的关键词列表相同（否则检查恒真、等于没查）。
const KEYWORD_GROUP_APPLICABILITY = {
  // capability-001 requiredConstraints
  systemApi: (parsed) => /-sys\.md$/.test(parsed.fileName) || /@systemapi|系统接口/.test(parsed.content),
  newApi: (parsed) => parsed.docType === 'api-doc' || /<sup>\s*\d+\s*\+?\s*<\/sup>|起始版本|@since/.test(parsed.content),
  performanceSensitive: (parsed) => /性能|耗时|频繁调用|资源占用|调用频率/.test(parsed.content),
  // capability-002 keywords：文档已涉及限制/注意事项时，才要求给出已知问题与规避方案
  knownIssues: (parsed) => parsed.docType === 'dev-guide' || /已知问题|限制|暂不支持|当前版本|注意事项/.test(parsed.content),
  workaround: (parsed, rule) => groupHasHit(parsed, rule, 'knownIssues'),
  // capability-006 keywords
  alternative: (parsed) => /方案|选型|多种|或者|另一种/.test(parsed.content),
  comparison: (parsed) => /方案|选型|多种|或者|另一种/.test(parsed.content),
  // capability-008 keywords
  errorHandling: (parsed) => parsed.docType === 'api-doc' || /错误码|异常|BusinessError/.test(parsed.content),
  debugging: (parsed) => parsed.docType === 'api-doc' || /错误码|异常|BusinessError/.test(parsed.content),
  // capability-011 keywords：只对不可逆/高代价操作要求前置警示
  precautions: (parsed) => /删除|清空|重置|不可逆|数据丢失|重启|恢复出厂/.test(parsed.content),
  // completeness-003 keywords
  device: (parsed) => parsed.docType === 'api-doc',
  systemCapability: (parsed) => parsed.docType === 'api-doc',
  version: () => true,
  permission: () => true,
  // clarity-004 keywords
  mechanism: (parsed) => /原理|机制|流程|架构|生命周期/.test(parsed.content),
  lifecycle: (parsed) => /生命周期|状态流转|回调时机|销毁/.test(parsed.content)
};

function ruleKeywordGroups(rule) {
  return rule.keywords ?? rule.requiredConstraints ?? {};
}

function groupHasHit(parsed, rule, groupName) {
  const keywords = ruleKeywordGroups(rule)[groupName];
  if (!keywords) return false;
  const list = (Array.isArray(keywords) ? keywords : Object.values(keywords).flat()).map(kw => String(kw).trim());
  return list.some(kw => kw && parsed.content.includes(kw));
}

// 关键词组覆盖：每组至少命中一个关键词；所有缺失组合并为一条问题（避免同一规则刷屏）
function checkKeywordCoverage(parsed, rule, context) {
  const missing = [];

  for (const [groupName, keywords] of Object.entries(ruleKeywordGroups(rule))) {
    const gate = KEYWORD_GROUP_APPLICABILITY[groupName];
    if (gate && !gate(parsed, rule)) continue;          // 该组对当前文档不适用

    const list = (Array.isArray(keywords) ? keywords : Object.values(keywords).flat())
      .map(kw => String(kw).trim())
      .filter(Boolean);
    if (list.length === 0) continue;
    if (list.some(kw => parsed.content.includes(kw))) continue;

    missing.push({ groupName, list });
  }

  if (missing.length === 0) return [];

  return [makeIssue(rule, context, {
    description: `${rule.message}：缺少 ${missing.map(m => `「${m.groupName}」`).join('、')} 相关说明`,
    suggestedFix: rule.suggestedFix ?? missing.map(m => `补充 ${m.groupName} 说明（如 ${m.list.slice(0, 3).join(' / ')}）`).join('；'),
    // 门禁是启发式判定，命中后仍需人工确认，置信度按 scoring-guide 下调一档
    confidence: Math.max(50, (rule.confidence ?? 70) - 15),
    evidence: missing.map(m => `${m.groupName}: [${m.list.join('|')}] 全部未命中`).join('; ')
  })];
}

// completeness-004：可选参数/默认行为说明。文档没有可选参数时本规则不适用
function checkDefaultBehavior(parsed, rule, context) {
  const shouldExplain = rule.indicators?.shouldExplain ?? [];
  const hasOptionalParam = parsed.tables.some(t => t.header.some(h => h.includes('必填'))
    && t.rows.some(r => cleanCell(r.cells[2] ?? '') === '否'));
  const mentionsOptional = /可选|非必填|不传|缺省/.test(parsed.content);

  if (!hasOptionalParam && !mentionsOptional) return [];
  if (shouldExplain.some(kw => parsed.content.includes(kw))) return [];

  return [makeIssue(rule, context, {
    description: `${rule.message}：文档存在可选参数/可选行为，但未说明默认值或默认行为`,
    suggestedFix: rule.suggestedFix ?? '为每个可选参数补充默认值与未设置时的行为说明',
    evidence: `indicators.shouldExplain [${shouldExplain.join('|')}] 全部未命中`
  })];
}

// 必备章节检查。requiredSections 有两种语义，必须区分，否则会静默不检查或成片误报：
// - 按文档类型分组（completeness-002 的 apiDoc/guideDoc）：组内章节**全部**必备
// - 按内容特征分组（clarity-004 的 complexFeature/lifecycle）：仅当 rule.keywords[组名] 的触发词出现时才要求，且组内**任一**章节即可
// indicators.shouldHaveSections（findability-003）为"任一即可"
// requiredSections 的键有两种含义，必须区分，否则会把另一种文档类型的章节要求套到当前文档上：
// - 文档类型键（apiDoc/guideDoc）：只有与当前 docType 相同的那一组生效，组内章节**全部**必备
// - 内容特征键（如 complexFeature/lifecycle）：仅当对应触发词出现时才生效，组内**任一**章节即可
const DOC_TYPE_SECTION_KEYS = new Set(['apiDoc', 'guideDoc']);
// 特征键与 keywords 键的对应关系（clarity-004 用 complexFeature 描述"机制原理"这一特征）
const SECTION_TRIGGER_ALIASES = { complexFeature: ['mechanism', 'complexFeature'] };

function resolveSectionGroups(parsed, rule) {
  const groups = [];
  const docTypeKey = parsed.docType === 'dev-guide' ? 'guideDoc' : 'apiDoc';

  for (const [key, names] of Object.entries(rule.requiredSections ?? {})) {
    if (!Array.isArray(names) || names.length === 0) continue;

    if (DOC_TYPE_SECTION_KEYS.has(key)) {
      if (key === docTypeKey) groups.push({ key, names, mode: 'all', applies: true });
      continue;                                  // 另一种文档类型的章节要求不适用于当前文档
    }

    if (key === 'apiDocPerSection') {
      // 逐个 API 章节检查（接口/枚举章节不适用），scope=per-section
      groups.push({ key, names, mode: 'all', applies: parsed.docType === 'api-doc', scope: 'section' });
      continue;
    }

    const triggerKeys = SECTION_TRIGGER_ALIASES[key] ?? [key];
    const triggers = triggerKeys.flatMap(k => rule.keywords?.[k] ?? []);
    // 没有触发词就无法判定该特征是否存在：判为不适用，而不是无条件要求
    groups.push({
      key, names, mode: 'any',
      applies: triggers.length > 0 && triggers.some(kw => parsed.content.includes(String(kw)))
    });
  }

  if (Array.isArray(rule.indicators?.shouldHaveSections)) {
    groups.push({ key: 'shouldHaveSections', names: rule.indicators.shouldHaveSections, mode: 'any', applies: true });
  }
  return groups.filter(g => g.applies);
}

// 逐 API 章节检查必备小节：把每个 API 章节切成一个局部视图后复用 sectionPresent
function checkSectionsPerApiUnit(parsed, rule, context, group) {
  const issues = [];

  for (const unit of collectExampleUnits(parsed)) {
    const section = parsed.sections.find(sec => sec.startLine === unit.startLine);
    if (!section) continue;

    const localView = {
      content: section.body,
      headings: parsed.headings.filter(h => h.line >= unit.startLine && h.line <= unit.endLine),
      tables: parsed.tables.filter(t => t.startLine >= unit.startLine && t.endLine <= unit.endLine + 1)
    };

    const missing = group.names.filter(name => !sectionPresent(localView, name));
    if (missing.length === 0) continue;

    issues.push(makeIssue(rule, context, {
      line: unit.startLine,
      lineEnd: unit.endLine,
      description: `${rule.message}：${unit.name} 章节缺少「${missing.join('」、「')}」小节`,
      suggestedFix: rule.suggestedFix ?? `为 ${unit.name} 补充 ${missing.join('、')} 小节`,
      evidence: `requiredSections.${group.key} 在 ${unit.name} 缺失: [${missing.join('|')}]`
    }));
  }
  return issues;
}

// 章节是否"存在"：标题、粗体标签（**参数**：）、或表格表头三者任一即可。
// OpenHarmony API 文档普遍用粗体标签而非 Markdown 标题组织参数/返回值/错误码，只认标题会成片误报。
function sectionPresent(parsed, name) {
  if (parsed.headings.some(h => h.text.includes(name))) return true;
  if (new RegExp(`\\*\\*\\s*${escapeRegex(name)}\\s*\\*\\*`).test(parsed.content)) return true;
  return parsed.tables.some(t => t.header.some(h => h.includes(name)));
}

function checkRequiredSections(parsed, rule, context) {
  const groups = resolveSectionGroups(parsed, rule);
  if (groups.length === 0) {
    // 没有可判定的章节配置时不能假装通过：明确记为不适用，由台账呈现
    return notApplicable(`规则 ${rule.id} 对文档类型 ${parsed.docType} 没有可判定的必备章节配置`);
  }

  const issues = [];

  for (const group of groups) {
    if (group.scope === 'section') {
      issues.push(...checkSectionsPerApiUnit(parsed, rule, context, group));
      continue;
    }

    const present = group.names.filter(name => sectionPresent(parsed, name));
    const missing = group.names.filter(name => !sectionPresent(parsed, name));

    if (group.mode === 'any') {
      if (present.length > 0) continue;
      const inBody = group.names.filter(name => parsed.content.includes(name));
      issues.push(makeIssue(rule, context, {
        description: `${rule.message}：缺少「${group.names.join(' / ')}」任一章节`,
        priority: inBody.length > 0 ? 'low' : rule.priority,
        confidence: inBody.length > 0 ? Math.max(50, (rule.confidence ?? 70) - 20) : rule.confidence,
        line: parsed.headings[parsed.headings.length - 1]?.line ?? null,
        evidence: `${group.key}（任一即可）: [${group.names.join('|')}] 均未作为章节标题出现`
      }));
      continue;
    }

    // mode === 'all'：合并为一条问题，避免同一规则刷屏
    if (missing.length === 0) continue;
    const missingInBodyOnly = missing.filter(name => parsed.content.includes(name));
    const fullyMissing = missing.filter(name => !parsed.content.includes(name));
    void present;
    issues.push(makeIssue(rule, context, {
      description: `${rule.message}：缺少必备章节 ${missing.map(n => `「${n}」`).join('、')}`
        + (missingInBodyOnly.length > 0 ? `（其中 ${missingInBodyOnly.join('、')} 在正文有相关字样但无独立章节）` : ''),
      priority: fullyMissing.length === 0 ? 'low' : rule.priority,
      confidence: fullyMissing.length === 0 ? Math.max(50, (rule.confidence ?? 70) - 20) : rule.confidence,
      line: parsed.headings[0]?.line ?? null,
      evidence: `requiredSections.${group.key} 缺失: [${missing.join('|')}]`
    }));
  }

  return issues;
}

// 正则/字面量模式扫描：patterns、ambiguousPatterns、requiredPatterns 共用
// spec.expect: 'hit' = 命中即报告；'missing' = 未命中才报告（文档本应出现该内容）
// options.lines 可指定扫描视图（默认全文逐行）；证据始终取原始行文本
function scanPatternSpecs(parsed, rule, context, specs, options = {}) {
  const issues = [];
  const missingSpecs = [];
  const hitsByLine = new Map();       // 同一行被同一规则多次命中时合并
  const view = options.lines ?? parsed.lines.map((text, idx) => ({ text, lineNo: idx + 1 }));

  for (const spec of specs) {
    const matcher = spec.kind === 'regex'
      ? (text) => countRegexMatches(text, spec.pattern, spec.flags ?? '') > 0
      : (text) => text.includes(spec.pattern);

    const hitLines = view.filter(entry => entry.text && matcher(entry.text)).map(entry => entry.lineNo);

    if (spec.expect === 'missing') {
      if (hitLines.length > 0) continue;              // 已出现，符合要求
      missingSpecs.push(spec);                        // 缺失项合并成一条，避免同一规则刷屏
      continue;
    }

    for (const line of hitLines) {
      const key = `${line}`;
      const existing = hitsByLine.get(key);
      const entry = {
        line,
        description: spec.message ?? rule.message,
        suggestedFix: spec.suggestion ?? spec.suggestedFix ?? rule.suggestedFix,
        priority: spec.severity ?? rule.priority,
        matched: spec.pattern
      };
      if (existing) {
        // 同一行被同一规则的多个模式命中：合并为一条，描述里列出全部命中项
        existing.description = `${rule.message}（命中：${existing.matched}、${spec.pattern}）`;
        existing.suggestedFix = [existing.suggestedFix, entry.suggestedFix].filter(Boolean).join('；');
        existing.matched = `${existing.matched}、${spec.pattern}`;
        continue;
      }
      hitsByLine.set(key, entry);
    }
  }

  for (const entry of hitsByLine.values()) {
    issues.push(makeIssue(rule, context, {
      line: entry.line,
      description: entry.description,
      suggestedFix: entry.suggestedFix,
      priority: entry.priority,
      evidence: parsed.lines[entry.line - 1].trim().slice(0, 160)
    }));
  }

  if (missingSpecs.length > 0) {
    issues.push(makeIssue(rule, context, {
      description: missingSpecs.length === 1
        ? (missingSpecs[0].message ?? rule.message)
        : `${rule.message}：${missingSpecs.map(spec => spec.message ?? spec.pattern).join('；')}`,
      suggestedFix: missingSpecs.map(spec => spec.suggestion ?? spec.suggestedFix).filter(Boolean).join('；') || rule.suggestedFix,
      evidence: `未匹配到 ${missingSpecs.map(spec => spec.pattern).join(' / ')}`
    }));
  }

  return issues;
}

// 按规则的 checkInCodeBlocks 决定扫描范围
function scopeLines(parsed, rule) {
  const all = parsed.lines.map((text, idx) => ({ text, lineNo: idx + 1 }));
  if (rule.checkInCodeBlocks !== false) return all;

  const codeLines = codeBlockLineSet(parsed);
  return all.filter(entry => !codeLines.has(entry.lineNo)).map(entry => ({
    ...entry,
    text: entry.text.replace(/`[^`]*`/g, m => ' '.repeat(m.length))    // 行内代码不参与拼写判定
  }));
}

function codeBlockLineSet(parsed) {
  const lines = new Set();
  for (const block of parsed.codeBlocks) {
    const from = block.fenceLine ?? block.startLine - 1;
    const to = block.endLine ?? (block.startLine + block.lineCount);
    for (let i = from; i <= to; i++) lines.add(i);
  }
  return lines;
}

// 描述性文本视图：排除代码块、行内代码，以及表格首列（参数名/名称列）。
// 专有名词大小写规范只约束描述文字——callback、resource、want 这类小写形式在标识符位置是合法写法。
function proseView(parsed) {
  const codeLines = codeBlockLineSet(parsed);

  return parsed.lines.map((text, idx) => {
    const lineNo = idx + 1;
    if (codeLines.has(lineNo)) return { text: '', lineNo };

    let masked = text.replace(/`[^`]*`/g, m => ' '.repeat(m.length));
    if (/^\s*\|/.test(masked)) masked = maskFirstTableCell(masked);
    return { text: masked, lineNo };
  });
}

function maskFirstTableCell(line) {
  const start = line.indexOf('|');
  const end = line.indexOf('|', start + 1);
  if (start < 0 || end < 0) return line;
  return line.slice(0, start + 1) + ' '.repeat(end - start - 1) + line.slice(end);
}

function checkAmbiguousWording(parsed, rule, context) {
  const specs = (rule.ambiguousPatterns ?? []).map(item => ({
    // type=keyword 表示字面量（如 "..."、"等等"）；缺省按正则处理（如 "doSomething|processData"）
    kind: item.type === 'keyword' ? 'literal' : 'regex',
    pattern: item.pattern,
    message: item.issue ? `${rule.message}：${item.issue}` : rule.message,
    suggestion: item.suggestion,
    expect: 'hit'
  }));
  return scanPatternSpecs(parsed, rule, context, specs);
}

function checkRequiredPatterns(parsed, rule, context) {
  const specs = (rule.requiredPatterns ?? []).map(item => ({
    kind: 'regex', pattern: item.pattern, message: item.message ?? rule.message, expect: 'missing'
  }));
  return scanPatternSpecs(parsed, rule, context, specs);
}

function checkRequiredPatternPresence(parsed, rule, context) {
  if (!rule.requiredPattern) return [];
  const specs = [{ kind: 'regex', pattern: rule.requiredPattern, message: rule.message, expect: 'missing' }];
  return scanPatternSpecs(parsed, rule, context, specs);
}

function checkDeprecationMarks(parsed, rule, context) {
  const indicators = rule.deprecationIndicators ?? [];
  const deprecatedHit = indicators.some(p => new RegExp(p.startsWith('@') ? p.replace('@', '\\@') : p).test(parsed.content));
  if (!deprecatedHit) return [];      // 文档未涉及废弃 API，本规则不适用（台账仍记 executed）

  const hasAlternative = /替代|请使用|改用|迁移/.test(parsed.content);
  if (hasAlternative) return [];
  return [makeIssue(rule, context, {
    description: `${rule.message}：出现废弃标记但未给出替代方案`,
    evidence: indicators.filter(p => parsed.content.includes(p)).join(', ')
  })];
}
```

### 4.3 资源丰富性/完整性执行器

`completeness-001` 的判定条件曾写成 `codeBlocks.length < rule.validation?.codeBlockMinCount || 1`：`<` 优先级高于 `||`，比较为假时整个表达式仍返回真值 `1`，导致**任何文档都被判为缺少示例**。修复为 `?? 1`（仅在读数缺失时取默认值），并按「每个 API/场景」而非全篇数量判定。

```javascript
function checkExampleCompleteness(parsed, rule, context) {
  const issues = [];
  const minCount = rule.validation?.codeBlockMinCount ?? 1;
  const minLines = rule.validation?.codeBlockMinLines ?? 0;

  // 按 API/场景粒度检查：每个 API 章节（或开发指南的每个操作步骤）都应至少有一个示例
  const units = collectExampleUnits(parsed);

  for (const unit of units) {
    const blocks = parsed.codeBlocks.filter(b => b.startLine >= unit.startLine && (b.endLine ?? b.startLine) <= unit.endLine);

    if (blocks.length < minCount) {
      issues.push(makeIssue(rule, context, {
        line: unit.startLine,
        lineEnd: unit.endLine,
        description: `${rule.message}：${unit.name} 有 ${blocks.length} 个代码块，少于要求的 ${minCount} 个`,
        suggestedFix: rule.suggestedFix ?? `为 ${unit.name} 补充可运行示例代码`,
        evidence: `codeBlockMinCount=${minCount}, actual=${blocks.length}`
      }));
      continue;
    }

    if (minLines > 0) {
      const tooShort = blocks.filter(b => b.lineCount < minLines);
      if (tooShort.length === blocks.length) {
        issues.push(makeIssue(rule, context, {
          line: tooShort[0].startLine,
          description: `${rule.message}：${unit.name} 的示例代码不足 ${minLines} 行，可能不完整`,
          priority: 'medium',
          confidence: Math.max(60, (rule.confidence ?? 80) - 15),
          evidence: `codeBlockMinLines=${minLines}, actual=${tooShort.map(b => b.lineCount).join('/')}`
        }));
      }
    }
  }

  // 全文没有任何代码块时（例如无章节结构的短文档）兜底报告一次
  if (units.length === 0 && parsed.codeBlocks.length < minCount) {
    issues.push(makeIssue(rule, context, {
      line: 1,
      description: `${rule.message}：全文 ${parsed.codeBlocks.length} 个代码块，少于要求的 ${minCount} 个`,
      evidence: `codeBlockMinCount=${minCount}, actual=${parsed.codeBlocks.length}`
    }));
  }

  return issues;
}

// API 文档：每个"函数型" API 章节为一个单元（接口/枚举章节只有属性表，不要求示例代码）；
// 开发指南：每个编号步骤为一个单元
function collectExampleUnits(parsed) {
  if (parsed.docType === 'api-doc') {
    return parsed.sections
      .filter(s => s.level >= 2 && /^[A-Za-z_$][\w$.]*/.test(s.title))
      .filter(s => !/\*\*属性\*\*|\*\*枚举值\*\*/.test(s.body))
      .map(s => ({ name: s.title, startLine: s.startLine, endLine: s.endLine }));
  }

  const units = [];
  let current = null;
  for (const { text, lineNo } of parsed.lines.map((t, i) => ({ text: t, lineNo: i + 1 }))) {
    const step = text.match(/^\s*(\d+)[.)]\s+(.*)$/);
    if (step) {
      if (current) current.endLine = lineNo - 1;
      current = { name: `步骤${step[1]} ${step[2].slice(0, 30)}`, startLine: lineNo, endLine: parsed.lines.length };
      units.push(current);
    }
  }
  if (units.length > 0) {
    const lastHeading = parsed.headings.filter(h => h.line < units[0].startLine).pop();
    units[units.length - 1].endLine = parsed.lines.length;
    void lastHeading;
  }
  return units;
}
```

### 4.4 资料正确性执行器

```javascript
function checkVersionSync(parsed, rule, context) {
  const specs = [];
  const versionPatterns = rule.validation?.versionPatterns ?? [];

  // API 文档必须使用 <sup>N+</sup> 标注版本；直接写 nameN+ 会让锚点与渲染都出错
  if (parsed.docType === 'api-doc') {
    const badVersionHeadings = parsed.headings.filter(h => /[A-Za-z_$][\w$.]*\d+\+\s*$/.test(h.text));
    for (const heading of badVersionHeadings) {
      specs.push({
        kind: 'literal', pattern: heading.text, expect: 'hit',
        message: `${rule.message}：版本标记未使用 <sup> 上标格式（"${heading.text}"）`,
        suggestion: rule.suggestedFix ?? `改为 ${heading.text.replace(/(\d+\+)$/, '<sup>$1</sup>')}`,
        severity: 'medium'
      });
    }
  }

  const issues = scanPatternSpecs(parsed, rule, context, specs);

  // 废弃标记存在但无替代方案由 capability-003 负责，此处只校验版本标记格式与变更说明
  const hasDeprecation = (rule.validation?.deprecationPatterns ?? []).some(p => parsed.content.includes(p));
  if (hasDeprecation && !/替代|请使用|改用|迁移/.test(parsed.content)) {
    issues.push(makeIssue(rule, context, {
      description: `${rule.message}：文档含废弃说明但未给出替代方案`,
      priority: 'medium'
    }));
  }
  return issues;
}

function checkExampleValidity(parsed, rule, context) {
  // 复用 syntax 模块的函数式检查器，对每个代码块做括号/引号配对验证；
  // 同一代码块的多处语法问题合并为一条，避免与 syntax-002/003/004/005 叠加刷屏
  const issues = [];
  const checks = Object.entries(FUNCTION_HANDLERS);

  for (const block of parsed.codeBlocks) {
    const hits = [];
    for (const [name, handler] of checks) {
      const syntaxRule = { id: rule.id, name: rule.name, message: rule.message, priority: rule.priority, confidence: rule.confidence };
      for (const hit of handler(block.content, syntaxRule)) {
        hits.push({ ...hit, checker: name });
      }
    }
    if (hits.length === 0) continue;

    issues.push(makeIssue(rule, context, {
      line: block.startLine + hits[0].offset,
      lineEnd: block.endLine ?? undefined,
      description: `${rule.message}：${hits.map(h => h.detail ?? h.checker).join('；')}`,
      evidence: hits.map(h => h.evidence ?? h.checker).filter(Boolean).join(' | ').slice(0, 200)
    }));
  }
  return issues;
}

function checkPathConsistency(parsed, rule, context) {
  // 文档内部路径一致性：同名目录/文件在不同步骤中的写法必须一致
  return checkCreationReferenceConsistency(parsed, rule, context);
}

// correctness-005：敏感信息泄露。规则 patterns 中 type=keyword 的项按 | 拆词做字面量匹配，
// type=regex 的项按正则匹配；示例号码/示例 IP 属规范推荐写法，必须放行，否则规则自身示例就会触发告警。
const SENSITIVE_ALLOWLIST = ['13000000000', '127.0.0.1', '0.0.0.0'];
const SENSITIVE_ALLOW_PREFIXES = ['192.168.', '10.0.0.', '172.16.0.'];

function isAllowlistedSensitiveValue(value) {
  const text = String(value);
  return SENSITIVE_ALLOWLIST.includes(text) || SENSITIVE_ALLOW_PREFIXES.some(p => text.startsWith(p));
}

function checkSensitiveInfoLeak(parsed, rule, context) {
  const issues = [];

  for (const item of rule.patterns ?? []) {
    if (item.type === 'keyword') {
      for (const word of String(item.pattern).split('|').map(w => w.trim()).filter(Boolean)) {
        parsed.lines.forEach((text, idx) => {
          if (!text.includes(word)) return;
          issues.push(makeIssue(rule, context, {
            line: idx + 1,
            description: item.message ?? rule.message,
            priority: item.severity ?? rule.priority,
            evidence: text.trim().slice(0, 160)
          }));
        });
      }
      continue;
    }

    const re = new RegExp(item.pattern, 'g');
    parsed.lines.forEach((text, idx) => {
      const hits = [...text.matchAll(re)].map(m => m[0]).filter(v => !isAllowlistedSensitiveValue(v));
      if (hits.length === 0) return;
      issues.push(makeIssue(rule, context, {
        line: idx + 1,
        description: `${item.message ?? rule.message}（命中：${hits.join(', ')}）`,
        priority: item.severity ?? rule.priority,
        evidence: text.trim().slice(0, 160)
      }));
    });
  }

  return issues;
}
```

### 4.5 其余模块执行器

```javascript
function checkCommonMisspelling(parsed, rule, context) {
  const table = context.ruleFile?.data?.commonMisspellings ?? {};
  const specs = Object.entries(table)
    // 对照表里存在 "separate": "separate" 这类自反条目，直接扫描会把正确写法报成错误
    .filter(([wrong, correct]) => String(wrong).toLowerCase() !== String(correct).toLowerCase())
    .map(([wrong, correct]) => ({
      kind: 'literal', pattern: wrong, expect: 'hit',
      message: (rule.message ?? '').replace('{wrong}', wrong).replace('{correct}', correct),
      suggestion: `将 "${wrong}" 改为 "${correct}"`,
      severity: rule.priority
    }));
  return scanPatternSpecs(parsed, rule, context, specs, { lines: scopeLines(parsed, rule) });
}

// harmonyOSGlossary 是多层嵌套结构：{ 分类: { 术语: { correct, variants[] } } }，
// 也兼容 { 术语: [variants] } 与 { 错误写法: 正确写法 } 两种扁平写法，因此递归收集。
function collectGlossaryPairs(node, pairs = []) {
  if (!node || typeof node !== 'object') return pairs;

  if (Array.isArray(node)) return pairs;

  if (typeof node.correct === 'string' && Array.isArray(node.variants)) {
    for (const wrong of node.variants) {
      if (wrong !== node.correct) pairs.push({ wrong, correct: node.correct });
    }
    return pairs;
  }

  for (const [key, value] of Object.entries(node)) {
    if (value && typeof value === 'object') {
      collectGlossaryPairs(value, pairs);
    } else if (Array.isArray(value)) {
      for (const wrong of value) if (wrong !== key) pairs.push({ wrong, correct: key });
    } else if (typeof value === 'string' && value !== key) {
      pairs.push({ wrong: key, correct: value });
    }
  }
  return pairs;
}

function checkHarmonyosGlossary(parsed, rule, context) {
  const pairs = collectGlossaryPairs(context.ruleFile?.data?.harmonyOSGlossary ?? {});
  const specs = pairs.map(({ wrong, correct }) => ({
    kind: 'literal', pattern: wrong, expect: 'hit',
    message: (rule.message ?? '').replace('{wrong}', wrong).replace('{correct}', correct),
    suggestion: `将 "${wrong}" 改为 "${correct}"`,
    severity: rule.priority
  }));
  // 术语大小写只在描述性文本中判定（见 spelling-002 的 checkScopeNote）
  return scanPatternSpecs(parsed, rule, context, specs, { lines: proseView(parsed) });
}

function checkUnknownDecorator(parsed, rule, context) {
  const valid = new Set(rule.validDecorators ?? []);
  const issues = [];
  const re = new RegExp(rule.pattern ?? '@([A-Za-z]+)', 'g');

  for (const block of parsed.codeBlocks) {
    block.lines.forEach(({ text, lineNo }) => {
      for (const m of text.matchAll(re)) {
        const decorator = m[1] ?? m[0].replace('@', '');
        if (valid.has(decorator)) continue;
        issues.push(makeIssue(rule, context, {
          line: lineNo,
          description: (rule.message ?? '').replace('{decorator}', decorator),
          evidence: text.trim().slice(0, 120)
        }));
      }
    });
  }
  return issues;
}

// path-001 / path-002 / correctness-004：创建名 vs 引用名交叉比对
function checkCreationReferenceConsistency(parsed, rule, context) {
  const extraction = rule.extraction ?? {};
  const caseSensitive = rule.validation?.caseSensitive ?? false;
  const norm = (v) => (caseSensitive ? v : v.toLowerCase());

  const created = collectByPatterns(parsed, extraction.creationPatterns);
  const referenced = collectByPatterns(parsed, extraction.referencePatterns);

  if (created.length === 0 || referenced.length === 0) return [];

  const createdKeys = new Map(created.map(c => [norm(c.value), c]));
  const issues = [];

  for (const ref of referenced) {
    if (createdKeys.has(norm(ref.value))) continue;
    // 只在存在"形似但不一致"的创建名时报告，避免把无关引用当缺陷
    const similar = created.find(c => norm(c.value).replace(/[-_]/g, '') === norm(ref.value).replace(/[-_]/g, '')
      || looksLikeSameName(norm(c.value), norm(ref.value)));
    if (!similar) continue;
    issues.push(makeIssue(rule, context, {
      line: ref.line,
      description: `${rule.message}：引用 "${ref.value}" 与步骤中创建的 "${similar.value}"（L${similar.line}）不一致`,
      suggestedFix: rule.suggestedFix ?? `统一为 "${similar.value}"`,
      evidence: `${similar.value} (L${similar.line}) vs ${ref.value} (L${ref.line})`
    }));
  }
  return issues;
}

function collectByPatterns(parsed, specs) {
  const found = [];
  for (const spec of specs ?? []) {
    const re = new RegExp(spec.pattern, 'g');
    parsed.lines.forEach((text, idx) => {
      for (const m of text.matchAll(re)) {
        const value = m[1];
        if (!value) continue;
        found.push({ value, line: idx + 1, type: spec.type ?? null });
      }
    });
  }
  return found;
}

// 形似判定：长度接近且共享 3 字符以上前缀（用于把 myabilitystage / exampleabilitystage 关联起来）
function looksLikeSameName(a, b) {
  if (a === b) return true;
  if (a.length < 4 || b.length < 4) return false;
  if (Math.abs(a.length - b.length) > Math.max(a.length, b.length) * 0.6) return false;
  return a.endsWith(b) || b.endsWith(a) || a.slice(0, 3) === b.slice(0, 3);
}

// path-003：与 Sample 仓库比对，需要外部数据。缺数据时返回 not-executed（进入台账与汇总，
// 影响评分），绝不允许静默按"0 问题"处理。
function checkSamplePathConsistency(parsed, rule, context) {
  const sampleData = context.options?.sampleData;
  if (rule.requiresExternalData && !sampleData) {
    return notExecuted(`规则 ${rule.id} 需要外部 Sample 数据（options.sampleData 或 ${rule.reference}），未提供`);
  }

  const docNames = collectByPatterns(parsed, rule.extraction?.creationPatterns ?? []);
  if (docNames.length === 0) {
    return notApplicable('文档未创建目录/文件，无需与 Sample 比对');
  }

  const issues = [];
  for (const item of docNames) {
    const sampleValue = sampleData?.[item.value];
    if (sampleValue === undefined || sampleValue === item.value) continue;
    issues.push(makeIssue(rule, context, {
      line: item.line,
      description: `${rule.message}：文档用 "${item.value}"，Sample 用 "${sampleValue}"`,
      suggestedFix: rule.suggestedFix ?? `与 Sample 保持一致，改为 "${sampleValue}"`,
      evidence: `${rule.reference ?? 'sample'} → ${sampleValue}`
    }));
  }
  return issues;
}

// path-004：module.json5 的 srcEntry 与步骤中创建的目录名一致性
function checkSrcEntryConsistency(parsed, rule, context) {
  const extraction = rule.extraction ?? {};
  if (!extraction.srcEntryPattern) return [];
  if (!parsed.content.includes('srcEntry')) return [];

  const srcEntryRe = new RegExp(extraction.srcEntryPattern, 'g');
  const dirRe = extraction.directoryInPathPattern ? new RegExp(extraction.directoryInPathPattern, 'g') : null;
  const createdDirs = new Set(collectByPatterns(parsed, [
    { pattern: '(?:新建|创建)(?:一个)?目录(?:并命名)?[为:]?[\\s`"]*([a-zA-Z_][a-zA-Z0-9_]*)' }
  ]).map(item => item.value));

  const issues = [];
  parsed.lines.forEach((text, idx) => {
    for (const m of text.matchAll(srcEntryRe)) {
      const entryPath = m[1];
      const dirs = dirRe ? [...entryPath.matchAll(dirRe)].map(x => x[1]) : [];
      for (const dir of dirs) {
        if (createdDirs.size === 0 || createdDirs.has(dir)) continue;
        issues.push(makeIssue(rule, context, {
          line: idx + 1,
          description: `${rule.message}：srcEntry 指向 "${dir}"，但步骤中创建的目录是 ${[...createdDirs].join(', ')}`,
          suggestedFix: rule.suggestedFix ?? `统一目录名（srcEntry 或创建步骤二者之一需要修改）`,
          evidence: `${rule.scope ?? 'module.json5'}: ${entryPath}`
        }));
      }
    }
  });
  return issues;
}

// semantics-001..004：占位符清晰度与硬编码值说明
function checkPlaceholderClarity(parsed, rule, context) {
  const extraction = rule.extraction ?? {};
  const validation = rule.validation ?? {};
  const targets = extraction.targetPatterns ?? (extraction.targetPattern ? [extraction.targetPattern] : []);
  const issues = [];

  const explanationKeywords = validation.explanationKeywords ?? ['替换', '修改', '实际', 'your', '替换为', '根据'];
  const window = validation.checkSurroundingText ?? 200;
  const acceptable = new Set([...(validation.expectedPlaceholders ?? []), ...(validation.commonValues ?? [])]);
  const badExamples = new Set(validation.badExamples ?? []);

  for (const target of targets) {
    const re = new RegExp(target.pattern, 'g');
    const placeholders = new Set((target.isPlaceholder ?? []).map(String));

    parsed.lines.forEach((text, idx) => {
      for (const m of text.matchAll(re)) {
        const value = m[1];
        if (value === undefined) continue;
        const isPlaceholder = acceptable.has(value) || placeholders.has(value) || /your|example|xxx|<[^>]+>/i.test(value);
        const surrounding = parsed.content.slice(Math.max(0, m.index - window), m.index + window);
        const explained = explanationKeywords.some(kw => surrounding.includes(kw));

        if (validation.type === 'placeholder-check') {
          if (isPlaceholder || explained) continue;
          if (badExamples.size > 0 && !badExamples.has(value) && !validation.requireNote) continue;
        } else if (validation.type === 'context-check') {
          if (explained) continue;
          const exclude = (target.exclude ?? []).map(Number);
          if (exclude.includes(Number(value))) continue;
        } else if (isPlaceholder || explained) {
          continue;
        }

        issues.push(makeIssue(rule, context, {
          line: idx + 1,
          description: `${rule.message}：${target.property ?? '取值'} "${value}" ${isPlaceholder ? '' : '不是可识别占位符，'}且上下文未说明需替换`,
          evidence: text.trim().slice(0, 120)
        }));
      }
    });
  }
  return issues;
}

// structure-001..003：工程结构符合性。
// project-structure.json 的 structure.directories / structure.files 是 [{correct, wrong[], pathPattern}]，
// 检查逻辑是"文档里出现了 wrong 写法"，而不是白名单比对。
function checkProjectStructure(parsed, rule, context) {
  const data = context.ruleFile?.data ?? {};

  // structure-003：关键文件扩展名（EntryAbility 必须是 .ets，module 必须是 .json5）
  if (rule.criticalExtensions) {
    const issues = [];
    for (const [extension, names] of Object.entries(rule.criticalExtensions)) {
      for (const name of names) {
        const re = new RegExp(`(?<![\\w.-])${escapeRegex(name)}\\.([A-Za-z0-9]+)`, 'g');
        parsed.lines.forEach((text, idx) => {
          for (const m of text.matchAll(re)) {
            const usedExtension = `.${m[1]}`;
            if (usedExtension === extension) continue;
            issues.push(makeIssue(rule, context, {
              line: idx + 1,
              description: (rule.message ?? '').replace('{file}', `${name}${usedExtension}`)
                + `（应为 ${name}${extension}）`,
              priority: rule.priority,
              confidence: rule.confidence,
              evidence: text.trim().slice(0, 120)
            }));
          }
        });
      }
    }
    return issues;
  }

  const entries = rule.applyTo === 'files' ? (data.structure?.files ?? []) : (data.structure?.directories ?? []);
  const issues = [];
  // 代码围栏行（三个反引号 + 语言标记，如 ts）里的语言标记不是目录名，必须排除，否则 ts/ETS 等 wrong 变体会成片误报
  const fenceLines = new Set(parsed.codeBlocks.flatMap(b => [b.fenceLine, b.endLine, b.startLine - 1]));

  for (const entry of entries) {
    for (const wrong of entry.wrong ?? []) {
      // 目录名要求紧邻路径分隔符（/wrong 或 wrong/），避免把普通英文词误判为目录
      const re = rule.applyTo === 'files'
        ? new RegExp(`(?<![\\w.-])${escapeRegex(wrong)}(?![\\w-])`)
        : new RegExp(`(?:(?<=/)${escapeRegex(wrong)}|${escapeRegex(wrong)}(?=/))`);

      parsed.lines.forEach((text, idx) => {
        if (fenceLines.has(idx + 1)) return;
        if (!re.test(text)) return;
        issues.push(makeIssue(rule, context, {
          line: idx + 1,
          description: (rule.message ?? '').replace('{wrong}', wrong).replace('{correct}', entry.correct),
          priority: entry.priority ?? rule.priority,
          confidence: entry.confidence ?? rule.confidence,
          evidence: `${entry.description ?? ''} ${wrong} → ${entry.correct}`.trim()
        }));
      });
    }
  }
  return issues;
}

function escapeRegex(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function checkExternalReference(parsed, rule, context) {
  const specs = (rule.validation?.warningPatterns ?? []).map(item => ({
    kind: 'regex', pattern: item.pattern, flags: item.flags, message: item.message ?? rule.message,
    severity: item.level === 'warning' ? 'low' : rule.priority, expect: 'hit'
  }));
  const issues = scanPatternSpecs(parsed, rule, context, specs);

  // 页内锚点有效性：链接目标必须能在标题锚点中找到
  const anchors = new Set(parsed.headings.map(h => `#${h.anchor}`));
  for (const link of parsed.links.filter(l => l.anchor)) {
    if (anchors.has(link.target)) continue;
    issues.push(makeIssue(rule, context, {
      line: link.line,
      description: `${rule.message}：页内链接 ${link.target} 无对应标题锚点（现有锚点：${[...anchors].slice(0, 5).join(', ')}…）`,
      priority: 'medium',
      evidence: `[${link.text}](${link.target})`
    }));
  }
  return issues;
}

function checkDiscoverability(parsed, rule, context) {
  const issues = checkRequiredSections(parsed, rule, context);

  // 交叉引用有效性：相对路径链接的目标文件必须存在
  const exists = requireIO('exists');
  const projectRoot = context.options?.projectRoot ?? '';
  const baseDir = String(parsed.fileName).split('/').slice(0, -1).join('/');
  for (const link of parsed.links.filter(l => !l.external && !l.anchor)) {
    const target = link.target.split('#')[0];
    if (!target) continue;
    const relative = target.startsWith('./') ? `${baseDir}/${target.slice(2)}` : target;
    const resolved = projectRoot ? `${String(projectRoot).replace(/\/+$/, '')}/${relative}` : relative;
    if (exists(resolved)) continue;
    issues.push(makeIssue(rule, context, {
      line: link.line,
      description: `链接目标文件不存在：${link.target}`,
      suggestedFix: '修正为实际存在的文档路径，或移除该链接',
      priority: 'medium',
      evidence: `resolved=${resolved}`
    }));
  }
  return issues;
}

function checkConceptLinks(parsed, rule, context) {
  const required = rule.linkPatterns?.required ?? [];
  const issues = [];
  for (const item of required) {
    const mentioned = parsed.content.includes(item.concept);
    if (!mentioned) continue;
    const linked = new RegExp(item.pattern).test(parsed.content);
    if (linked) continue;
    const line = parsed.lines.findIndex(t => t.includes(item.concept)) + 1;
    issues.push(makeIssue(rule, context, {
      line: line || null,
      description: `${rule.message}：概念 "${item.concept}" 已提及但未链接到详细文档`,
      suggestedFix: `为 ${item.concept} 添加官方文档链接`
    }));
  }
  return issues;
}

function checkTerminologyConsistency(parsed, rule, context) {
  const issues = [];
  for (const [standard, variants] of Object.entries(rule.termMappings ?? {})) {
    for (const wrong of variants) {
      if (wrong === standard) continue;
      parsed.lines.forEach((text, idx) => {
        if (!text.includes(wrong)) return;
        issues.push(makeIssue(rule, context, {
          line: idx + 1,
          description: `${rule.message}："${wrong}" 应统一写作 "${standard}"`,
          suggestedFix: `将 "${wrong}" 改为 "${standard}"`,
          evidence: text.trim().slice(0, 120)
        }));
      });
    }
  }
  return issues;
}
```

### 4.6 Agent 规则（checkPoints 语义判定）

`execution: "agent"` 的规则（`findability-001`、`clarity-001`、`correctness-003`、`capability-005`、`capability-009`、`capability-010`）没有机器可判定的驱动配置，只有 `checkPoints` 语义描述。执行要求：

1. Agent 必须**逐条** checkPoint 判定，并通过 `options.agentVerdicts[ruleId]` 回填 verdict：`{ checkPoint, status: pass|fail|not-applicable, evidence, description?, suggestedFix?, line?, priority? }`。
2. 判定 `fail` 必须给出 `evidence`（原文行号或片段），否则 `agentRule()` 抛错。
3. 未回填、回填不全（缺 checkPoint）、状态非法都会抛错并由台账记为 `failed`——**不允许**因为"看不出问题"而静默按 0 问题通过。
4. 判定 `not-applicable` 时必须写明理由（例如文档不含生命周期内容），理由进入台账 `reason`。

### 4.7 函数式语法检查处理器

`pattern.type === "function"` 的规则由这里实现。所有处理器返回 `[{ offset, offsetEnd?, detail?, evidence? }]`，`offset` 是代码块内的 0-based 行偏移，由调用方换算成文档行号。

```javascript
// 剔除注释与字符串字面量，避免把注释里的括号/引号计入配对
function stripCommentsAndStrings(code) {
  let out = '';
  let i = 0;
  while (i < code.length) {
    const two = code.slice(i, i + 2);
    if (two === '//') {
      while (i < code.length && code[i] !== '\n') { out += ' '; i++; }
      continue;
    }
    if (two === '/*') {
      while (i < code.length && code.slice(i, i + 2) !== '*/') { out += code[i] === '\n' ? '\n' : ' '; i++; }
      out += '  '; i += 2;
      continue;
    }
    const ch = code[i];
    if (ch === '"' || ch === "'" || ch === '`') {
      out += ' '; i++;
      while (i < code.length && code[i] !== ch) {
        if (code[i] === '\\') { out += '  '; i += 2; continue; }
        out += code[i] === '\n' ? '\n' : ' ';
        i++;
      }
      out += ' '; i++;
      continue;
    }
    out += ch; i++;
  }
  return out;
}

function balanceScan(code, rule, opener, closer) {
  const stripped = stripCommentsAndStrings(code);
  const lines = stripped.split('\n');
  const rawLines = code.split('\n');
  let depth = 0;
  const hits = [];

  lines.forEach((line, idx) => {
    for (const ch of line) {
      if (ch === opener) depth++;
      else if (ch === closer) depth--;
    }
    if (depth < 0) {
      hits.push({ offset: idx, detail: `第 ${idx + 1} 行出现多余的 "${closer}"`, evidence: rawLines[idx]?.trim().slice(0, 120) });
      depth = 0;
    }
  });

  if (depth > 0) {
    // 定位最后一个未闭合的 opener 所在行
    let d = 0;
    let lastOpen = 0;
    lines.forEach((line, idx) => {
      for (const ch of line) {
        if (ch === opener) { d++; lastOpen = idx; }
        else if (ch === closer) d--;
      }
    });
    hits.push({
      offset: lastOpen,
      offsetEnd: lines.length - 1,
      detail: `有 ${depth} 个 "${opener}" 未闭合（代码块共 ${lines.length} 行）`,
      evidence: rawLines[lastOpen]?.trim().slice(0, 120)
    });
  }
  return hits;
}

// 引号配对：字符级状态机。单/双引号字符串不允许跨行，行尾仍处于字符串内即未闭合；
// 反引号模板字符串允许跨行，只在整段代码结束时仍未闭合才报告。
// 不能用"剥离字符串后统计引号奇偶"的做法——剥离阶段会把未闭合字符串连同引号一起吃掉，导致漏检。
function quoteBalanceScan(code, rule) {
  const hits = [];
  const lines = code.split('\n');
  let state = 'code';           // code | single | double | template | block-comment
  let openLine = 0;

  for (let idx = 0; idx < lines.length; idx++) {
    const line = lines[idx];
    let i = 0;

    while (i < line.length) {
      const ch = line[i];
      const next = line[i + 1];

      if (state === 'block-comment') {
        if (ch === '*' && next === '/') { state = 'code'; i += 2; continue; }
        i++; continue;
      }
      if (state === 'single' || state === 'double') {
        if (ch === '\\') { i += 2; continue; }
        if ((state === 'single' && ch === "'") || (state === 'double' && ch === '"')) { state = 'code'; }
        i++; continue;
      }
      if (state === 'template') {
        if (ch === '\\') { i += 2; continue; }
        if (ch === '`') { state = 'code'; }
        i++; continue;
      }

      // state === 'code'
      if (ch === '/' && next === '/') break;                       // 行注释：本行剩余不参与判定
      if (ch === '/' && next === '*') { state = 'block-comment'; i += 2; continue; }
      if (ch === "'" || ch === '"' || ch === '`') {
        state = ch === "'" ? 'single' : (ch === '"' ? 'double' : 'template');
        openLine = idx;
        i++; continue;
      }
      i++;
    }

    if (state === 'single' || state === 'double') {
      hits.push({
        offset: openLine,
        detail: `第 ${openLine + 1} 行的${state === 'single' ? '单' : '双'}引号字符串未闭合`,
        evidence: lines[openLine]?.trim().slice(0, 120)
      });
      state = 'code';           // 不跨行继承状态，避免一处缺陷污染后续所有行
    }
  }

  if (state === 'template') {
    hits.push({
      offset: openLine,
      detail: `第 ${openLine + 1} 行开始的模板字符串未闭合`,
      evidence: lines[openLine]?.trim().slice(0, 120)
    });
  }

  return hits;
}
```

> 说明：`balanceScan()` 先用 `stripCommentsAndStrings()` 剔除注释与字符串内容，避免把注释/字符串里的括号计入配对；
> `quoteBalanceScan()` 不能复用这一剥离结果，必须自己做字符级状态机——未闭合字符串在剥离阶段会被整段吃掉，奇偶统计恒为 0。

## 步骤 5：生成报告数据

```javascript
function generateReport(result, fileName) {
  const { issuesByDimension, ledger, sdk } = result;
  const excelData = [];

  const summary = {
    total: 0,
    byDimension: {},
    critical: 0, high: 0, medium: 0, low: 0,
    autoFixable: 0,
    rulesExecuted: 0,
    rulesNotExecuted: [],
    rulesFailed: [],
    sdkCheckState: sdk?.state ?? 'not-executed',
    sdkCheckReason: sdk?.reason ?? null
  };

  for (const [dimensionKey, issues] of Object.entries(issuesByDimension)) {
    const dimensionName = DIMENSION_NAME[dimensionKey] ?? dimensionKey;
    summary.byDimension[dimensionName] = issues.length;
    summary.total += issues.length;

    for (const issue of issues) {
      if (issue.priority === 'critical') summary.critical++;
      else if (issue.priority === 'high') summary.high++;
      else if (issue.priority === 'medium') summary.medium++;
      else if (issue.priority === 'low') summary.low++;
      if (issue.autoFixable) summary.autoFixable++;

      excelData.push(toExcelRow(issue, fileName, dimensionName));
    }
  }

  for (const record of ledger) {
    if (!record.ruleId) continue;
    if (record.status === 'executed') summary.rulesExecuted++;
    if (record.status === 'not-executed') summary.rulesNotExecuted.push({ ruleId: record.ruleId, reason: record.reason });
    if (record.status === 'failed') summary.rulesFailed.push({ ruleId: record.ruleId, reason: record.reason });
  }

  const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  excelData.sort((a, b) => {
    const diff = (priorityOrder[a.priority] ?? 9) - (priorityOrder[b.priority] ?? 9);
    if (diff !== 0) return diff;
    return String(a.filename).localeCompare(String(b.filename));
  });

  summary.score = calculateScore(summary);

  return { excelData, summary, ledger, sdk, fileName };
}

// Excel 行的唯一构造点：报告端不得再自行拼字段
function toExcelRow(issue, fileName, dimensionName) {
  const row = {
    filename: issue.filename ?? fileName,
    designer: issue.designer ?? '-',
    issueType: issue.type ?? dimensionName,
    lineNumber: formatLineNumber(issue.line, issue.lineEnd),
    reason: issue.description,
    suggestion: issue.suggestedFix,
    severity: translatePriority(issue.priority),
    // 非表格列，仅供排序/追溯
    priority: issue.priority,
    dimension: dimensionName,
    ruleId: issue.ruleId,
    confidence: issue.confidence
  };

  if (!row.filename) throw new Error('toExcelRow: filename 为空，报告定位信息丢失');
  if (!row.reason) throw new Error('toExcelRow: reason 为空');
  if (!row.suggestion) throw new Error('toExcelRow: suggestion 为空');
  return row;
}

function formatLineNumber(start, end) {
  if (start === null || start === undefined || start === '') return '-';
  if (end === null || end === undefined || start === end) return String(start);
  return `${start}-${end}`;
}

function translatePriority(priority) {
  const map = { critical: '严重', high: '高', medium: '中', low: '低' };
  return map[priority] ?? priority;
}

function calculateScore(summary) {
  const weights = { critical: 10, high: 5, medium: 2, low: 1 };
  const totalWeight = summary.critical * weights.critical
    + summary.high * weights.high
    + summary.medium * weights.medium
    + summary.low * weights.low;
  // 未执行/失败的检查会削弱结论可信度，按条扣分并在汇总中显式呈现
  const penalty = (summary.rulesNotExecuted.length + summary.rulesFailed.length) * 3;
  return Math.max(0, 100 - totalWeight - penalty);
}
```

## 步骤 6：SDK 源码一致性检查

### 6.1 文件映射

映射规则来自 `correctness-rules.json → sdkSourceCheck.mappingRules`。要点：

- **数组顺序即优先级**，更具体的规则（`-sys`、`app-ability`、`inner`）必须排在更宽泛的规则之前；
- `docPattern` 必须**锚定整个文件名**（`^…$`），`{module}` 使用惰性匹配，避免贪婪吞掉 `{name}`；
- 名称转换必须通过 `transforms` 显式声明（`hyphen-to-dot` / `hyphen-to-underscore`），**禁止**对文件名整体做连字符替换；
- 特殊命名走 `explicitMapping`；调用方可用 `options.sdkFilePath` 直接指定；
- 失败时返回 `{ path: null, reason }`，由调用方产出问题并把检查标记为 `failed`，**不得**返回 `null` 后当作"无 SDK 可比对，0 问题"。

```javascript
const NAME_TRANSFORMS = {
  'hyphen-to-dot': (value) => value.replace(/-/g, '.'),
  'hyphen-to-underscore': (value) => value.replace(/-/g, '_'),
  none: (value) => value
};

function applyNameTransform(value, transformName) {
  if (transformName === undefined || transformName === null) return value;
  const fn = NAME_TRANSFORMS[transformName];
  if (!fn) throw new Error(`未知的名称转换 "${transformName}"（可用：${Object.keys(NAME_TRANSFORMS).join(', ')}）`);
  return fn(value);
}

function joinSdkPath(basePath, relativePath) {
  const base = String(basePath ?? '').replace(/\/+$/, '');
  const rel = String(relativePath).replace(/^\/+/, '');
  return base ? `${base}/${rel}` : rel;
}

// 兼容两种写法：数组（推荐，顺序即优先级）与旧的对象映射（按插入顺序）
function normalizeMappingRules(sdkFileMapping) {
  if (Array.isArray(sdkFileMapping)) return sdkFileMapping;
  if (sdkFileMapping && typeof sdkFileMapping === 'object') {
    return Object.entries(sdkFileMapping).map(([docPattern, sdkPath]) => ({ docPattern, sdkPath }));
  }
  throw new Error('mappingRules.sdkFileMapping 缺失或格式非法（应为数组）');
}

function compileDocPattern(docPattern) {
  // 允许两种形式：直接给正则（^…$），或给 js-apis-{name}.md 这类模板
  if (docPattern.startsWith('^')) {
    if (!docPattern.endsWith('$')) {
      throw new Error(`docPattern 必须锚定整个文件名（缺少结尾 $）：${docPattern}`);
    }
    return new RegExp(docPattern);
  }
  const source = docPattern
    .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\\\{module\\\}/g, '(?<module>[A-Za-z0-9_.]+?)')
    .replace(/\\\{name\\\}/g, '(?<name>[A-Za-z0-9_.-]+)');
  return new RegExp(`^${source}$`);
}

function resolveSdkFilePath(docFileName, mappingRules, sdkBasePath, options = {}) {
  const fileName = String(docFileName ?? '').split('/').pop();
  if (!fileName) return { path: null, reason: 'doc-filename-missing' };

  // 0) 调用方显式指定，优先级最高
  if (options.sdkFilePath) {
    return { path: joinSdkPath(sdkBasePath, options.sdkFilePath), rule: 'options.sdkFilePath' };
  }

  // 1) 显式映射表
  const explicit = mappingRules?.explicitMapping?.[fileName];
  if (explicit) return { path: joinSdkPath(sdkBasePath, explicit), rule: 'explicitMapping' };

  // 2) 按声明顺序匹配模式规则
  for (const rule of normalizeMappingRules(mappingRules?.sdkFileMapping)) {
    let regex;
    try {
      regex = compileDocPattern(rule.docPattern);
    } catch (err) {
      throw new Error(`映射规则 "${rule.docPattern}" 无法编译：${err.message}`);
    }
    const match = fileName.match(regex);
    if (!match) continue;

    const resolvedPath = rule.sdkPath.replace(/\{(\w+)\}/g, (whole, key) => {
      const raw = match.groups?.[key] ?? match[key];
      if (raw === undefined) {
        throw new Error(`映射规则 "${rule.docPattern}" 的占位符 {${key}} 没有对应命名捕获组`);
      }
      return applyNameTransform(raw, rule.transforms?.[key]);
    });

    return { path: joinSdkPath(sdkBasePath, resolvedPath), rule: rule.docPattern };
  }

  return { path: null, reason: 'no-mapping-rule-matched' };
}

// 规则文件里的 assertions 必须在检查开始前跑通（含文件存在性）
function runMappingAssertions(mappingRules, sdkBasePath) {
  const assertions = mappingRules?.assertions ?? [];
  const results = [];
  for (const assertion of assertions) {
    const resolved = resolveSdkFilePath(assertion.docFileName, mappingRules, sdkBasePath);
    const pathOk = resolved.path === joinSdkPath(sdkBasePath, assertion.expected);
    const exists = resolved.path ? requireIO('exists')(resolved.path) : false;
    results.push({
      docFileName: assertion.docFileName,
      expected: assertion.expected,
      actual: resolved.path,
      pathOk,
      fileExists: exists,
      rule: resolved.rule ?? resolved.reason
    });
    if (!pathOk) {
      throw new Error(`SDK 映射断言失败：${assertion.docFileName} → 期望 ${assertion.expected}，实际 ${resolved.path}`);
    }
  }
  return results;
}
```

### 6.2 主流程

```javascript
function checkSdkSourceConsistency(parsed, sdkConfig, options = {}) {
  const exists = requireIO('exists');
  const read = requireIO('read');
  const result = { state: 'passed', reason: null, sdkFilePath: null, checkpoints: [], issues: [] };

  const fail = (reason, issueSpec) => {
    result.state = 'failed';
    result.reason = reason;
    if (issueSpec) {
      result.issues.push(makeIssue(
        { id: 'correctness.sdkSourceCheck', name: 'sdk-source-consistency', message: issueSpec.description, priority: issueSpec.priority ?? 'medium', confidence: issueSpec.confidence ?? 80, suggestedFix: issueSpec.suggestedFix },
        { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer },
        { description: issueSpec.description, line: issueSpec.line, evidence: issueSpec.evidence ?? reason }
      ));
    }
    return result;
  };

  if (!parsed.fileName) return fail('doc-filename-missing', { description: '缺少被检文档文件名，无法执行 SDK 映射', priority: 'high' });

  if (options.runMappingAssertions !== false) {
    try {
      runMappingAssertions(sdkConfig.mappingRules, options.sdkSourcePath);
    } catch (err) {
      return fail('mapping-assertion-failed', { description: err.message, priority: 'high' });
    }
  }

  const resolved = resolveSdkFilePath(parsed.fileName, sdkConfig.mappingRules, options.sdkSourcePath, options);
  if (!resolved.path) {
    return fail(resolved.reason, {
      description: `无法找到文档对应的 SDK 源文件：${parsed.fileName}（原因：${resolved.reason}）`,
      suggestedFix: '在 mappingRules.explicitMapping 中登记该文件名，或通过 options.sdkFilePath 指定 SDK 路径',
      priority: 'medium'
    });
  }
  result.sdkFilePath = resolved.path;

  if (!exists(resolved.path)) {
    return fail('sdk-file-not-found', {
      description: `SDK 源文件不存在：${resolved.path}`,
      suggestedFix: `确认 ${options.sdkSourcePath ?? 'SDK 仓库'} 是否完整，或用 options.sdkFilePath 指定正确路径`,
      priority: 'medium'
    });
  }

  const sdkParsed = parseSdkSource(read(resolved.path));
  const docApis = extractDocApis(parsed);

  // 空提取必须判失败：把"没提取到"当成"0 问题"是本检查最危险的失效模式
  if (docApis.length === 0) {
    return fail('doc-api-extraction-empty', {
      description: `未从 ${parsed.fileName} 提取到任何 API/接口/枚举，SDK 一致性检查未实际执行`,
      suggestedFix: '确认文档结构（## 名称<sup>N+</sup> + 参数/返回值/错误码/属性表）符合 OpenHarmony API 文档规范',
      priority: 'high'
    });
  }
  if (sdkParsed.apis.length === 0) {
    return fail('sdk-parse-empty', {
      description: `未从 ${resolved.path} 解析到任何声明，SDK 一致性检查未实际执行`,
      suggestedFix: '确认 SDK 文件为带 JSDoc 的 .d.ts/.h 声明文件',
      priority: 'high'
    });
  }

  const checkTypes = new Set(sdkConfig.checkTypes ?? []);
  const runCheck = (name, fn) => {
    if (checkTypes.size > 0 && !checkTypes.has(name)) {
      result.checkpoints.push({ name, status: 'not-applicable', reason: 'index.json sdkSourceCheck.checkTypes 未包含该检查点' });
      return;
    }
    const produced = fn();
    result.checkpoints.push({ name, status: 'executed', issueCount: produced.length });
    result.issues.push(...produced);
  };

  for (const docApi of docApis) {
    const sdkApi = findSdkApi(sdkParsed, docApi.name);
    if (!sdkApi) {
      result.issues.push(makeIssue(
        { id: 'correctness.sdkSourceCheck', name: 'sdk-source-consistency', message: 'SDK 中未找到对应 API', priority: 'high', confidence: 90, suggestedFix: '确认 API 名称拼写正确，或检查 SDK 版本是否匹配' },
        { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer },
        { description: `文档中的 API "${docApi.name}" 在 SDK 源码中未找到`, line: docApi.line, evidence: `${result.sdkFilePath}` }
      ));
      continue;
    }

    runCheck('api-since-version-match', () => wrapNullable(checkSinceVersion(docApi, sdkApi, parsed)));
    runCheck('param-count-match', () => checkParameters(docApi, sdkApi, parsed).filter(i => i.subType === '入参数量不一致'));
    runCheck('param-name-match', () => checkParameters(docApi, sdkApi, parsed).filter(i => i.subType === '入参名称不匹配'));
    runCheck('param-type-match', () => checkParameters(docApi, sdkApi, parsed).filter(i => i.subType === '入参类型不一致'));
    runCheck('return-type-match', () => wrapNullable(checkReturnType(docApi, sdkApi, parsed)));
    runCheck('error-code-match', () => checkErrorCodes(docApi, sdkApi, parsed));
    runCheck('systemapi-mark-match', () => wrapNullable(checkSystemApiMark(docApi, sdkApi, parsed)));
    runCheck('stagemodelonly-mark-match', () => wrapNullable(checkStageModelMark(docApi, sdkApi, parsed)));
    runCheck('enum-values-complete', () => (docApi.type === 'enum' ? checkEnumValues(docApi, sdkApi, parsed) : markCheckpointSkipped(result, 'enum-values-complete', `${docApi.name} 不是枚举`)));
    runCheck('interface-fields-complete', () => (docApi.type === 'interface' ? checkInterfaceFields(docApi, sdkApi, parsed) : markCheckpointSkipped(result, 'interface-fields-complete', `${docApi.name} 不是接口`)));
  }

  return result;
}

function wrapNullable(issue) {
  return issue ? [issue] : [];
}

function markCheckpointSkipped(result, name, reason) {
  const last = result.checkpoints.find(c => c.name === name);
  if (last) last.reason = reason;
  return [];
}
```

### 6.3 SDK 源码解析（含 fields / enumValues）

`parseSdkSource` 必须产出后续检查依赖的**接口字段集合**与**枚举值集合**，否则 `interface-fields-complete` / `enum-values-complete` 会因空集合而恒不报问题。

```javascript
function parseSdkSource(content) {
  const lines = content.split('\n');
  const apis = [];
  let namespace = null;
  let pendingJsdoc = null;
  let typeContext = null;     // 当前 interface/enum 上下文
  let depth = 0;

  const countChar = (text, ch) => (text.split(ch).length - 1);

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const line = raw.trim();

    if (line.startsWith('/**')) {
      const buf = [];
      let j = i;
      for (; j < lines.length; j++) {
        buf.push(lines[j]);
        if (lines[j].includes('*/')) break;
      }
      pendingJsdoc = { text: formatJsdoc(buf), startLine: i + 1 };
      i = j;
      continue;
    }

    const decl = line.match(/^(?:export\s+)?(?:declare\s+)?(namespace|interface|class|enum|function|type|const)\s+([A-Za-z_$][\w$]*)/);
    if (decl) {
      const [, kind, name] = decl;
      if (kind === 'namespace') {
        namespace = { name, since: parseSdkVersion(extractTag(pendingJsdoc?.text ?? '', '@since')), line: i + 1 };
      } else {
        const api = buildSdkApi(kind, name, line, pendingJsdoc, i + 1);
        apis.push(api);
        if (kind === 'interface' || kind === 'enum' || kind === 'class') {
          typeContext = { api, depthAtOpen: depth + countChar(raw, '{') - 1 };
        }
      }
      depth += countChar(raw, '{') - countChar(raw, '}');
      pendingJsdoc = null;
      if (typeContext && depth <= typeContext.depthAtOpen) typeContext = null;
      continue;
    }

    // 类型成员：字段或枚举值
    if (typeContext && line.length > 0 && !line.startsWith('//')) {
      const member = parseTypeMember(line, typeContext.api.kind);
      if (member) {
        const target = typeContext.api.kind === 'enum' ? typeContext.api.enumValues : typeContext.api.fields;
        target.push({ ...member, since: parseSdkVersion(extractTag(pendingJsdoc?.text ?? '', '@since')), line: i + 1 });
      }
    }

    depth += countChar(raw, '{') - countChar(raw, '}');
    if (typeContext && depth <= typeContext.depthAtOpen) typeContext = null;
    if (!line.startsWith('/**')) pendingJsdoc = null;
  }

  return { namespace, apis };
}

function formatJsdoc(blockLines) {
  return blockLines
    .map(l => l.replace(/^\s*/, '').replace(/^\/\*\*/, '').replace(/\*\/$/, '').replace(/^\*/, '').trim())
    .filter(l => l.length > 0)
    .join('\n');
}

function buildSdkApi(kind, name, line, pendingJsdoc, lineNo) {
  const jsdoc = pendingJsdoc?.text ?? '';
  const signature = line;
  // 优先解析声明签名；签名不可用时（如 C API 头文件、跨行声明）回退到 JSDoc 的 @param/@returns
  const signatureParams = kind === 'function' ? parseSignatureParams(signature) : [];
  const params = signatureParams.length > 0 ? signatureParams : extractParams(jsdoc);
  const signatureReturn = kind === 'function' ? parseSignatureReturn(signature) : null;
  const returns = signatureReturn ?? extractReturn(jsdoc);

  return {
    name,
    kind,
    jsdoc,
    since: parseSdkVersion(extractTag(jsdoc, '@since')),
    deprecated: extractTag(jsdoc, '@deprecated'),
    permission: extractTag(jsdoc, '@permission'),
    systemapi: /@systemapi/.test(jsdoc),
    stagemodelonly: /@stagemodelonly/.test(jsdoc),
    params,
    returns,
    throws: extractThrows(jsdoc),
    fields: [],
    enumValues: [],
    line: lineNo
  };
}

function parseTypeMember(line, kind) {
  if (kind === 'enum') {
    const m = line.match(/^([A-Za-z_$][\w$]*)\s*=\s*([^,;]+)/);
    if (!m) return null;
    return { name: m[1], value: m[2].trim().replace(/,$/, '') };
  }
  const m = line.match(/^([A-Za-z_$][\w$]*)\s*(\?)?\s*:\s*([^;]+);/);
  if (!m) return null;
  return { name: m[1], optional: Boolean(m[2]), type: m[3].trim() };
}

function parseSignatureParams(signature) {
  const inner = signature.match(/\(([^)]*)\)/);
  if (!inner || inner[1].trim() === '') return [];
  return splitTopLevel(inner[1]).map(part => {
    const [rawName, ...rest] = part.split(':');
    return { name: rawName.replace('?', '').trim(), type: rest.join(':').trim() };
  }).filter(p => p.name);
}

function parseSignatureReturn(signature) {
  const m = signature.match(/\)\s*:\s*([^;{]+);?/);
  return m ? m[1].trim() : null;
}

// 按顶层逗号切分，忽略泛型 <...> 内的逗号
function splitTopLevel(text) {
  const parts = [];
  let depth = 0;
  let current = '';
  for (const ch of text) {
    if (ch === '<' || ch === '(' || ch === '[' || ch === '{') depth++;
    if (ch === '>' || ch === ')' || ch === ']' || ch === '}') depth--;
    if (ch === ',' && depth === 0) { parts.push(current.trim()); current = ''; continue; }
    current += ch;
  }
  if (current.trim()) parts.push(current.trim());
  return parts;
}

function findSdkApi(sdkParsed, name) {
  return sdkParsed.apis.find(a => a.name === name) ?? null;
}
```

### 6.4 文档 API 提取

`extractDocApis` 必须是**真实实现**：它为空时 SDK 检查等于没做。返回的每个条目按 `步骤 6.2` 的检查点需要，携带 `since`、`params`、`returns`、`errorCodes`、`fields`、`enumValues`、`line`。

```javascript
const API_HEADING = /^([A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\s*(?:<sup>\s*(\d+)\s*\+?\s*<\/sup>|(\d+)\s*\+)?\s*$/;

function extractDocApis(parsed) {
  const apis = [];
  const moduleSince = detectModuleSince(parsed);

  for (const section of parsed.sections) {
    if (section.level < 2 || section.level > 3) continue;
    const m = section.rawTitle.match(API_HEADING);
    if (!m) continue;

    const fullName = m[1];
    const name = fullName.includes('.') ? fullName.split('.').pop() : fullName;
    const since = Number(m[2] ?? m[3] ?? moduleSince ?? NaN);
    const tables = parsed.tables.filter(t => t.startLine >= section.startLine && t.endLine <= section.endLine + 1);
    const type = classifyDocApi(section, tables);

    const api = {
      name,
      fullName,
      type,
      since: Number.isFinite(since) ? since : null,
      line: section.startLine,
      lineEnd: section.endLine,
      params: [],
      returns: null,
      errorCodes: [],
      fields: [],
      enumValues: [],
      examples: parsed.codeBlocks.filter(b => b.startLine >= section.startLine && b.startLine <= section.endLine),
      permission: matchFirst(section.body, /需要权限\s*[:：]?\s*([A-Za-z0-9_.]+)/) ?? matchFirst(section.body, /(ohos\.permission\.[A-Za-z0-9_.]+)/),
      systemCapability: matchFirst(section.body, /(SystemCapability\.[A-Za-z0-9_.]+)/),
      constraints: extractDocConstraints(section.body)
    };

    const paramTable = tables.find(t => t.header.some(h => h.includes('参数名')));
    if (paramTable) {
      api.params = paramTable.rows.map(r => ({
        name: cleanCell(r.cells[0]),
        type: cleanCell(r.cells[1]),
        required: cleanCell(r.cells[2]) === '是',
        description: cleanCell(r.cells[3]),
        line: r.lineNo
      }));
    }

    const returnsMatch = section.body.match(/\*\*返回值\*\*\s*[:：]\s*(.+)/);
    if (returnsMatch) api.returns = cleanCell(returnsMatch[1]);

    const errorTable = tables.find(t => t.header.some(h => h.includes('错误码')));
    if (errorTable) {
      api.errorCodes = errorTable.rows
        .map(r => normalizeErrorCode(cleanCell(r.cells[0])))
        .filter(code => Number.isFinite(code));
      api.errorCodeLine = errorTable.startLine;
    }

    const fieldTable = tables.find(t => t.header.some(h => h.includes('名称')) && t.header.some(h => h.includes('类型')));
    if (fieldTable) {
      const rows = fieldTable.rows.map(r => ({
        name: cleanCell(r.cells[0]),
        type: cleanCell(r.cells[1]),
        readable: cleanCell(r.cells[2]),
        writable: cleanCell(r.cells[3]),
        description: cleanCell(r.cells[4]),
        line: r.lineNo
      }));
      if (type === 'enum') api.enumValues = rows.map(r => ({ name: r.name, value: r.type, line: r.line }));
      else api.fields = rows;
    }

    apis.push(api);
  }

  return apis;
}

function classifyDocApi(section, tables) {
  if (/\*\*枚举值\*\*|枚举值\s*[:：]/.test(section.body)) return 'enum';
  if (tables.some(t => t.header.some(h => h.includes('枚举值')))) return 'enum';
  if (/\*\*属性\*\*\s*[:：]/.test(section.body)) return 'interface';
  if (tables.some(t => t.header.some(h => h.includes('名称')) && t.header.some(h => h.includes('可读')))) return 'interface';
  return 'function';
}

function detectModuleSince(parsed) {
  const m = parsed.content.match(/起始版本为\s*(\d+)/);
  return m ? Number(m[1]) : null;
}

function matchFirst(text, re) {
  const m = text.match(re);
  return m ? m[1] : null;
}

function extractDocConstraints(body) {
  const constraints = [];
  if (/Stage模型/.test(body)) constraints.push('Stage模型');
  if (/系统接口|systemapi/i.test(body)) constraints.push('系统接口');
  if (/需要权限|ohos\.permission/.test(body)) constraints.push('权限');
  return constraints;
}

// Markdown 单元格清洗：去链接、去反引号、解码 HTML 实体
function cleanCell(value) {
  return String(value ?? '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/`/g, '')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .trim();
}

// 错误码统一为数字：文档表格是字符串，SDK @throws 是数字，直接比较会全部失配
function normalizeErrorCode(value) {
  const text = String(value ?? '').trim();
  const m = text.match(/\d{3,}/);
  return m ? Number(m[0]) : NaN;
}
```

### 6.5 检查点实现

```javascript
function checkSinceVersion(docApi, sdkApi, parsed) {
  const docVersion = docApi.since;
  const sdkVersion = sdkApi.since;

  if (docVersion === null || docVersion === undefined || sdkVersion === null || sdkVersion === undefined) return null;
  if (docVersion === sdkVersion) return null;

  return makeIssue(SDK_RULE, { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer }, {
    subType: 'API起始版本不一致',
    priority: 'critical',
    confidence: 95,
    line: docApi.line,
    description: `API "${docApi.name}" 起始版本不一致：文档标注为 ${docVersion}+，SDK 中为 @since ${sdkVersion}`,
    suggestedFix: `统一为正确的起始版本（以 SDK @since ${sdkVersion} 为准，或推动 SDK 修正）`,
    evidence: `doc=${docVersion}, sdk=${sdkVersion}`
  });
}

const SDK_RULE = {
  id: 'correctness.sdkSourceCheck',
  name: 'sdk-source-consistency',
  message: 'SDK 源码一致性检查',
  suggestedFix: '核对文档与 SDK 源码，统一不一致项'
};

function checkParameters(docApi, sdkApi, parsed) {
  const issues = [];
  const context = { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer };
  const docParams = docApi.params ?? [];
  const sdkParams = sdkApi.params ?? [];

  if (docParams.length !== sdkParams.length) {
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '入参数量不一致',
      priority: 'high',
      confidence: 90,
      line: docApi.line,
      description: `API "${docApi.name}" 入参数量不一致：文档 ${docParams.length} 个，SDK ${sdkParams.length} 个`,
      suggestedFix: '核对并补充缺失的参数说明',
      evidence: `doc=[${docParams.map(p => p.name).join(',')}], sdk=[${sdkParams.map(p => p.name).join(',')}]`
    }));
  }

  for (const docParam of docParams) {
    const sdkParam = sdkParams.find(p => p.name === docParam.name);
    if (!sdkParam) {
      issues.push(makeIssue(SDK_RULE, context, {
        subType: '入参名称不匹配',
        priority: 'high',
        confidence: 90,
        line: docParam.line ?? docApi.line,
        description: `参数 "${docParam.name}" 在 SDK 中未找到，可能拼写错误`,
        suggestedFix: `检查参数名拼写，SDK 中的参数名为：${sdkParams.map(p => p.name).join(', ')}`,
        evidence: `sdk=[${sdkParams.map(p => p.name).join(',')}]`
      }));
    } else if (normalizeTypeName(docParam.type) !== normalizeTypeName(sdkParam.type)) {
      issues.push(makeIssue(SDK_RULE, context, {
        subType: '入参类型不一致',
        priority: 'high',
        confidence: 85,
        line: docParam.line ?? docApi.line,
        description: `参数 "${docParam.name}" 类型不一致：文档为 ${docParam.type}，SDK 中为 ${sdkParam.type}`,
        suggestedFix: '统一参数类型描述',
        evidence: `doc=${docParam.type}, sdk=${sdkParam.type}`
      }));
    }
  }
  return issues;
}

// 文档写 AsyncCallback<number>，SDK 写 AsyncCallback<number>；去掉空白后比较
function normalizeTypeName(type) {
  return String(type ?? '').replace(/\s+/g, '').replace(/；$/, '');
}

function checkReturnType(docApi, sdkApi, parsed) {
  if (!docApi.returns || !sdkApi.returns) return null;
  if (normalizeTypeName(docApi.returns) === normalizeTypeName(sdkApi.returns)) return null;

  return makeIssue(SDK_RULE, { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer }, {
    subType: '返回值类型不一致',
    priority: 'high',
    confidence: 85,
    line: docApi.line,
    description: `API "${docApi.name}" 返回值类型不一致：文档为 ${docApi.returns}，SDK 中为 ${sdkApi.returns}`,
    suggestedFix: '统一返回值类型描述',
    evidence: `doc=${docApi.returns}, sdk=${sdkApi.returns}`
  });
}

function checkErrorCodes(docApi, sdkApi, parsed) {
  const issues = [];
  const context = { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer };

  const docCodes = (docApi.errorCodes ?? []).map(normalizeErrorCode).filter(Number.isFinite);
  const sdkCodes = (sdkApi.throws ?? []).map(t => normalizeErrorCode(t.code)).filter(Number.isFinite);

  // SDK 侧一个错误码都没解析到时，不能反推"文档里的错误码无效"——那会建议删除正确内容
  if (sdkCodes.length === 0 && docCodes.length > 0) {
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '错误码无法比对',
      priority: 'medium',
      confidence: 70,
      line: docApi.errorCodeLine ?? docApi.line,
      description: `API "${docApi.name}" 在 SDK 中未解析到 @throws 错误码，无法判定文档错误码（${docCodes.join(', ')}）是否有效`,
      suggestedFix: '确认 SDK 版本与 @throws 声明是否完整；未确认前不要删除文档中的错误码',
      evidence: 'sdk throws=[]'
    }));
    return issues;
  }

  for (const code of docCodes) {
    if (sdkCodes.includes(code)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '错误码不一致',
      priority: 'medium',
      confidence: 80,
      line: docApi.errorCodeLine ?? docApi.line,
      description: `错误码 ${code} 在 SDK 的 @throws 中未定义`,
      suggestedFix: `核对 SDK 版本；SDK 声明的错误码为 ${sdkCodes.join(', ')}，确认无效后再从文档移除`,
      evidence: `doc=${code}, sdk=[${sdkCodes.join(',')}]`
    }));
  }

  for (const code of sdkCodes) {
    if (docCodes.includes(code)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '错误码缺失',
      priority: 'medium',
      confidence: 85,
      line: docApi.errorCodeLine ?? docApi.line,
      description: `SDK 中定义的错误码 ${code} 在文档中未列出`,
      suggestedFix: '在文档错误码表中补充该错误码及触发条件',
      evidence: `sdk=${code}, doc=[${docCodes.join(',')}]`
    }));
  }

  return issues;
}

function checkSystemApiMark(docApi, sdkApi, parsed) {
  const isSysDoc = parsed.fileBaseName.includes('-sys') || docApi.constraints?.includes('系统接口');
  const isSysSdk = Boolean(sdkApi.systemapi);
  const context = { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer };

  if (isSysDoc && !isSysSdk) {
    return makeIssue(SDK_RULE, context, {
      subType: '系统接口标记不一致', priority: 'high', confidence: 90, line: docApi.line,
      description: `文档标记为系统接口（-sys），但 SDK 中未标记 @systemapi`,
      suggestedFix: '确认 API 是否为系统接口，统一标记方式'
    });
  }
  if (!isSysDoc && isSysSdk) {
    return makeIssue(SDK_RULE, context, {
      subType: '系统接口标记缺失', priority: 'high', confidence: 90, line: docApi.line,
      description: `SDK 标记为 @systemapi，但文档未标记为系统接口`,
      suggestedFix: '文档文件名应添加 -sys 后缀，或补充系统接口说明'
    });
  }
  return null;
}

function checkStageModelMark(docApi, sdkApi, parsed) {
  const hasStageModelInDoc = docApi.constraints?.includes('Stage模型');
  const isStageModelOnly = Boolean(sdkApi.stagemodelonly);
  if (!hasStageModelInDoc || isStageModelOnly) return null;

  return makeIssue(SDK_RULE, { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer }, {
    subType: '模型约束标记不一致', priority: 'medium', confidence: 85, line: docApi.line,
    description: `文档标注 Stage 模型约束，但 SDK 未标记 @stagemodelonly`,
    suggestedFix: '确认模型约束是否正确'
  });
}

function checkEnumValues(docApi, sdkApi, parsed) {
  const issues = [];
  const context = { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer };
  const docValues = docApi.enumValues ?? [];
  const sdkValues = sdkApi.enumValues ?? [];

  if (sdkValues.length === 0) {
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '枚举值无法比对', priority: 'medium', confidence: 70, line: docApi.line,
      description: `SDK 中未解析到 "${docApi.name}" 的枚举成员，枚举值完整性检查未实际执行`,
      suggestedFix: '确认 SDK 枚举声明格式，或人工比对枚举值'
    }));
    return issues;
  }

  for (const value of sdkValues) {
    if (docValues.some(v => v.name === value.name)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '枚举值缺失', priority: 'medium', confidence: 85, line: docApi.line,
      description: `枚举值 "${value.name}" 在文档中未列出`,
      suggestedFix: '在文档中补充该枚举值的说明'
    }));
  }
  for (const value of docValues) {
    if (sdkValues.some(v => v.name === value.name)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '枚举值不存在', priority: 'high', confidence: 90, line: value.line ?? docApi.line,
      description: `枚举值 "${value.name}" 在 SDK 中不存在，可能拼写错误`,
      suggestedFix: `检查枚举值拼写，SDK 中的枚举值为：${sdkValues.map(v => v.name).join(', ')}`
    }));
  }
  return issues;
}

function checkInterfaceFields(docApi, sdkApi, parsed) {
  const issues = [];
  const context = { dimension: DIMENSION_NAME.correctness, filename: parsed.fileName, designer: parsed.designer };
  const docFields = docApi.fields ?? [];
  const sdkFields = sdkApi.fields ?? [];

  if (sdkFields.length === 0) {
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '接口字段无法比对', priority: 'medium', confidence: 70, line: docApi.line,
      description: `SDK 中未解析到 "${docApi.name}" 的字段，接口字段完整性检查未实际执行`,
      suggestedFix: '确认 SDK 接口声明格式，或人工比对字段列表'
    }));
    return issues;
  }

  for (const field of sdkFields) {
    if (docFields.some(f => f.name === field.name)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '接口字段缺失', priority: 'medium', confidence: 85, line: docApi.line,
      description: `接口字段 "${field.name}"（${field.type}）在文档中未列出`,
      suggestedFix: `在属性表补充一行：${field.name} | ${field.type} | 是 | ${field.optional ? '是' : '是'} | ${field.description ?? ''}`.trim(),
      evidence: `sdk field ${field.name}: ${field.type} (L${field.line})`
    }));
  }
  for (const field of docFields) {
    if (sdkFields.some(f => f.name === field.name)) continue;
    issues.push(makeIssue(SDK_RULE, context, {
      subType: '接口字段不存在', priority: 'high', confidence: 85, line: field.line ?? docApi.line,
      description: `接口字段 "${field.name}" 在 SDK 中不存在，可能拼写错误`,
      suggestedFix: `检查字段名拼写，SDK 中的字段为：${sdkFields.map(f => f.name).join(', ')}`
    }));
  }
  return issues;
}

// 辅助函数
function extractTag(jsdoc, tagName) {
  const escaped = tagName.replace('@', '@');
  const match = jsdoc.match(new RegExp(`${escaped}\\s+(.+)`));
  return match ? match[1].trim() : null;
}

function extractParams(jsdoc) {
  const params = [];
  const regex = /@param\s+\{([^}]+)\}\s+([A-Za-z_$][\w$]*)/g;
  for (const match of jsdoc.matchAll(regex)) {
    params.push({ type: match[1].trim(), name: match[2] });
  }
  return params;
}

function extractReturn(jsdoc) {
  const match = jsdoc.match(/@returns?\s+\{([^}]+)\}/);
  return match ? match[1].trim() : null;
}

// OpenHarmony .d.ts 的 @throws 形如：@throws {BusinessError} 401 - Parameter error.
// 错误码是 3 位及以上的十进制数（401/801/1600001…）；旧实现的 \d{6,} 会漏掉 401/801，
// 进而把文档里正确的 401 判成"SDK 未定义"并建议删除。
function extractThrows(jsdoc) {
  const result = [];
  const regex = /@throws\s+\{([^}]+)\}\s*(\d{3,})(?!\d)/g;
  for (const match of jsdoc.matchAll(regex)) {
    result.push({ type: match[1].trim(), code: Number(match[2]) });
  }
  return result;
}

function parseSdkVersion(sinceTag) {
  if (!sinceTag) return null;

  // @since arkts {'1.1':'12', '1.2':'20'} 格式：取最大的 API 版本号
  const arktsMatch = sinceTag.match(/arkts\s*\{[^}]*\}/);
  if (arktsMatch) {
    const versions = [...sinceTag.matchAll(/'\d+\.\d+'\s*:\s*'(\d+)'/g)].map(m => Number(m[1]));
    return versions.length > 0 ? Math.max(...versions) : null;
  }

  const numMatch = sinceTag.match(/(\d+)/);
  return numMatch ? Number(numMatch[1]) : null;
}
```

## 步骤 7：自检验收断言

运行方式（无需第三方依赖，Node 18+）：

```bash
node evals/scripts/run_self_check.mjs      # 退出码 0 = A1-A16 全部通过
python3 evals/check_ground_truth.py        # 评测 ground truth 与 fixture 一致性
```

`run_self_check.mjs` 原样抽取本文档与 `excel-format.md` 中标记为 javascript 的代码块，按顺序拼接后执行，再用 `references/` 下的真实规则 JSON 与 `evals/inputs/` 下的真实 fixture 断言行为，不使用合成规则或合成文档。

以下断言必须在改动执行器或规则 JSON 后全部通过：

| # | 断言 | 覆盖的历史缺陷 |
|---|------|--------------|
| A1 | `syntax-001` 的 good 样例（含 `${ error.message }`、`${error.message }`）全部不命中，bad 样例全部命中；fixture 第 46 行只命中 `$ {` 一处，同行 `${err.message}` 不被标记 | 正则用 `\$\s*\{` 把正确插值判为错误 |
| A2 | 所有 `enabled` 规则的正则均可 `new RegExp` 构造；`syntax-005` 改为函数式检查后，`let msg = 'unclosed;` 命中、`let msg = 'closed';` 与注释中的引号不命中 | JSON→RegExp 两层转义错误导致 `Unterminated group` |
| A3 | `validateRuleCoverage()` 对当前规则库返回 `{ enabled: 47 }` 且不抛错；删掉任一注册表条目或把 `correctness-005` 的 `name` 改成 `link-validity` 时必须抛错 | 21 个启用 ID 无分派分支、`correctness-005` 错配链接检查 |
| A4 | `mapToDimension('能力易用性') === 'capability'`；未知分类抛错 | semantics 模块被静默归入 correctness |
| A5 | `extractDocApis(fixture)` 返回 3 条：`createTask`（params 2、errorCodes `[401]`、since 9）、`queryTasks`（returns `Promise<Array<TaskInfo>>`、errorCodes `[]`）、`TaskInfo`（type `interface`、fields `[name, delay]`） | `extractDocApis` 是空实现，返回 `[]` |
| A6 | `parseSdkSource(d.ts)` 中 `TaskInfo.fields` 为 `[name, delay, priority]`，`createTask.throws` 为 `[401, 801]`，`queryTasks.throws` 为 `[401]` | `parseSdkSource` 不产出字段集合；`\d{6,}` 漏掉 3 位错误码 |
| A7 | `checkErrorCodes` 对 `createTask` 只报"缺 801"，不报 401；SDK 无 `@throws` 时报"无法比对"而不是建议删除文档错误码 | 合法 401 被判"SDK 未定义"并建议移除 |
| A8 | `resolveSdkFilePath` 对 `mappingRules.assertions` 中 6 个样例全部得到期望路径，且 fixture 对应文件存在；**清空 `explicitMapping` 后重跑同一样例集**，确保模式规则本身正确（显式表会掩盖模式回归） | 映射对 `demo-taskmanager`/`capi-native-bundle` 返回 null，`-sys` 误映射 |
| A9 | `checkExampleCompleteness`：0 个代码块 → 1 条问题；≥1 个代码块 → 0 条；`validation` 缺失时按默认阈值 1 判定 | `< x \|\| 1` 优先级错误导致恒真 |
| A10 | `generateReport().excelData` 每行 `filename`/`designer`/`lineNumber`/`reason`/`suggestion`/`severity` 均非 `undefined`；`line: 42` 的 issue 渲染为 `"42"`；无 `<!--Designer:-->` 时 `designer` 为 `"-"` | Excel 端读 `issue.lineNumber`/`issue.filename` 得到 `-`/`undefined` |
| A11 | `executeChecks` 未提供 `sdkSourcePath` 时 `sdk.state === 'not-executed'` 且带 reason；提供后 `state === 'passed'`；提取为空时 `state === 'failed'` | 未执行被当成 0 问题 |
| A12 | `assertCompleteExecution()` 在任一启用规则缺台账记录时抛错 | 必选检查被静默遗漏 |
| A13 | `spelling-002` 只在描述性文本判定：正文第 55 行的 `UiAbility` 被报，参数表首列的 `callback`、代码块里的 `resource`/`want` 不被报 | 术语大小写规则把合法标识符判为错误 |
| A14 | `completeness-002` 对 API 文档逐章节检查必备小节：`queryTasks` 缺「错误码」被报，`createTask`（四小节齐全）不被报，`TaskInfo`（接口章节）不参与判定 | 章节要求按全文判定，漏掉单个 API 缺错误码表 |
| A15 | `python3 evals/check_ground_truth.py` 退出码为 0 | 评测植入行号与 fixture 脱节，判分结论失效 |
| A16 | 退化正则探测：把 `clarity-002` 的 `"..."` 字面量按正则配置（不加 `"type": "keyword"`）时 `validateRulePatterns()` 必须抛错 | 字面量被当正则，导致每行都报问题 |
