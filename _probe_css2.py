# -*- coding: utf-8 -*-
"""探查：CSS .tiny/.mono、planStatusView、openGrr 184731、seed 六类记录内容"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) .tiny / .mono CSS
for cls in ['\.tiny', '\.mono', '\.row-link']:
    for m in re.finditer(r'\.%s\s*\{[^}]*\}' % cls.lstrip('\\'), s):
        print(m.group(0))
print()

# 2) planStatusView
i = s.find('planStatusView')
j = s.find('function planStatusView')
print('=== planStatusView ===')
if j >= 0:
    print(s[j:j+400])
else:
    print('not found, ctx:', s[i-100:i+200])
