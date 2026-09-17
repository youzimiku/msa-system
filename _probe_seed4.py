# -*- coding: utf-8 -*-
"""统计 buildSeed 中六类台账 seed 记录数（const 定义）"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function buildSeed')
seg = s[i:i+120000]

for name in ['grr', 'kappa', 'linear', 'stability', 'cgcgk', 'resolution', 'calibrations', 'instGroups']:
    # 找 `const grr = [` 或 `let grr = [` 或 `grr=[`
    for pat in [r'const\s+' + name + r'\s*=\s*\[', r'let\s+' + name + r'\s*=\s*\[', r'\b' + name + r'\s*=\s*\[']:
        m = re.search(pat, seg)
        if m:
            start = m.end()
            depth = 0
            for j in range(start, min(start+200000, len(seg))):
                c = seg[j]
                if c == '[': depth += 1
                elif c == ']':
                    depth -= 1
                    if depth == 0:
                        block = seg[m.start():j+1]
                        items = block.count('{id:') + block.count('{ id:') + block.count('id:')
                        print(name, '->', items, '条 (', pat, ')')
                        break
            break
    else:
        print(name, '-> 未找到 const 定义')
