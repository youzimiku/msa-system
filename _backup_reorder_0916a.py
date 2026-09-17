# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(ROOT, 'index.html')
SNAP = os.path.join(ROOT, 'index_备份_20260916_224614_模块顺序换位前.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
theme = '计划弹窗模块顺序换位'
dst = os.path.join(ROOT, 'backups', ts + '_' + theme)
os.makedirs(dst, exist_ok=True)

cur = io.open(CUR, encoding='utf-8').read()
snap = io.open(SNAP, encoding='utf-8').read()

shutil.copy2(CUR, os.path.join(dst, 'index.html'))
diff = ''.join(difflib.unified_diff(snap.splitlines(True), cur.splitlines(True),
             fromfile='index_备份_20260916_224614_模块顺序换位前.html', tofile='index.html', n=2))
io.open(os.path.join(dst, '调整内容.diff.txt'), 'w', encoding='utf-8').write(diff)

md = """# 调整内容（2026-09-16 %s）

## 创建MSA计划弹窗（器具 / 人员）· 模块顺序换位
- 弹窗内三个模块从上到下调整为：**器具选择 → 计划填写信息 → 分析方法**。
- 原顺序为 计划填写信息 → 分析方法 → 器具选择；本次仅换位，未改动任何字段、控件与联动逻辑。
- 器具选择模块保持撑满剩余高度（搜索器具组 + 器具/人员多选表格）；计划填写信息与分析方法的字段、控件保持不变。
- 按器具创建与按人员创建两个弹窗同时生效。

## 备注
- 未发布正式版；仅备份到 backups/。
"""
io.open(os.path.join(dst, '调整内容.md'), 'w', encoding='utf-8').write(md % ts)

cl = os.path.join(ROOT, 'backups', 'CHANGELOG.md')
line = '- [%s] %s：创建MSA计划弹窗模块顺序换位为 器具选择→计划填写信息→分析方法（器具/人员两弹窗，仅换位不动逻辑）。未发布正式版。\n' % (ts, theme)
with io.open(cl, 'a', encoding='utf-8') as f:
    f.write(line)

print('备份目录:', dst)
print('diff 行数:', diff.count('\n'))
