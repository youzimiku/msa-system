# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()
orig_len = len(t)

def rep(old, new):
    global t
    assert t.count(old) == 1, ('锚点不唯一或不存在: %s...' % old[:60])
    t = t.replace(old, new)

# R1 状态行
rep("  const [anlRec,setAnlRec]=useState(null); const [opsRec,setOpsRec]=useState(null); const [prevRec,setPrevRec]=useState(null);",
    "  const [anlRec,setAnlRec]=useState(null); const [opsRec,setOpsRec]=useState(null); const [prevRec,setPrevRec]=useState(null);\n  const [pickRec,setPickRec]=useState(null); const [pickedMap,setPickedMap]=useState({});")

# R2 操作列宽度+首按钮
rep("    {title:'操作', width:560, fixed:'left', render:(_,r)=><Space size={0} wrap>\n      <Button size=\"small\" type=\"link\" onClick={()=>setAuditOpen(true)}>审核</Button>",
    "    {title:'操作', width:680, fixed:'left', render:(_,r)=><Space size={0} wrap>\n      <Button size=\"small\" type=\"link\" onClick={()=>setPickRec(r)}>样本/人员选择</Button>\n      <Button size=\"small\" type=\"link\" onClick={()=>setAuditOpen(true)}>审核</Button>")

# R3 录入数据按钮后加已选 Tag
rep("      <Button size=\"small\" type=\"link\" disabled={!canDo(d.me.role,'edit')||r.reviewStatus!=='待采集'} onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>录入数据</Button>\n    </Space>},",
    "      <Button size=\"small\" type=\"link\" disabled={!canDo(d.me.role,'edit')||r.reviewStatus!=='待采集'} onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>录入数据</Button>\n      {pickedMap[r.id]&&<Tooltip title={'样本：'+((pickedMap[r.id].samples||[]).map(s=>s.id).join('、')||'—')+'；人员：'+((pickedMap[r.id].ops||[]).join('、')||'—')}><Tag color=\"blue\">{(pickedMap[r.id].samples||[]).length}样本/{(pickedMap[r.id].ops||[]).length}人</Tag></Tooltip>}\n    </Space>},")

# R4 挂载 SamplePersonModal
rep("    {auditOpen && <Modal cancelText=\"取消\" title=\"审核 · 选择审核人员\"",
    "    {pickRec && <SamplePersonModal rec={pickRec} picked={pickedMap[pickRec.id]} onOk={(samples,ops)=>{ setPickedMap(p=>{const n={...p}; n[pickRec.id]={samples:samples,ops:ops}; return n;}); setPickRec(null); }} onClose={()=>setPickRec(null)}/>}\n    {auditOpen && <Modal cancelText=\"取消\" title=\"审核 · 选择审核人员\"")

# R5 插入组件函数
rep("function ImportPreviewModal({rec, kind, onClose}){",
    """function SamplePersonModal({rec, picked, onOk, onClose}){
  const d=Store.get();
  const OPS=['王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'];
  const [kw,setKw]=useState('');
  const [selS,setSelS]=useState((picked&&picked.samples?picked.samples:[]).map(s=>s.id));
  const [selP,setSelP]=useState(picked&&picked.ops?picked.ops:[]);
  const samples=(d.sampleLib||[]).filter(s=>!kw||(s.id+s.name+(s.partNo||'')+(s.charDim||'')).toLowerCase().includes(kw.toLowerCase()));
  return <Modal cancelText="取消" title={'样本/人员选择 · '+(rec?rec.id:'')} open width={900} okText="确定" destroyOnClose
    onOk={()=>{ if(!selS.length){ toast.warn('请至少选择一个样本'); return; } if(!selP.length){ toast.warn('请至少选择一名人员'); return; }
      const chosenSamples=samples.filter(s=>selS.includes(s.id)); onOk(chosenSamples, selP); toast.ok('已选择 '+chosenSamples.length+' 个样本、'+selP.length+' 名人员'); }}
    onCancel={onClose}>
    <div style={{marginBottom:8,fontSize:14,color:'#333333'}}>第一步：选择本次使用的样本（来自样本库，可多选）</div>
    <Input.Search allowClear placeholder="搜索 样本编号/名称/零件号/被测参数" style={{width:340,marginBottom:8}} value={kw} onChange={e=>setKw(e.target.value)}/>
    <Table size="small" rowKey="id" dataSource={samples} pagination={{pageSize:5,showTotal:t=>'共 '+t+' 条'}} scroll={{y:210}}
      rowSelection={{selectedRowKeys:selS, onChange:setSelS}}
      columns={[
        {title:'样本编号', dataIndex:'id', width:90},
        {title:'样本名称', dataIndex:'name', width:190, ellipsis:true},
        {title:'零件号', dataIndex:'partNo', width:90, render:(v)=><span>{v||'—'}</span>},
        {title:'被测参数', dataIndex:'charDim', width:150, ellipsis:true},
        {title:'真值', dataIndex:'refValue', width:90, render:(v)=><span>{v||'—'}</span>},
        {title:'有效期至', dataIndex:'expireDate', width:100, render:(v)=><span>{v||'—'}</span>},
        {title:'状态', dataIndex:'status', width:70, render:(v)=><Tag color={v==='启用'?'green':'default'}>{v}</Tag>}
      ]}/>
    <Divider style={{margin:'12px 0'}}/>
    <div style={{marginBottom:8,fontSize:14,color:'#333333'}}>第二步：选择操作/分析人员（可多选）</div>
    <Space wrap>
      {OPS.map(n=>{ const on=selP.includes(n); return <Tag key={n} color={on?'blue':'default'} style={{cursor:'pointer',padding:'3px 12px',fontSize:13}} onClick={()=>setSelP(on?selP.filter(x=>x!==n):[...selP,n])}>{n}</Tag>; })}
    </Space>
  </Modal>;
}
function ImportPreviewModal({rec, kind, onClose}){""")

io.open(P, 'w', encoding='utf-8').write(t)
print('替换完成，文件长度', orig_len, '->', len(t))
