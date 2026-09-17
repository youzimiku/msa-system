# -*- coding: utf-8 -*-
"""定位未命中文本的实际情况"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

print('=== entryRec state 声明（全部）===')
for m in re.finditer(r'const \[entryRec,setEntryRec\]=useState\(null\);', s):
    a = max(0, m.start()-80)
    print('@%d :: %s' % (m.start(), s[a:m.start()+120].replace('\n', '⏎')[-200:]))
    print()

print('\n=== GrrPage/KappaPage 残留 Drawer ===')
for m in re.finditer(r'\{entryRec && <Drawer', s):
    a = max(0, m.start()-40)
    print('@%d :: %s' % (m.start(), s[a:m.start()+260].replace('\n', '⏎')[-300:]))
    print()
