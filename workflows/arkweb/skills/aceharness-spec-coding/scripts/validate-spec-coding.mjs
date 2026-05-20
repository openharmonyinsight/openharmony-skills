#!/usr/bin/env node

import { existsSync, readdirSync, readFileSync, statSync } from 'fs';
import { resolve, join } from 'path';

function fail(message) {
  console.error(`ACEHarness Spec Coding 校验失败: ${message}`);
  process.exitCode = 1;
}

function info(message) {
  console.log(`ACEHarness Spec Coding: ${message}`);
}

function isDirectory(path) {
  try { return statSync(path).isDirectory(); } catch { return false; }
}

function isFile(path) {
  try { return statSync(path).isFile(); } catch { return false; }
}

function read(path) {
  return readFileSync(path, 'utf-8');
}

function listDirs(path) {
  if (!isDirectory(path)) return [];
  return readdirSync(path, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

function requirePattern(content, pattern, file, message) {
  if (!pattern.test(content)) {
    fail(`${file}: ${message}`);
  }
}

// ---- requirements.md 校验 ----
function validateRequirements(file) {
  if (!isFile(file)) {
    fail(`${file}: 缺少 requirements.md`);
    return;
  }
  const content = read(file);
  requirePattern(content, /^# 需求文档[：:].+/m, file, '必须以 `# 需求文档：<功能名称>` 开头');
  requirePattern(content, /^## 需求$/m, file, '缺少 `## 需求` 章节');
  requirePattern(content, /^### 需求 \d+[：:].+/m, file, '至少需要一个 `### 需求 N：<名称>`');
  requirePattern(content, /\*\*用户故事[：:]\*\*/m, file, '至少需要一个用户故事');
  requirePattern(content, /^#### 验收标准$/m, file, '至少需要一个 `#### 验收标准` 章节');
  requirePattern(content, /WHEN .+ THEN .+/m, file, '至少需要一个 WHEN/THEN 验收标准');
}

// ---- design.md 校验 ----
function validateDesign(file) {
  if (!isFile(file)) {
    fail(`${file}: 缺少 design.md`);
    return;
  }
  const content = read(file);
  requirePattern(content, /^# 设计文档[：:].+/m, file, '必须以 `# 设计文档：<功能名称>` 开头');
  requirePattern(content, /^## 概述$/m, file, '缺少 `## 概述` 章节');
  // 检查是否有 Mermaid 图或架构图
  const hasMermaid = /```mermaid/m.test(content);
  const hasArchSection = /^## 架构$/m.test(content);
  if (!hasMermaid && !hasArchSection) {
    fail(`${file}: 缺少架构图（Mermaid 代码块或 ## 架构 章节）`);
  }
  requirePattern(content, /^## 关键决策$/m, file, '缺少 `## 关键决策` 章节');
  // 检查关键决策表至少有一行数据
  const tableRowPattern = /^\|[^|]+\|[^|]+\|[^|]+\|/m;
  if (!tableRowPattern.test(content)) {
    fail(`${file}: 关键决策表至少需要一行数据`);
  }
}

// ---- tasks.md 校验 ----
function validateTasks(file) {
  if (!isFile(file)) {
    fail(`${file}: 缺少 tasks.md`);
    return;
  }
  const content = read(file);
  requirePattern(content, /^# 实现计划[：:].+/m, file, '必须以 `# 实现计划：<功能名称>` 开头');
  requirePattern(content, /^## 任务$/m, file, '缺少 `## 任务` 章节');

  // 检查多级嵌套 checkbox
  const topLevelTasks = content.match(/^- \[[ xX-]\] \d+\./gm) || [];
  if (topLevelTasks.length === 0) {
    fail(`${file}: 至少需要一个顶层任务（格式：- [ ] N. <标题>）`);
  }

  const subTasks = content.match(/^\s{2,}- \[[ xX-]\] \d+\.\d+/gm) || [];
  if (subTasks.length === 0) {
    fail(`${file}: 至少需要一个子任务（格式：  - [ ] N.M <标题>）`);
  }

  // 检查需求引用
  const reqRefs = content.match(/_需求[：:].+?_/gm) || [];
  if (reqRefs.length === 0) {
    fail(`${file}: 至少需要一个需求引用（格式：_需求：x.x_）`);
  }

  // 检查检查点
  const checkpoints = content.match(/^- \[[ xX-]\] \d+\.\s*检查点/gm) || [];
  if (checkpoints.length === 0) {
    fail(`${file}: 至少需要一个检查点任务`);
  }
}

// ---- 目录校验 ----
function validateSpecDomain(domainDir) {
  const requirements = join(domainDir, 'requirements.md');
  const design = join(domainDir, 'design.md');
  const tasks = join(domainDir, 'tasks.md');

  validateRequirements(requirements);
  validateDesign(design);
  validateTasks(tasks);
}

function validateMasterFiles(rootDir) {
  const masterSpec = join(rootDir, 'spec.md');
  const checklist = join(rootDir, 'checklist.md');

  if (!isFile(masterSpec)) {
    fail(`${masterSpec}: 缺少 master spec.md`);
  }

  if (isFile(checklist)) {
    const content = read(checklist);
    const questions = content.match(/^- \[[ xX]\] .+/gm) || [];
    if (questions.length === 0) {
      fail(`${checklist}: checklist.md 至少需要一个 \`- [ ] 问题内容\` 或 \`- [x] 问题内容\``);
    }
  } else {
    info(`${checklist}: 未发现 checklist.md，跳过问题清单校验`);
  }
}

function validateRoot(rootDir) {
  if (!isDirectory(rootDir)) {
    fail(`根目录不存在: ${rootDir}`);
    return;
  }

  validateMasterFiles(rootDir);

  const specsRoot = join(rootDir, 'specs');
  if (!isDirectory(specsRoot)) {
    fail(`${specsRoot}: 缺少 specs 目录`);
    return;
  }

  const runs = listDirs(specsRoot);
  if (runs.length === 0) {
    fail(`${specsRoot}: 至少需要一个 <workflowName>-<runId> delta 目录`);
    return;
  }

  for (const runDir of runs) {
    info(`校验 delta spec: ${runDir}`);
    validateSpecDomain(join(specsRoot, runDir));
  }
}

const input = process.argv[2];
if (!input) {
  console.error('用法: node validate-spec-coding.mjs <spec-root>');
  process.exit(1);
}

const rootDir = resolve(input);
validateRoot(rootDir);

if (process.exitCode && process.exitCode !== 0) {
  process.exit(process.exitCode);
}

info(`校验通过: ${rootDir}`);
