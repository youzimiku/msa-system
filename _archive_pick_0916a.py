# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder_name = ts + '_台账选择样本弹窗'
folder = os.path.join(BASE, 'backups', folder_name)
os.makedirs(folder, exist_ok=True)

CUR = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_20260916_212126_台账选择样本前.html')

shutil.copy2(CUR, os.path.join(folder, 'index.html'))

a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_台账选择样本前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

md = """# 台账「样本/人员选择」功能（2026-09-16 %s）

## 调整内容
1. 五个台账页面（GRR / KAPPA / 线性偏移 / 稳定性 / CG-CGK）操作列，新增「样本/人员选择」按钮（放操作列第一位）
2. 点击按钮打开合并弹窗，分两步：
   - 第一步：从样本库选择本次使用的样本（多选），支持按 样本编号/名称/零件号/被测参数 搜索，显示样本编号/名称/零件号/被测参数/真值/有效期至/状态
   - 第二步：选择操作/分析人员（多选，标签式点选）
   - 点「确定」后关闭弹窗，操作列尾部显示已选 Tag（如 2样本/3人），悬停可见明细（样本编号、人员名单）
3. 仅前端显示效果，不做数据交互/落库；重新打开弹窗时回显已选内容

## 依据
- 腾讯会议 9/15 15:44、16:23 场：台账录入界面增加「选择样本」（从样本库挑）；选择样本+选择人员合并到同一弹窗
- 用户 2026-09-16 确认：放操作列、五个台账都加、合并一个弹窗
""" % ts
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

# CHANGELOG
cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
if os.path.exists(cl):
    c = io.open(cl, encoding='utf-8').read()
else:
    c = '# MSA 系统备份索引\n\n| 时间 | 批次 | 说明 |\n|---|---|---|\n'
row = '| %s | %s | 台账操作列新增「样本/人员选择」按钮+合并选择弹窗（样本多选/人员多选/已选回显） |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), folder_name)
io.open(cl, 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + row)
print('归档:', folder_name)
print('diff 行数:', len(diff))
