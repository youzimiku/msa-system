# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder_name = ts + '_台账样本人员选择_人员列表化'
folder = os.path.join(BASE, 'backups', folder_name)
os.makedirs(folder, exist_ok=True)

CUR = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_20260916_212641_人员列表化前.html')

shutil.copy2(CUR, os.path.join(folder, 'index.html'))

a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_人员列表化前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

md = """# 台账「样本/人员选择」弹窗 · 人员选择列表化（2026-09-16 %s）

## 调整内容
五个台账页面「样本/人员选择」弹窗，第二步"选择操作/分析人员"：
- 由标签点选改为**支持多选的列表**（Table + 行勾选）
- 列表字段：人员编号（empNo）、姓名（name）、部门（dept）、岗位（postName），数据源为系统人员档案
- 确定后仍以姓名回显到操作列 Tag；再次打开弹窗按姓名反查回显已勾选
""" % ts
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| %s | %s | 样本/人员选择弹窗：人员选择改为多选列表（人员编号/姓名/部门/岗位） |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), folder_name)
io.open(cl, 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + row)
print('归档:', folder_name)
print('diff 行数:', len(diff))
