#!/usr/bin/env node
import { readFileSync } from 'fs';
import { resolve } from 'path';

function usage() {
  console.error('Usage: node validate_merge_result.mjs <06_merge_result.json> [--batch-status <batch_status.json>] [--issue-id <id>]');
  process.exit(2);
}

const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith('-')) usage();
const mergeResultPath = resolve(args[0]);
let batchStatusPath = '';
let issueId = '';
for (let i = 1; i < args.length; i += 1) {
  if (args[i] === '--batch-status') batchStatusPath = resolve(args[++i] || '');
  else if (args[i] === '--issue-id') issueId = args[++i] || '';
  else usage();
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

const merge = readJson(mergeResultPath);
issueId = issueId || String(merge.issue_id || '');
const blockers = merge.blockers || [];
const finalChanged = merge.final_changed_files || [];
const applyOk = merge.apply_ok === true || merge.patch_apply_ok === true || (merge.applied_patches || []).length > 0;
const manualApplied = merge.manual_applied === true;
const semanticLanded = merge.semantic_landed === true;
const manualAttempted = merge.manual_attempted === true;
const stageStatus = merge.stage_status || merge.status || '';

const errors = [];
const warnings = [];

if (manualAttempted && !manualApplied && !semanticLanded && stageStatus === 'ready_for_next') {
  errors.push('manual_attempted_without_manual_applied_cannot_be_ready');
}
if (blockers.length && stageStatus === 'ready_for_next') {
  errors.push(`ready_for_next_with_blockers:${blockers.join(',')}`);
}
if (!blockers.length && stageStatus === 'ready_for_next' && !(applyOk || manualApplied || semanticLanded)) {
  errors.push('ready_for_next_without_apply_manual_or_semantic_landing');
}
if ((applyOk || manualApplied || semanticLanded) && !finalChanged.length) {
  errors.push('landed_without_issue_scoped_final_changed_files');
}
if (finalChanged.some((p) => String(p).startsWith('third_party/rust-toolchain/'))) {
  errors.push('final_changed_files_contains_global_rust_toolchain_diff');
}
if ((merge.commands || []).some((cmd) => /git diff --name-status"?$/.test(String(cmd.cmd || '').trim()))) {
  warnings.push('commands_include_unscoped_global_git_diff');
}

let batchIssue = null;
if (batchStatusPath) {
  const batch = readJson(batchStatusPath);
  batchIssue = (batch.issues || []).find((item) => String(item.issue_id) === issueId) || null;
  if (!batchIssue && issueId) {
    for (const key of ['ready_for_next', 'pending_current_stage', 'terminal_failed', 'deferred_for_archive']) {
      if ((batch[key] || []).map(String).includes(issueId)) batchIssue = { issue_id: issueId, stage_status: key };
    }
  }
  if (batchIssue?.stage_status && stageStatus && batchIssue.stage_status !== stageStatus) {
    errors.push(`batch_status_mismatch:${batchIssue.stage_status}!=${stageStatus}`);
  }
}

const result = {
  valid: errors.length === 0,
  issue_id: issueId || null,
  merge_result: mergeResultPath,
  stage_status: stageStatus || null,
  apply_ok: applyOk,
  manual_attempted: manualAttempted,
  manual_applied: manualApplied,
  semantic_landed: semanticLanded,
  blocker_count: blockers.length,
  final_changed_count: finalChanged.length,
  errors,
  warnings,
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.valid ? 0 : 1);
