# -*- coding: utf-8 -*-
import io, os, datetime, shutil, subprocess

base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder = ts + '_修复检验方法分号显示'
bk = os.path.join(base, 'backups', folder)
os.makedirs(bk, exist_ok=True)

shutil.copy2(os.path.join(base, 'index.html'), os.path.join(bk, 'index.html'))

# diff：对比上一个备份版本（40f29ba 归档）
prev = os.path.join(base, 'backups', '20260916_140818_删三列分号方法日期控件去检验标准', 'index.html')
r = subprocess.run(['git', 'diff', '--no-index', '--', prev, os.path.join(base, 'index.html')],
                   cwd=base, capture_output=True, encoding='utf-8', errors='replace')
io.open(os.path.join(bk, '调整内容.diff.txt'), 'w', encoding='utf-8').write((r.stdout or '') + (r.stderr or ''))

md = '''# 调整内容 — 2026-09-16（修复检验方法分号显示）

## 被测项目维护 · 被测参数列表 · 检验方法列修复
- 问题：上一轮将检验方法改为「；」分隔展示后，实际未显示分号，且部分值显示为小写代码（linear / cgcgk）
- 原因 1：CSS 选择器写的是 `.ant-select-selection-item`，但该 antd 版本多选实际结构为 `.ant-select-selection-overflow-item`，选择器不匹配导致分号未渲染
- 原因 2：缓存数据中检验方法值为小写（linear/cgcgk），方法代码表为大写（LINEAR/CGCGK），antd 精确匹配失败，直接显示原始小写值
- 修复：
  1. CSS 选择器改为 `.ant-select-selection-overflow-item + .ant-select-selection-overflow-item::before`（排除 suffix 搜索框项），分号正常显示
  2. 检验方法列 value 统一 `.toUpperCase()` 后再匹配选项，显示为方法名称（GRR；线性；Cg/Cgk）
- 验证：无头 Chrome 渲染被测项目维护页面，检验方法渲染结果为 GRR / 线性 / Cg/Cgk
'''
io.open(os.path.join(bk, '调整内容.md'), 'w', encoding='utf-8').write(md)

cl = os.path.join(base, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| ' + ts[0:4] + '-' + ts[4:6] + '-' + ts[6:8] + ' ' + ts[9:11] + ':' + ts[11:13] + ' | ' + folder + ' | 修复检验方法分号显示：修正CSS选择器、value转大写匹配方法名称 |\n'
anchor = '| 2026-09-16 14:08 | 20260916_140818_删三列分号方法日期控件去检验标准 | 删分析方法三字段；检验方法分号连接展示；日期/时间改选择器；样本库查询去检验标准 |\n'
assert anchor in c
c = c.replace(anchor, anchor + row)
io.open(cl, 'w', encoding='utf-8').write(c)
print('ARCHIVED:', folder)
