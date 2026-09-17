# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
start = None
end = None
for i, l in enumerate(lines):
    if l.strip().startswith('/* 台账-计划锚点对齐'):
        start = i
    if start is not None and 'syncPlanFromRecord(d,p.id)' in l:
        end = i
        break
print('anchor block lines:', start + 1, end + 1)
block = lines[start:end + 1]
del lines[start:end + 1]
for i, l in enumerate(lines):
    if l.strip() == '}' and i + 1 < len(lines) and '枚举字典' in lines[i + 1]:
        print('fn end line:', i + 1)
        lines[i:i] = block
        break
open(p, 'w', encoding='utf-8').write(''.join(lines))
print('moved ok')
