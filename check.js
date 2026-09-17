const fs = require('fs');
const path = require('path');
const Babel = require('./lib/babel.min.js');
const html = fs.readFileSync('index.html','utf8');
// extract text/babel blocks
const re = /<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/g;
let m, i=0, errs=0;
while((m=re.exec(html))){
  i++;
  const code = m[1];
  try{
    Babel.transform(code, {presets:['react'], filename:'block'+i+'.js'});
    console.log('block'+i+': OK ('+code.length+' chars)');
  }catch(e){
    errs++;
    console.log('block'+i+': ERROR -> '+e.message.slice(0,300));
    console.log('  snippet: '+code.slice(Math.max(0,e.pos-80),e.pos+80).replace(/\n/g,'\\n'));
  }
}
console.log('total blocks: '+i+', errors: '+errs);
process.exit(errs?1:0);
