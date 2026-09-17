# -*- coding: utf-8 -*-
import re, io
t = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\lib\antd.min.js', encoding='utf-8', errors='replace').read(200000)
m = re.search(r'"version":"([0-9.]+)"', t)
print('version:', m.group(1) if m else 'not found')
# 检查 labelRender / optionRender 是否存在于产物（粗略特征）
for k in ['labelRender', 'optionRender', 'dropdownRender']:
    print(k, ':', k in t)
