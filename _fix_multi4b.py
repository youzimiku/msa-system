# -*- coding: utf-8 -*-
"""修复 multi4 插入缺逗号问题 v2"""
import io
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

fixed = []
for rid in ['GRR-2026-004', 'STB-2026-003', 'CG-2026-004']:
    i = s.find("{id:'" + rid + "'")
    assert i > 0, rid
    j = s.rfind('}', 0, i)
    seg = s[j+1:i]
    if ',' not in seg and seg.strip() == '':
        s = s[:j+1] + ',' + s[j+1:]
        fixed.append(rid)
    else:
        print(rid, 'seg:', repr(seg))

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('修复:', fixed)
