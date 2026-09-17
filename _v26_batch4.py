# -*- coding: utf-8 -*-
"""v2.6 第四批（修正）：seed 标准加 charIds + 表单/列表/详情 关联质量特性"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:90])
    s = s.replace(old, new, cnt)

# ---------- 1. seed 6 条标准加 charIds ----------
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V3.0：按AIAG第4版修订，新增公差%GRR补充判定'},",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V3.0：按AIAG第4版修订，新增公差%GRR补充判定', charIds:['CHAR-2026-001','CHAR-2026-002','CHAR-2026-004','CHAR-2026-007']},",
    1, 'seed-s1')
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：明确2~4档需过程能力佐证'},",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：明确2~4档需过程能力佐证', charIds:['CHAR-2026-001','CHAR-2026-002']},",
    1, 'seed-s2')
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：阈值与客户SPEC对齐'},",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：阈值与客户SPEC对齐', charIds:['CHAR-2026-003']},",
    1, 'seed-s3')
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：按业务三档判定表对齐（有效性=正确决定次数/总决定次数）'},",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：按业务三档判定表对齐（有效性=正确决定次数/总决定次数）', charIds:['CHAR-2026-003']},",
    1, 'seed-s4')
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V1.0 初始版本'},",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V1.0 初始版本', charIds:['CHAR-2026-004','CHAR-2026-007']},",
    1, 'seed-s5')
rep("owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V1.0 初始版本'}",
    "owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V1.0 初始版本', charIds:['CHAR-2026-002','CHAR-2026-006']}",
    1, 'seed-s6')

# ---------- 2. StandardModal 表单加 关联质量特性 ----------
rep("""        <Col span={24}><Form.Item name="groupIds" label="绑定器具组（会议口径：为周期自动选样准备）" tooltip="周期 MSA 校验时，系统按标准绑定的器具组自动筛选样机器具生成计划"><Select mode="multiple" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+' '+g.name}))}/></Form.Item></Col>""",
    """        <Col span={24}><Form.Item name="groupIds" label="绑定器具组（会议口径：为周期自动选样准备）" tooltip="周期 MSA 校验时，系统按标准绑定的器具组自动筛选样机器具生成计划"><Select mode="multiple" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+' '+g.name}))}/></Form.Item></Col>
        <Col span={24}><Form.Item name="charIds" label="关联质量特性"><Select mode="multiple" allowClear options={(d.characteristics||[]).map(c=>({value:c.id,label:c.name+'（'+c.type+'）'}))}/></Form.Item></Col>""",
    1, 'std-modal-char')

# ---------- 3. extra 收集 charIds ----------
rep("""    ['partName','processName','method','numOps','numTrials','numParts','res','unit','target','usl','lsl','note','qcArea','plant','subplant','editor','editorDate','groupIds']
      .forEach(k=>{ if(v[k]!==undefined) extra[k]=v[k]; });""",
    """    ['partName','processName','method','numOps','numTrials','numParts','res','unit','target','usl','lsl','note','qcArea','plant','subplant','editor','editorDate','groupIds','charIds']
      .forEach(k=>{ if(v[k]!==undefined) extra[k]=v[k]; });""",
    1, 'std-extra-char')

# ---------- 4. StandardPage 列表加列 ----------
rep("""    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className="tiny">{gs.map(g=>g.name).join('、')}</span> : <span className="tiny">暂无</span>; }},""",
    """    {title:'关联质量特性', width:180, render:(_,r)=>{ const cs=(r.charIds||[]).map(cid=>(d.characteristics||[]).find(c=>c.id===cid)).filter(Boolean); return cs.length? <span className="tiny">{cs.map(c=>c.name).join('、')}</span> : <span className="tiny">暂无</span>; }},
    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className="tiny">{gs.map(g=>g.name).join('、')}</span> : <span className="tiny">暂无</span>; }},""",
    1, 'std-list-char')

# ---------- 5. StandardPage 详情 Drawer 加 关联质量特性 ----------
rep("""        {key:'绑定器具组', label:'绑定器具组', children: (()=>{ const gs=(detail.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? gs.map(g=>g.name).join('、') : <span className="tiny">未绑定</span>; })()},""",
    """        {key:'关联质量特性', label:'关联质量特性', children: (()=>{ const cs=(detail.charIds||[]).map(cid=>(d.characteristics||[]).find(c=>c.id===cid)).filter(Boolean); return cs.length? cs.map(c=>c.name).join('、') : <span className="tiny">暂无</span>; })()},
        {key:'绑定器具组', label:'绑定器具组', children: (()=>{ const gs=(detail.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? gs.map(g=>g.name).join('、') : <span className="tiny">未绑定</span>; })()},""",
    1, 'std-detail-char')

open(P, 'w', encoding='utf-8').write(s)
print('batch4 OK 长度', len(s))
