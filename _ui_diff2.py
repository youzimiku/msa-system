# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read()
new = open(NEW, encoding='utf-8').read()

def collect(src):
    labels = set(re.findall(r'label="([^"]{2,40})"', src))
    btns = set()
    for m in re.finditer(r'<Button[^>]*>\s*([^<>{]{2,24}?)\s*</Button>', src):
        t = m.group(1).strip()
        if t: btns.add(t)
    menus = set()
    for m in re.finditer(r"label:\s*'([^']{2,24})'", src):
        menus.add(m.group(1))
    desc = set(re.findall(r'<Descriptions\.Item\s+label="([^"]{2,40})"', src))
    grp = set(re.findall(r'className="grp-label"[^>]*>([^<]{2,30})<', src))
    panel = set(re.findall(r'<Panel title=\{?["\']?([^"\']{2,30})["\']?', src))
    return labels, btns, menus, desc, grp, panel

ol, ob, om, od, og, op = collect(old)
nl, nb, nm, nd, ng, np = collect(new)

def dump(name, os_, ns_):
    added = ns_ - os_
    removed = os_ - ns_
    print('='*20, name, '='*20)
    print('--- 新增 ---')
    for x in sorted(added): print(' +', x)
    print('--- 删除 ---')
    for x in sorted(removed): print(' -', x)

dump('表单标签 label=', ol, nl)
