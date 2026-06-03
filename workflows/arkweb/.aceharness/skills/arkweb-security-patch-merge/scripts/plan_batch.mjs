#!/usr/bin/env node
import { createHash } from 'crypto';
import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { basename, join, resolve } from 'path';

function usage() {
  console.error('Usage: node plan_batch.mjs --archive-dir <dir> --output-dir <dir> [--project-root <dir>] [--normalizer <normalize_patch.mjs>]');
  process.exit(2);
}

const args = process.argv.slice(2);
let archiveDir = '';
let outputDir = '';
let projectRoot = '';
for (let i = 0; i < args.length; i += 1) {
  if (args[i] === '--archive-dir') archiveDir = resolve(args[++i] || '');
  else if (args[i] === '--output-dir') outputDir = resolve(args[++i] || '');
  else if (args[i] === '--project-root') projectRoot = resolve(args[++i] || '');
  else if (args[i] === '--normalizer') i += 1;
  else usage();
}
if (!archiveDir) usage();
if (!outputDir) outputDir = process.cwd();
if (outputDir.includes('/.aceharness/runs/')) {
  console.error(`invalid output-dir under ACEHarness run logs: ${outputDir}`);
  process.exit(2);
}
if (projectRoot) {
  const actualParent = resolve(outputDir, '..');
  if (basename(actualParent) !== '.ace-outputs') {
    console.error(`invalid output-dir: ${outputDir}; expected <workflowRoot>/.ace-outputs/<runId>`);
    process.exit(2);
  }
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function firstIssue(meta) {
  if (meta && Array.isArray(meta.issues) && meta.issues.length && typeof meta.issues[0] === 'object') {
    return meta.issues[0];
  }
  return meta || {};
}

function mergePolicyFromImpact(impact) {
  const policy = impact?.merge_policy && typeof impact.merge_policy === 'object' ? impact.merge_policy : {};
  const forceMerge = policy.force_merge === true || policy.forceMerge === true || policy.impact_mode === 'force_affected';
  return {
    force_merge: forceMerge,
    impact_mode: policy.impact_mode || (forceMerge ? 'force_affected' : 'normal'),
    reason: policy.reason || '',
  };
}

function issueDirs(root) {
  if (existsSync(join(root, '02_patch_fetch.json'))) return [root];
  return readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d+$/.test(entry.name))
    .map((entry) => join(root, entry.name))
    .filter((dir) => existsSync(join(dir, '02_patch_fetch.json')))
    .sort((a, b) => Number(basename(a)) - Number(basename(b)));
}

function normalizePath(p) {
  const value = typeof p === 'object' && p !== null ? (p.path || p.file || p.new_path || p.old_path || '') : p;
  return String(value || '').replace(/^a\//, '').replace(/^b\//, '').replace(/^src\//, '');
}

function sha256(buffer) {
  return createHash('sha256').update(buffer).digest('hex');
}

function signals(text) {
  const found = [];
  if (/^diff --git /m.test(text)) found.push('diff --git');
  if (/^Index: /m.test(text)) found.push('Index:');
  if (/^--- [ab]\//m.test(text) && /^\+\+\+ [ab]\//m.test(text)) found.push('--- a/ +++ b/');
  if (/^From [0-9a-f]{7,40}/m.test(text) && /^Subject:/m.test(text)) found.push('mbox');
  return found;
}

function looksBase64(text) {
  const compact = text.replace(/\s+/g, '');
  return compact.length > 0 && compact.length % 4 === 0 && /^[A-Za-z0-9+/=]+$/.test(compact);
}

function diffPaths(text) {
  const paths = new Set();
  for (const line of text.split(/\r?\n/)) {
    let m = line.match(/^diff --git a\/(.+?) b\/(.+)$/);
    if (m) {
      paths.add(m[1]);
      paths.add(m[2]);
      continue;
    }
    m = line.match(/^(---|\+\+\+) [ab]\/(.+)$/);
    if (m && m[2] !== '/dev/null') paths.add(m[2]);
  }
  return Array.from(paths).filter((p) => p && p !== '/dev/null').sort();
}

function normalizePatch(inputPath, outPath) {
  const original = readFileSync(inputPath);
  const originalText = original.toString('utf8');
  let normalized = original;
  let format = 'invalid';
  let found = signals(originalText);

  if (found.length) {
    format = found.includes('mbox') ? 'raw_mbox' : 'raw_diff';
  } else if (looksBase64(originalText)) {
    try {
      const decoded = Buffer.from(originalText.replace(/\s+/g, ''), 'base64');
      const decodedText = decoded.toString('utf8');
      const decodedSignals = signals(decodedText);
      if (decodedSignals.length) {
        normalized = decoded;
        found = decodedSignals;
        format = decodedSignals.includes('mbox') ? 'base64_mbox' : 'base64_diff';
      }
    } catch {
      format = 'invalid';
    }
  }

  const valid = format !== 'invalid';
  if (valid) writeFileSync(outPath, normalized);
  const normalizedText = normalized.toString('utf8');
  return {
    original_path: inputPath,
    normalized_path: valid ? outPath : null,
    format,
    valid,
    validation_signals: found,
    original_sha256: sha256(original),
    normalized_sha256: valid ? sha256(normalized) : null,
    diff_paths: valid ? diffPaths(normalizedText) : [],
  };
}

function patchPaths(issueDir, patchFetch) {
  const paths = [];
  for (const item of patchFetch.patch_files || []) {
    const p = typeof item === 'string' ? item : item.path;
    if (!p) continue;
    const candidates = [
      resolve(issueDir, p),
      resolve(issueDir, 'patches', p),
      resolve(archiveDir, p),
      resolve(p),
    ];
    const found = candidates.find((candidate) => existsSync(candidate));
    if (found) paths.push(found);
  }
  const patchDir = join(issueDir, 'patches');
  if (!paths.length && existsSync(patchDir)) {
    for (const name of readdirSync(patchDir)) {
      if (/\.(patch|diff|txt)$/i.test(name)) paths.push(join(patchDir, name));
    }
  }
  return Array.from(new Set(paths));
}

const issues = [];
const fileToIssues = new Map();
mkdirSync(outputDir, { recursive: true });

for (const dir of issueDirs(archiveDir)) {
  const issueId = basename(dir);
  const patchFetchPath = join(dir, '02_patch_fetch.json');
  const impactPath = join(dir, '03_impact_decision.json');
  const issueOutDir = join(outputDir, 'issues', issueId, 'normalized_patches');
  mkdirSync(issueOutDir, { recursive: true });
  let patchFetch = {};
  let blockers = [];
  try {
    patchFetch = firstIssue(readJson(patchFetchPath));
  } catch (e) {
    blockers.push(`patch_fetch_json_invalid:${e.message}`);
  }
  let impact = {};
  try {
    if (existsSync(impactPath)) impact = firstIssue(readJson(impactPath));
  } catch (e) {
    blockers.push(`impact_json_invalid:${e.message}`);
  }
  const mergePolicy = mergePolicyFromImpact(impact);

  const modified = (patchFetch.modified_files || []).map(normalizePath).filter(Boolean);
  const normalizations = [];
  for (const patchPath of patchPaths(dir, patchFetch)) {
    const out = join(issueOutDir, `${normalizations.length}-${basename(patchPath)}.patch`);
    try {
      normalizations.push(normalizePatch(patchPath, out));
    } catch (e) {
      normalizations.push({ original_path: patchPath, valid: false, format: 'invalid', diff_paths: [], error: e.message });
    }
    if (!normalizations[normalizations.length - 1].valid) blockers.push(`invalid_patch_format:${patchPath}`);
  }

  const files = Array.from(new Set([
    ...modified,
    ...normalizations.flatMap((item) => item.diff_paths || []).map(normalizePath),
  ].filter(Boolean))).sort();

  for (const file of files) {
    if (!fileToIssues.has(file)) fileToIssues.set(file, new Set());
    fileToIssues.get(file).add(issueId);
  }

  issues.push({
    issue_id: issueId,
    issue_dir: dir,
    patch_fetch_json: patchFetchPath,
    impact_json: existsSync(impactPath) ? impactPath : null,
    arkweb_impact: impact.arkweb_impact || impact.impact || 'unknown',
    merge_policy: mergePolicy,
    patch_count: normalizations.length,
    modified_files: modified,
    patch_normalization: normalizations,
    target_files: files,
    blockers,
  });
}

const duplicateFiles = [];
const losers = new Set();
const winners = new Set();
for (const [file, set] of Array.from(fileToIssues.entries()).sort()) {
  const issueIds = Array.from(set).sort((a, b) => Number(a) - Number(b));
  if (issueIds.length <= 1) continue;
  const winner = issueIds[0];
  const loserList = issueIds.slice(1);
  winners.add(winner);
  loserList.forEach((id) => losers.add(id));
  duplicateFiles.push({ file, issue_ids: issueIds, winner_issue_id: winner, loser_issue_ids: loserList });
}

const ready = issues.filter((issue) => !issue.blockers.length).map((issue) => issue.issue_id);
const activeBatch = ready.filter((id) => !losers.has(id)).sort((a, b) => Number(a) - Number(b));
const deferred = Array.from(losers).sort((a, b) => Number(a) - Number(b));
const blocked = issues.filter((issue) => issue.blockers.length).map((issue) => ({
  issue_id: issue.issue_id,
  blockers: issue.blockers,
}));

const plan = {
  archive_dir: archiveDir,
  generated_at: new Date().toISOString(),
  merge_policy: {
    force_merge: issues.some((issue) => issue.merge_policy?.force_merge === true),
    issue_policies: Object.fromEntries(issues.map((issue) => [issue.issue_id, issue.merge_policy])),
  },
  issues,
  duplicate_files: duplicateFiles,
  overlap_winners: Array.from(winners).sort((a, b) => Number(a) - Number(b)),
  ready_for_apply: ready,
  active_batch: activeBatch,
  deferred_for_archive: deferred,
  blocked,
};

writeFileSync(join(outputDir, '00_batch_plan.json'), `${JSON.stringify(plan, null, 2)}\n`);
writeFileSync(join(outputDir, '00_batch_plan.md'), [
  '# Batch Plan',
  '',
  `archive_dir: ${archiveDir}`,
  `force_merge: ${issues.some((issue) => issue.merge_policy?.force_merge === true)}`,
  `active_batch: ${activeBatch.join(', ') || '(none)'}`,
  `deferred_for_archive: ${deferred.join(', ') || '(none)'}`,
  `blocked: ${blocked.map((item) => item.issue_id).join(', ') || '(none)'}`,
  '',
  '## duplicate_files',
  ...duplicateFiles.map((item) => `- ${item.file}: issues=${item.issue_ids.join(', ')} winner=${item.winner_issue_id}`),
  '',
].join('\n'));

console.log(JSON.stringify(plan, null, 2));
