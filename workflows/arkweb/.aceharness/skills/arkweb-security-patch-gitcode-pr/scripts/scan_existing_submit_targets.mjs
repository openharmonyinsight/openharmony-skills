#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

function usage() {
  console.error('usage: node scan_existing_submit_targets.mjs --run-dir <.ace-outputs/runId> --repo <git-repo> --upstream-repo <owner/project> --fork-remote <remote> [--fork-owner <owner>] [--date <YYYYMMDD>]');
  process.exit(2);
}

function parseArgs(argv) {
  const out = { runDir: '', repo: '', upstreamRepo: '', forkRemote: '', forkOwner: '', date: '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--run-dir') out.runDir = argv[++i] || '';
    else if (a === '--repo') out.repo = argv[++i] || '';
    else if (a === '--upstream-repo') out.upstreamRepo = argv[++i] || '';
    else if (a === '--fork-remote') out.forkRemote = argv[++i] || '';
    else if (a === '--fork-owner') out.forkOwner = argv[++i] || '';
    else if (a === '--date') out.date = argv[++i] || '';
    else usage();
  }
  if (!out.runDir || !out.repo || !out.upstreamRepo || !out.forkRemote) usage();
  return out;
}

function run(cmd, args, opts = {}) {
  try {
    return {
      ok: true,
      stdout: execFileSync(cmd, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], ...opts }).trim(),
      stderr: '',
    };
  } catch (e) {
    return {
      ok: false,
      stdout: String(e.stdout || '').trim(),
      stderr: String(e.stderr || e.message || '').trim(),
    };
  }
}

function inferForkOwner(repo, remote) {
  const url = run('git', ['-C', repo, 'remote', 'get-url', remote]);
  if (!url.ok) return '';
  const m = url.stdout.match(/gitcode\.com[/:]([^/]+)\//);
  return m ? m[1] : '';
}

function loadReady(runDir) {
  const p = path.join(runDir, 'batch_status.json');
  const obj = JSON.parse(fs.readFileSync(p, 'utf8'));
  return (obj.ready_for_next || []).map(String).sort((a, b) => Number(a) - Number(b));
}

function listRemoteBranches(repo, remote) {
  const res = run('git', ['-C', repo, 'ls-remote', '--heads', remote, 'arkweb-security-*']);
  if (!res.ok) return { ok: false, error: res.stderr || res.stdout, branches: new Map() };
  const branches = new Map();
  for (const line of res.stdout.split('\n').filter(Boolean)) {
    const [sha, ref] = line.split(/\s+/);
    const name = ref.replace(/^refs\/heads\//, '');
    branches.set(name, sha);
  }
  return { ok: true, error: '', branches };
}

function listOpenPrs(upstreamRepo, forkOwner) {
  const args = ['pr', 'list', '--repo', upstreamRepo, '--state', 'open', '--limit', '500', '--json'];
  if (forkOwner) args.push('--author', forkOwner);
  const res = run('oh-gc', args);
  if (!res.ok) return { ok: false, error: res.stderr || res.stdout, prs: [] };
  try {
    return { ok: true, error: '', prs: JSON.parse(res.stdout || '[]') };
  } catch (e) {
    return { ok: false, error: `failed to parse oh-gc pr list JSON: ${e.message}`, prs: [] };
  }
}

function prHead(pr) {
  const head = pr.head || pr.source_branch || pr.source || {};
  if (typeof head === 'string') return head;
  return head.label || head.ref || head.name || head.branch || '';
}

const args = parseArgs(process.argv.slice(2));
const runDir = fs.realpathSync(args.runDir);
const repo = fs.realpathSync(args.repo);
const forkOwner = args.forkOwner || inferForkOwner(repo, args.forkRemote);
const date = args.date || new Date().toISOString().slice(0, 10).replaceAll('-', '');
const ready = loadReady(runDir);
const remote = listRemoteBranches(repo, args.forkRemote);
const prs = listOpenPrs(args.upstreamRepo, forkOwner);

const rows = ready.map((issueId) => {
  const prefix = `arkweb-security-${issueId}-`;
  const preferredBranch = `arkweb-security-${issueId}-${date}`;
  const matchingBranches = remote.ok
    ? [...remote.branches.entries()].filter(([name]) => name.startsWith(prefix)).map(([name, sha]) => ({ name, sha }))
    : [];
  const matchingPrs = prs.ok
    ? prs.prs.filter((pr) => prHead(pr).includes(`${forkOwner}:${prefix}`) || prHead(pr).startsWith(prefix) || JSON.stringify(pr).includes(prefix))
    : [];
  const openPr = matchingPrs[0] || null;
  return {
    issue_id: issueId,
    preferred_branch: preferredBranch,
    branch_exists: remote.ok && remote.branches.has(preferredBranch),
    matching_branches: matchingBranches,
    open_pr: openPr ? {
      number: openPr.number || openPr.id || '',
      url: openPr.html_url || openPr.web_url || openPr.url || '',
      head: prHead(openPr),
    } : null,
    action: openPr ? 'reuse_open_pr' : (matchingBranches.length ? 'inspect_existing_branch_before_push' : 'create_commit_and_push'),
  };
});

console.log(JSON.stringify({
  ok: remote.ok && prs.ok,
  run_dir: runDir,
  repo,
  upstream_repo: args.upstreamRepo,
  fork_remote: args.forkRemote,
  fork_owner: forkOwner,
  date,
  remote_scan_error: remote.error,
  pr_scan_error: prs.error,
  ready_count: ready.length,
  results: rows,
}, null, 2));
