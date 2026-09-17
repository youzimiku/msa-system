# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
pat = re.compile(r'<Button size="small"([^>]{0,80}?)>')
c = n = p = 0
for m in pat.finditer(s):
    seg = m.group(0)
    if 'type=' not in seg: c += 1
    elif 'type="link"' in seg: n += 1
    elif 'type="primary"' in seg: p += 1
print('no-type', c, 'link', n, 'primary', p)
# 列出 no-type 与 primary 的示例（前后文判断是否操作列）
for m in pat.finditer(s):
    seg = m.group(0)
    if 'type=' not in seg or 'type="primary"' in seg:
        print('>>', seg[:100])
