# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
# instruments 清单
i = s.find('const instruments = [')
seg = s[i:i+4000]
for m in re.finditer(r"id:'([^']+)', name:'([^']+)'", seg):
    print(m.group(1), '|', m.group(2))
print('--- 各记录数组结尾 id ---')
for arr in ['grr','kappa','linear','stability','cgcgk','resolution']:
    k = s.find('const '+arr+' = [')
    if k < 0:
        print(arr, 'NOT FOUND'); continue
    # 找到该数组的结束 '];'（第一个出现）
    e = s.find('];', k)
    tail = s[max(k, e-400):e]
    ids = re.findall(r"id:'([A-Z]+-2026-\d+)'", tail)
    print(arr, '->', ids[-3:])
