# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder_name = ts + '_列名与页面名称调整'
folder = os.path.join(BASE, 'backups', folder_name)
os.makedirs(folder, exist_ok=True)

CUR = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_20260916_215639_名称方法组调整前.html')

shutil.copy2(CUR, os.path.join(folder, 'index.html'))

a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_名称方法组调整前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

md = """# 列名与页面名称调整（2026-09-16 %s）

## 调整内容
1. 被测参数维护页面 · 被测参数列表：列名「检验方法」→「分析方法」（检验标准列表的「检验方法」列保留）
2. 抽样方法维护页面 · 分析方法列表：线性和偏倚性的方法组统一为同一个英文组名 **LIN_BIAS**（原 LINEAR 组 BIAS、BIAS 组 LINEAR）
3. 台账层级：菜单「线性/偏移台账」→「线性/偏倚台账」（含页面标题、选择台账类型下拉、操作人弹窗标题、记录列表标题）
4. 数据录入层级：菜单「线性/偏移录入数据」→「线性/偏倚录入数据」（含页面标题映射）
""" % ts
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| %s | %s | 被测参数列名改分析方法；线性/偏倚方法组统一LIN_BIAS；线性/偏移台账与录入数据改名线性/偏倚 |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), folder_name)
io.open(cl, 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + row)
print('归档:', folder_name)
print('diff 行数:', len(diff))
