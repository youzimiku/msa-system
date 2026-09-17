# -*- coding: utf-8 -*-
"""V2.5 朴素化 UI 改造：
1. CSS 字号收敛 16/14、文字色收敛 #333/#666
2. 追加全局覆盖层（AntD 组件 + 按钮两形式）
3. JSX 内联 fontSize 归一
4. StatusTag/VerdictTag 固定宽度
5. 所有「状态」列 width 统一 90
6. GRR/KAPPA 等台账命名恢复（取数录入 -> 台账）
"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# ---------- 1. CSS 块内替换 ----------
m = re.search(r'<style>(.*?)</style>', s, re.S)
assert m, 'style block not found'
css = m.group(1)

# 字号收敛：>=15 -> 16；<=14 -> 14
FS = {'11': '14', '11.5': '14', '12': '14', '12.5': '14', '13': '14', '15': '16', '20': '16', '21': '16', '24': '16'}
for k, v in FS.items():
    css = css.replace('font-size:%spx' % k, 'font-size:%spx' % v)

# 文字色收敛：次要灰 -> #666666；深色 -> #333333；蓝色链接/节点 -> #333333
SEC = ['#94a3b8', '#64748b', '#6b7280', '#475569', '#92400e', '#98a2b3', '#8899aa', '#7a8ba6']
MAIN = ['#0f172a', '#1f2733', '#334155', '#111827', '#1e293b', '#0b1220']
BLUE = ['#2563eb', '#1d4ed8', '#0958d9', '#1677ff', '#3b8bff']
for c in SEC:
    css = css.replace('color:%s' % c, 'color:#666666')
for c in MAIN:
    css = css.replace('color:%s' % c, 'color:#333333')
for c in BLUE:
    css = css.replace('color:%s' % c, 'color:#333333')

# ---------- 2. 追加全局覆盖层 ----------
overlay = '''
/* ============ V2.5 朴素化全局覆盖：字号 16/14、文字色 #333/#666、按钮两形式 ============ */
body{font-size:14px;color:#333333}
.ant-btn{font-size:14px;border-radius:4px}
.ant-btn-primary{background:#1677ff;border-color:#1677ff;color:#fff}
.ant-btn-primary:not(:disabled):hover{background:#4096ff;border-color:#4096ff;color:#fff}
.ant-btn-primary:not(:disabled):active{background:#0958d9;border-color:#0958d9}
.ant-btn-default{background:#fff;border-color:#1677ff;color:#1677ff}
.ant-btn-default:not(:disabled):hover{background:#fff;border-color:#4096ff;color:#4096ff}
.ant-btn-default:not(:disabled):active{background:#fff;border-color:#0958d9;color:#0958d9}
.ant-btn-default.ant-btn-dangerous{background:#fff;border-color:#1677ff;color:#1677ff}
.ant-btn-link{background:#fff;border:1px solid #1677ff;color:#1677ff;border-radius:4px}
.ant-btn-link.ant-btn-sm{padding:0 8px;height:24px;line-height:22px;font-size:14px}
.ant-btn-link.ant-btn-dangerous{background:#fff;border:1px solid #1677ff;color:#1677ff}
.ant-btn-text{background:#fff;border:1px solid #1677ff;color:#1677ff;border-radius:4px}
.ant-btn-sm{font-size:14px}
.ant-input,.ant-input-affix-wrapper,.ant-select .ant-select-selector,.ant-picker,
.ant-input-number,.ant-input-number-input,.ant-input-search .ant-input{font-size:14px!important;color:#333333!important}
.ant-input::placeholder,.ant-picker-input>input::placeholder{color:#666666!important}
.ant-select-selection-placeholder{color:#666666!important}
.ant-select-dropdown .ant-select-item,.ant-select-dropdown .ant-select-item-option-content{font-size:14px;color:#333333}
.ant-select-single .ant-select-selection-item{color:#333333}
.ant-table{font-size:14px;color:#333333}
.ant-table-thead>tr>th{color:#333333!important;font-size:14px!important}
.ant-modal-title{font-size:16px;color:#333333}
.ant-modal-body{font-size:14px;color:#333333}
.ant-form-item-label>label{font-size:14px;color:#333333}
.ant-form-item .ant-form-item-explain,.ant-form-item .ant-form-item-extra{font-size:14px;color:#666666}
.ant-menu-item,.ant-menu-submenu-title{font-size:14px!important}
.ant-tabs-tab{font-size:14px}
.ant-tabs-tab-active .ant-tabs-tab-btn{color:#333333}
.ant-pagination-item,.ant-pagination-total-text,.ant-pagination-options{font-size:14px}
.ant-typography{font-size:14px;color:#333333}
.ant-tag{font-size:14px;line-height:22px}
a{color:#333333}
.row-link{color:#333333!important;text-decoration:none}
.row-link:hover{color:#1677ff}
'''
css = css + overlay
s = s[:m.start(1)] + css + s[m.end(1):]

# ---------- 3. JSX 内联 fontSize 归一 ----------
s = s.replace('fontSize:15', 'fontSize:16').replace('fontSize:11', 'fontSize:14').replace('fontSize:12', 'fontSize:14')
# 静态内联色：灰 -> #666666；红（错误/删除语义）保留
s = s.replace("color:'#bbb'", "color:'#666666'").replace("color:'#888'", "color:'#666666'")

# ---------- 4. StatusTag / VerdictTag 固定宽度 ----------
old_st = "function StatusTag({s}){ return <Tag color={ENUM.statusColor[s]||'default'}>{s}</Tag>; }"
new_st = "function StatusTag({s}){ return <Tag color={ENUM.statusColor[s]||'default'} style={{minWidth:78,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{s}</Tag>; }"
assert s.count(old_st) == 1
s = s.replace(old_st, new_st)
old_vt = "function VerdictTag({v}){ return <Tag color={verdictColor(v)} className=\"spec-tag\">{v}</Tag>; }"
new_vt = "function VerdictTag({v}){ return <Tag color={verdictColor(v)} className=\"spec-tag\" style={{minWidth:84,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{v}</Tag>; }"
assert s.count(old_vt) == 1
s = s.replace(old_vt, new_vt)

# ---------- 5. 所有「状态」列 width 统一 90 ----------
s2, n = re.subn(r"(\{title:'状态'(?:, dataIndex:'[^']*')?, width:)\d+", r'\g<1>90', s)
s = s2
print('状态列 width 统一:', n, '处')

# ---------- 6. 台账命名 ----------
# MENU（注意：GRR/KAPPA/Cg/Cgk 带空格，线性/偏移、稳定性不带空格）
MENU_MAP = [
    ('GRR 取数录入', 'GRR 台账'),
    ('KAPPA 取数录入', 'KAPPA 台账'),
    ('线性/偏移取数录入', '线性/偏移台账'),
    ('稳定性取数录入', '稳定性台账'),
    ('Cg/Cgk 取数录入', 'Cg/Cgk 台账'),
]
for old, new in MENU_MAP:
    oldm = "label:'%s', group:'取数录入'" % old
    newm = "label:'%s', group:'台账'" % new
    assert s.count(oldm) == 1, ('MENU', old, s.count(oldm))
    s = s.replace(oldm, newm)
# PAGE_TITLE / ENTRY_CFG title（各出现 1 次，共 2 处）
for old, new in MENU_MAP:
    oldp = "'%s'" % old
    newp = "'%s'" % new
    assert s.count(oldp) == 2, ('PT/CFG', old, s.count(oldp))
    s = s.replace(oldp, newp)
# toast 与说明文案
old = "' 取数录入')"  # 跳转 toast：...+' 取数录入'
assert s.count(old) == 1
s = s.replace(old, "' 台账')")
s = s.replace("待取数录入页录入数据", "待台账页录入数据")
s = s.replace("对应「取数录入」页录入", "对应「台账」页录入")
s = s.replace("「%s取数录入」页录入并提交审核" % 'GRR ', "「GRR 台账」页录入并提交审核")
s = s.replace("「%s取数录入」页录入并提交审核" % 'KAPPA ', "「KAPPA 台账」页录入并提交审核")
s = s.replace("{CFG.name}取数录入：{CFG.desc}", "{CFG.name}台账：{CFG.desc}")
s = s.replace("取数录入页（5 套：按分析方法独立页面）", "台账页（5 套：按分析方法独立页面）")
s = s.replace("'MSA 计划（计划即分析任务）'", "'MSA 计划'")

# 断言剩余「取数录入」
left = s.count('取数录入')
print('剩余 取数录入 出现次数:', left)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved, delta:', len(s) - len(orig))
