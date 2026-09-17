# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
for m in ['m1','m2','m3']:
    p = base + '\\_transcript_' + m + '.json'
    raw = open(p, encoding='utf-8-sig').read()
    try:
        data = json.loads(raw)
    except Exception as e:
        print(m, 'JSON ERR', e, 'len', len(raw)); continue
    paras = data.get('data', {}).get('minutes', {}).get('paragraphs', [])
    print(m, 'paragraphs=', len(paras))
    out = base + '\\_transcript_' + m + '.txt'
    with open(out, 'w', encoding='utf-8') as f:
        for p in paras:
            sp = p.get('speaker', {}).get('user_name', '?')
            st = p.get('start_time', ''); et = p.get('end_time', '')
            txt = ' '.join(s.get('text', '') for s in p.get('sentences', []))
            f.write('[%s-%s] %s: %s\n' % (st, et, sp, txt))
    print('  ->', out)
