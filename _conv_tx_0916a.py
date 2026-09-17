# -*- coding: utf-8 -*-
import io, json, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

src = r'C:\Users\youzi\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38440120376335362\agents\m_0cwEzAKMzjT\system\tool-results\bash_8B1F428BF31F.txt'
out = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_transcript_0916_0921.txt'

raw = io.open(src, encoding='utf-8').read()
# 截取 JSON 部分（从第一个 { 到最后一个 }）
start = raw.find('{')
end = raw.rfind('}')
data = json.loads(raw[start:end+1])

paras = data['data']['minutes']['paragraphs']
lines = []
for p in paras:
    sp = p.get('speaker', {})
    who = sp.get('user_name', '未知')
    t = p.get('start_time', '')
    texts = []
    for s in p.get('sentences', []):
        for w in s.get('words', []):
            texts.append(w.get('text', ''))
    line = '[%s] %s: %s' % (t, who, ''.join(texts))
    lines.append(line)

io.open(out, 'w', encoding='utf-8').write('\n'.join(lines))
print('段落数:', len(paras), '输出:', out)
