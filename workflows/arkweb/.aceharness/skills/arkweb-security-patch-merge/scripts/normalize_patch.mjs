#!/usr/bin/env node
import { createHash } from 'crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'fs';
import { basename, dirname, resolve } from 'path';

function usage() {
  console.error('Usage: node normalize_patch.mjs <patch-file> [--out <normalized-file>]');
  process.exit(2);
}

const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith('-')) usage();

const inputPath = resolve(args[0]);
let outPath = null;
for (let i = 1; i < args.length; i += 1) {
  if (args[i] === '--out') {
    outPath = resolve(args[i + 1] || '');
    i += 1;
  } else {
    usage();
  }
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

if (!outPath) {
  outPath = resolve(process.cwd(), `${basename(inputPath)}.normalized.patch`);
}

const normalizedText = normalized.toString('utf8');
const valid = format !== 'invalid';
if (valid) {
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, normalized);
}

const result = {
  original_path: inputPath,
  normalized_path: valid ? outPath : null,
  format,
  valid,
  validation_signals: found,
  original_sha256: sha256(original),
  normalized_sha256: valid ? sha256(normalized) : null,
  diff_paths: valid ? diffPaths(normalizedText) : [],
};

console.log(JSON.stringify(result, null, 2));
process.exit(valid ? 0 : 1);
