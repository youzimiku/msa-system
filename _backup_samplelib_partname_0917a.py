# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '样本库关键词加零件名称'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：样本库管理 · 关键词支持字段增加零件名称

## 改动范围
样本库管理页面（SampleLibPage）关键词查询。

## 改动明细
1. 关键词过滤字段增加「零件名称」（partName）：现支持 样本编号/样本名称/零件号/零件名称/被测项目。
2. 关键词输入框 placeholder 同步增加「零件名称」。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\backups\20260917_110042_关键词提示去支持前缀\index.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '上版', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：样本库管理关键词支持字段增加零件名称（过滤与 placeholder 同步）。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)

for cmd in [
    ['git', 'add', 'backups/'],
    ['git', 'commit', '-m', '备份：样本库关键词增加零件名称'],
    ['git', 'push'],
]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(cmd), '->', r.returncode)
    if r.stdout.strip(): print(r.stdout.strip()[:400])
    if r.stderr.strip(): print(r.stderr.strip()[:400])
