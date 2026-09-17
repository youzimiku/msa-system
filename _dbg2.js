// 打印 _compiled.js 指定行
const fs = require('fs');
const lines = fs.readFileSync('C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA系统/_compiled.js', 'utf-8').split('\n');
console.log('total lines:', lines.length);
for (let i = 13195; i <= 13215; i++) {
  if (i < lines.length) console.log((i + 1) + ': ' + lines[i].slice(0, 220));
}
