# -*- coding: utf-8 -*-
"""探查 CSS 内 font-size / color 分布 与 ENUM.statusColor"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

style_m = re.search(r'<style>(.*?)</style>', s, re.S)
css = style_m.group(1)
print('CSS length:', len(css))

fs = Counter(re.findall(r'font-size\s*:\s*([0-9.]+)px', css))
print('CSS font-size counts:')
for k, v in sorted(fs.items(), key=lambda x: float(x[0])):
    print('  ', k, v)

cs = Counter(re.findall(r'color\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|white)', css))
print('CSS color counts:')
for k, v in cs.most_common(40):
    print('  ', k, v)

# ENUM.statusColor
i = s.find('statusColor')
print('--- statusColor context ---')
print(s[i-200:i+500])
