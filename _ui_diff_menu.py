# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read()
new = open(NEW, encoding='utf-8').read()

def menus(src):
    # 找 key:'xxx' 紧邻 label 的菜单项
    items = re.findall(r"key:\s*'([a-z_0-9]+)'[^}]*?label:\s*'([^']+)'", src)
    items2 = re.findall(r"label:\s*'([^']+)'[^}]*?key:\s*'([a-z_0-9]+)'", src)
    all_items = []
    for k, l in items: all_items.append((k, l))
    for l, k in items2: all_items.append((k, l))
    return all_items

om = menus(old)
nm = menus(new)
print('OLD MENU:')
for k, l in om: print(' ', k, '=', l)
print()
print('NEW MENU:')
for k, l in nm: print(' ', k, '=', l)
print()
ok = set(om); nk = set(nm)
print('新增菜单:', sorted(set(k for k, l in nk) - set(k for k, l in ok)))
print('删除菜单:', sorted(set(k for k, l in ok) - set(k for k, l in nk)))
