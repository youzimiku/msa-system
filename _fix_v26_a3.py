# -*- coding: utf-8 -*-
"""Step1b：残留 '-' 占位统一替换"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

nA = s.count(":'-'"); s = s.replace(":'-'", ":'暂无'")
nB = s.count(": '-'"); s = s.replace(": '-'", ": '暂无'")
nC = s.count("? '-'"); s = s.replace("? '-'", "? '暂无'")
nD = s.count("?'-'"); s = s.replace("?'-'", "?'暂无'")
# 权限表（用户中心角色权限）：'-' = 无权限
nE = s.count("edit:'-', review:'-', approve:'-'"); s = s.replace("edit:'-', review:'-', approve:'-'", "edit:'无', review:'无', approve:'无'")

# 残查：所有独立 '-': 出现在引号内的 '-'
left = []
for m in re.finditer(r"'\-'", s):
    ctx = s[max(0,m.start()-40):m.start()+20]
    if m.group(0) == "'-'" and '!==' not in ctx and '!=' not in ctx and '=>' not in ctx[:2]:
        left.append(m.start())
print('A:%d B:%d C:%d D:%d E:%d' % (nA, nB, nC, nD, nE))
print('剩余独立 \'-\' 出现数:', len(left))
# 打印前 25 个剩余上下文
shown = 0
for st in left:
    ctx = s[max(0,st-55):st+25].replace('\n',' ')
    print('  @%d :: %s' % (st, ctx[-80:]))
    shown += 1
    if shown >= 25: break

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
