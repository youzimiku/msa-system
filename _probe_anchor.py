# -*- coding: utf-8 -*-
"""探查：GrrEntry 提交尾部、renderPage、EntryOpen 声明、计划 result 显示、校准/样本状态 Tag"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) EntryOpen 声明
for m in re.finditer(r'(let|var)\s+EntryOpen', s):
    print('EntryOpen 声明:', s[m.start():m.start()+40])
for m in re.finditer(r'(let|var)\s+GrrOpenId|KpaOpenId|AnlOpen', s):
    print('OpenId 声明:', s[m.start():m.start()+40])

# 2) renderPage
i = s.find('function renderPage')
j = s.find('\nfunction ', i+10)
print('\n=== renderPage ===')
print(s[i:j])

# 3) GrrEntry 提交尾部（找 onClose 调用）
i = s.find('function GrrEntry')
seg = s[i:i+4000]
for m in re.finditer(r'onClose', seg):
    print('GrrEntry onClose @', m.start(), '::', seg[max(0,m.start()-80):m.start()+40].replace('\n',' ')[-120:])
