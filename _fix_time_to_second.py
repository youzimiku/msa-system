# -*- coding: utf-8 -*-
import io

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
with io.open(path, encoding='utf-8') as f:
    content = f.read()

# ========== 1. NOW 常量（165 行后） ==========
old = "const TODAY = (window.dayjs && dayjs().format('YYYY-MM-DD')) || '2026-09-03';"
new = old + "\nconst NOW = (window.dayjs && dayjs().format('YYYY-MM-DD HH:mm:ss')) || TODAY+' 09:00:00';"
assert content.count(old) == 1
content = content.replace(old, new)

# ========== 2. localStorage key 版本化（强制新 seed 生效，避免旧缓存） ==========
old = "localStorage.setItem('msa_demo_data'"
assert content.count(old) == 1
content = content.replace(old, "localStorage.setItem('msa_demo_data_v20260916'")
old = "localStorage.getItem('msa_demo_data'"
assert content.count(old) == 1
content = content.replace(old, "localStorage.getItem('msa_demo_data_v20260916'")

# ========== 3. applyFieldDefaults 回填修正 ==========
old = "ymd:i.ymd||(i.lastCal||TODAY)"
assert content.count(old) == 1
content = content.replace(old, "ymd:i.ymd||((i.lastCal||TODAY)+'').slice(0,10)")
old = "ledgerDate:i.ledgerDate||(i.buy||TODAY)"
assert content.count(old) == 1
content = content.replace(old, "ledgerDate:i.ledgerDate||((i.buy||TODAY)+' 09:30:00')")

# ========== 4. 保存动作：时间字段 TODAY → NOW ==========
# editorDate（录入/维护时间）、modifyDate（修改时间）、ledgerDate（入账时间）→ NOW；ymd/calDate/effDate/analysisDate 等日期字段保持 TODAY
assert 'editorDate=TODAY' in content or 'editorDate:TODAY' in content
content = content.replace('editorDate=TODAY', 'editorDate=NOW').replace('editorDate:TODAY', 'editorDate:NOW')
assert 'modifyDate=TODAY' in content or 'modifyDate:TODAY' in content
content = content.replace('modifyDate=TODAY', 'modifyDate=NOW').replace('modifyDate:TODAY', 'modifyDate:NOW')
assert "ledgerDate:TODAY" in content
content = content.replace('ledgerDate:TODAY', 'ledgerDate:NOW')

# ========== 5. sampleLibLogs time 补秒 ==========
for old, new in [("time:'2026-08-30 14:22'", "time:'2026-08-30 14:22:33'"),
                 ("time:'2026-09-01 09:15'", "time:'2026-09-01 09:15:47'"),
                 ("time:'2026-09-05 16:40'", "time:'2026-09-05 16:40:21'")]:
    assert content.count(old) == 2, (old, content.count(old))
    content = content.replace(old, new)

# ========== 6. 3546 日志 now 到秒 ==========
old = "const now=dayjs().format('YYYY-MM-DD HH:mm');"
assert content.count(old) == 1
content = content.replace(old, "const now=dayjs().format('YYYY-MM-DD HH:mm:ss');")

# ========== 7. seed 值：按 id 行内替换 ==========
inst_lastcal = {
  'JJQ-2023-010': ('2026-03-02', '2026-03-02 10:30:00'),
  'JJQ-2024-001': ('2026-05-10', '2026-05-10 09:15:00'),
  'JJQ-2024-002': ('2026-01-15', '2026-01-15 14:00:00'),
  'JJQ-2024-003': ('2026-07-02', '2026-07-02 11:20:00'),
  'JJQ-2024-004': ('2025-09-15', '2025-09-15 15:40:00'),
  'JJQ-2024-005': ('2026-03-20', '2026-03-20 10:05:00'),
  'JJQ-2024-006': ('2025-11-11', '2025-11-11 16:30:00'),
  'JJQ-2024-007': ('2025-12-05', '2025-12-05 09:45:00'),
  'JJQ-2024-008': ('2026-02-18', '2026-02-18 13:30:00'),
  'JJQ-2024-009': ('2026-04-01', '2026-04-01 10:25:00'),
  'JJQ-2024-011': ('2026-03-01', '2026-03-01 14:10:00'),
}
group_times = {
  'G-01': (('2026-03-15','2026-03-15 10:30:00'), ('2027-03-15','2027-03-15 08:00:00'), ('2026-06-01','2026-06-01 14:20:00'), ('2026-03-15','2026-03-15 10:30:00')),
  'G-02': (('2026-06-10','2026-06-10 09:20:00'), ('2026-12-10','2026-12-10 08:00:00'), ('2026-06-01','2026-06-01 14:35:00'), ('2026-06-10','2026-06-10 09:20:00')),
  'G-03': (('2026-03-18','2026-03-18 11:00:00'), ('2027-03-18','2027-03-18 08:00:00'), ('2026-06-01','2026-06-01 15:00:00'), ('2026-03-18','2026-03-18 11:00:00')),
  'G-04': (('2026-08-22','2026-08-22 10:10:00'), ('2026-10-05','2026-10-05 08:00:00'), ('2026-06-01','2026-06-01 15:30:00'), ('2026-08-22','2026-08-22 10:10:00')),
  'P-01': (('2026-08-22','2026-08-22 10:10:00'), ('2027-02-02','2027-02-02 08:00:00'), ('2026-08-25','2026-08-25 09:40:00'), ('2026-08-22','2026-08-22 10:10:00')),
  'P-02': (('2026-08-22','2026-08-22 10:10:00'), ('2027-02-02','2027-02-02 08:00:00'), ('2026-08-25','2026-08-25 09:55:00'), None),
  'P-03': (('2026-09-01','2026-09-01 10:05:00'), ('2027-02-09','2027-02-09 08:00:00'), ('2026-09-01','2026-09-01 10:05:00'), None),
  'P-04': (('2026-09-01','2026-09-01 10:20:00'), ('2027-02-09','2027-02-09 08:00:00'), ('2026-09-01','2026-09-01 10:20:00'), None),
}
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
char_times = {
  'CHAR-2026-001': '2026-09-09 10:24:00', 'CHAR-2026-002': '2026-09-09 10:26:00',
  'CHAR-2026-003': '2026-09-09 10:28:00', 'CHAR-2026-004': '2026-09-09 10:30:00',
  'CHAR-2026-005': '2026-09-09 10:32:00', 'CHAR-2026-006': '2026-09-09 10:34:00',
  'CHAR-2026-007': '2026-09-09 10:36:00',
}
std_times = {
  'STD-MSA-001': ('2026-01-01', '2026-01-01 09:30:00'),
  'STD-MSA-002': ('2025-07-01', '2025-07-01 09:30:00'),
  'STD-MSA-003': ('2025-07-01', '2025-07-01 10:15:00'),
  'STD-MSA-004': ('2025-07-01', '2025-07-01 11:00:00'),
  'STD-MSA-005': ('2025-01-01', '2025-01-01 09:30:00'),
  'STD-MSA-006': ('2025-01-01', '2025-01-01 10:00:00'),
}

lines = content.split('\n')

for iid,(oldv,newv) in inst_lastcal.items():
    hits=0
    for idx,l in enumerate(lines):
        if ("id:'"+iid+"'" in l) and ("lastCal:'"+oldv+"'" in l):
            lines[idx]=l.replace("lastCal:'"+oldv+"'", "lastCal:'"+newv+"'")
            hits+=1
    assert hits==1, ('inst lastCal', iid, hits)

for gid,(le,nr,ed,rt) in group_times.items():
    found=False
    for idx,l in enumerate(lines):
        if "id:'"+gid+"'" in l:
            if le and ("lastExec:'"+le[0]+"'" in l):
                lines[idx]=lines[idx].replace("lastExec:'"+le[0]+"'","lastExec:'"+le[1]+"'")
            if nr and ("nextRemind:'"+nr[0]+"'" in l):
                lines[idx]=lines[idx].replace("nextRemind:'"+nr[0]+"'","nextRemind:'"+nr[1]+"'")
            if ed and ("editorDate:'"+ed[0]+"'" in l):
                lines[idx]=lines[idx].replace("editorDate:'"+ed[0]+"'","editorDate:'"+ed[1]+"'")
            if rt and ("time:'"+rt[0]+"'" in l):
                lines[idx]=lines[idx].replace("time:'"+rt[0]+"'","time:'"+rt[1]+"'")
            found=True
    assert found, ('instGroups', gid)

for pid,(ed,pl) in plan_times.items():
    found=False
    for idx,l in enumerate(lines):
        if "id:'"+pid+"'" in l:
            if "editorDate:'"+ed[0]+"'" in l:
                lines[idx]=lines[idx].replace("editorDate:'"+ed[0]+"'","editorDate:'"+ed[1]+"'")
            if "planDate:'"+pl[0]+"'" in l:
                lines[idx]=lines[idx].replace("planDate:'"+pl[0]+"'","planDate:'"+pl[1]+"'")
            found=True
    assert found, ('plans', pid)

for cid,tv in char_times.items():
    hits=0
    for idx,l in enumerate(lines):
        if ("id:'"+cid+"'" in l) and ("editorDate:'2026-09-09'" in l):
            lines[idx]=l.replace("editorDate:'2026-09-09'","editorDate:'"+tv+"'")
            hits+=1
    assert hits==1, ('characteristics', cid, hits)

for sid,(eff,tv) in std_times.items():
    hits=0
    for idx,l in enumerate(lines):
        if ("id:'"+sid+"'" in l) and ("effDate:'"+eff+"'" in l):
            old="effDate:'"+eff+"'"
            lines[idx]=l.replace(old, "effDate:'"+eff+"', editorDate:'"+tv+"'", 1)
            hits+=1
    assert hits==1, ('standards', sid, hits)

content='\n'.join(lines)

with io.open(path,'w',encoding='utf-8') as f:
    f.write(content)
print('ALL OK')
