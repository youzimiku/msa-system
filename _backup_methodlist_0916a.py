# -*- coding: utf-8 -*-
import datetime, difflib, io, os, shutil, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
THEME = '分析方法两段式列表'
DIR = ROOT + r'\backups' + '\\' + TS + '_' + THEME
os.makedirs(DIR, exist_ok=True)

# 1) 备份本次改动后的页面
shutil.copy2(P, DIR + r'\index.html')

# 2) 调整内容 md
md = """# 调整内容（{ts}）：创建MSA计划弹窗 · 分析方法两段式改造

## 改动范围
创建MSA计划-器具 / 创建MSA计划-人员 两个弹窗的「分析方法」模块。

## 改动明细
1. **勾选区（上半部分）**
   - 选完被测参数后自动带出该特性支持的方法，但**不再自动勾选**，需手动勾选。
   - 人员弹窗只显示 KAPPA，同样**不自动勾选**（取消原来的「默认选择+禁用」）。
   - 勾选框行右侧新增**「确定」按钮**：把勾选中且未入列表的方法加入下方列表；已入列表的方法**不允许重复添加**。

2. **配置列表（下半部分，原「勾选即展开配置行」改为表格）**
   - 默认**为空**，显示空态提示「未添加分析方法，请在上方勾选后点击确定」。
   - 默认开启编辑模式，列：分析方法（标签）、人数（仅有人数的方法）、次数、样本数（数字输入框）。
   - 每行操作列：**保存**（保存该行配置）+ **删除**（移除该行，**无二次确认**）。

3. **勾选框 × 列表联动**
   - 方法已加入列表 → 对应勾选框**保持勾选且禁用**（不允许手动取消勾选）。
   - 删除列表某行 → 对应勾选框**自动取消勾选并恢复可用**。
   - 切换被测参数或器具组 → **清空整个列表**。

4. **提交逻辑**
   - 创建计划时以列表中**已保存（点了保存）的行**为准，每方法的 人数/次数/样本数 从列表行读取；
   - 计划与台账记录的检验标准（standard）字段同样从列表行读取。
   - 未添加且保存任何方法时提示先勾选并确定、保存。

## 未改动
- 器具选择、计划填写信息两个模块未动；提交生成计划/台账的其余逻辑未动。
""".format(ts=TS)
io.open(DIR + r'\调整内容.md', 'w', encoding='utf-8').write(md)

# 3) diff（对比改动前快照 230249）
before = ROOT + r'\index_备份_20260916_230249_分析方法列表化前.html'
if os.path.exists(before):
    a = io.open(before, encoding='utf-8').read().splitlines(keepends=True)
    b = io.open(P, encoding='utf-8').read().splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, '改动前', '改动后', lineterm='\n'))
    io.open(DIR + r'\调整内容.diff.txt', 'w', encoding='utf-8').write(diff)
    print('diff 行数:', diff.count('\n'))

# 4) CHANGELOG 更新
cl = ROOT + r'\backups\CHANGELOG.md'
entry = '\n## {ts} {theme}\n- 文件：backups/{ts}_{theme}/index.html\n- 调整：创建MSA计划弹窗分析方法改为两段式（勾选+确定入列表+行内编辑保存/删除；不自动勾选；入列表勾选框禁用；删除联动取消勾选；切换清空；提交按已保存行）。\n'.format(ts=TS, theme=THEME)
if os.path.exists(cl):
    io.open(cl, 'a', encoding='utf-8').write(entry)
else:
    io.open(cl, 'w', encoding='utf-8').write('# 备份索引\n' + entry)

print('备份目录:', DIR)
