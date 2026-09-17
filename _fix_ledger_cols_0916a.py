# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_台账列调整前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. MSA计划列表：录入人后加录入时间列
EDITS.append((
"""    {title:'录入人', dataIndex:'editor', width:100, ellipsis:true, render:v=><span>{v||'—'}</span>}
  ];""",
"""    {title:'录入人', dataIndex:'editor', width:100, ellipsis:true, render:v=><span>{v||'—'}</span>},
    {title:'录入时间', dataIndex:'editorDate', width:115, render:v=><span className="mono">{v||'—'}</span>}
  ];""", 1))

# 2. 五个台账页面操作列：手动分析→分析；全部按钮平铺去掉更多折叠
EDITS.append((
"""    {title:'操作', width:290, fixed:'left', render:(_,r)=><OpBtns items={[
      {label:'审核',onClick:()=>setAuditOpen(true)},
      {label:'手动分析',disabled:!canDo(d.me.role,'edit')||r.reviewStatus!=='待分析',onClick:()=>setAnlRec(r)},
      {label:'查看结果',onClick:()=>goResult(r)},
      {label:'修改数据',disabled:!canDo(d.me.role,'edit')||r.reviewStatus!=='待分析',onClick:()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}},
      {label:'操作人',onClick:()=>setOpsRec(r)},
      {label:'预览',onClick:()=>{}},
      {label:'录入数据',disabled:!canDo(d.me.role,'edit')||r.reviewStatus!=='待采集',onClick:()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}
    ]}/>},""",
"""    {title:'操作', width:560, fixed:'left', render:(_,r)=><Space size={0} wrap>
      <Button size="small" type="link" onClick={()=>setAuditOpen(true)}>审核</Button>
      <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')||r.reviewStatus!=='待分析'} onClick={()=>setAnlRec(r)}>分析</Button>
      <Button size="small" type="link" onClick={()=>goResult(r)}>查看结果</Button>
      <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')||r.reviewStatus!=='待分析'} onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>修改数据</Button>
      <Button size="small" type="link" onClick={()=>setOpsRec(r)}>操作人</Button>
      <Button size="small" type="link" onClick={()=>{}}>预览</Button>
      <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')||r.reviewStatus!=='待采集'} onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>录入数据</Button>
    </Space>},""", 1))

# 3. 分辨力列：KAPPA/稳定性 去掉（条件列）
EDITS.append((
"""    {title:'分辨力', width:100, render:(_,r)=>{ const it=d.instruments.find(i=>i.id===r.instId); return <span>{it&&it.res?it.res:'暂无'}</span>; }},""",
"""    ...(kind==='kappa'||kind==='stability'?[]:[{title:'分辨力', width:100, render:(_,r)=>{ const it=d.instruments.find(i=>i.id===r.instId); return <span>{it&&it.res?it.res:'暂无'}</span>; }}]),""", 1))

# 4. 测量对象 → 被测参数（五个台账页统一）
EDITS.append((
"""    {title:'测量对象', dataIndex:'object', width:170, ellipsis:true},""",
"""    {title:'被测参数', dataIndex:'object', width:170, ellipsis:true},""", 1))

# 5. 上限/下限/标准值：KAPPA 去掉（条件列）
EDITS.append((
"""    {title:'上限', width:90, render:(_,r)=><span>{r.tolerance&&r.tolerance.has?r.tolerance.usl:'暂无'}</span>},
    {title:'下限', width:90, render:(_,r)=><span>{r.tolerance&&r.tolerance.has?r.tolerance.lsl:'暂无'}</span>},
    {title:'标准值', width:100, render:(_,r)=>{ const sp=(d.sampleLib||[]).find(s=>s.charDim===r.object); return <span>{sp&&sp.refValue&&sp.refValue!=='待维护'?sp.refValue:'暂无'}</span>; }},""",
"""    ...(kind==='kappa'?[]:[
      {title:'上限', width:90, render:(_,r)=><span>{r.tolerance&&r.tolerance.has?r.tolerance.usl:'暂无'}</span>},
      {title:'下限', width:90, render:(_,r)=><span>{r.tolerance&&r.tolerance.has?r.tolerance.lsl:'暂无'}</span>},
      {title:'标准值', width:100, render:(_,r)=>{ const sp=(d.sampleLib||[]).find(s=>s.charDim===r.object); return <span>{sp&&sp.refValue&&sp.refValue!=='待维护'?sp.refValue:'暂无'}</span>; }}
    ]),""", 1))

# 6. 审核时间（审核人后）+ 确认人/确认时间（确认状态前后）
EDITS.append((
"""    {title:'审核人', width:90, render:(_,r)=><span>{r.reviewer||'暂无'}</span>},
    {title:'确认状态', width:90, render:(_,r)=>{ const ok=!!(r.approver||r.approveDate); return <Tooltip title={ok?'该记录已完成确认':'该记录尚未确认'}><span style={{color:ok?'#52c41a':'#666666'}}>{ok?'已确认':'未确认'}</span></Tooltip>; }}
  ];""",
"""    {title:'审核人', width:90, render:(_,r)=><span>{r.reviewer||'—'}</span>},
    {title:'审核时间', width:115, render:(_,r)=><span className="mono">{r.reviewDate||'—'}</span>},
    {title:'确认人', width:90, render:(_,r)=><span>{r.approver||'—'}</span>},
    {title:'确认状态', width:90, render:(_,r)=>{ const ok=!!(r.approver||r.approveDate); return <Tooltip title={ok?'该记录已完成确认':'该记录尚未确认'}><span style={{color:ok?'#52c41a':'#666666'}}>{ok?'已确认':'未确认'}</span></Tooltip>; }},
    {title:'确认时间', width:115, render:(_,r)=><span className="mono">{r.approveDate||'—'}</span>}
  ];""", 1))

# 7. 表格横向滚动宽度加大（操作列 560 + 更多列）
EDITS.append((
"""rowSelection={{selectedRowKeys:selKeys, onChange:setSelKeys}} scroll={{x:1500}} pagination={false}/>""",
"""rowSelection={{selectedRowKeys:selKeys, onChange:setSelKeys}} scroll={{x:2100}} pagination={false}/>""", 1))

fail = False
for i, (old, new, exp) in enumerate(EDITS):
    cnt = src.count(old)
    if cnt != exp:
        print(f"[FAIL] #{i} 期望 {exp} 实际 {cnt} | old[:80]={old[:80]!r}")
        fail = True
    else:
        src = src.replace(old, new)
        print(f"[OK] #{i} 替换 {cnt} 处")

if fail:
    print('存在未匹配项，未写回')
else:
    io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
    folder = os.path.join(BASE, 'backups', ts + '_台账列调整')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：台账列调整（2026-09-16）

## 改动清单
1. MSA计划列表：录入人列后新增「录入时间」列（editorDate）
2. 五个台账页面（GRR/KAPPA/线性偏移/稳定性/CgCgk）：
   - 操作列：「手动分析」→「分析」；原来折叠进「更多」的按钮全部平铺显示（审核/分析/查看结果/修改数据/操作人/预览/录入数据 7个），去掉更多折叠，操作列宽 290→560
   - 「测量对象」列名统一改为「被测参数」（含GRR、KAPPA）
   - 审核人列后新增「审核时间」列（reviewDate）
   - 确认状态列前新增「确认人」列（approver），确认状态列后新增「确认时间」列（approveDate）
   - 列顺序：…状态 → 审核人 → 审核时间 → 确认人 → 确认状态 → 确认时间
   - 表格横向滚动宽度 1500→2100
3. KAPPA台账：去掉「分辨力」「标准值」「上限」「下限」4列（条件列）
4. 稳定性台账：去掉「分辨力」列（条件列）
5. 分辨力去单位：线性/偏移、Cg/Cgk 台账分辨力值上一轮已全局清洗，自动无单位
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} MSA计划列表加录入时间列；五个台账页操作按钮平铺去折叠、手动分析改分析、测量对象改被测参数、加审核时间/确认人/确认时间列；KAPPA去分辨力标准值上下限、稳定性去分辨力\n")
    print('已写回 + 归档:', folder)
