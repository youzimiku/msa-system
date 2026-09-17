const fs = require('fs');
const path = require('path');
const Babel = require(path.join(__dirname, 'lib', 'babel.min.js'));
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
const m = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
const out = Babel.transform(m[1], { presets: ['react'], filename: 'app.jsx' }).code.split('\n');
for (let i = 2680; i <= 2694; i++) console.log((i + 1) + ': ' + String(out[i] || '').slice(0, 260));
