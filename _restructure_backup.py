# -*- coding: utf-8 -*-
import io, os, shutil

repo = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
backup_dir = os.path.join(repo, 'backups')

# 本次备份的新文件夹：时间戳 + 简短说明
folder = '20260916_132711_时间到秒状态列移动范围合并'
target = os.path.join(backup_dir, folder)
os.makedirs(target, exist_ok=True)

# 1) 页面快照：index_时间戳.html -> 文件夹/index.html
old_html = os.path.join(backup_dir, 'index_20260916_132711.html')
shutil.move(old_html, os.path.join(target, 'index.html'))
print('moved page ->', os.path.join(folder, 'index.html'))

# 2) 代码级差异：diffs/时间戳.diff.txt -> 文件夹/调整内容.diff.txt
old_diff = os.path.join(backup_dir, 'diffs', '20260916_132711.diff.txt')
shutil.move(old_diff, os.path.join(target, '调整内容.diff.txt'))
print('moved diff ->', os.path.join(folder, '调整内容.diff.txt'))

# 3) 人话记录：文件夹/调整内容.md
md = """# 本次调整内容（2026-09-16 13:27）

## 改动说明
1. **时间字段统一到秒（YYYY-MM-DD HH:mm:ss）**，日期字段保持到日
   - 新增 NOW 常量；所有保存动作的录入时间 / 维护时间 / 修改时间 / 入账时间改为写到秒
   - 假数据补齐到秒：器具台账校准时间（11台）、器具组上次执行/下次提醒/维护时间（8组）、MSA计划录入时间/计划完成时间（12条）、被测参数录入时间（7条）、检验标准录入时间（6条）、样本库日志时间（3条）
   - 回填逻辑：入账时间回填购置日并补 09:30:00；年月日字段强制取日期部分
   - localStorage 缓存键升级为 msa_demo_data_v20260916
2. **被测项目维护页面**：检验标准列表的"状态"列从"版本"之后前移到"分析类型"之后
3. **抽样方法维护-分析方法列表**：
   - 样品数下限 + 样品数上限 → 合并为"样品数范围"（编辑模式两个输入框 + 波浪线）
   - 人数下限 + 人数上限 → 合并为"人数范围"（同上）
   - 次数下限 + 次数上限 → 合并为"次数范围"（同上）
   - 删除"读数下限"、"读数上限"两个字段
4. 其他字段均未增删，仅改值或移动位置（代码级差异见"调整内容.diff.txt"）

## 说明
- 本文件夹 = 本次备份的完整快照（index.html）+ 本次调整内容（md 人话版 + diff 代码版）
- 根目录 index.html 保持上次正式发布版本，本次改动仅归档在 backups/，未发布
"""
io.open(os.path.join(target, '调整内容.md'), 'w', encoding='utf-8').write(md)
print('wrote ->', os.path.join(folder, '调整内容.md'))

# 4) 清理空的 diffs 目录，更新根级 CHANGELOG 为索引格式
old_diffs = os.path.join(backup_dir, 'diffs')
if os.path.isdir(old_diffs) and not os.listdir(old_diffs):
    os.rmdir(old_diffs)
    print('removed empty diffs/')

changelog = """# MSA系统 版本备份记录

每次调整后，在 backups/ 下新建独立文件夹归档（页面快照 + 调整内容），正式发布时才更新根目录 index.html。

## 备份索引

| 备份时间 | 文件夹 | 一句话说明 |
|---|---|---|
| 2026-09-16 13:27 | 20260916_132711_时间到秒状态列移动范围合并 | 时间字段统一到秒；检验标准状态列前移；范围字段合并、读数下限/上限删除 |
"""
io.open(os.path.join(backup_dir, 'CHANGELOG.md'), 'w', encoding='utf-8').write(changelog)
print('updated CHANGELOG.md')

print('=== backups/ 结构 ===')
for n in sorted(os.listdir(backup_dir)):
    p = os.path.join(backup_dir, n)
    print(('[D] ' if os.path.isdir(p) else '[F] ') + n)
    if os.path.isdir(p):
        for f in sorted(os.listdir(p)):
            print('     -', f)
