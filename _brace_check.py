# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
# 提取所有 <script> 块
import re
blocks = re.findall(r'<script[^>]*>(.*?)</script>', c, re.S)
print('script blocks:', len(blocks))
for bi, b in enumerate(blocks):
    if len(b) < 50:
        continue
    for op, cl in [('{','}'), ('(',')'), ('[',']')]:
        o = b.count(op); cl2 = b.count(cl)
        if o != cl2:
            print(f'  block {bi}: {op}{o} vs {cl}{cl2} MISMATCH')
print('brace check done')
# 也统计整个文件
for op, cl in [('{','}'), ('(',')'), ('[',']')]:
    print(op, c.count(op), cl, c.count(cl), 'ok' if c.count(op)==c.count(cl) else 'MISMATCH')
