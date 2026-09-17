# -*- coding: utf-8 -*-
import io
path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
c = io.open(path, encoding='utf-8').read()

plan_times = {
  'MSAP-2026-001': (('2026-03-15','2026-03-15 09:00:00'), ('2026-03-15','2026-03-15 17:30:00')),
  'MSAP-2026-002': (('2026-04-20','2026-04-20 09:00:00'), ('2026-04-20','2026-04-20 17:00:00')),
  'MSAP-2026-003': (('2026-06-10','2026-06-10 09:00:00'), ('2026-06-10','2026-06-10 16:40:00')),
  'MSAP-2026-004': (('2026-08-20','2026-08-20 09:00:00'), ('2026-09-20','2026-09-20 17:00:00')),
  'MSAP-2026-005': (('2026-08-22','2026-08-22 09:00:00'), ('2026-09-20','2026-09-20 17:00:00')),
  'MSAP-2026-006': (('2026-08-25','2026-08-25 09:00:00'), ('2026-09-30','2026-09-30 17:00:00')),
  'MSAP-2026-007': (('2026-08-25','2026-08-25 10:00:00'), ('2026-10-15','2026-10-15 17:00:00')),
  'MSAP-2026-008': (('2026-08-26','2026-08-26 09:00:00'), ('2026-09-25','2026-09-25 17:00:00')),
  'MSAP-2026-009': (('2026-09-08','2026-09-08 09:00:00'), ('2026-10-15','2026-10-15 17:00:00')),
  'MSAP-2026-010': (('2026-09-05','2026-09-05 09:00:00'), ('2026-10-05','2026-10-05 17:00:00')),
  'MSAP-2026-011': (('2026-09-10','2026-09-10 09:00:00'), ('2026-09-10','2026-09-10 16:30:00')),
  'MSAP-2026-012': (('2026-09-12','2026-09-12 09:00:00'), ('2026-09-12','2026-09-12 16:20:00')),
}

lines = c.split('\n')
for pid,(ed,pl) in plan_times.items():
    id_idx = None
    for idx,l in enumerate(lines):
        if "id:'"+pid+"'" in l:
            id_idx = idx
            break
    assert id_idx is not None, pid
    end = len(lines)
    for j in range(id_idx+1, len(lines)):
        if ("{id:'" in lines[j]) or ("];" in lines[j]):
            end = j
            break
    block = "\n".join(lines[id_idx:end])
    changed = []
    if ed and ("editorDate:'"+ed[0]+"'" in block):
        block = block.replace("editorDate:'"+ed[0]+"'", "editorDate:'"+ed[1]+"'")
        changed.append('editorDate')
    if pl and ("planDate:'"+pl[0]+"'" in block):
        block = block.replace("planDate:'"+pl[0]+"'", "planDate:'"+pl[1]+"'")
        changed.append('planDate')
    lines[id_idx:end] = block.split('\n')
    print(pid, '->', ','.join(changed) if changed else 'NO-CHANGE')

c = '\n'.join(lines)
io.open(path,'w',encoding='utf-8').write(c)
print('PLANS DONE')
