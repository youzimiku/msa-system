# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
checks = [
    ('样品数范围', "title:'样品数范围'"),
    ('人数范围', "title:'人数范围'"),
    ('次数范围', "title:'次数范围'"),
    ('读数下限应不存在', "title:'读数下限'"),
    ('读数上限应不存在', "title:'读数上限'"),
    ('样品数下限应不存在(列)', "title:'样品数下限'"),
    ('人数下限应不存在(列)', "title:'人数下限'"),
    ('次数下限应不存在(列)', "title:'次数下限'"),
    ('页面标题-被测项目维护(PageHead)', "被测项目维护"),
    ('scroll x 2500', "scroll:{x:2500"),
]
for name, pat in checks:
    n = c.count(pat)
    print(('PASS' if (n >= 1 if '应不存在' not in name else n == 0) else 'FAIL') + f' [{n}] {name}')
