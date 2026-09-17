# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '抽样方法维护重构'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：抽样方法维护页面重构

## 改动范围
抽样方法维护页面（SamplingPage）及 种子数据（anMethods / samplingRules / judgeRules）。

## 改动明细
1. **分析方法 = 固定代码表**
   - 方法名称改为只读纯文本（不再可编辑）；去掉「状态」列（默认全部启用）；去掉「新增分析方法」按钮；方法不可删除。
   - 方法组 / 数据类型 / 是否需要取样 / 方法备注 仍可编辑，行首「保存」按钮常驻。
   - 原内嵌在方法行里的取样规则列（默认样品数/人数/次数、样品数/人数/次数范围、工厂）全部移出，归入下方「抽样规则」页签。

2. **新增「抽样规则」页签**（与 判断规则 / 计算参数 并列）
   - 列：操作（保存/删除）｜方法（下拉）｜工厂（下拉）｜车间（下拉）｜默认样品数/人数/次数｜样品数/人数/次数范围｜备注。
   - 同一「方法 + 工厂 + 车间」唯一：保存时校验，重复则拦截提示，不可重复创建。
   - 新增「新增抽样规则」按钮；删除需二次确认。

3. **判断规则页签加工厂 / 车间维度**
   - 新增「工厂」「车间」下拉列；同一方法+工厂+车间下允许多个判定条件。
   - 「判定结论」列由文本框改为下拉框，值固定：可接受 / 有条件接受 / 不可接受。
   - 原 seed 中非常理想可接受/理想可接受/较理想可接受/优秀等非三档值已规范映射到三档。

4. **种子数据**
   - samplingRules：原 5 条保留，新增 3 条演示（GRR/KAPPA@烟台工厂一分厂、stability@青岛工厂一分厂），共 8 条。
   - judgeRules：18 条补齐 工厂/车间 字段并规范化结论；新增 2 条演示（GRR/KAPPA@烟台工厂一分厂），共 20 条；applyFieldDefaults 兜底 seed 同步更新。

5. **查询条件**：去掉「状态」单选（方法状态列已移除），保留 工厂 / 关键词 / 方法名称。

6. **页面说明**文案同步更新。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_092828_样本库判定状态列\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：分析方法改为固定代码表（名称只读、去状态列、不可增删）；新增「抽样规则」页签（方法+工厂+车间唯一）；判断规则加工厂/车间维度且判定结论改下拉（可接受/有条件接受/不可接受）；种子数据同步扩充。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

# git 备份推送（仅 backups/，不推根 index.html 正式版）
for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：抽样方法维护页面重构（方法代码表+抽样规则页签+判断规则工厂车间与结论下拉）'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
