# -*- coding: utf-8 -*-
"""Step1c：剩余 2 处结论列 return '-' + 权限表 '-'"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# 计划列表/详情 结论列（2 处）
n = s.count("if(!recs.length) return '-'; return <Space size={")
s = s.replace("if(!recs.length) return '-'; return <Space size={",
              "if(!recs.length) return '待采集'; return <Space size={")
print('结论列 return: x%d' % n)

# 权限表 edit/review/approve '-' -> '无'
n1 = s.count("edit:'-'"); s = s.replace("edit:'-'", "edit:'无'")
n2 = s.count("review:'-'"); s = s.replace("review:'-'", "review:'无'")
n3 = s.count("approve:'-'"); s = s.replace("approve:'-'", "approve:'无'")
print('权限表: edit x%d, review x%d, approve x%d' % (n1, n2, n3))

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
