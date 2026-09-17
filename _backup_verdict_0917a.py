# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '样本库判定状态列'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)
shutil.copy2(P, DIR + r'\index.html')

md = """# 调整内容（{ts}）：样本库管理 · 样本列表新增判定状态列 & 标准值/真值去占位文字

## 改动范围
样本库管理页面，样本列表。

## 改动明细
1. **新增「判定状态」列**（列名自定，避免与已有「状态」启停列混淆）
   - 位于「被测参数」列之后、「标准值」列之前。
   - 控件：下拉框，值固定为 合格 / 不合格。
   - 数据字段 verdict；5 条模拟样本已赋值（SPL-001~003/005 合格、SPL-004 不合格）；新增空行默认空；已有存量记录自动补空值。

2. **标准值 / 真值列去掉占位文字**
   - 值若为「待维护」「合格」「—」时显示为空，不再出现在单元格内。
   - 移除原 placeholder「待维护」。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

before = ROOT + r'\index_备份_20260916_230249_分析方法列表化前.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '基准', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：样本库样本列表被测参数后新增判定状态列（合格/不合格下拉）；标准值/真值去掉待维护/合格占位文字。\n'.format(ts=TS, theme=THEME)
io.open(cl, 'a', encoding='utf-8').write(entry)
print('备份目录:', DIR)
