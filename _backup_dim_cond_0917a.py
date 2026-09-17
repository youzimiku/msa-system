# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '维度列加有条件接受状态'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：MSA计划 · 维度列状态新增「有条件接受」（黄色）

## 改动范围
MSA计划页面列表分项列（CG/CGK、偏倚、线性、稳定性、重复性、再现性、KAPPA）与计划详情抽屉分项维度。

## 改动明细
1. **新增「有条件接受」状态**：维度结论含「有条件接受」时显示该状态（此前并入「通过」）。
   - 列表：黄色感叹号图标（CondSvg，黄底白感叹号），可点击跳转结果页。
   - 详情抽屉：Tag 显示「有条件接受」，黄色（#fadb14）。
   - 优先级：不可接受（红）> 有条件接受（黄）> 可接受（绿），多记录取最差。

2. **页面说明「维度列状态标识」表新增一行**：有条件接受（黄色感叹号）——对应台账分析已完成，结论为有条件接受（可接受但需关注）；多个分计划以最差结论为准。「通过」行文案相应改为结论为可接受。

## 说明
「判定结果」列的状态定义在 sumVerdict（任一有条件接受则汇总为有条件接受）→ VerdictTag / verdictColor / ENUM.verdictTagColor（有条件接受→orange），本次未改动该链路，仅维度列状态新增黄色档。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_112023_页面说明加关键逻辑\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：MSA计划维度列新增有条件接受（黄色感叹号/黄色Tag），页面说明表同步增加该状态行。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：MSA计划维度列新增有条件接受黄色状态'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
