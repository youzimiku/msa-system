# -*- coding: utf-8 -*-
import io, re, os
from collections import Counter

base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat'
backup_dir = None
for name in os.listdir(base):
    if name.startswith('MSA系统_backup_20260916'):
        backup_dir = os.path.join(base, name)
        break
print('backup dir:', backup_dir)

def extract_titles(path):
    c = io.open(path, encoding='utf-8').read()
    # 提取所有列定义里的 title:'xxx'
    titles = re.findall(r"title:'([^']+)'", c)
    return Counter(titles)

cur = extract_titles(os.path.join(base, 'MSA系统', 'index.html'))
bak = extract_titles(os.path.join(backup_dir, 'index.html'))

print('--- 仅备份中有(本次删除的列标题) ---')
for t, n in sorted(bak.items()):
    if t not in cur:
        print(f'  {t}  x{n}')
    elif bak[t] > cur[t]:
        print(f'  {t}  备份x{bak[t]} -> 现在x{cur[t]} (减少)')

print('--- 仅现在有(本次新增的列标题) ---')
for t, n in sorted(cur.items()):
    if t not in bak:
        print(f'  {t}  x{n}')
    elif cur[t] > bak[t]:
        print(f'  {t}  备份x{bak[t]} -> 现在x{cur[t]} (增加)')

print('--- 次数相同的公共列(示例前40个) ---')
same = [(t, bak[t]) for t in bak if t in cur and bak[t] == cur[t]]
print('  公共列总数:', len(same))
for t, n in sorted(same)[:40]:
    print(f'  {t}  x{n}')
