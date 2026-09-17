# -*- coding: utf-8 -*-
"""验证改造后 CSS 分布与菜单文案"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

style_m = re.search(r'<style>(.*?)</style>', s, re.S)
css = style_m.group(1)
print('CSS length:', len(css))
fs = Counter(re.findall(r'font-size\s*:\s*([0-9.]+)px', css))
print('font-size counts:', dict(sorted(fs.items(), key=lambda x: float(x[0]))))
cs = Counter(re.findall(r'color\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|white)', css))
print('color counts:')
for k, v in cs.most_common(20):
    print('  ', k, v)

i = s.find('const MENU')
print('\nMENU:')
print(s[i:i+1200])
print('\nPAGE_TITLE:')
j = s.find('const PAGE_TITLE')
print(s[j:j+700])
