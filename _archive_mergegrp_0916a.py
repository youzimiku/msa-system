# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder_name = ts + '_方法组LIN_BIAS兼容本地旧数据'
folder = os.path.join(BASE, 'backups', folder_name)
os.makedirs(folder, exist_ok=True)

CUR = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_20260916_220034_方法组归一前.html')

shutil.copy2(CUR, os.path.join(folder, 'index.html'))

a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_方法组归一前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

md = """# 方法组 LIN_BIAS 兼容本地旧数据（2026-09-16 %s）

## 背景
上一轮已把 anMethods 种子数据里 LINEAR/BIAS 的 mergeWith 统一为 LIN_BIAS，但用户浏览器本地 localStorage 中存有旧数据（mergeWith 仍为 LINEAR/BIAS），刷新后旧数据覆盖了新种子。

## 调整内容
在 applyFieldDefaults 数据初始化/迁移逻辑中新增归一规则：运行到 LINEAR 或 BIAS 方法且 canMerge='是'（或已有 mergeWith）时，强制将 mergeWith 设为 LIN_BIAS。
- 该逻辑对 seed 和 localStorage 旧数据均生效，用户刷新页面（重新加载 index.html）后即可看到方法组列为 LIN_BIAS
""" % ts
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| %s | %s | 方法组归一：LINEAR/BIAS 强制合并为 LIN_BIAS（兼容 localStorage 旧数据，刷新即生效） |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), folder_name)
io.open(cl, 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + row)
print('归档:', folder_name)
print('diff 行数:', len(diff))
