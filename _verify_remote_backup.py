# -*- coding: utf-8 -*-
import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

# 根目录
root = get('https://api.github.com/repos/youzimiku/msa-system/contents/')
print('=== 根目录 ===')
for f in root:
    print(f['type'], f['name'], (f.get('sha','')[:7]))

# backups 目录
bks = get('https://api.github.com/repos/youzimiku/msa-system/contents/backups')
print('=== backups/ ===')
for f in bks:
    print(f['type'], f['name'], (f.get('sha','')[:7]))

# 根目录 index.html 的 sha 与 HEAD 提交里 index.html 的 sha 对比
idx = get('https://api.github.com/repos/youzimiku/msa-system/contents/index.html')
print('=== 根目录 index.html sha:', idx['sha'][:12])
