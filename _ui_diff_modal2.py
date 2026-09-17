# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read().split('\n')
new = open(NEW, encoding='utf-8').read().split('\n')

def slice_(lines, name):
    start=None; depth=0
    for i,l in enumerate(lines):
        if re.search(r'function '+name+r'\(', l): start=i; depth=0
        if start is not None and i>=start:
            depth += l.count('{')-l.count('}')
            if depth==0 and i>start: return '\n'.join(lines[start:i+1])
    return ''

ob = slice_(old, 'BatchPlanModal')
nb = slice_(new, 'BatchPlanModal')
def seq(src):
    out=[]
    for m in re.finditer(r'(?:label|title|placeholder|name|dataIndex|text)\s*[:=]\s*["\']([^"\']{2,30})["\']', src):
        out.append(m.group(1))
    # 也抓纯文本节点
    for m in re.finditer(r'>\s*([\u4e00-\u9fff][^<>{}]{1,24}?)\s*<', src):
        t=m.group(1).strip()
        if t: out.append(t)
    return out
o=seq(ob); n=seq(nb)
# 顺序 diff（简化：按出现顺序，标记新增/删除）
import difflib
sm = difflib.SequenceMatcher(None, o, n, autojunk=False)
print('旧序列长度', len(o), '新序列长度', len(n))
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag=='equal': continue
    if tag in ('replace','delete'):
        print('旧有:', ' | '.join(o[i1:i2]))
    if tag in ('replace','insert'):
        print('新增:', ' | '.join(n[j1:j2]))
