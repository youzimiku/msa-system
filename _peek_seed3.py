# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
# 所有 instruments 定义（可能在 buildSeed 或 seed 对象里）
for m in re.finditer(r"(?:id|instId):'(JJQ-[\w-]+)'", s):
    pass
ids = re.findall(r"id:'(JJQ-[\w-]+)'", s)
inst_defs = {}
for m in re.finditer(r"\{id:'(JJQ-[\w-]+)', name:'([^']+)'[^}]*?range:'([^']*)'[^}]*?(?:prototype:'([^']*)')?", s):
    inst_defs[m.group(1)] = (m.group(2), m.group(3), m.group(4))
for k, v in inst_defs.items():
    print(k, v)
# 所有 seed 计划 instId 使用情况
print('--- plans instId ---')
plans = re.findall(r"id:'MSAP-[\w-]+'[^}]*?instId:'(JJQ-[\w-]+)'", s)
print(plans)
