# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '抽样规则按方法过滤'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：抽样规则页签 · 按选中方法过滤 & 方法列只读

## 改动范围
抽样方法维护页面（SamplingPage）·「抽样规则」页签。

## 改动明细
1. **抽样规则列表按当前选中分析方法过滤**
   - 在分析方法列表点击某方法（高亮行）后，抽样规则页签只显示该方法的规则。
   - 未选择方法时显示全部规则。

2. **抽样规则「方法」列改为只读**
   - 方法列由下拉框改为纯文本展示（显示方法名称，不显示代码），不可再修改。

3. **新增抽样规则交互调整**
   - 必须先选中分析方法才能新增规则（未选择时提示「请先在分析方法列表中选择一个方法」）。
   - 新增行自动带入当前选中的方法。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_101427_抽样方法维护重构\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：抽样规则页签列表按当前选中分析方法过滤；抽样规则方法列改为只读纯文本；新增抽样规则需先选中方法并自动带入。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：抽样规则按选中方法过滤、方法列只读、新增需先选方法'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
