#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

function parseArgs(argv) {
  const out = { mergeResult: null, buildFix: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--merge-result') out.mergeResult = argv[++i];
    else if (arg === '--build-fix') out.buildFix = argv[++i];
    else throw new Error(`unknown argument: ${arg}`);
  }
  if (!out.mergeResult) throw new Error('--merge-result is required');
  return out;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function addList(set, value) {
  if (!value) return;
  if (Array.isArray(value)) {
    for (const item of value) addList(set, item);
    return;
  }
  if (typeof value === 'object') {
    addList(set, value.path || value.file || value.file_path || value.target_path);
    return;
  }
  if (typeof value === 'string' && value.trim()) {
    const candidate = value.trim();
    // Only keep repo-relative file paths. Local adaptation summaries may be
    // free-form prose and must not leak into the submit file scope.
    if (
      candidate.includes('/') &&
      !candidate.startsWith('/') &&
      !candidate.includes('\n') &&
      !candidate.split('/').includes('..')
    ) {
      set.add(candidate);
    }
  }
}

const args = parseArgs(process.argv.slice(2));
const merge = readJson(args.mergeResult);
const build = args.buildFix && fs.existsSync(args.buildFix) ? readJson(args.buildFix) : {};
const scope = new Set();
const explicitFinalFiles = new Set();
const targetRepo =
  merge.target_git_subrepo ||
  merge.target_subrepo ||
  build.target_git_subrepo ||
  build.target_subrepo ||
  null;

addList(scope, merge.modified_files);
addList(scope, merge.final_changed_files);
addList(explicitFinalFiles, merge.final_changed_files);
for (const key of ['local_adaptations']) addList(scope, merge[key]);
for (const key of ['compile_fix_files', 'local_adaptations']) addList(scope, build[key]);

const filteredScope = [...scope].filter((candidate) => {
  if (!targetRepo) return true;
  const absPath = path.join(targetRepo, candidate);
  return fs.existsSync(absPath) || explicitFinalFiles.has(candidate);
});

const blockers = [];
if (merge.semantic_landed !== true && merge.manual_applied !== true && merge.apply_ok !== true) {
  blockers.push('patch_not_landed');
}
if (Array.isArray(merge.blockers) && merge.blockers.length > 0) blockers.push(...merge.blockers);

console.log(JSON.stringify({
  issue_id: merge.issue_id || build.issue_id || null,
  target_subrepo: targetRepo,
  submit_files: filteredScope.sort(),
  blockers,
  ready: blockers.length === 0 && filteredScope.length > 0,
}, null, 2));
