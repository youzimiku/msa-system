# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '判定结果归一四档与列表数字判空'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：判定结果归一四档 + MSA计划列表数字判空

## 改动范围
全站结论展示（VerdictTag）与 MSA计划列表 测量人数/次数/样本数量 列。

## 改动明细
1. **结论文字归一为四档**：新增 normVerdict()，VerdictTag 统一输出 可接受 / 不可接受 / 待采集 / 有条件接受。
   - 优秀（可接受）、非常理想可接受、理想可接受、较理想可接受、评价人可接受、可接受 等 → 可接受
   - 良好（有条件接受）、可接受边缘-可能需改进 等 → 有条件接受
   - 不可接受-需改进（结论取最差档） → 不可接受
   - 空 / - / 待采集 → 待采集
2. **待采集统一为标签**：MSA计划列表「判定结果」列与详情抽屉中原本的纯文字「待采集」改为 VerdictTag 标签（与其他状态同款样式）。
3. **MSA计划列表 测量人数/测量次数/样本数量 判空**：无值时不再渲染 undefined，统一显示「-」。

## 验证
- 渲染验证：MSA计划列表判定结果正常显示有条件接受标签；无纯文字待采集残留；列表数据无 undefined（检测到的 undefined 仅为 AntD CSS-in-JS 占位符，与数据无关）。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_112524_维度列加有条件接受状态\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：判定结果文字归一四档（可接受/不可接受/待采集/有条件接受）；待采集统一标签；计划列表测量人数/次数/样本数量判空显示-。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：判定结果归一四档，计划列表数字判空'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
