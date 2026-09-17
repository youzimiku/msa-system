# -*- coding: utf-8 -*-
"""查看 seed 六类记录内容（用于 ensureDemoData 复用字段）"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function buildSeed')
seg = s[i:i+120000]

for name, pat in [('grr', r'const\s+grr\s*=\s*\['), ('kappa', r'const\s+kappa\s*=\s*\['),
                  ('linear', r'const\s+linear\s*=\s*\['), ('stability', r'\bstability\s*=\s*\['),
                  ('cgcgk', r'\bcgcgk\s*=\s*\['), ('resolution', r'\bresolution\s*=\s*\[')]:
    m = re.search(pat, seg)
    if not m:
        print(name, 'NOT FOUND')
        continue
    start = m.end(); depth = 0
    for j in range(start, min(start+300000, len(seg))):
        c = seg[j]
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                block = seg[m.start():j+1]
                # 拆出每条记录（按 '{id:' 切）
                items = re.split(r'(?=\{id:)', block)
                print('\n======== %s: %d 条 ========' % (name, len(items)-1))
                for it in items[1:4]:
                    print(it.strip()[:600])
                break
