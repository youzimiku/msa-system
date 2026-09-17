const fs = require('fs');
const raw = fs.readFileSync('_transcript.json', 'utf8').replace(/^\uFEFF/, '');
const j = JSON.parse(raw);
const paras = j.data.minutes.paragraphs;
console.log('total paragraphs:', paras.length);
const lines = paras.map(p => {
  const txt = p.sentences.map(s => (s.words || []).map(w => w.text).join('')).join('');
  return '[' + p.start_time + '] ' + p.speaker.user_name + ': ' + txt;
});
fs.writeFileSync('_transcript.txt', lines.join('\n'), 'utf8');
console.log('written _transcript.txt, lines=', lines.length);
