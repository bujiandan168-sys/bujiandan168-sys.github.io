// 用法: node tests/run.js [--dump]
// 抽出 index.html 里的体检脚本，在假 DOM 中执行，拿到 audit()；
// 跑 tests/samples/*.md（外部可再分发样本）+ skills/*/SKILL.md（自家）+ tests/local/*.md（本地、不推送），
// 对照 tests/expected.json 计算误报/漏报与通过率。
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(process.env.HTML || path.join(ROOT, 'index.html'), 'utf8');
const m = html.match(/<script>\s*\(function \(\) \{([\s\S]*?)\n      \}\)\(\);\s*<\/script>/);
if (!m) { console.log('找不到体检脚本'); process.exit(1); }
const el = () => new Proxy(function () {}, { get: (t, k) => k === Symbol.toPrimitive ? () => '' : k === 'length' ? 0 : el(), set: () => true, apply: () => el() });
global.document = { getElementById: () => el(), querySelectorAll: () => [], querySelector: () => el(), addEventListener() {}, createElement: () => el() };
global.window = global; global.navigator = {}; global.localStorage = { getItem: () => null, setItem() {} };
try { new Function(m[1].replace('"use strict";', '') + '\nglobal.__audit=audit;')(); }
catch (e) { console.log('SYNTAX/LOAD ERROR:', e.message); process.exit(1); }

const cases = [];
const add = (id, file, folder) => cases.push({ id, raw: fs.readFileSync(file, 'utf8'), folder });
for (const f of fs.readdirSync(path.join(__dirname, 'samples')).sort())
  add('samples/' + f, path.join(__dirname, 'samples', f), f.replace(/^.*__/, '').replace(/\.md$/, ''));
for (const f of fs.readdirSync(path.join(__dirname, 'synthetic')).sort())
  add('synthetic/' + f, path.join(__dirname, 'synthetic', f), f.replace(/^.*__/, '').replace(/\.md$/, ''));
for (const d of fs.readdirSync(path.join(ROOT, 'skills')).sort()) {
  const p = path.join(ROOT, 'skills', d, 'SKILL.md');
  if (fs.existsSync(p)) add('skills/' + d, p, d);
}
const LOCAL = path.join(__dirname, 'local');
if (fs.existsSync(LOCAL)) for (const f of fs.readdirSync(LOCAL).sort())
  add('local/' + f, path.join(LOCAL, f), f.replace(/^.*__/, '').replace(/\.md$/, ''));

const expected = JSON.parse(fs.readFileSync(path.join(__dirname, 'expected.json'), 'utf8'));
const key = t => t.replace(/\s*\d+\s*个$/, '').replace(/：.*$/, '');
let pass = 0, n = 0, fp = 0, fn = 0, unl = 0;
const dump = process.argv.includes('--dump');
for (const c of cases) {
  const r = __audit(c.raw, c.folder);
  const got = [...new Set(r.spec.concat(r.sec).map(it => key(it.title)))].sort();
  const exp = expected[c.id];
  if (dump) console.log(c.id, r.score, JSON.stringify(got));
  if (!exp) { unl++; continue; }
  n++;
  const want = [...new Set(exp.findings)].sort();
  const extra = got.filter(x => !want.includes(x)), miss = want.filter(x => !got.includes(x));
  fp += extra.length; fn += miss.length;
  if (!extra.length && !miss.length) pass++;
  else console.log('✗', c.id, extra.length ? '误报:' + extra.join('|') : '', miss.length ? '漏报:' + miss.join('|') : '');
}
console.log(`\n样本 ${cases.length}（已标注 ${n}，未标注 ${unl}）  完全一致 ${pass}/${n} = ${n ? (100 * pass / n).toFixed(1) : 0}%  误报 ${fp}  漏报 ${fn}`);
process.exit(fp + fn ? 1 : 0);
