# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()

print('=== 菜单定义（NAV / MENU / items） ===')
for i, l in enumerate(lines):
    if ('Menu' in l or 'NAV_ITEMS' in l or 'navItems' in l or 'menus' in l or 'NAV' in l) and ('ledger' in l or 'instgroup' in l or '器具' in l or 'char' in l or 'sampling' in l or 'label' in l):
        print(i + 1, '|', l.rstrip()[:220])
