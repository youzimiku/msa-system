# -*- coding: utf-8 -*-
"""全量排查：所有 Button 中 非 type=link 的实例（重点操作列）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
lines = s.split('\n')

pat = re.compile(r'<Button(?![^>]*type="link")(?=[^>]*>)')
print('=== 所有非 link Button（含 size/ghost/primary/danger）===')
for m in pat.finditer(s):
    line_no = s.count('\n', 0, m.start()) + 1
    seg = m.group(0)
    # 截取完整标签
    end = s.find('>', m.start())
    full = s[m.start():end+1]
    print(line_no, '|', full[:130])
