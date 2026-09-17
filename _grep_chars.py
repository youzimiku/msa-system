# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat'
files = [
    base + r'\notes\7683370846434315511\unified_transcript.md',
    base + r'\MSA系统\_tr_0909.txt',
    base + r'\MSA系统\_tr_0909_p1.json',
    base + r'\MSA系统\_m1.json',
    base + r'\MSA系统\_m2.json',
    base + r'\MSA系统\_tr_m1.txt',
    base + r'\MSA系统\_tr_m2.txt',
    base + r'\MSA系统\_minutes1.txt',
    base + r'\MSA系统\_minutes2.txt',
    base + r'\_kappa_report.txt',
]
kws = ['SC', 'CC', '特殊特性', '关键特性', '安全特性', '特性类型', '特性分级', '特性分类', 'SC2', '特殊', '特性']
for f in files:
    if not os.path.exists(f):
        print('MISS', f)
        continue
    txt = open(f, encoding='utf-8', errors='ignore').read()
    hits = {}
    for kw in kws:
        c = txt.count(kw)
        if c:
            hits[kw] = c
    print('====', os.path.basename(f), '总长', len(txt))
    if hits:
        for kw, c in hits.items():
            print('  ', kw, 'x', c)
    else:
        print('   无任何命中')
    # 打印命中行的上下文（仅特性/特殊）
    for m in re.finditer(r'特性|特殊', txt):
        a = max(0, m.start()-40); b = min(len(txt), m.end()+60)
        seg = txt[a:b].replace('\n', ' ')
        print('   >>', seg)
