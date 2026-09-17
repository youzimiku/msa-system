# -*- coding: utf-8 -*-
import io, re
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

checks = [
    ("NOW 常量", "const NOW = (window.dayjs && dayjs().format('YYYY-MM-DD HH:mm:ss'))"),
    ("localStorage set 版本化", "localStorage.setItem('msa_demo_data_v20260916'"),
    ("localStorage get 版本化", "localStorage.getItem('msa_demo_data_v20260916'"),
    ("ymd 回填取日期", "ymd:i.ymd||((i.lastCal||TODAY)+'').slice(0,10)"),
    ("ledgerDate 回填到秒", "ledgerDate:i.ledgerDate||((i.buy||TODAY)+' 09:30:00')"),
    ("editorDate=NOW", "editorDate=NOW"),
    ("editorDate:NOW", "editorDate:NOW"),
    ("modifyDate=NOW", "modifyDate=NOW"),
    ("日志 now 到秒", "dayjs().format('YYYY-MM-DD HH:mm:ss')"),
    ("lastCal 001 到秒", "lastCal:'2026-03-02 10:30:00'"),
    ("lastCal 011 到秒", "lastCal:'2026-03-01 14:10:00'"),
    ("G-01 上次执行到秒", "lastExec:'2026-03-15 10:30:00'"),
    ("G-01 下次提醒到秒", "nextRemind:'2027-03-15 08:00:00'"),
    ("G-04 维护时间到秒", "editorDate:'2026-06-01 15:30:00'"),
    ("P-01 执行记录到秒", "time:'2026-08-22 10:10:00'"),
    ("计划001 录入到秒", "editorDate:'2026-03-15 09:00:00'"),
    ("计划001 计划完成到秒", "planDate:'2026-03-15 17:30:00'"),
    ("计划012 到秒", "editorDate:'2026-09-12 09:00:00'"),
    ("特性001 录入到秒", "editorDate:'2026-09-09 10:24:00'"),
    ("特性007 录入到秒", "editorDate:'2026-09-09 10:36:00'"),
    ("标准001 补录入时间", "effDate:'2026-01-01', editorDate:'2026-01-01 09:30:00'"),
    ("标准004 补录入时间", "effDate:'2025-07-01', editorDate:'2025-07-01 11:00:00'"),
    ("样本日志1 到秒", "time:'2026-08-30 14:22:33'"),
    ("样本日志3 到秒", "time:'2026-09-05 16:40:21'"),
]
allok = True
for name, pat in checks:
    n = c.count(pat)
    ok = n >= 1
    if not ok:
        allok = False
    print(('OK ' if ok else 'FAIL') + f' [{n}] {name}: {pat[:60]}')

# 状态列顺序：检验标准列表区域内，分析类型 -> 状态 -> 关联被测参数；版本 -> 录入人（无状态）
i_type = c.find("{title:'分析类型', width:84")
seg_a = c[i_type:i_type+700]
order_ok = seg_a.find("{title:'状态', dataIndex:'status'") != -1 and seg_a.find("{title:'状态', dataIndex:'status'") < seg_a.find("{title:'关联被测参数'")
i_ver = c.find("{title:'版本', dataIndex:'version', width:70")
seg_b = c[i_ver:i_ver+200]
order_ok = order_ok and ("{title:'状态'" not in seg_b[:seg_b.find("{title:'录入人'")] if "{title:'录入人'" in seg_b else False)
print('ORDER' + (' OK' if order_ok else ' FAIL'))

# 检查是否残留旧的 14:22 / 09:15 / 16:40（不带秒）
for v in ["time:'2026-08-30 14:22'", "time:'2026-09-01 09:15'", "time:'2026-09-05 16:40'",
          "editorDate:TODAY", "editorDate=TODAY", "modifyDate=TODAY", "modifyDate:TODAY"]:
    n = c.count(v)
    if n:
        allok = False
        print(f'RESIDUAL FAIL [{n}] {v}')

print('ALL' + (' OK' if allok and order_ok else ' FAIL'))
