# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'

old = open(OLD, encoding='utf-8').read()
new = open(NEW, encoding='utf-8').read()

def collect(src):
    """提取列标题、表单标签、按钮文本、菜单文本、区域标题"""
    titles = set(re.findall(r"title:'([^']{2,40})'", src))
    labels = set(re.findall(r'label="([^"]{2,40})"', src))
    btns = set()
    for m in re.finditer(r'<Button[^>]*>([^<]{2,24})</Button>', src):
        btns.add(m.group(1).strip())
    for m in re.finditer(r'<Button[^>]*>\s*([\u4e00-\u9fffA-Za-z/（）·+×\- ]{2,24})\s*</Button>', src):
        btns.add(m.group(1).strip())
    menus = set()
    for m in re.finditer(r"label:'([^']{2,24})'", src):
        menus.add(m.group(1))
    # 描述项标签
    desc = set(re.findall(r'<Descriptions\.Item\s+label="([^"]{2,40})"', src))
    return titles, labels, btns, menus, desc

ot, ol, ob, om, od = collect(old)
nt, nl, nb, nm, nd = collect(new)

def dump(name, oldset, newset):
    added = newset - oldset
    removed = oldset - newset
    print('='*20, name, '='*20)
    print('--- 新增 ---')
    for x in sorted(added): print(' +', x)
    print('--- 删除 ---')
    for x in sorted(removed): print(' -', x)

dump('列标题 title:{}', ot, nt)
