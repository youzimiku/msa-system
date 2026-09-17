# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = io.open(P, encoding='utf-8').read().splitlines()
# PAGE_GUIDE 位于 1485-1496 行（0-based 1484-1495）
seg = lines[1484:1496]
src = '\n'.join(seg)
m = re.search(r'const PAGE_GUIDE = \{(.*)\n\};', src, re.S)
body = m.group(1)
# 按顶层键拆分（键行以两个空格 + key: 开头）
entries = re.findall(r'\n  ([a-z_]+):\{(.*?)(?=\n  [a-z_]+:\{|$)', body, re.S)
def getf(s, k):
    m = re.search(r"\b%s:'(.*?)'" % k, s, re.S)
    return m.group(1) if m else ''
rows = []
order = ['text','logic','ops','perm','status']
labels = {'text':'页面说明','logic':'关键逻辑','ops':'关键操作','perm':'权限说明','status':'维度列状态标识'}
status_rows = [
    ('不做（灰色横线）','该分析方法不在本计划创建时勾选的方法范围内，本计划无需开展'),
    ('未做（灰色虚线圆圈）','属于计划范围，但尚未完成对应台账分析'),
    ('通过（绿色对勾）','对应台账分析已完成，结论为可接受'),
    ('有条件接受（黄色感叹号）','对应台账分析已完成，结论为有条件接受（可接受但需关注）；多个分计划以最差结论为准'),
    ('不通过（红色叉）','对应台账分析已完成，结论为不可接受，需整改；多个分计划以最差结论为准'),
]
perm_text = '①「查看全部台账」权限：可查看所有责任人的全部台账记录；②「仅查看本人台账」权限：只能看到当前登录人自己负责的台账记录。'
for key, s in entries:
    label = getf(s, 'label')
    for k in order:
        if k == 'status':
            if 'status:true' in s:
                for i, (mark, desc) in enumerate(status_rows, 1):
                    rows.append([key, label, labels[k], 'status_%d' % i, mark, desc])
        elif k == 'perm':
            if 'perm:true' in s:
                rows.append([key, label, labels[k], k, '', perm_text])
        else:
            v = getf(s, k)
            if k == 'ops' and v == '' and key not in ('ledger','ledger_img'):
                rows.append([key, label, labels[k], k, '', ''])
            elif v:
                rows.append([key, label, labels[k], k, '', v])
print('页面数:', len(entries))
for r in rows:
    print(r[0], r[2], '|', (r[4] or r[5])[:24])
# 保存行数据供后续写 Excel
import json
json.dump(rows, io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_pageguide_rows.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('行数:', len(rows))
