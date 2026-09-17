# -*- coding: utf-8 -*-
import io, re
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\lib\antd.min.js', encoding='utf-8', errors='replace').read()
print('HEAD:', repr(c[:600]))
# 尝试找版本模式
for pat in [r'version:"([0-9][0-9.]*)"', r'"([0-9]+\.[0-9]+\.[0-9]+)"', r'antd@([0-9.]+)', r'v([0-9]+)\.([0-9]+)\.([0-9]+)']:
    m = re.search(pat, c[:500000])
    if m:
        print('match', pat, '->', m.group(0))
# 找 moment 相关
print('has moment ref:', 'moment' in c[:200000])
# 找 dayjs generateConfig
print('has dayjsGenerateConfig:', 'dayjsGenerateConfig' in c)
print('has generatePicker:', 'generatePicker' in c)
