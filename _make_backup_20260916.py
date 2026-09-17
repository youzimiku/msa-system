# -*- coding: utf-8 -*-
import io, os, shutil, subprocess, datetime

repo = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = '20260916_132711'

backup_dir = os.path.join(repo, 'backups')
diff_dir = os.path.join(backup_dir, 'diffs')
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(diff_dir, exist_ok=True)

# 1) 复制当前 index.html 为备份
src = os.path.join(repo, 'index.html')
dst = os.path.join(backup_dir, 'index_%s.html' % ts)
shutil.copy2(src, dst)
print('backup file:', dst, os.path.getsize(dst), 'bytes')

# 2) 生成 git diff（B 自动版）到 diffs/
diff_path = os.path.join(diff_dir, '%s.diff.txt' % ts)
r = subprocess.run(['git', '-C', repo, 'diff', 'HEAD', '--', 'index.html'], capture_output=True)
diff_text = r.stdout.decode('utf-8', errors='replace')
io.open(diff_path, 'w', encoding='utf-8').write(diff_text)
print('diff file:', diff_path, len(diff_text), 'chars')

# 3) CHANGELOG.md（A 人话版）
entry = """## 2026-09-16 13:27（index_%s.html）

### 本次改动内容
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
4. 其他字段均未增删，仅改值或移动位置（git diff 见 diffs/%s.diff.txt）

### 当前状态
- 根目录 index.html 保持上次正式发布版本（本次改动仅归档在 backups/，未发布）
- 预览地址 https://youzimiku.github.io/msa-system/ 暂不更新

"""
changelog_path = os.path.join(backup_dir, 'CHANGELOG.md')
if os.path.exists(changelog_path):
    old = io.open(changelog_path, encoding='utf-8').read()
    content = old.rstrip() + '\n\n' + entry
else:
    content = '# MSA系统 版本备份记录\n\n每次调整后自动归档到 backups/，正式发布时才更新根目录 index.html。\n\n' + entry
io.open(changelog_path, 'w', encoding='utf-8').write(content)
print('changelog updated:', changelog_path)
