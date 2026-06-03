#!/usr/bin/env node
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { spawnSync } from 'child_process';

function usage() {
  console.error('Usage: node issue_diff_scope.mjs --repo <git-repo> --merge-result <06_merge_result.json> [--build-fix <10_build_fix.json>]');
  process.exit(2);
}

const args = process.argv.slice(2);
let repo = '';
let mergeResultPath = '';
let buildFixPath = '';
for (let i = 0; i < args.length; i += 1) {
  if (args[i] === '--repo') repo = resolve(args[++i] || '');
  else if (args[i] === '--merge-result') mergeResultPath = resolve(args[++i] || '');
  else if (args[i] === '--build-fix') buildFixPath = resolve(args[++i] || '');
  else usage();
}
if (!repo || !mergeResultPath) usage();

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function pathVariants(p) {
  const raw = String(p || '').replace(/^a\//, '').replace(/^b\//, '');
  if (!raw) return [];
  const variants = new Set([raw]);
  if (raw.startsWith('src/')) variants.add(raw.replace(/^src\//, ''));
  return Array.from(variants);
}

const merge = readJson(mergeResultPath);
const buildFix = buildFixPath ? readJson(buildFixPath) : {};
const allowed = new Set();

for (const p of merge.modified_files || []) {
  for (const variant of pathVariants(p)) allowed.add(variant);
}
for (const item of merge.patch_normalization || merge.normalized_patches || []) {
  for (const p of item.diff_paths || []) {
    for (const variant of pathVariants(p)) allowed.add(variant);
  }
}
for (const item of merge.local_adaptations || []) {
  const p = typeof item === 'string' ? item : item.path || item.file;
  if (p) {
    for (const variant of pathVariants(p)) allowed.add(variant);
  }
}
for (const p of buildFix.compile_fix_files || []) {
  for (const variant of pathVariants(p)) allowed.add(variant);
}
for (const item of buildFix.local_adaptations || []) {
  const p = typeof item === 'string' ? item : item.path || item.file;
  if (p) {
    for (const variant of pathVariants(p)) allowed.add(variant);
  }
}

const allowedFiles = Array.from(allowed).filter(Boolean).sort();
let diffOutput = '';
if (allowedFiles.length) {
  const run = spawnSync('git', ['diff', '--name-status', '--', ...allowedFiles], {
    cwd: repo,
    encoding: 'utf8',
    maxBuffer: 20 * 1024 * 1024,
  });
  diffOutput = run.stdout || '';
}

const entries = diffOutput.split(/\r?\n/).filter(Boolean).map((line) => {
  const parts = line.split(/\t+/);
  return { status: parts[0], path: parts[parts.length - 1] };
});

const result = {
  repo,
  merge_result: mergeResultPath,
  build_fix: buildFixPath || null,
  allowed_files: allowedFiles,
  final_changed_files: entries.map((entry) => entry.path),
  final_diff_name_status: diffOutput.trim(),
  changed_count: entries.length,
};

console.log(JSON.stringify(result, null, 2));
process.exit(entries.length ? 0 : 1);
