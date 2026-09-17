# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder_name = ts + '_台账选择样本_去掉已选回显标签'
folder = os.path.join(BASE, 'backups', folder_name)
os.makedirs(folder, exist_ok=True)

CUR = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_20260916_213222_去回显标签前.html')

shutil.copy2(CUR, os.path.join(folder, 'index.html'))

a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_去回显标签前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

md = """# 台账「样本/人员选择」· 移除操作列已选回显标签（2026-09-16 %s）

## 调整内容
五个台账页面操作列尾部的已选回显标签（如 1样本/2人）移除：
- 选择样本/人员后不再在操作列显示数量标签
- 「样本/人员选择」按钮、弹窗选择与回显逻辑保持不变
""" % ts
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| %s | %s | 台账操作列移除已选回显标签（1样本/2人） |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), folder_name)
io.open(cl, 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + row)
print('归档:', folder_name)
print('diff 行数:', len(diff))
