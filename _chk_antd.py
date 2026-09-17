# -*- coding: utf-8 -*-
import io, re
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\lib\antd.min.js', encoding='utf-8', errors='replace').read()
m = re.search(r'version["\']?:["\']([0-9.]+)', c[:300000])
print('antd version:', m.group(1) if m else 'unknown')
print('has DatePicker:', c.find('DatePicker') != -1)
d = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\lib\dayjs.min.js', encoding='utf-8', errors='replace').read()
print('dayjs size:', len(d))
