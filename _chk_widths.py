# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for w in ['280','300','320','120','130','140','150','180','230','90']:
    n = len(re.findall(r'style=\{\{width:'+w+r'\}\}', s))
    print('style width', w, '->', n)
for m in re.finditer(r"title:'操作', width:(\d+)", s):
    print('OP-COL', m.group(1))
