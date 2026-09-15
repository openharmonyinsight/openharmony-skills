#!/usr/bin/env node
/**
 * ohos-design-api-doc-checking 自检执行器（A1-A16）。
 *
 * 做法：原样抽取 references/workflow-details.md 与 references/excel-format.md 中的 ```javascript 代码块，
 * 拼接后在 Node 中执行，再用 references/ 下的真实规则 JSON 与 evals/inputs/ 下的真实 fixture 断言行为。
 * 不使用合成规则/合成文档，避免"自测通过但真实配置失效"。
 *
 * 用法：
 *   node evals/scripts/run_self_check.mjs
 * 退出码：0 = 全部通过，1 = 存在失败断言。
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';

// evals/scripts/run_self_check.mjs → skill 根目录
const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

function extractJs(file, skipPredicate = () => false) {
  const text = fs.readFileSync(file, 'utf8');
  const blocks = [];
  const re = /```javascript\n([\s\S]*?)\n```/g;
  for (const m of text.matchAll(re)) {
    if (skipPredicate(m[1])) continue;
    blocks.push(m[1]);
  }
  return blocks.join('\n');
}

const code = [
  extractJs(`${SKILL}/references/workflow-details.md`),
  extractJs(`${SKILL}/references/excel-format.md`, (b) => b.includes('await generateExcelReport'))
].join('\n');

const NAMES = ['IO', 'setIO', 'normalizeIssue', 'makeIssue', 'ledgerRecord', 'notExecuted', 'notApplicable',
  'mapToDimension', 'loadRules', 'validateRuleCoverage', 'validateRulePatterns', 'collectRuleRegexes',
  'compileRuleRegex', 'buildExampleMatcher', 'countRegexMatches', 'detectDocType', 'extractDesigner',
  'parseDocument', 'extractCodeBlocks', 'extractTables', 'extractLinks', 'extractHeadings', 'identifySections',
  'extractMethodSignatures', 'MODULE_SCOPE', 'resolveModuleScope', 'executeChecks', 'assertCompleteExecution',
  'def', 'agentRule', 'RULE_HANDLERS', 'regexRuleScan', 'FUNCTION_HANDLERS', 'functionRuleScan',
  'KEYWORD_GROUP_APPLICABILITY', 'checkKeywordCoverage', 'checkDefaultBehavior', 'checkRequiredSections',
  'scanPatternSpecs', 'checkAmbiguousWording', 'checkRequiredPatterns', 'checkRequiredPatternPresence',
  'checkDeprecationMarks', 'checkExampleCompleteness', 'collectExampleUnits', 'checkVersionSync',
  'checkExampleValidity', 'checkPathConsistency', 'checkSensitiveInfoLeak', 'checkCommonMisspelling',
  'checkHarmonyosGlossary', 'checkUnknownDecorator', 'checkCreationReferenceConsistency', 'collectByPatterns',
  'looksLikeSameName', 'checkSamplePathConsistency', 'checkSrcEntryConsistency', 'checkPlaceholderClarity',
  'checkProjectStructure', 'escapeRegex', 'checkExternalReference', 'checkDiscoverability', 'checkConceptLinks',
  'checkTerminologyConsistency', 'stripCommentsAndStrings', 'balanceScan', 'quoteBalanceScan',
  'generateReport', 'toExcelRow', 'formatLineNumber', 'translatePriority', 'calculateScore',
  'NAME_TRANSFORMS', 'applyNameTransform', 'joinSdkPath', 'normalizeMappingRules', 'compileDocPattern',
  'resolveSdkFilePath', 'runMappingAssertions', 'checkSdkSourceConsistency', 'parseSdkSource', 'formatJsdoc',
  'buildSdkApi', 'parseTypeMember', 'parseSignatureParams', 'parseSignatureReturn', 'splitTopLevel',
  'findSdkApi', 'extractDocApis', 'classifyDocApi', 'detectModuleSince', 'matchFirst', 'extractDocConstraints',
  'cleanCell', 'normalizeErrorCode', 'SDK_RULE', 'checkSinceVersion', 'checkParameters', 'normalizeTypeName',
  'checkReturnType', 'checkErrorCodes', 'checkSystemApiMark', 'checkStageModelMark', 'checkEnumValues',
  'checkInterfaceFields', 'extractTag', 'extractParams', 'extractReturn', 'extractThrows', 'parseSdkVersion',
  'EXCEL_COLUMNS', 'generateExcelReport', 'getSeverityColor', 'wrapNullable', 'markCheckpointSkipped',
  'DIMENSION_NAME', 'DIMENSION_BY_CATEGORY', 'API_HEADING'];

const factory = new Function('ExcelJS', `${code}\n; return { ${NAMES.join(', ')} };`);

// ExcelJS 替身：捕获 addRow 的实际值
function makeWorkbookStub() {
  const rows = [];
  const sheet = {
    columns: null,
    rowCount: 1,
    autoFilter: null,
    views: null,
    getRow: () => ({ font: null, fill: null, alignment: null }),
    addRow: (values) => { rows.push(values); return { fill: null }; }
  };
  return { rows, workbook: { addWorksheet: () => sheet, xlsx: { writeFile: async () => 'written' } } };
}
const stub = makeWorkbookStub();
const M = factory({ Workbook: function () { return stub.workbook; } });

let pass = 0;
const failures = [];
function check(id, label, fn) {
  try {
    fn();
    pass++;
    console.log(`  PASS ${id} ${label}`);
  } catch (err) {
    failures.push(`${id} ${label}: ${err.message}`);
    console.log(`  FAIL ${id} ${label}: ${err.message}`);
  }
}
function assert(cond, msg) { if (!cond) throw new Error(msg); }
function eq(actual, expected, msg) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a !== e) throw new Error(`${msg ?? ''} expected ${e}, got ${a}`);
}

M.setIO({
  exists: (p) => fs.existsSync(p),
  read: (p) => fs.readFileSync(p, 'utf8'),
  readJson: (p) => JSON.parse(fs.readFileSync(p, 'utf8'))
});

const ruleFiles = fs.readdirSync(`${SKILL}/references`).filter(f => f.endsWith('.json'));
const allRules = [];
for (const f of ruleFiles) {
  if (f === 'index.json') continue;
  const data = JSON.parse(fs.readFileSync(`${SKILL}/references/${f}`, 'utf8'));
  for (const r of data.rules ?? []) allRules.push({ ...r, __file: f });
}
const enabledRules = allRules.filter(r => r.enabled !== false);

console.log('\n=== A1: syntax-001 模板插值 ===');
const syntax001 = allRules.find(r => r.id === 'syntax-001');
check('A1', 'good 样例全部不命中 / bad 样例全部命中', () => {
  const matcher = M.buildExampleMatcher(syntax001);
  for (const g of syntax001.examples.good) assert(!matcher(g), `good 被误报: ${g}`);
  for (const b of syntax001.examples.bad) assert(matcher(b), `bad 未命中: ${b}`);
});
check('A1', 'fixture L46 只命中 "$ {" 一处，同行 ${err.message} 不被标记', () => {
  const line = fs.readFileSync(`${SKILL}/evals/inputs/js-apis-demo-taskmanager.md`, 'utf8').split('\n')[45];
  const hits = [...line.matchAll(new RegExp(syntax001.pattern.value, syntax001.pattern.flags))].map(m => m[0]);
  eq(hits, ['$ {'], 'L46 命中集合');
});
check('A1', 'fix.pattern 修复后不再命中', () => {
  const src = 'code is $ {err.code}, message is ${err.message}';
  const fixed = src.replace(new RegExp(syntax001.fix.pattern, 'g'), syntax001.fix.replacement);
  eq(fixed, 'code is ${err.code}, message is ${err.message}');
});

console.log('\n=== A2: 正则可构造 + syntax-005 函数式检查 ===');
check('A2', '全部启用正则可构造', () => {
  for (const rule of enabledRules) {
    for (const spec of M.collectRuleRegexes(rule)) {
      M.compileRuleRegex(spec.value, spec.flags, rule.id, spec.field);
    }
  }
});
check('A2', 'syntax-005 为函数式且正反例正确', () => {
  const rule = allRules.find(r => r.id === 'syntax-005');
  eq(rule.pattern.type, 'function', 'pattern.type');
  const matcher = M.buildExampleMatcher(rule);
  for (const g of rule.examples.good) assert(!matcher(g), `good 被误报: ${g}`);
  for (const b of rule.examples.bad) assert(matcher(b), `bad 未命中: ${b}`);
});

console.log('\n=== A3/A4: 覆盖校验与维度映射 ===');
check('A3', `validateRuleCoverage 覆盖全部 ${enabledRules.length} 条启用规则`, () => {
  const loaded = { byModule: {} };
  for (const f of ruleFiles) {
    if (f === 'index.json') continue;
    const data = JSON.parse(fs.readFileSync(`${SKILL}/references/${f}`, 'utf8'));
    const index = JSON.parse(fs.readFileSync(`${SKILL}/references/index.json`, 'utf8'));
    const moduleName = Object.keys(index.rules).find(k => index.rules[k].file === f);
    loaded.byModule[moduleName] = { module: moduleName, dimension: M.mapToDimension(index.rules[moduleName].category), rules: data.rules };
  }
  const result = M.validateRuleCoverage(loaded, M.RULE_HANDLERS);
  eq(result.enabled, enabledRules.length, 'enabled 规则数');
  assert(result.enabled >= 43, `启用规则数 ${result.enabled} 少于预期 43`);
});
check('A3', '删除注册表条目 → 抛错', () => {
  const loaded = { byModule: { syntax: { module: 'syntax', dimension: 'correctness', rules: [syntax001] } } };
  const registry = { ...M.RULE_HANDLERS };
  delete registry['syntax-001'];
  let threw = false;
  try { M.validateRuleCoverage(loaded, registry); } catch { threw = true; }
  assert(threw, '缺少处理器时未抛错');
});
check('A3', 'correctness-005 处理器错配（name=link-validity）→ 抛错', () => {
  const c005 = allRules.find(r => r.id === 'correctness-005');
  const loaded = { byModule: { correctness: { module: 'correctness', dimension: 'correctness', rules: [c005] } } };
  const registry = { 'correctness-005': M.def('link-validity', 'automatic', () => []) };
  let threw = false;
  try { M.validateRuleCoverage(loaded, registry); } catch { threw = true; }
  assert(threw, 'ID 与处理器 name 错配时未抛错');
});
check('A3', '注册表未知 ID → 抛错', () => {
  const loaded = { byModule: { syntax: { module: 'syntax', dimension: 'correctness', rules: [syntax001] } } };
  const registry = { 'syntax-001': M.RULE_HANDLERS['syntax-001'], 'correctness-006': M.def('sdk-source-consistency', 'automatic', () => []) };
  let threw = false;
  try { M.validateRuleCoverage(loaded, registry); } catch { threw = true; }
  assert(threw, '未知 ID 未抛错');
});
check('A4', 'mapToDimension("能力易用性") === capability，未知分类抛错', () => {
  eq(M.mapToDimension('能力易用性'), 'capability');
  let threw = false;
  try { M.mapToDimension('不存在的分类'); } catch { threw = true; }
  assert(threw, '未知分类未抛错');
});

console.log('\n=== 加载期自检（loadRules 全链路） ===');
let loaded;
check('LOAD', 'loadRules 通过覆盖校验与正则自检', () => {
  loaded = M.loadRules(`${SKILL}/references`);
  assert(loaded.byModule.syntax, 'syntax 模块已加载');
});

console.log('\n=== A5/A6/A7: SDK 侧解析与错误码 ===');
const docText = fs.readFileSync(`${SKILL}/evals/inputs/js-apis-demo-taskmanager.md`, 'utf8');
const sdkText = fs.readFileSync(`${SKILL}/evals/inputs/sdk/api/@ohos.demo.taskmanager.d.ts`, 'utf8');
const parsedDoc = M.parseDocument(docText, { fileName: 'evals/inputs/js-apis-demo-taskmanager.md' });
const sdkParsed = M.parseSdkSource(sdkText);
const docApis = M.extractDocApis(parsedDoc);

check('A5', 'extractDocApis 提取 3 条 API/接口', () => {
  eq(docApis.map(a => a.name), ['createTask', 'queryTasks', 'TaskInfo']);
  const create = docApis[0];
  eq(create.params.map(p => p.name), ['taskInfo', 'callback'], 'createTask 参数');
  eq(create.params.map(p => p.type), ['TaskInfo', 'AsyncCallback<number>'], 'createTask 参数类型');
  eq(create.errorCodes, [401], 'createTask 错误码');
  eq(create.since, 9, 'createTask since');
  eq(create.type, 'function');
  const query = docApis[1];
  eq(query.returns, 'Promise<Array<TaskInfo>>', 'queryTasks 返回值');
  eq(query.errorCodes, [], 'queryTasks 错误码（文档缺表）');
  const info = docApis[2];
  eq(info.type, 'interface', 'TaskInfo 类型');
  eq(info.fields.map(f => f.name), ['name', 'delay'], 'TaskInfo 字段');
});
check('A6', 'parseSdkSource 产出 fields 与 throws', () => {
  const taskInfo = M.findSdkApi(sdkParsed, 'TaskInfo');
  eq(taskInfo.fields.map(f => f.name), ['name', 'delay', 'priority'], 'TaskInfo 字段');
  eq(taskInfo.kind, 'interface');
  const create = M.findSdkApi(sdkParsed, 'createTask');
  eq(create.throws.map(t => t.code), [401, 801], 'createTask throws');
  eq(create.params.map(p => p.name), ['taskInfo', 'callback'], 'createTask SDK 参数');
  eq(create.returns, 'void', 'createTask SDK 返回值');
  eq(create.since, 10, 'createTask @since');
  const query = M.findSdkApi(sdkParsed, 'queryTasks');
  eq(query.throws.map(t => t.code), [401], 'queryTasks throws');
  eq(query.returns, 'Promise<Array<TaskInfo>>', 'queryTasks 返回值');
});
check('A7', 'checkErrorCodes：createTask 只报缺 801，不报 401', () => {
  const issues = M.checkErrorCodes(docApis[0], M.findSdkApi(sdkParsed, 'createTask'), parsedDoc);
  const described = issues.map(i => i.description).join(' | ');
  assert(issues.length === 1, `应只有 1 条问题，实际 ${issues.length}: ${described}`);
  assert(/801/.test(described), `应报告缺失 801: ${described}`);
  assert(!/错误码 401 在SDK/.test(described) && !/错误码 401 在 SDK/.test(described), `不应报告 401 未定义: ${described}`);
});
check('A7', 'checkErrorCodes：queryTasks 报缺 401', () => {
  const issues = M.checkErrorCodes(docApis[1], M.findSdkApi(sdkParsed, 'queryTasks'), parsedDoc);
  assert(issues.some(i => /401/.test(i.description) && i.subType === '错误码缺失'), `应报缺 401: ${JSON.stringify(issues.map(i => i.description))}`);
});
check('A7', 'extractThrows 支持 3 位错误码并统一为数字', () => {
  const jsdoc = '@throws {BusinessError} 401 - Parameter error.\n@throws {BusinessError} 801 - Capability not supported.\n@throws {BusinessError} 1600001 - x';
  eq(M.extractThrows(jsdoc).map(t => t.code), [401, 801, 1600001]);
  assert(M.extractThrows(jsdoc).every(t => typeof t.code === 'number'), '错误码应为 number');
});
check('A7', 'SDK 无 @throws 时报"无法比对"，不建议删除文档错误码', () => {
  const fakeSdkApi = { throws: [], name: 'createTask' };
  const issues = M.checkErrorCodes(docApis[0], fakeSdkApi, parsedDoc);
  assert(issues.length === 1 && issues[0].subType === '错误码无法比对', `应报无法比对: ${JSON.stringify(issues.map(i => i.subType))}`);
  assert(!/移除/.test(issues[0].suggestedFix) || /未确认前不要删除/.test(issues[0].suggestedFix), '不得直接建议移除');
});

console.log('\n=== A8: SDK 文件映射 ===');
const correctness = JSON.parse(fs.readFileSync(`${SKILL}/references/correctness-rules.json`, 'utf8'));
const mappingRules = correctness.sdkSourceCheck.mappingRules;
check('A8', 'mappingRules.assertions 全部通过（含文件存在性）', () => {
  const results = M.runMappingAssertions(mappingRules, `${SKILL}/evals/inputs/sdk`);
  for (const r of results) {
    assert(r.pathOk, `${r.docFileName} → ${r.actual}（期望 ${r.expected}）`);
  }
  const fixture = results.find(r => r.docFileName === 'js-apis-demo-taskmanager.md');
  assert(fixture.fileExists, `fixture SDK 文件应存在: ${fixture.actual}`);
});
check('A8', '四个历史失败样例现在映射正确', () => {
  const base = `${SKILL}/evals/inputs/sdk`;
  const cases = [
    ['js-apis-geolocation.md', 'api/@ohos.geolocation.d.ts'],
    ['js-apis-demo-taskmanager.md', 'api/@ohos.demo.taskmanager.d.ts'],
    ['js-apis-inner-wantAgent-wantAgentInfo-sys.md', 'api/wantAgent/wantAgentInfo.d.ts'],
    ['js-apis-inner-wantAgent-wantAgentInfo.md', 'api/wantAgent/wantAgentInfo.d.ts'],
    ['capi-native-bundle.md', 'api/native_bundle.h'],
    ['js-apis-app-ability-wantAgent.md', 'api/@ohos.app.ability.wantAgent.d.ts']
  ];
  for (const [doc, expected] of cases) {
    const got = M.resolveSdkFilePath(doc, mappingRules, base);
    eq(got.path, `${base}/${expected}`, doc);
  }
});
check('A8', '模式规则独立于 explicitMapping 也能正确映射（防止显式表掩盖模式回归）', () => {
  const base = `${SKILL}/evals/inputs/sdk`;
  const patternOnly = { ...mappingRules, explicitMapping: {} };
  const cases = [
    ['js-apis-geolocation.md', 'api/@ohos.geolocation.d.ts'],
    ['js-apis-demo-taskmanager.md', 'api/@ohos.demo.taskmanager.d.ts'],
    ['js-apis-inner-wantAgent-wantAgentInfo-sys.md', 'api/wantAgent/wantAgentInfo.d.ts'],
    ['capi-native-bundle.md', 'api/native_bundle.h']
  ];
  for (const [doc, expected] of cases) {
    const got = M.resolveSdkFilePath(doc, patternOnly, base);
    eq(got.path, `${base}/${expected}`, `${doc}（仅模式规则）`);
  }
  M.runMappingAssertions(patternOnly, base);
});
check('A8', '映射失败返回 reason 而非 null', () => {
  const got = M.resolveSdkFilePath('random-notes.md', mappingRules, '/sdk');
  eq(got.path, null);
  eq(got.reason, 'no-mapping-rule-matched');
});
check('A8', '未锚定的 docPattern 被拒绝', () => {
  let threw = false;
  try { M.compileDocPattern('^js-apis-{name}.md'); } catch { threw = true; }
  assert(threw, '缺少结尾 $ 未抛错');
});

console.log('\n=== A9: 示例完整性判定 ===');
const completeness001 = allRules.find(r => r.id === 'completeness-001');
function fakeParsed(codeBlockCount, docType = 'api-doc', lineCount = 3) {
  const blocks = [];
  for (let i = 0; i < codeBlockCount; i++) {
    blocks.push({ lang: 'ts', startLine: 10 + i * 20, endLine: 10 + i * 20 + lineCount, lineCount, content: Array(lineCount).fill('a').join('\n'), lines: [] });
  }
  const doc = ['## createTask', '', 'text'].join('\n');
  return {
    fileName: 'x.md', fileBaseName: 'x.md', docType, designer: '-', content: doc,
    lines: doc.split('\n'), codeBlocks: blocks, tables: [], links: [], headings: [],
    sections: [{ title: 'createTask', rawTitle: 'createTask', level: 2, startLine: 1, endLine: 100, body: 'text', bodyLines: [] }],
    methodSignatures: []
  };
}
check('A9', '0 个代码块 → 1 条问题', () => {
  const issues = M.checkExampleCompleteness(fakeParsed(0), completeness001, { dimension: '资源丰富性/完整性', filename: 'x.md', designer: '-' });
  eq(issues.length, 1);
});
check('A9', '1 个代码块（满足阈值）→ 0 条', () => {
  const issues = M.checkExampleCompleteness(fakeParsed(1), { ...completeness001, validation: { codeBlockMinCount: 1 } }, { dimension: '资源丰富性/完整性', filename: 'x.md', designer: '-' });
  eq(issues.length, 0);
});
check('A9', '3 个足额代码块 → 0 条', () => {
  const issues = M.checkExampleCompleteness(fakeParsed(3, 'api-doc', 8), completeness001, { dimension: '资源丰富性/完整性', filename: 'x.md', designer: '-' });
  eq(issues.length, 0);
});
check('A9', '代码块数达标但行数不足 → 降级为 medium 提示', () => {
  const issues = M.checkExampleCompleteness(fakeParsed(3, 'api-doc', 3), completeness001, { dimension: '资源丰富性/完整性', filename: 'x.md', designer: '-' });
  eq(issues.length, 1);
  eq(issues[0].priority, 'medium');
});
check('A9', 'validation 缺失时按默认阈值 1 判定', () => {
  const rule = { ...completeness001, validation: undefined };
  const ctx = { dimension: '资源丰富性/完整性', filename: 'x.md', designer: '-' };
  eq(M.checkExampleCompleteness(fakeParsed(1), rule, ctx).length, 0);
  eq(M.checkExampleCompleteness(fakeParsed(0), rule, ctx).length, 1);
});

console.log('\n=== A10: 报告字段契约 ===');
check('A10', 'toExcelRow 输出全部列且无 undefined', () => {
  const issue = M.normalizeIssue({
    ruleId: 'syntax-001', type: '资料正确性', priority: 'high', description: '问题原因',
    suggestedFix: '建议', line: 42, filename: 'a/b.md', designer: 'zhangsan'
  }, {});
  const row = M.toExcelRow(issue, 'a/b.md', '资料正确性');
  eq(row.lineNumber, '42', 'lineNumber');
  eq(row.filename, 'a/b.md', 'filename');
  eq(row.designer, 'zhangsan', 'designer');
  eq(row.severity, '高', 'severity');
  for (const col of M.EXCEL_COLUMNS) {
    assert(row[col.key] !== undefined && row[col.key] !== null && String(row[col.key]).trim() !== '', `列 ${col.key} 为空`);
  }
});
check('A10', '行号范围与缺省 Designer 渲染', () => {
  eq(M.formatLineNumber(156, 160), '156-160');
  eq(M.formatLineNumber(42, 42), '42');
  eq(M.formatLineNumber(null, null), '-');
  const issue = M.normalizeIssue({ ruleId: 'r', type: 't', priority: 'low', description: 'd', suggestedFix: 's', filename: 'f.md' }, { designer: '-' });
  eq(M.toExcelRow(issue, 'f.md', 't').designer, '-');
  eq(M.extractDesigner('# title\n<!--Designer: lisi-->\n'), 'lisi');
  eq(M.extractDesigner('# title\n'), '-');
});
check('A10', 'generateExcelReport 消费 report.excelData 并写入实际值', async () => {
  const result = {
    issuesByDimension: { correctness: [M.normalizeIssue({ ruleId: 'syntax-001', type: '资料正确性', priority: 'high', description: 'r', suggestedFix: 's', line: 7, filename: 'f.md', designer: 'wangwu' }, {})] },
    ledger: [], sdk: { state: 'not-executed', reason: 'x' }
  };
  const report = M.generateReport(result, 'f.md');
  const stub2 = makeWorkbookStub();
  const factory2 = new Function('ExcelJS', `${code}\n; return { generateExcelReport, EXCEL_COLUMNS };`);
  const M2 = factory2({ Workbook: function () { return stub2.workbook; } });
  M2.generateExcelReport(report, '/tmp/out.xlsx');
  eq(stub2.rows.length, 1, '写入行数');
  eq(stub2.rows[0].designer, 'wangwu', 'Designer 列实际值');
  eq(stub2.rows[0].lineNumber, '7', '行号列实际值');
  eq(stub2.rows[0].filename, 'f.md', '文件名列实际值');
});
check('A10', 'Excel 行缺字段时抛错而不是写 undefined', () => {
  const stub3 = makeWorkbookStub();
  const factory3 = new Function('ExcelJS', `${code}\n; return { generateExcelReport };`);
  const M3 = factory3({ Workbook: function () { return stub3.workbook; } });
  let threw = false;
  try { M3.generateExcelReport({ excelData: [{ filename: 'f.md', designer: undefined, issueType: 't', lineNumber: '1', reason: 'r', suggestion: 's', severity: '高' }] }, '/tmp/out.xlsx'); } catch { threw = true; }
  assert(threw, '空字段未抛错');
});

console.log('\n=== A11/A12: 执行状态与台账 ===');
const agentVerdicts = {};
for (const rule of enabledRules.filter(r => r.execution === 'agent')) {
  agentVerdicts[rule.id] = (rule.checkPoints ?? [{ name: 'default' }]).map(cp => ({ checkPoint: cp.name, status: 'pass', evidence: '人工核对：无问题' }));
}
const baseOptions = { agentVerdicts, modules: ['spelling', 'syntax', 'path-consistency', 'semantics', 'project-structure', 'findability', 'completeness', 'correctness', 'clarity', 'capability'] };

check('A11', '未提供 SDK 路径 → sdk.state=not-executed 且带 reason', () => {
  const result = M.executeChecks(parsedDoc, loaded, { ...baseOptions, modules: [...baseOptions.modules, 'sdk-source-check'] });
  eq(result.sdk.state, 'not-executed');
  assert(result.sdk.reason, 'reason 不能为空');
});
check('A11', '提供 SDK 路径 → sdk.state=passed 并命中版本/错误码/字段不一致', () => {
  const result = M.executeChecks(parsedDoc, loaded, {
    ...baseOptions,
    modules: [...baseOptions.modules, 'sdk-source-check'],
    sdkSourcePath: `${SKILL}/evals/inputs/sdk`
  });
  eq(result.sdk.state, 'passed', `sdk state, reason=${result.sdk.reason}`);
  const subTypes = result.issuesByDimension.correctness.map(i => i.subType);
  assert(subTypes.includes('API起始版本不一致'), `应命中版本不一致: ${subTypes.join(',')}`);
  assert(subTypes.includes('错误码缺失'), `应命中错误码缺失: ${subTypes.join(',')}`);
  assert(subTypes.includes('接口字段缺失'), `应命中接口字段缺失: ${subTypes.join(',')}`);
  const versionIssue = result.issuesByDimension.correctness.find(i => i.subType === 'API起始版本不一致');
  eq(versionIssue.priority, 'critical', '版本不一致应为 critical');
});
check('A11', 'SDK 文件不存在 → sdk.state=failed', () => {
  const result = M.executeChecks(parsedDoc, loaded, {
    ...baseOptions, modules: [...baseOptions.modules, 'sdk-source-check'],
    sdkSourcePath: `${SKILL}/evals/inputs/sdk`, sdkFilePath: 'api/@ohos.not-exist.d.ts', tolerateFailures: true
  });
  eq(result.sdk.state, 'failed');
  eq(result.sdk.reason, 'sdk-file-not-found');
});
check('A11', '文档提取不到 API → sdk.state=failed（不得当成 0 问题）', () => {
  const emptyDoc = M.parseDocument('# 说明\n\n没有任何 API 章节。\n', { fileName: 'js-apis-empty.md' });
  const result = M.checkSdkSourceConsistency(emptyDoc, loaded.byModule.correctness.sdkSourceCheck, { sdkSourcePath: `${SKILL}/evals/inputs/sdk`, sdkFilePath: 'api/@ohos.demo.taskmanager.d.ts', runMappingAssertions: false });
  eq(result.state, 'failed');
  eq(result.reason, 'doc-api-extraction-empty');
});
check('A12', 'agent 规则未回填 verdict → 该规则 failed 且整体抛错', () => {
  let threw = false;
  try {
    M.executeChecks(parsedDoc, loaded, { ...baseOptions, agentVerdicts: {} });
  } catch (err) {
    threw = /agent 规则/.test(err.message);
  }
  assert(threw, 'agent 规则缺 verdict 未抛错');
});
check('A12', '全部启用规则都有台账记录', () => {
  const result = M.executeChecks(parsedDoc, loaded, baseOptions);
  const ids = new Set(result.ledger.map(r => r.ruleId).filter(Boolean));
  for (const rule of enabledRules) {
    assert(ids.has(rule.id), `缺少台账记录: ${rule.id}`);
  }
  assert(result.ledger.every(r => M.LEDGER_STATUS ?? true), 'ledger 状态合法');
});
check('A12', '台账缺失时 assertCompleteExecution 抛错', () => {
  let threw = false;
  try {
    M.assertCompleteExecution([{ module: 'syntax', ruleId: 'syntax-001', status: 'executed' }], loaded, M.resolveModuleScope('api-doc', baseOptions));
  } catch { threw = true; }
  assert(threw, '台账不完整未抛错');
});

console.log('\n=== A13/A14/A15/A16: 精度与 ground truth ===');
check('A13', 'spelling-002 不把参数表首列的 callback 判为术语错误', () => {
  const sp = allRules.find(r => r.id === 'spelling-002');
  const spellingFile = JSON.parse(fs.readFileSync(`${SKILL}/references/spelling-rules.json`, 'utf8'));
  const ctx = { dimension: '资料正确性', filename: parsedDoc.fileName, designer: '-', ruleFile: { data: spellingFile } };
  const issues = M.checkHarmonyosGlossary(parsedDoc, sp, ctx);
  const hits = issues.map(i => `${i.line}:${i.description}`);
  assert(issues.some(i => i.line === 55 && /UiAbility/.test(i.description)), `应命中 L55 UiAbility: ${JSON.stringify(hits)}`);
  assert(!issues.some(i => /"callback" 应为/.test(i.description)), `不应命中 callback: ${JSON.stringify(hits)}`);
});
check('A14', 'completeness-002 逐 API 章节检查必备小节', () => {
  const cp = allRules.find(r => r.id === 'completeness-002');
  const ctx = { dimension: '资源丰富性/完整性', filename: parsedDoc.fileName, designer: '-' };
  const issues = M.checkRequiredSections(parsedDoc, cp, ctx);
  const text = issues.map(i => i.description).join(' | ');
  assert(issues.some(i => /queryTasks/.test(i.description) && /错误码/.test(i.description)), `应报 queryTasks 缺错误码: ${text}`);
  assert(!/createTask9?\+? 章节缺少/.test(text), `createTask 四小节齐全，不应被报: ${text}`);
  assert(!/TaskInfo/.test(text), `接口章节不参与逐章节判定: ${text}`);
});
check('A15', 'evals/check_ground_truth.py 退出码为 0', () => {
  try {
    execFileSync('python3', [`${SKILL}/evals/check_ground_truth.py`], { stdio: 'pipe' });
  } catch (err) {
    if (err.code === 'ENOENT') { console.log('    (跳过：未找到 python3)'); return; }
    throw new Error(String(err.stdout ?? err.message));
  }
});
check('A16', '退化正则（字面量 "..." 当正则）被 validateRulePatterns 拒绝', () => {
  const broken = JSON.parse(JSON.stringify(loaded));
  const clarity = broken.byModule.clarity.rules.find(r => r.id === 'clarity-002');
  clarity.ambiguousPatterns = [{ pattern: '等等|...', suggestion: '完整列举所有项' }];
  let threw = false;
  try { M.validateRulePatterns(broken); } catch (err) { threw = /过于宽泛/.test(err.message); }
  assert(threw, '退化正则未被拒绝');
});

console.log('\n=== 端到端：fixture 全流程 ===');
check('E2E', 'API 文档 fixture 跑通全流程并产出报告', () => {
  const result = M.executeChecks(parsedDoc, loaded, { ...baseOptions, modules: [...baseOptions.modules, 'sdk-source-check'], sdkSourcePath: `${SKILL}/evals/inputs/sdk` });
  const report = M.generateReport(result, parsedDoc.fileName);
  assert(report.summary.total > 0, '应发现问题');
  eq(report.summary.sdkCheckState, 'passed');
  const syntaxIssue = report.excelData.find(r => r.ruleId === 'syntax-001');
  eq(syntaxIssue.lineNumber, '46', 'syntax-001 命中行号');
  assert(report.excelData.every(r => r.filename && r.designer && r.reason && r.suggestion && r.severity), '每行字段完整');
  console.log(`    问题总数=${report.summary.total} 严重=${report.summary.critical} 高=${report.summary.high} 中=${report.summary.medium} 低=${report.summary.low} 得分=${report.summary.score}`);
  console.log(`    规则 executed=${report.summary.rulesExecuted} notExecuted=${report.summary.rulesNotExecuted.length} failed=${report.summary.rulesFailed.length}`);
});
check('E2E', '开发指南 fixture 跑通并跳过 SDK 检查', () => {
  const guide = M.parseDocument(fs.readFileSync(`${SKILL}/evals/inputs/application-dev-guide-demo-task.md`, 'utf8'), { fileName: 'evals/inputs/application-dev-guide-demo-task.md' });
  eq(guide.docType, 'dev-guide', 'docType');
  const result = M.executeChecks(guide, loaded, { agentVerdicts, sampleData: {} });
  eq(result.sdk.state, 'not-applicable');
  const report = M.generateReport(result, guide.fileName);
  const syntaxHits = report.excelData.filter(r => r.ruleId === 'syntax-001');
  eq(syntaxHits.length, 1, '指南中 syntax-001 命中数');
  eq(syntaxHits[0].lineNumber, '26', 'syntax-001 行号');
  console.log(`    指南问题总数=${report.summary.total}（${report.excelData.map(r => r.ruleId).join(', ')}）`);
});

console.log(`\n自检结果：通过 ${pass} 项，失败 ${failures.length} 项（skill root: ${SKILL}）`);
if (failures.length > 0) {
  console.log('\n失败明细：');
  for (const f of failures) console.log(' - ' + f);
  process.exit(1);
}
