# -*- coding: utf-8 -*-
"""V2.6 静态逻辑冒烟：接线完整性检查"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
ok, fail = [], []

def chk(name, cond, detail=''):
    (ok if cond else fail).append(name + ('' if not detail else ' :: ' + detail))

# Step1 需求2
chk('结论列 return 待采集', s.count("if(!recs.length) return '待采集'") >= 2)
chk('无 <span tiny>-</span>', '<span className="tiny">-</span>' not in s)
chk('无 >-< 显示', ">'-'<" not in s)
chk('无 return \'-\'', "return '-'" not in s)
chk('权限表 edit 无', s.count("edit:'无'") >= 1 or s.count("edit:'暂无'") >= 1)

# Step2 需求1 Tooltip
chk('TIPS 字典', 'const TIPS = {' in s)
chk('StatusTag Tooltip', 'TIPS.status[s]||s' in s)
chk('VerdictTag Tooltip', 'TIPS.verdict[vv]' in s)
chk('VerdictTag 待采集兜底', "const vv=(!v||v==='-')?'待采集':v" in s)
chk('计划状态 Tooltip', 'TIPS.plan[v.text]' in s)
chk('校准状态 Tooltip', "TIPS.calib['超期']" in s and "TIPS.calib['临期']" in s and "TIPS.calib['正常']" in s)
chk('样本状态 Tooltip', 'TIPS.sample[s]' in s and 'TIPS.sample[detail.status]' in s)

# Step3 拆页
chk('DataOpen 声明', 'let DataOpen=null;' in s)
chk('无 EntryOpen 残留', 'EntryOpen' not in s)
chk('openGrr 智能分派', "rec.reviewStatus==='待采集'){ DataOpen={kind:'grr',id}; setPage('data_grr')" in s)
chk('openKappa 智能分派', "rec.reviewStatus==='待采集'){ DataOpen={kind:'kappa',id}; setPage('data_kappa')" in s)
chk('openAnl 智能分派', "setPage('data_'+kind)" in s and "AnlOpen={kind,id}; setPage(ANA_PAGE[kind])" in s)
chk('DataEntryPage 定义', 'function DataEntryPage({kind}){' in s)
chk('DataEntryPage 渲染分支', s.count("return <DataEntryPage kind=") == 5)
chk('MENU 录入组', s.count("group:'录入数据'") == 5)
chk('PAGE_TITLE 录入', s.count("'data_grr':'GRR 录入数据'") == 1)
# EntryPage 段无 entryRec（AnlPage 保留给 resolution，故只查 EntryPage 段）
# EntryPage 还有 entryRec 吗？grep 在 EntryPage 区间
ep = s[s.find('function EntryPage'):s.find('const ENTRY_CFG')]
chk('EntryPage 纯净', 'setEntryRec' not in ep and 'entryRec' not in ep, 'entryRec' if 'entryRec' in ep else '')
# GrrPage/KappaPage 无 entryRec
gp = s[s.find('function GrrPage'):s.find('function GrrDetail')]
kp = s[s.find('function KappaPage'):s.find('function KappaDetail')]
chk('GrrPage 无录入Drawer', 'setEntryRec' not in gp)
chk('KappaPage 无录入Drawer', 'setEntryRec' not in kp)
# AnlPage：entryRec 仅 resolution
ap = s[s.find('function AnlPage'):s.find('function AnlActionForm')]
chk('AnlPage Drawer 限 resolution', "kind==='resolution' && entryRec && <Drawer" in ap)
chk('AnlPage 去录入跳 data', "DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind)" in ap)

# Step4 模拟数据
chk('seed linear 有记录', 'LIN-2026-001' in s and 'LIN-2026-002' in s)
chk('seed stability 有记录', 'STB-2026-001' in s and 'STB-2026-002' in s)
chk('seed cgcgk 有记录', 'CG-2026-001' in s and 'CG-2026-003' in s)
chk('seed resolution 有记录', 'RES-2026-001' in s and 'RES-2026-002' in s)
chk('存量兜底补种', "['linear','stability','cgcgk','resolution'].forEach" in s)

# Step1 需求5 文字统一
chk('tiny 色 #333', '.tiny{font-size:14px;color:#333333}' in s)

print('PASS %d / %d' % (len(ok), len(ok)+len(fail)))
for f in fail:
    print('  FAIL:', f)
