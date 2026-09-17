# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(ROOT, 'index.html')
SNAP = os.path.join(ROOT, 'index_备份_20260916_222921_质量特性器具组前.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
theme = '特殊特性器具组'
dst = os.path.join(ROOT, 'backups', ts + '_' + theme)
os.makedirs(dst, exist_ok=True)

cur = io.open(CUR, encoding='utf-8').read()
snap = io.open(SNAP, encoding='utf-8').read()

# 1) 备份当前版本
shutil.copy2(CUR, os.path.join(dst, 'index.html'))

# 2) diff（快照 -> 当前）
diff = ''.join(difflib.unified_diff(snap.splitlines(True), cur.splitlines(True),
             fromfile='index_备份_20260916_222921_质量特性器具组前.html', tofile='index.html', n=2))
io.open(os.path.join(dst, '调整内容.diff.txt'), 'w', encoding='utf-8').write(diff)

# 3) 调整内容.md
md = """# 调整内容（2026-09-16 %s）

## 1. 被测参数维护页面
- **检验标准列表**：移除「绑定器具组」列（该列原样展示绑定的器具组名称）。
- **检验标准列表操作列**：新增「器具组」按钮（放在保存/删除前），点击弹出查看弹窗，展示当前检验标准绑定的器具组列表（组编号、组名称、组类型、成员数、说明）；未绑定则显示“未绑定器具组”。
- **被测参数列表**：新增「特殊特性」列（行内下拉框，可搜索，选项为特殊特性编号+名称，如 SC-001 轴径 φ50；数据源为特殊特性主数据，按顺序自动绑定到各被测参数）。
- **详情抽屉**：新增「特殊特性」行（显示编号+名称）。

## 2. 创建MSA计划-器具 / 创建MSA计划-人员 弹窗
- 计划填写信息模块：在「零件名称」字段后面新增「质量特性」下拉框（可搜索，选项为特性编号+特性名称，如 SC-001 轴径 φ50）。

## 3. 数据（模拟）
- 新增特殊特性主数据：SC-001 轴径 φ50、SC-002 轴径 φ10、SC-003 拧紧力矩 25N·m、SC-004 壳体关键尺寸、SC-005 外观判定。
- 被测参数自动绑定特殊特性（按顺序循环绑定）。

## 备注
- 未发布正式版；仅备份到 backups/。
"""
io.open(os.path.join(dst, '调整内容.md'), 'w', encoding='utf-8').write(md % ts)

# 4) CHANGELOG 追加
cl = os.path.join(ROOT, 'backups', 'CHANGELOG.md')
line = '- [%s] %s：检验标准列表去「绑定器具组」列+操作列新增「器具组」弹窗；被测参数列表新增「特殊特性」列；计划弹窗新增「质量特性」下拉；新增特殊特性主数据（SC-001~005）。未发布正式版。\n' % (ts, theme)
with io.open(cl, 'a', encoding='utf-8') as f:
    f.write(line)

print('备份目录:', dst)
print('diff 行数:', diff.count('\n'))
print('CHANGELOG 已追加')
