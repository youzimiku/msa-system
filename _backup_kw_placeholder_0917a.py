# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '关键词支持字段提示'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：所有页面 · 关键词输入框标注支持字段 & 加宽

## 改动范围
全部含「关键词」查询条件的页面，共 13 处输入框。

## 改动明细
1. **关键词输入框加 placeholder 灰字提示**，写明该页面关键词实际支持的检索字段（按各页现有过滤逻辑提取，未改任何搜索逻辑）：
   - 计量器具台账：编号/名称/型号/出厂编号/领用人
   - 器具组维护：组编码/组名称/说明
   - 校准管理：器具编号/器具名称/校准机构/证书编号
   - MSA计划：计划号/器具编号/器具名称/零件号/零件名称
   - 检验标准维护：标准编号/标准名称/零件名称/工序名称/检验依据
   - 被测参数维护：参数编号/参数名称/零件号/零件名称/工序名称
   - 抽样方法维护：方法代码/方法名称（判断规则：规则编号/方法/结论）——按确认去掉方法备注
   - 样本库管理：样本编号/样本名称/零件号/被测项目
   - 样品明细：样本编号/样本名称/器具编号/计划号
   - 五个台账页面：台账编号/计划号/器具编号/器具名称/测量对象

2. **输入框宽度 140 → 220**，保证提示文字可见。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_103952_抽样方法查询加车间\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：13 处关键词输入框新增 placeholder 支持字段提示并加宽至 220；抽样方法维护不含方法备注。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：所有页面关键词输入框标注支持字段并加宽'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
