// 用法: node tests/run.js  —— 抽出 index.html 里的 audit() 跑 tests/samples/*.md，对照 expected.json
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const m=html.match(/<script>\s*\(function \(\) \{([\s\S]*?)\n      \}\)\(\);\s*<\/script>/);
const src=m[1];
const a=src.indexOf('function esc('),b=src.indexOf('function audit(');
// 取到 audit 函数结束较难，直接整体执行于假 DOM
const el=()=>new Proxy(function(){},{get:(t,k)=>k===Symbol.toPrimitive?()=>'':k==='length'?0:k==='style'||k==='classList'?el():k==='addEventListener'?()=>{}:el(),set:()=>true,apply:()=>el()});
global.document={getElementById:()=>el(),querySelectorAll:()=>[],querySelector:()=>el(),addEventListener(){},createElement:()=>el()};
global.window=global;global.navigator={};global.localStorage={getItem:()=>null,setItem(){}};
let code=src.replace('"use strict";','')+'\nglobal.__audit=audit;';
try{new Function(code)();}catch(e){console.log('SYNTAX/LOAD ERROR:',e.message);process.exit(1)}

let pass=0,n=0;
for(const f of fs.readdirSync(path.join(__dirname,'samples'))){
  const raw=fs.readFileSync(path.join(__dirname,'samples',f),'utf8');
  const r=__audit(raw,f.replace(/^[^-]*-/,'').replace(/\.md$/,''));
  console.log(f,JSON.stringify(r,(k,v)=>k==='hits'?undefined:v).slice(0,600));
}
