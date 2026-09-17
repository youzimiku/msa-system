# -*- coding: utf-8 -*-
"""手册 V2.5：取数录入 -> 台账 文字同步 + 版本号"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_gen_manual.py'
s = io.open(P, encoding='utf-8').read()
orig = s

repl = [
    ('七、取数录入与分析结果', '七、台账与分析结果'),
    ('取数录入与分析结果', '台账与分析结果'),
    ('「取数录入」页录入并提交', '「台账」页录入并提交'),
    ('<b>进入取数录入页</b><span>菜单「取数录入」下按分析方法分 5 个独立页面', '<b>进入台账页</b><span>菜单「台账」下按分析方法分 5 个独立页面'),
    ('alt="GRR取数录入"', 'alt="GRR台账"'),
    ('▲ GRR 取数录入页：待采集记录展开录入面板', '▲ GRR 台账页：待采集记录展开录入面板'),
    ('alt="KAPPA取数录入"', 'alt="KAPPA台账"'),
    ('▲ KAPPA 取数录入页：检验员判定矩阵', '▲ KAPPA 台账页：检验员判定矩阵'),
    ('alt="CgCgk取数录入"', 'alt="CgCgk台账"'),
    ('▲ Cg/Cgk 取数录入页（VDA Type1）', '▲ Cg/Cgk 台账页（VDA Type1）'),
    ('alt="线性取数录入"', 'alt="线性台账"'),
    ('▲ 线性/偏移取数录入页：标准件数与每件次数可调', '▲ 线性/偏移台账页：标准件数与每件次数可调'),
    ('<td>取数录入 → GRR 取数录入 → 待采集行「录入数据」</td>', '<td>台账 → GRR 台账 → 待采集行「录入数据」</td>'),
    ('<td>取数录入 → KAPPA 取数录入 → 待采集行「录入数据」</td>', '<td>台账 → KAPPA 台账 → 待采集行「录入数据」</td>'),
    ('版本 V2.4 ｜ 取样数量规则对齐版', '版本 V2.5 ｜ 朴素化 UI 与台账命名版'),
]
for old, new in repl:
    n = s.count(old)
    assert n >= 1, ('MISS', old[:40], n)
    s = s.replace(old, new)

left = s.count('取数录入')
print('剩余取数录入:', left)
io.open(P, 'w', encoding='utf-8').write(s)
print('gen_manual.py saved, delta:', len(s) - len(orig))
