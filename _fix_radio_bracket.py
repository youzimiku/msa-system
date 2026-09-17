# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').read().split('\n')
fix = 0
for i, l in enumerate(lines):
    if 'Radio.Group' in l and 'options=[' in l:
        l = l.replace('options=[', 'options={[')
        if l.rstrip().endswith(']/>'):
            l = l.rstrip()[:-2] + '}]}/>'
        lines[i] = l
        fix += 1
        print('修复行', i+1)
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('共修复', fix, '行')
