# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '页面说明加关键逻辑'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：所有页面 · 顶部页面说明新增「关键逻辑」

## 改动范围
全部页面顶部的可折叠「页面说明」。

## 改动明细
1. **每个页面的页面说明新增「关键逻辑」段**，写明页面核心业务规则（数据来源、联动、约束、状态判定等）：
   - 器具组维护：组类型决定用途（器具组/人员组）、行内编辑常驻、被引用不可删
   - 被测参数维护：特性=零件+工序+方法、检验标准号自动生成、创建计划自动带出方法
   - 抽样方法维护：方法固定代码表、抽样规则方法+工厂+车间唯一、判断规则三档结论
   - 样本库管理：零件号下拉联动零件名称、判定状态、二维码打印补打
   - MSA计划：创建交互顺序（器具→特性→勾选方法→确定入列表）、状态列只读、维度状态判定
   - 台账（五个）：计划定型自动生成、审核/确认流转、样本人员选择弹窗按类型区分
   - 数据录入：多操作员×多样本二维、录入人页签、不可改参数
   - 分析结果：只读
2. **恢复基础数据三页（器具组/被测参数/抽样方法）的页面说明显示**（此前按旧要求隐藏，现按新要求全部页面展示）。
3. 渲染顺序：页面说明 → 关键逻辑 → 关键操作 → 权限说明 → 维度列状态标识。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_110820_样本库关键词加零件名称\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：全部页面页面说明新增关键逻辑段；恢复基础数据三页说明显示。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：所有页面说明新增关键逻辑，恢复基础数据三页说明'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
