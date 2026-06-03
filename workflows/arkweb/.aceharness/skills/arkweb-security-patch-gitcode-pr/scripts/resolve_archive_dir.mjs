#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

function usage() {
  console.error('Usage: resolve_archive_dir.mjs <archive-dir>');
  process.exit(2);
}

const input = process.argv[2];
if (!input) usage();

const real = fs.realpathSync(input);
const stat = fs.statSync(real);
if (!stat.isDirectory()) {
  throw new Error(`archive path is not a directory: ${input}`);
}

function hasFinalArchive(dir) {
  return fs.existsSync(path.join(dir, '04_final_archive.md'));
}

const entries = fs.readdirSync(real, { withFileTypes: true });
const issues = [];

if (hasFinalArchive(real)) {
  issues.push({ issue_id: path.basename(real), dir: real, final_archive: path.join(real, '04_final_archive.md') });
} else {
  for (const entry of entries) {
    if (!entry.isDirectory() || !/^\d+$/.test(entry.name)) continue;
    const issueDir = path.join(real, entry.name);
    if (hasFinalArchive(issueDir)) {
      issues.push({ issue_id: entry.name, dir: issueDir, final_archive: path.join(issueDir, '04_final_archive.md') });
    }
  }
}

if (issues.length === 0) {
  throw new Error(`no issue archive containing 04_final_archive.md under resolved path: ${real}`);
}

console.log(JSON.stringify({ input, realpath: real, issue_count: issues.length, issues }, null, 2));
