// 用项目自带 Babel standalone 编译 index.html 的 text/babel 脚本，捕获语法错误
const fs = require('fs');
const Babel = require('./lib/babel.min.js');
const html = fs.readFileSync('index.html', 'utf-8');
const m = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
if(!m){ console.log('NO SCRIPT'); process.exit(1); }
try{
  const out = Babel.transform(m[1], { presets:['react'], filename:'app.jsx' });
  console.log('BABEL OK, compiled len', out.code.length);
}catch(e){
  console.log('BABEL ERROR:');
  console.log(e.message);
  process.exit(2);
}
