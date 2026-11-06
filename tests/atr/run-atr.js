// 用法: node tests/atr/run-atr.js [--split dev|holdout|all] [--list]
// 用 index.html 里的体检规则跑 ATR Skill-Security Benchmark（MIT）。样本只当文本读，绝不执行。
// 判恶意口径：安全风险里出现「高危」或「中危」项（不含仅「外部网址」提示）。
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', '..');
const html = fs.readFileSync(process.env.HTML || path.join(ROOT, 'index.html'), 'utf8');
const m = html.match(/<script>\s*\(function \(\) \{([\s\S]*?)\n      \}\)\(\);\s*<\/script>/);
const el = () => new Proxy(function () {}, { get: (t, k) => k === Symbol.toPrimitive ? () => '' : k === 'length' ? 0 : el(), set: () => true, apply: () => el() });
global.document = { getElementById: () => el(), querySelectorAll: () => [], querySelector: () => el(), addEventListener() {}, createElement: () => el() };
global.window = global; global.navigator = {}; global.localStorage = { getItem: () => null, setItem() {} };
new Function(m[1].replace('"use strict";', '') + '\nglobal.__audit=audit;')();
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const split = arg('--split') || 'all', list = process.argv.includes('--list');
const rows = fs.readFileSync(path.join(__dirname, 'atr-skill-benchmark.jsonl'), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
// 固定切分：按 id 排序后，同一 label 内奇偶交替 → dev / holdout（规则只对照 dev 调）
const byLabel = {}; rows.forEach(r => (byLabel[r.label] = byLabel[r.label] || []).push(r));
Object.values(byLabel).forEach(a => a.sort((x, y) => x.id < y.id ? -1 : 1).forEach((r, i) => r.split = i % 2 ? 'holdout' : 'dev'));
const S = rows.filter(r => split === 'all' || r.split === split);
let tp = 0, fp = 0, P = 0, N = 0; const missed = [], fps = [];
for (const r of S) {
  const res = __audit(r.text, '');
  const hits = res.sec.filter(it => it.sev === '高危' || it.sev === '中危').map(it => it.title);
  const flag = hits.length > 0, mal = r.label === 'malicious';
  if (mal) { P++; if (flag) tp++; else missed.push(r.attack_type); }
  else { N++; if (flag) { fp++; fps.push(r.id + ' ← ' + hits.join('|')); } }
  if (list && mal) console.log(flag ? '✓' : '✗', r.split, r.attack_type, hits.join('|'));
}
console.log(`[${split}] 召回 ${tp}/${P} = ${(100 * tp / P).toFixed(1)}%   误报 ${fp}/${N} = ${(100 * fp / N).toFixed(2)}%`);
if (missed.length) console.log('漏报:', missed.join(', '));
if (fps.length) console.log('误报样本:\n  ' + fps.join('\n  '));
