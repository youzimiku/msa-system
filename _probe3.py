# -*- coding: utf-8 -*-
"""搜索所有包含 size=small 但非 link 的 Button；以及操作列 render 内 Button"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1. 所有含 size="small" 的 Button 标签
print('=== 含 size="small" 的 Button（检查是否 link）===')
pat = re.compile(r'<Button[^>]*?size="small"[^>]*>')
for m in pat.finditer(s):
    line_no = s.count('\n', 0, m.start()) + 1
    full = m.group(0)
    tag = 'LINK' if 'type="link"' in full else ('PRIMARY' if 'type="primary"' in full else ('NO-TYPE' if 'type=' not in full else 'OTHER'))
    print(line_no, tag, '|', full[:120])

# 2. 操作列 render 上下文里的 Button（render:(_,r) 或 render:(_,r)=>）
print()
print('=== 操作列 render 内的 Button 非 link ===')
pat2 = re.compile(r'render:\s*\(_?,?r?\w*\)\s*=>[^;]{0,300}?<Button(?![^>]*type="link")[^>]*>')
for m in pat2.finditer(s):
    line_no = s.count('\n', 0, m.start()) + 1
    print(line_no, '|', m.group(0)[:150])
