#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';

function parseArgs(argv) {
  const out = { repo: null, scope: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--repo') out.repo = argv[++i];
    else if (arg === '--scope') out.scope = argv[++i];
    else throw new Error(`unknown argument: ${arg}`);
  }
  if (!out.repo || !out.scope) throw new Error('--repo and --scope are required');
  return out;
}

function git(repo, args) {
  return execFileSync('git', ['-C', repo, ...args], { encoding: 'utf8' }).trim();
}

const forbidden = [
  /^src\/out\//,
  /(^|\/)out\//,
  /^\.ace-outputs\//,
  /\.(zip|tar|tar\.gz|tgz|7z|so|a|o|jar|bin)$/i,
];

const args = parseArgs(process.argv.slice(2));
const scopeJson = JSON.parse(fs.readFileSync(args.scope, 'utf8'));
const allowed = new Set(scopeJson.submit_files || []);
const staged = git(args.repo, ['diff', '--cached', '--name-only']).split('\n').filter(Boolean);
const unstagedAllowed = allowed.size
  ? git(args.repo, ['diff', '--name-only', '--', ...allowed]).split('\n').filter(Boolean)
  : [];

const outsideScope = staged.filter((file) => !allowed.has(file));
const forbiddenFiles = staged.filter((file) => forbidden.some((re) => re.test(file)));
const ok = outsideScope.length === 0 && forbiddenFiles.length === 0 && staged.length > 0;

console.log(JSON.stringify({
  ok,
  staged,
  allowed: [...allowed].sort(),
  unstaged_allowed: unstagedAllowed,
  outside_scope: outsideScope,
  forbidden_files: forbiddenFiles,
}, null, 2));

if (!ok) process.exit(1);
