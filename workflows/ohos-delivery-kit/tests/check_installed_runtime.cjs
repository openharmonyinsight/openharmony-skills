// Maintainer check: local installer code only; all writes stay in temporary dirs.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');

const workflow = path.resolve(__dirname, '..');
const installer = path.resolve(process.argv[2]);
assert.equal(require(path.join(installer, 'package.json')).name, 'oh-skillhub');
const {loadNeutralPlugin} = require(path.join(installer, 'src/plugin-builder.js'));
const {planPluginInstall, applyPluginInstallPlan} = require(path.join(installer, 'src/plugin-installer.js'));
const {installPluginV2} = require(path.join(installer, 'src/plugin-v2-installer.js'));
const plugin = loadNeutralPlugin(path.resolve(workflow, '../..'), 'ohos-delivery-kit');
const portable = value => value.split(path.sep).join('/');

function files(root) {
  return fs.readdirSync(root, {withFileTypes: true}).flatMap(entry => {
    const file = path.join(root, entry.name);
    return entry.isDirectory() ? files(file) : entry.isFile() ? [file] : [];
  }).sort();
}

function checkReference(root, reference) {
  const clean = reference.split('#')[0];
  const dynamic = clean.search(/[<*]/);
  const literal = dynamic < 0 ? clean : clean.slice(0, clean.lastIndexOf('/', dynamic) + 1);
  const target = path.resolve(root, literal);
  const relative = path.relative(root, target);
  assert.ok(relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative));
  assert.ok(fs.existsSync(target), `missing installed reference: ${target}`);
}

function verify(payload, businessRoot) {
  let assets = 0;
  let references = 0;
  for (const source of plugin.skillFiles) {
    const name = path.basename(path.dirname(source));
    const installed = path.join(payload.payloadRoot, 'skills', name);
    const text = fs.readFileSync(path.join(installed, 'SKILL.md'), 'utf8');
    assert.doesNotMatch(text, /\{\{(?:PLUGIN_ROOT|ASSET_ROOT|EXECUTABLE_ROOT)\}\}/);
    const sourceRoot = path.dirname(source);
    const inventory = root => files(root).map(file => path.relative(root, file));
    assert.deepEqual(inventory(installed), inventory(sourceRoot), `${name}: auxiliary file inventory differs`);
    for (const file of files(sourceRoot).filter(file => file !== source)) {
      const relative = path.relative(sourceRoot, file);
      assert.deepEqual(fs.readFileSync(path.join(installed, relative)), fs.readFileSync(file), `${name}/${relative}`);
      assets++;
    }
    const original = fs.readFileSync(source, 'utf8');
    const paths = [...original.matchAll(/`((?:templates|contracts|profiles|rules|adapters|runtime\/assets|runtime\/executables)\/[^`\n]+)`/g)].map(match => match[1]);
    paths.push(...[...original.matchAll(/\bpython3\s+"?(runtime\/executables\/[^\s`"]+)/g)].map(match => match[1]));
    for (let reference of paths) {
      const executable = reference.startsWith('runtime/executables/');
      const root = executable ? payload.executableRoot : payload.assetRoot;
      reference = reference.replace(/^runtime\/(?:assets|executables)\//, '');
      assert.ok(text.includes(portable(root) + '/' + reference), `${name}: unresolved runtime reference ${reference}`);
      checkReference(root, reference);
      references++;
    }
    if (name === 'odk-validate') {
      const command = text.match(/Run `([^`]+)` for Draft/)[1].replace('<change-dir>', '--help');
      const result = spawnSync(command, {cwd: businessRoot, shell: true, encoding: 'utf8'});
      assert.equal(result.status, 0, result.stderr);
      assert.match(result.stdout, /usage:/);
    }
  }
  assert.ok(assets > 0 && references > 0, 'installation checks did not inspect assets and references');
  console.log(`PASS ${payload.target.agent}: ${plugin.skillFiles.length} skills, ${assets} auxiliary files, ${references} runtime references`);
}

const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'odk installed contract '));
try {
  for (const layout of ['v1', 'v2']) {
    const cwd = path.join(temporary, layout);
    fs.mkdirSync(cwd);
    const targets = ['claude', 'codex', 'opencode'].map(agent => ({agent, scope: 'project', dir: path.join(cwd, '.' + agent, 'skills')}));
    const options = {cwd, homeDir: path.join(cwd, 'home'), skipHostRegistration: true};
    const installed = layout === 'v1'
      ? applyPluginInstallPlan(planPluginInstall(plugin, targets), options)
      : installPluginV2(plugin, targets, options).targets;
    assert.equal(installed.length, targets.length);
    for (const result of installed) verify(result.payload, cwd);
  }
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
