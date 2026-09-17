# -*- coding: utf-8 -*-
"""看 buildSeed 中 grr/kappa 完整记录（raw 结构）+ 检查 recCalc/calcGRR 输入格式"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function buildSeed')
seg = s[i:i+120000]

for name, pat in [('grr', r'const\s+grr\s*=\s*\['), ('kappa', r'const\s+kappa\s*=\s*\[')]:
    m = re.search(pat, seg)
    start = m.end(); depth = 0
    for j in range(start, min(start+300000, len(seg))):
        c = seg[j]
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                print('\n======== %s 数组（%d 字符）========' % (name, j-m.start()))
                print(seg[m.start():j+1][:4000])
                break

# recCalc 定义
i2 = s.find('function recCalc')
print('\n=== recCalc ===')
print(s[i2:i2+1500] if i2>=0 else 'not found')
