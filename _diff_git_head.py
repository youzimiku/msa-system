# -*- coding: utf-8 -*-
import io, re, subprocess
from collections import Counter

repo = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
r = subprocess.run(['git','-C',repo,'show','HEAD:index.html'], capture_output=True)
head_text = r.stdout.decode('utf-8', errors='replace')
cur_text = io.open(repo + r'\index.html', encoding='utf-8').read()
print('HEAD bytes:', len(head_text), 'CUR bytes:', len(cur_text))

def titles(c):
    return Counter(re.findall(r"title:'([^']+)'", c))

h = titles(head_text)
c = titles(cur_text)

print('--- 改动前有、现在没有（本次删除的列标题） ---')
for t, n in sorted(h.items()):
    if t not in c:
        print(f'  [删除] {t}  x{n}')
    elif h[t] > c[t]:
        print(f'  [减少] {t}  x{h[t]} -> x{c[t]}')

print('--- 现在有、改动前没有（本次新增的列标题） ---')
for t, n in sorted(c.items()):
    if t not in h:
        print(f'  [新增] {t}  x{n}')
    elif c[t] > h[t]:
        print(f'  [增加] {t}  x{h[t]} -> x{c[t]}')

# 名称变了但可能只是列改名：列出仅存在于一边的所有
print('--- 仅一边存在的完整清单 ---')
only_h = set(h) - set(c)
only_c = set(c) - set(h)
print('only-before:', sorted(only_h))
print('only-now  :', sorted(only_c))
