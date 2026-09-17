# -*- coding: utf-8 -*-
import io
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
old = "  entry:{label:'台账', perm:true}\n};"
new = ("  data:{label:'数据录入', logic:'采用多操作员 × 多样本二维录入：每人只看/只改本人数据；录入人仅可录入测量数据'},\n"
       "  entry:{label:'台账', perm:true}\n};")
assert old in s, 'old not found'
s = s.replace(old, new)
io.open(P, 'w', encoding='utf-8').write(s)
print('patched ok')
