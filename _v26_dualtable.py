# -*- coding: utf-8 -*-
"""MSA计划页调整：
① 去掉 创建MSA计划 右侧 5 个「转 xxx」按钮（批量定型入口移除，详情内单计划定型保留）
② 列表改上下双表：上=MSA计划（点行选中），下=当前选中计划的分析单（分计划）信息
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:110])
    s = s.replace(old, new, cnt)

# ① 删除 selectedRowKeys state
rep("""  const [selectedRowKeys,setSelectedRowKeys]=useState([]); // 勾选用于转分析方法
""", "", 1, 'sel-state')

# ② 删除批量转方法函数 doConvert（含注释与行首缩进）
OLD_DC = """  // 转分析方法（GRR / KAPPA / 线性偏移 / 稳定性 / CgCgk）：将勾选计划的分析关联类型改为对应方法，生成台账「待采集」记录，并跳转对应录入数据页；一个计划可追加多个方法（一计划多任务）
  const doConvert=(t)=>{
    if(!selectedRowKeys.length){ toast.warn('请先在列表中勾选要转 '+ANAL_SHORT[t]+' 的 MSA 计划'); return; }
    let done=0, skipped=0, firstRid='';
    mut(s=>{
      selectedRowKeys.forEach(id=>{
        const p=s.plans.find(x=>x.id===id); if(!p) return;
        if(planRecords(s,id).some(r=>recKindId(r)===t)){ skipped++; return; } // 已存在该方法记录的不重复转换
        const std=(d.standards||[]).find(st=>st.status==='启用'&&(stdTypeOf(st.id)===t || ['linear','stability','cgcgk'].indexOf(t)>=0) && (!p.partName||p.partName==='—'||st.partName===p.partName));
        if(!std){ skipped++; return; } // 该零件无匹配类型标准
        const params=TYPE_PARAMS[t]? {...TYPE_PARAMS[t], ops:TYPE_PARAMS[t].ops, trials:TYPE_PARAMS[t].trials, parts:TYPE_PARAMS[t].parts} : {ops:3, trials:3, parts:10};
        const had=p.type||planRecords(s,id).length;
        if(!had) p.type=t;
        p.method=ENUM.taskMethod[t][0]; p.standard=std.id; p.params=params;
        p.dept=p.dept||'质量'; p.dataType=(t==='KAPPA'?'计数型':'计量型'); p.opMethod=p.opMethod||'《测量系统分析操作指导书》';
        p.msaMethods=[...new Set([...(p.msaMethods||[]), ...msaExcelMap(t)].filter(Boolean))];
        p.methods=[...new Set([...(p.methods||[]), t])];
        const instIds = (p.instIds&&p.instIds.length)? p.instIds : [p.instId];
        let rid='';
        instIds.forEach(iid=>{
          const inst=s.instruments.find(i=>i.id===iid);
          rid=spawnRecord(s, p.id, { type:t, standard:std.id, method:ENUM.taskMethod[t][0], params,
            object:p.object, instId:iid, instName:inst?inst.name:'', owner:p.owner||s.me.name, note:'顶部按钮转 '+ANAL_SHORT[t]+'，待台账页录入数据' });
          if(!firstRid) firstRid=rid;
        });
        p.recordId=rid;
        syncPlanFromRecord(s,p.id);
        logAction(s.me.name,'计划定型',p.id,'批量转 '+ANAL_SHORT[t]+' · '+std.id+'，生成台账记录');
        done++;
      });
    });
    if(!done){ toast.warn('所选计划均缺少匹配的 '+ANAL_SHORT[t]+' 检验标准或已存在该方法记录，未执行转换'); setSelectedRowKeys([]); return; }
    if(done) toast.ok('已转 '+ANAL_SHORT[t]+' '+done+' 个计划（生成台账待采集记录），跳转对应「录入数据」页');
    if(skipped) toast.warn(skipped+' 个计划已存在该方法记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    if(firstRid){ if(t==='GRR') NavAPI.openGrr(firstRid); else if(t==='KAPPA') NavAPI.openKappa(firstRid); else NavAPI.openAnl(t, firstRid); }
    else NavAPI.go(t==='GRR'?'entry_grr': t==='KAPPA'?'entry_kappa':'entry_'+t);
  };;
"""
assert s.count(OLD_DC) == 1, 'doConvert 定位失败 %d' % s.count(OLD_DC)
s = s.replace(OLD_DC, "", 1)

# ③ 加 curPlan 选中 state（放在 doQuery 定义后）
rep("""  const doQuery=()=>{ setQkw(fkw); setQType(ftype); setQStatus(fstatus); };""",
    """  const doQuery=()=>{ setQkw(fkw); setQType(ftype); setQStatus(fstatus); };
  const [curPlan,setCurPlan]=useState(null); // 当前选中计划（下栏展示其分析单）
  const cur = curPlan && rows.some(p=>p.id===curPlan.id) ? curPlan : (rows[0]||null);""",
    1, 'curplan')

# ④ 查询栏文案去掉已勾选
rep("""<span className="tiny">已勾选 {selectedRowKeys.length} 个计划 ｜ 共 {rows.length} 条</span>""",
    """<span className="tiny">共 {rows.length} 条</span>""",
    1, 'cnt-text')

# ⑤ 删除 5 个转方法按钮
rep("""        <Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={()=>setBatchModal({})}>⚡ 创建MSA计划</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('GRR')}>转 GRR</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('KAPPA')}>转 KAPPA</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('linear')}>转线性偏移</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('stability')}>转稳定性</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('cgcgk')}>转 Cg/Cgk</Button>""",
    """        <Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={()=>setBatchModal({})}>⚡ 创建MSA计划</Button>""",
    1, 'conv-btns')

# ⑥ 上列表：去 rowSelection/expandable，行点击选中；下方追加「当前计划的分析单」面板
rep("""    <Panel title="MSA 计划列表">
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:4400}} pagination={false}
        rowSelection={{ selectedRowKeys, onChange:setSelectedRowKeys }}
        expandable={{ expandedRowRender:(r)=>{ const recs=planRecords(d,r.id); return recs.length? <Table rowKey="id" size="small" dataSource={recs} columns={subPlanCols()} pagination={false} scroll={{x:960}}/> : <span className="tiny">该计划尚未定型，无分计划</span>; } }}/>
    </Panel>""",
    """    <Panel title="MSA 计划列表">
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:4400}} pagination={false}
        onRow={r=>({ onClick:()=>setCurPlan(r), style:{cursor:'pointer'} })}
        rowClassName={r=> cur && r.id===cur.id ? 'row-selected' : ''}/>
    </Panel>
    <Panel title={'当前计划的分析单：'+(cur? cur.id+(cur.instName?' '+cur.instName:'') : '请选择计划')}>
      {cur? <Table rowKey="id" size="middle" dataSource={planRecords(d,cur.id)} columns={subPlanCols()} scroll={{x:960}} pagination={false}/> : <span className="tiny">请先在上方列表选择 MSA 计划</span>}
    </Panel>""",
    1, 'dual-table')

# ⑦ 选中行高亮样式
rep(""".row-link{color:#333333;cursor:pointer}
""",
    """.row-link{color:#333333;cursor:pointer}
.row-selected{background:#e6f4ff !important;cursor:pointer}
""",
    1, 'css')

open(P, 'w', encoding='utf-8').write(s)
print('dualtable OK 长度', len(s))
