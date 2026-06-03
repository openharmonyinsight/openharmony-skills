#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function parseArgs(argv) {
  const out = {
    repo: null,
    scope: null,
    baseRef: null,
    branch: null,
    messageFile: null,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--repo') out.repo = argv[++i];
    else if (arg === '--scope') out.scope = argv[++i];
    else if (arg === '--base-ref') out.baseRef = argv[++i];
    else if (arg === '--branch') out.branch = argv[++i];
    else if (arg === '--message-file') out.messageFile = argv[++i];
    else throw new Error(`unknown argument: ${arg}`);
  }
  for (const [key, value] of Object.entries(out)) {
    if (!value) throw new Error(`--${key.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)} is required`);
  }
  return out;
}

function git(repo, args, opts = {}) {
  return execFileSync('git', ['-C', repo, ...args], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    ...opts,
  }).trim();
}

function gitWithIndex(repo, indexFile, args) {
  return git(repo, args, {
    env: { ...process.env, GIT_INDEX_FILE: indexFile },
  });
}

function isForbidden(file) {
  return [
    /^src\/out\//,
    /(^|\/)out\//,
    /^\.ace-outputs\//,
    /\.(zip|tar|tar\.gz|tgz|7z|so|a|o|jar|bin)$/i,
  ].some((re) => re.test(file));
}

function assertRelative(file) {
  if (!file || file.startsWith('/') || file.includes('\0') || file.split('/').includes('..')) {
    throw new Error(`unsafe path in submit scope: ${file}`);
  }
}

function fileMode(absPath) {
  try {
    const stat = fs.statSync(absPath);
    return (stat.mode & 0o111) ? '100755' : '100644';
  } catch {
    return '100644';
  }
}

const args = parseArgs(process.argv.slice(2));
const repo = fs.realpathSync(args.repo);
const scopeJson = JSON.parse(fs.readFileSync(args.scope, 'utf8'));
const submitFiles = [...new Set(scopeJson.submit_files || [])].sort();
const signoffName = git(repo, ['config', 'user.name']);
const signoffEmail = git(repo, ['config', 'user.email']);

if (submitFiles.length === 0) throw new Error('submit scope is empty');
if (!signoffName || !signoffEmail) throw new Error('git user.name/user.email must be configured for signoff');
for (const file of submitFiles) {
  assertRelative(file);
  if (isForbidden(file)) throw new Error(`forbidden file in submit scope: ${file}`);
}

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'arkweb-submit-index-'));
const indexFile = path.join(tmpDir, 'index');

try {
  const baseCommit = git(repo, ['rev-parse', '--verify', args.baseRef]);
  const baseTree = git(repo, ['rev-parse', `${baseCommit}^{tree}`]);
  const rawMessage = fs.readFileSync(args.messageFile, 'utf8').trimEnd();
  const signoffLine = `Signed-off-by: ${signoffName} <${signoffEmail}>`;
  const finalMessage = rawMessage.includes(signoffLine)
    ? `${rawMessage}\n`
    : `${rawMessage}\n\n${signoffLine}\n`;
  const finalMessageFile = path.join(tmpDir, 'commit-message.txt');
  fs.writeFileSync(finalMessageFile, finalMessage, 'utf8');

  gitWithIndex(repo, indexFile, ['read-tree', baseCommit]);

  const changed = [];
  for (const file of submitFiles) {
    const absPath = path.join(repo, file);
    if (fs.existsSync(absPath)) {
      const objectId = git(repo, ['hash-object', '-w', '--path', file, absPath]);
      gitWithIndex(repo, indexFile, ['update-index', '--add', '--cacheinfo', `${fileMode(absPath)},${objectId},${file}`]);
      changed.push(file);
    } else {
      gitWithIndex(repo, indexFile, ['update-index', '--force-remove', '--', file]);
      changed.push(file);
    }
  }

  const diffNameStatus = gitWithIndex(repo, indexFile, ['diff', '--cached', '--name-status', baseCommit, '--', ...submitFiles])
    .split('\n')
    .filter(Boolean);
  if (diffNameStatus.length === 0) {
    throw new Error('submit scope produced no diff against manifest/upstream baseline');
  }

  const tree = gitWithIndex(repo, indexFile, ['write-tree']);
  if (tree === baseTree) throw new Error('tree is unchanged against manifest/upstream baseline');

  const commit = execFileSync('git', ['-C', repo, 'commit-tree', tree, '-p', baseCommit, '-F', finalMessageFile], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
  git(repo, ['branch', '-f', args.branch, commit]);

  console.log(JSON.stringify({
    ok: true,
    base_ref: args.baseRef,
    base_commit: baseCommit,
    branch: args.branch,
    commit,
    submit_files: submitFiles,
    diff_name_status: diffNameStatus,
    worktree_untouched: true,
  }, null, 2));
} finally {
  fs.rmSync(tmpDir, { recursive: true, force: true });
}
