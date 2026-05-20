#!/usr/bin/env node
/**
 * Aceharness Chat Card JSON 校验脚本
 *
 * 用法:
 *   echo '{"header":{"title":"test"},"blocks":[]}' | node validate-card.mjs
 *   node validate-card.mjs card.json
 *   node validate-card.mjs --generate info    # 生成示例
 */

import { readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load full Material Icons list for icon validation
const MATERIAL_ICONS = (() => {
  try {
    const icons = JSON.parse(readFileSync(resolve(__dirname, 'material-icons.json'), 'utf-8'));
    return new Set(icons);
  } catch {
    return null; // Skip icon validation if file missing
  }
})();

let iconWarnings = 0;

function validateIcon(name, path) {
  if (!name || !MATERIAL_ICONS) return;
  const clean = name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
  if (!MATERIAL_ICONS.has(clean)) {
    console.warn(`  ⚠ ${path}: "${name}" is not a valid Material Icon`);
    iconWarnings++;
  }
}

const VALID_BLOCK_TYPES = ['info', 'badges', 'text', 'code', 'progress', 'steps', 'tabs', 'collapse', 'list', 'status', 'actions', 'divider'];
const VALID_COLORS = ['blue', 'green', 'red', 'yellow', 'purple', 'orange', 'gray', 'cyan', 'pink'];

function validateBlock(block, path = 'block') {
  const errors = [];
  if (!block || typeof block !== 'object') {
    errors.push(`${path}: must be an object`);
    return errors;
  }
  if (!block.type || !VALID_BLOCK_TYPES.includes(block.type)) {
    errors.push(`${path}.type: must be one of ${VALID_BLOCK_TYPES.join(', ')}, got "${block.type}"`);
    return errors;
  }

  switch (block.type) {
    case 'info':
      if (!Array.isArray(block.rows)) errors.push(`${path}.rows: must be an array`);
      else block.rows.forEach((r, i) => {
        if (!r.label) errors.push(`${path}.rows[${i}].label: required`);
        if (r.value === undefined) errors.push(`${path}.rows[${i}].value: required`);
        if (r.icon) validateIcon(r.icon, `${path}.rows[${i}].icon`);
      });
      break;
    case 'badges':
      if (!Array.isArray(block.items)) errors.push(`${path}.items: must be an array`);
      else block.items.forEach((b, i) => {
        if (!b.text) errors.push(`${path}.items[${i}].text: required`);
      });
      break;
    case 'text':
      if (typeof block.content !== 'string') errors.push(`${path}.content: must be a string`);
      break;
    case 'code':
      if (typeof block.code !== 'string') errors.push(`${path}.code: must be a string`);
      break;
    case 'progress':
      if (typeof block.value !== 'number') errors.push(`${path}.value: must be a number`);
      break;
    case 'steps':
      if (typeof block.current !== 'number') errors.push(`${path}.current: must be a number`);
      if (typeof block.total !== 'number') errors.push(`${path}.total: must be a number`);
      break;
    case 'tabs':
      if (!Array.isArray(block.tabs)) errors.push(`${path}.tabs: must be an array`);
      else block.tabs.forEach((t, i) => {
        if (!t.key) errors.push(`${path}.tabs[${i}].key: required`);
        if (!t.label) errors.push(`${path}.tabs[${i}].label: required`);
        if (!Array.isArray(t.blocks)) errors.push(`${path}.tabs[${i}].blocks: must be an array`);
        else t.blocks.forEach((b, j) => errors.push(...validateBlock(b, `${path}.tabs[${i}].blocks[${j}]`)));
      });
      break;
    case 'collapse':
      if (typeof block.title !== 'string') errors.push(`${path}.title: must be a string`);
      if (block.icon) validateIcon(block.icon, `${path}.icon`);
      if (!Array.isArray(block.blocks)) errors.push(`${path}.blocks: must be an array`);
      else block.blocks.forEach((b, i) => errors.push(...validateBlock(b, `${path}.blocks[${i}]`)));
      break;
    case 'list':
      if (!Array.isArray(block.items)) errors.push(`${path}.items: must be an array`);
      else block.items.forEach((item, i) => {
        if (typeof item.text !== 'string') errors.push(`${path}.items[${i}].text: must be a string`);
        if (item.icon) validateIcon(item.icon, `${path}.items[${i}].icon`);
      });
      break;
    case 'status':
      if (typeof block.state !== 'string') errors.push(`${path}.state: must be a string`);
      break;
    case 'actions':
      if (!Array.isArray(block.items)) errors.push(`${path}.items: must be an array`);
      else block.items.forEach((a, i) => {
        if (!a.label) errors.push(`${path}.items[${i}].label: required`);
        if (!a.prompt) errors.push(`${path}.items[${i}].prompt: required`);
        if (a.icon) validateIcon(a.icon, `${path}.items[${i}].icon`);
      });
      break;
    case 'divider':
      break;
  }
  return errors;
}

function validateCard(card) {
  const errors = [];
  if (!card || typeof card !== 'object') {
    errors.push('card: must be an object');
    return errors;
  }
  if (!Array.isArray(card.blocks)) {
    errors.push('card.blocks: required and must be an array');
    return errors;
  }
  if (card.header) {
    if (typeof card.header !== 'object') errors.push('card.header: must be an object');
    else if (!card.header.title) errors.push('card.header.title: required');
    if (card.header?.icon) validateIcon(card.header.icon, 'header.icon');
  }
  card.blocks.forEach((b, i) => errors.push(...validateBlock(b, `blocks[${i}]`)));
  if (card.actions) {
    if (!Array.isArray(card.actions)) errors.push('card.actions: must be an array');
    else card.actions.forEach((a, i) => {
      if (!a.label) errors.push(`actions[${i}].label: required`);
      if (!a.prompt) errors.push(`actions[${i}].prompt: required`);
      if (a.icon) validateIcon(a.icon, `actions[${i}].icon`);
    });
  }
  return errors;
}

// --- Generate examples ---
const EXAMPLES = {
  info: { header: { icon: 'info', title: '信息卡片' }, blocks: [{ type: 'info', rows: [{ label: '名称', value: '示例', icon: 'badge' }, { label: '状态', value: '正常' }] }] },
  badges: { header: { icon: 'label', title: '标签卡片' }, blocks: [{ type: 'badges', items: [{ text: 'TypeScript', color: 'blue' }, { text: 'React', color: 'cyan' }] }] },
  progress: { header: { icon: 'trending_up', title: '进度卡片' }, blocks: [{ type: 'progress', value: 75, max: 100, label: '75% 完成' }] },
  status: { header: { icon: 'play_circle', title: '状态卡片', gradient: 'from-green-500 to-emerald-500' }, blocks: [{ type: 'status', state: '运行中', color: 'green', animated: true, rows: [{ label: '阶段', value: '测试' }] }] },
  full: {
    header: { icon: 'dashboard', title: '完整示例', subtitle: '包含多种 block 类型', gradient: 'from-purple-500 to-pink-500', badges: [{ text: 'demo', color: 'purple' }] },
    blocks: [
      { type: 'info', rows: [{ label: '类型', value: '演示', icon: 'category' }] },
      { type: 'badges', items: [{ text: 'tag1', color: 'blue' }, { text: 'tag2', color: 'green' }] },
      { type: 'text', content: '这是一段说明文字', maxLines: 3 },
      { type: 'divider' },
      { type: 'progress', value: 60, max: 100, label: '60%' },
      { type: 'collapse', title: '详细信息', blocks: [{ type: 'code', code: '{"key": "value"}', lang: 'json', copyable: true }] },
    ],
    actions: [{ label: '下一步', prompt: '继续操作', icon: 'arrow_forward' }],
  },
};

// --- Main ---
const args = process.argv.slice(2);

if (args[0] === '--generate') {
  const type = args[1] || 'full';
  const example = EXAMPLES[type];
  if (!example) {
    console.error(`Unknown example type: ${type}. Available: ${Object.keys(EXAMPLES).join(', ')}`);
    process.exit(1);
  }
  console.log(JSON.stringify(example, null, 2));
  process.exit(0);
}

let input;
if (args[0] && args[0] !== '-') {
  input = readFileSync(args[0], 'utf-8');
} else {
  input = readFileSync('/dev/stdin', 'utf-8');
}

// Support multiple cards separated by ---
const cards = input.split(/^---$/m).map(s => s.trim()).filter(Boolean);
let hasError = false;

for (let ci = 0; ci < cards.length; ci++) {
  const prefix = cards.length > 1 ? `Card ${ci + 1}: ` : '';
  try {
    const card = JSON.parse(cards[ci]);
    const errors = validateCard(card);
    if (errors.length > 0) {
      hasError = true;
      console.error(`${prefix}INVALID`);
      errors.forEach(e => console.error(`  - ${e}`));
    } else {
      console.log(`${prefix}VALID ✓`);
    }
  } catch (e) {
    hasError = true;
    console.error(`${prefix}JSON parse error: ${e.message}`);
  }
}

if (iconWarnings > 0) {
  console.warn(`\n⚠ ${iconWarnings} icon warning(s) — invalid Material Icon names detected`);
}

process.exit(hasError ? 1 : 0);
