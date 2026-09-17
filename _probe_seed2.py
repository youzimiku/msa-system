# -*- coding: utf-8 -*-
"""统计 seed 各数组记录数 + EntryPage 完整代码 + Entry 组件签名 + '-'分布"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) seed 数组：找 buildSeed 内顶层数组
i = s.find('function buildSeed')
seg = s[i:i+120000]
# 统计各数组字面量长度：const instruments = [...]; 或返回对象里的数组
print('=== seed 结构 ===')
for name in ['instruments', 'groups', 'standards', 'samples', 'sampleItems', 'calibs', 'plans', 'grr', 'kappa', 'linear', 'stability', 'cgcgk', 'resolution', 'logs']:
    # const name = [ ... ]; 或 name: [ ... ]
    m1 = re.search(r'const\s+' + name + r'\s*=\s*\[', seg)
    m2 = re.search(r'\b' + name + r'\s*:\s*\[', seg)
    m = m1 or m2
    if m:
        start = m.end()
        depth = 0
        for j in range(start, min(start+300000, len(seg))):
            c = seg[j]
            if c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    block = seg[m.start():j+1]
                    items = block.count('{id:') + block.count('{ id:')
                    print(name, '->', items, '条 | 结束偏移', j)
                    break

print('\n=== 返回对象数组（若用 return {...}）===')
mret = re.search(r'return\s*\{', seg)
if mret:
    seg2 = seg[mret.start():mret.start()+80000]
    for name in ['instruments', 'groups', 'standards', 'samples', 'calibs', 'plans', 'grr', 'kappa', 'linear', 'stability', 'cgcgk', 'resolution']:
        mm = re.search(r'\b' + name + r'\s*:\s*\[', seg2)
        if mm:
            start = mm.end(); depth = 0
            for j in range(start, min(start+300000, len(seg2))):
                c = seg2[j]
                if c == '[': depth += 1
                elif c == ']':
                    depth -= 1
                    if depth == 0:
                        block = seg2[mm.start():j+1]
                        items = block.count('{id:') + block.count('{ id:')
                        print('return:', name, '->', items, '条')
                        break
