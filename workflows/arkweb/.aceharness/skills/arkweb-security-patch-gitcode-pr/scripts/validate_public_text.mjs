#!/usr/bin/env node
import fs from 'node:fs';

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Usage: validate_public_text.mjs <file>...');
  process.exit(2);
}

const forbidden = [
  { name: 'absolute_local_path', re: /(^|[\s"'(:])\/(home|tmp|var|mnt)\// },
  { name: 'ace_outputs', re: /\.ace-outputs/ },
  { name: 'run_dir', re: /run-[0-9]{12,}/ },
  { name: 'local_archive_filename', re: /(00_batch_plan|batch_status|03_impact_decision|04_final_archive|12_submit_result|13_final_report)\.md/ },
  { name: 'token', re: /(GITCODE_TOKEN|gitcode-askpass|Authorization:|Bearer\s+[A-Za-z0-9._-]+)/i },
  { name: 'batch_cross_issue_context', re: /(批量统计|批量失败|批量处理顺序|overlap 总览|blocked_overlap_conflict)/ },
];

let failed = false;
const findings = [];

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8');
  for (const rule of forbidden) {
    if (rule.re.test(text)) {
      failed = true;
      findings.push({ file, rule: rule.name });
    }
  }
}

console.log(JSON.stringify({ ok: !failed, findings }, null, 2));
if (failed) process.exit(1);
