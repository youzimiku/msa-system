# -*- coding: utf-8 -*-
"""v2.6 第一批 b：插入 CharPage/SamplingPage 组件 + 状态/提示补充"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:80])
    s = s.replace(old, new, cnt)

# ---------- statusColor 补 启用/停用 ----------
rep("                 '草稿':'default','待执行':'orange','样本准备中':'processing','数据采集中':'blue','分析中':'cyan','已完成':'green' },",
    "                 '草稿':'default','待执行':'orange','样本准备中':'processing','数据采集中':'blue','分析中':'cyan','已完成':'green',\n                 '启用':'green','停用':'default' },",
    1, 'statusColor')

# ---------- TIPS 补 charType / 启用停用 ----------
rep("  sample: {'已测量':'该样本已完成测量','待测量':'该样本等待测量','已作废':'该样本已作废'}\n};",
    "  sample: {'已测量':'该样本已完成测量','待测量':'该样本等待测量','已作废':'该样本已作废'},\n  charType: {'SC':'关键特性（Safety/Critical）：影响安全法规或功能的关键尺寸，须全量覆盖 MSA 监控','CC':'重要特性（Critical Characteristic）：影响装配/性能/客户要求的重要特性，纳入周期 MSA','普通':'一般特性：非特殊特性，按量具风险管理需要开展 MSA'},\n  status2: {'启用':'基础数据生效，可用于计划创建','停用':'基础数据停用，不再参与选择'}\n};",
    1, 'TIPS')

# ---------- 插入组件 ----------
COMP = """
/* ================= 质量特性维护（基础数据） ================= */
function CharPage(){
  const d=Store.get();
  const [kw,setKw]=useState('');
  const [fType,setFType]=useState();
  const [fStatus,setFStatus]=useState();
  const [detail,setDetail]=useState(null);
  const [modal,setModal]=useState(null);
  const rows=(d.characteristics||[]).filter(r=>(!kw || (r.id+r.name+r.partName+r.processName).includes(kw)))
    .filter(r=>!fType || r.type===fType).filter(r=>!fStatus || r.status===fStatus);
  const cols=[
    {title:'操作', width:150, fixed:'left', render:(_,r)=><Space size={4}>
      <Button size="small" type="primary" onClick={()=>setDetail(r)}>查看</Button>
      <Button size="small" onClick={()=>setModal({record:r})}>编辑</Button>
      <Button size="small" danger={r.status==='启用'} onClick={()=>{mut(s=>{const g=s.characteristics.find(x=>x.id===r.id);g.status=r.status==='启用'?'停用':'启用';logAction(s.me.name,r.status==='启用'?'停用特性':'启用特性',g.id,g.name);});toast.ok('已'+(r.status==='启用'?'停用':'启用'));}}>{r.status==='启用'?'停用':'启用'}</Button>
    </Space>},
    {title:'特性编号', dataIndex:'id', width:130, render:v=><span className="mono">{v}</span>},
    {title:'特性名称', dataIndex:'name', width:170, ellipsis:true},
    {title:'特性类型', dataIndex:'type', width:90, render:v=><Tooltip title={TIPS.charType[v]||v}><Tag color={v==='SC'?'red':v==='CC'?'orange':'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},
    {title:'所属零件', dataIndex:'partName', width:100, ellipsis:true},
    {title:'工序', dataIndex:'processName', width:90, ellipsis:true},
    {title:'特性类别', dataIndex:'category', width:90},
    {title:'单位', dataIndex:'unit', width:64, render:v=><span className="mono">{v||'—'}</span>},
    {title:'标准值', dataIndex:'target', width:80, render:v=><span className="mono">{v||'—'}</span>},
    {title:'上限USL', dataIndex:'usl', width:80, render:v=><span className="mono">{v||'—'}</span>},
    {title:'下限LSL', dataIndex:'lsl', width:80, render:v=><span className="mono">{v||'—'}</span>},
    {title:'来源', dataIndex:'source', width:140, ellipsis:true},
    {title:'关联检验标准', dataIndex:'standardId', width:110, render:(v,r)=><span className="row-link mono" onClick={()=>NavAPI.go('standard')}>{v||'—'}</span>},
    {title:'状态', dataIndex:'status', width:80, render:v=><Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},
    {title:'录入人', dataIndex:'editor', width:100},
    {title:'录入时间', dataIndex:'editorDate', width:100, render:v=><span className="mono">{v}</span>}
  ];
  return <div>
    <PageHead title="质量特性维护" sub="质量特性基础数据（SC/CC/普通），MSA 计划创建时引用"/>
    <Panel>
      <Space wrap size={10}>
        <Input.Search allowClear placeholder="特性编号 / 名称 / 零件 / 工序" style={{width:220}} onSearch={setKw} onChange={e=>!e.target.value&&setKw('')}/>
        <Select allowClear placeholder="特性类型" style={{width:140}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} value={fType} onChange={setFType}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fStatus} onChange={setFStatus}/>
        <Button type="primary" onClick={()=>setModal({})}>新增特性</Button>
      </Space>
    </Panel>
    <Panel>
      <Table rowKey="id" size="small" dataSource={rows} scroll={{x:1500}} pagination={{pageSize:10,showTotal:t=>'共 '+t+' 条'}} columns={cols}/>
    </Panel>
    {detail && <Drawer title={detail.id+' · '+detail.name} width={620} open onClose={()=>setDetail(null)}>
      <Descriptions column={2} size="small" bordered items={[
        {key:'id',label:'特性编号',children:<span className="mono">{detail.id}</span>},
        {key:'name',label:'特性名称',children:detail.name},
        {key:'type',label:'特性类型',children:<Tag color={detail.type==='SC'?'red':detail.type==='CC'?'orange':'default'}>{detail.type}</Tag>},
        {key:'category',label:'特性类别',children:detail.category},
        {key:'partName',label:'所属零件',children:detail.partName},
        {key:'processName',label:'工序',children:detail.processName},
        {key:'unit',label:'单位',children:detail.unit||'—'},
        {key:'target',label:'标准值',children:detail.target||'—'},
        {key:'usl',label:'上限USL',children:detail.usl||'—'},
        {key:'lsl',label:'下限LSL',children:detail.lsl||'—'},
        {key:'source',label:'来源',children:detail.source||'—'},
        {key:'standardId',label:'关联检验标准',children:<span className="mono">{detail.standardId||'—'}</span>},
        {key:'status',label:'状态',children:<Tooltip title={TIPS.status2[detail.status]||detail.status}><Tag color={ENUM.statusColor[detail.status]||'default'}>{detail.status}</Tag></Tooltip>},
        {key:'editor',label:'录入人',children:detail.editor||'—'},
        {key:'editorDate',label:'录入时间',children:detail.editorDate||'—'},
        {key:'note',label:'备注',children:detail.note||'—', span:2}
      ]}/>
    </Drawer>}
    {modal && <CharModal value={modal} onClose={()=>setModal(null)}/>}
  </div>;
}

function CharModal({value,onClose}){
  const [form]=Form.useForm();
  const d=Store.get();
  const revise=value.record;
  useEffect(()=>{
    if(revise) form.setFieldsValue(revise);
    else form.setFieldsValue({type:'普通', category:'计量型', status:'启用', editor:d.me.name, editorDate:TODAY, id:'CHAR-2026-0'+(d.characteristics.length+1)});
  },[]);
  const onOk=async()=>{
    const v=await form.validateFields();
    mut(s=>{
      if(revise){ Object.assign(s.characteristics.find(x=>x.id===revise.id), v); logAction(s.me.name,'编辑特性',v.id,v.name); }
      else { s.characteristics.unshift(v); logAction(s.me.name,'新增特性',v.id,v.name); }
    });
    toast.ok(revise?'已保存':'已新增'); onClose();
  };
  return <Modal title={revise?'编辑质量特性':'新增质量特性'} open width={760} onCancel={onClose} onOk={onOk} okText="保存" destroyOnClose>
    <Form form={form} layout="vertical" size="small">
      <Row gutter={12}>
        <Col span={6}><Form.Item name="id" label="特性编号"><Input disabled={revise}/></Form.Item></Col>
        <Col span={12}><Form.Item name="name" label="特性名称" rules={[{required:true}]}><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="type" label="特性类型" rules={[{required:true}]}><Select options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]}/></Form.Item></Col>
        <Col span={6}><Form.Item name="partName" label="所属零件"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="processName" label="工序"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="category" label="特性类别"><Select options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]}/></Form.Item></Col>
        <Col span={6}><Form.Item name="unit" label="单位"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="target" label="标准值"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="usl" label="上限USL"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="lsl" label="下限LSL"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="standardId" label="关联检验标准"><Select allowClear options={(d.standards||[]).map(s=>({value:s.id,label:s.id}))}/></Form.Item></Col>
        <Col span={12}><Form.Item name="source" label="来源"><Input placeholder="如：CP-控制计划号"/></Form.Item></Col>
        <Col span={6}><Form.Item name="status" label="状态"><Select options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/></Form.Item></Col>
        <Col span={24}><Form.Item name="note" label="备注"><Input.TextArea rows={2}/></Form.Item></Col>
      </Row>
    </Form>
  </Modal>;
}

/* ================= 抽样方法维护（基础数据） ================= */
function SamplingPage(){
  const d=Store.get();
  const [kw,setKw]=useState('');
  const [fNeed,setFNeed]=useState();
  const [fSt,setFSt]=useState();
  const [mModal,setMModal]=useState(null);
  const [rModal,setRModal]=useState(null);
  const mRows=(d.anMethods||[]).filter(r=>(!kw || (r.code+r.name).toLowerCase().includes(kw.toLowerCase())))
    .filter(r=>!fNeed || r.needSample===fNeed).filter(r=>!fSt || r.status===fSt);
  const rRows=(d.samplingRules||[]).slice();
  const methodCols=[
    {title:'操作', width:110, fixed:'left', render:(_,r)=><Space size={4}>
      <Button size="small" type="primary" onClick={()=>setMModal({record:r})}>编辑</Button>
      <Button size="small" danger={r.status==='启用'} onClick={()=>{mut(s=>{const g=s.anMethods.find(x=>x.code===r.code);g.status=r.status==='启用'?'停用':'启用';});toast.ok('已'+(r.status==='启用'?'停用':'启用'));}}>{r.status==='启用'?'停用':'启用'}</Button>
    </Space>},
    {title:'方法代码', dataIndex:'code', width:110, render:v=><span className="mono">{v}</span>},
    {title:'方法名称', dataIndex:'name', width:230},
    {title:'是否需要取样', dataIndex:'needSample', width:100, render:v=><Tag color={v==='是'?'blue':'default'}>{v}</Tag>},
    {title:'可否合并取样', dataIndex:'canMerge', width:100, render:v=><Tag color={v==='是'?'green':'default'}>{v}</Tag>},
    {title:'合并对象', dataIndex:'mergeWith', width:90, render:v=><span className="mono">{v||'—'}</span>},
    {title:'默认适用', dataIndex:'defaultType', width:90},
    {title:'状态', dataIndex:'status', width:80, render:v=><Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},
    {title:'备注', dataIndex:'note', width:280, ellipsis:true}
  ];
  const ruleCols=[
    {title:'操作', width:90, fixed:'left', render:(_,r)=><Button size="small" type="primary" onClick={()=>setRModal({record:r})}>编辑</Button>},
    {title:'规则编号', dataIndex:'id', width:100, render:v=><span className="mono">{v}</span>},
    {title:'所属方法', dataIndex:'method', width:110, render:v=><span className="mono">{v}</span>},
    {title:'策略类别', dataIndex:'category', width:90},
    {title:'默认样品数', dataIndex:'sampleDefault', width:96, render:v=><span className="mono">{v}</span>},
    {title:'默认人数', dataIndex:'opsDefault', width:90, render:v=><span className="mono">{v}</span>},
    {title:'默认次数', dataIndex:'trialsDefault', width:90, render:v=><span className="mono">{v}</span>},
    {title:'样品数范围', width:100, render:(_,r)=><span className="mono">{r.sampleMin}~{r.sampleMax}</span>},
    {title:'人数范围', width:88, render:(_,r)=><span className="mono">{r.opsMin}~{r.opsMax}</span>},
    {title:'次数范围', width:88, render:(_,r)=><span className="mono">{r.trialsMin}~{r.trialsMax}</span>},
    {title:'读数建议', dataIndex:'readings', width:90, render:v=><span className="mono">{v}</span>},
    {title:'策略说明', dataIndex:'note', width:440, ellipsis:true}
  ];
  return <div>
    <PageHead title="抽样方法维护" sub="七大检测分析方法代码表 + 取样规则（默认值可调，计划创建时引用）"/>
    <Panel>
      <Space wrap size={10}>
        <Input.Search allowClear placeholder="方法代码 / 名称" style={{width:220}} onSearch={setKw} onChange={e=>!e.target.value&&setKw('')}/>
        <Select allowClear placeholder="是否需要取样" style={{width:140}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} value={fNeed} onChange={setFNeed}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fSt} onChange={setFSt}/>
        <Button type="primary" onClick={()=>setMModal({})}>新增方法</Button>
        <Button onClick={()=>setRModal({})}>新增取样规则</Button>
      </Space>
    </Panel>
    <Panel title="分析方法代码表">
      <Table rowKey="code" size="small" dataSource={mRows} scroll={{x:1200}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={methodCols}/>
    </Panel>
    <Panel title="取样规则表">
      <Table rowKey="id" size="small" dataSource={rRows} scroll={{x:1700}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={ruleCols}/>
    </Panel>
    {mModal && <MethodModal value={mModal} onClose={()=>setMModal(null)}/>}
    {rModal && <RuleModal value={rModal} onClose={()=>setRModal(null)}/>}
  </div>;
}

function MethodModal({value,onClose}){
  const [form]=Form.useForm();
  const d=Store.get();
  const revise=value.record;
  useEffect(()=>{
    if(revise) form.setFieldsValue(revise);
    else form.setFieldsValue({code:'', name:'', needSample:'是', canMerge:'否', mergeWith:'', defaultType:'计量型', status:'启用'});
  },[]);
  const onOk=async()=>{
    const v=await form.validateFields();
    mut(s=>{
      if(revise){ Object.assign(s.anMethods.find(x=>x.code===revise.code), v); logAction(s.me.name,'编辑方法',v.code,v.name); }
      else { s.anMethods.push(v); logAction(s.me.name,'新增方法',v.code,v.name); }
    });
    toast.ok(revise?'已保存':'已新增'); onClose();
  };
  return <Modal title={revise?'编辑分析方法':'新增分析方法'} open width={640} onCancel={onClose} onOk={onOk} okText="保存" destroyOnClose>
    <Form form={form} layout="vertical" size="small">
      <Row gutter={12}>
        <Col span={8}><Form.Item name="code" label="方法代码" rules={[{required:true}]}><Input disabled={revise}/></Form.Item></Col>
        <Col span={16}><Form.Item name="name" label="方法名称" rules={[{required:true}]}><Input/></Form.Item></Col>
        <Col span={8}><Form.Item name="needSample" label="是否需要取样"><Select options={[{value:'是',label:'是'},{value:'否',label:'否'}]}/></Form.Item></Col>
        <Col span={8}><Form.Item name="canMerge" label="可否合并取样"><Select options={[{value:'是',label:'是'},{value:'否',label:'否'}]}/></Form.Item></Col>
        <Col span={8}><Form.Item name="mergeWith" label="合并对象"><Select allowClear options={['GRR','KAPPA','LINEAR','BIAS','STABILITY','CGCGK','RES'].map(c=>({value:c,label:c}))}/></Form.Item></Col>
        <Col span={8}><Form.Item name="defaultType" label="默认适用"><Select options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]}/></Form.Item></Col>
        <Col span={8}><Form.Item name="status" label="状态"><Select options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/></Form.Item></Col>
        <Col span={24}><Form.Item name="note" label="备注"><Input.TextArea rows={2}/></Form.Item></Col>
      </Row>
    </Form>
  </Modal>;
}

function RuleModal({value,onClose}){
  const [form]=Form.useForm();
  const d=Store.get();
  const revise=value.record;
  useEffect(()=>{
    if(revise) form.setFieldsValue(revise);
    else form.setFieldsValue({id:'SR-0'+(d.samplingRules.length+1), method:'GRR', category:'其他', sampleDefault:10, sampleMin:1, sampleMax:30, opsDefault:3, opsMin:1, opsMax:5, trialsDefault:3, trialsMin:2, trialsMax:5, useOps:true, readings:''});
  },[]);
  const onOk=async()=>{
    const v=await form.validateFields();
    mut(s=>{
      if(revise){ Object.assign(s.samplingRules.find(x=>x.id===revise.id), v); logAction(s.me.name,'编辑取样规则',v.id,'方法 '+v.method); }
      else { s.samplingRules.push(v); logAction(s.me.name,'新增取样规则',v.id,'方法 '+v.method); }
    });
    toast.ok(revise?'已保存':'已新增'); onClose();
  };
  return <Modal title={revise?'编辑取样规则':'新增取样规则'} open width={680} onCancel={onClose} onOk={onOk} okText="保存" destroyOnClose>
    <Form form={form} layout="vertical" size="small">
      <Row gutter={12}>
        <Col span={6}><Form.Item name="id" label="规则编号"><Input disabled={revise}/></Form.Item></Col>
        <Col span={6}><Form.Item name="method" label="所属方法" rules={[{required:true}]}><Select options={['GRR','KAPPA','linear','stability','cgcgk','resolution'].map(c=>({value:c,label:c}))}/></Form.Item></Col>
        <Col span={6}><Form.Item name="category" label="策略类别"><Select options={[{value:'线性类',label:'线性类'},{value:'稳定性类',label:'稳定性类'},{value:'其他',label:'其他'}]}/></Form.Item></Col>
        <Col span={6}><Form.Item name="useOps" label="是否按人数取样"><Select options={[{value:true,label:'是'},{value:false,label:'否'}]}/></Form.Item></Col>
        <Col span={6}><Form.Item name="sampleDefault" label="默认样品数"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="opsDefault" label="默认人数"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="trialsDefault" label="默认次数"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="readings" label="读数建议"><Input/></Form.Item></Col>
        <Col span={6}><Form.Item name="sampleMin" label="样品数下限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="sampleMax" label="样品数上限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="opsMin" label="人数下限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="opsMax" label="人数上限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="trialsMin" label="次数下限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={6}><Form.Item name="trialsMax" label="次数上限"><InputNumber style={{width:'100%'}} min={0}/></Form.Item></Col>
        <Col span={24}><Form.Item name="note" label="策略说明"><Input.TextArea rows={2}/></Form.Item></Col>
      </Row>
    </Form>
  </Modal>;
}

"""
rep("/* ============================================================================\n *  样本管理 / 样本录入 / GRR 台账\n * ==========================================================================*/",
    COMP + "/* ============================================================================\n *  样本管理 / 样本录入 / GRR 台账\n * ==========================================================================*/",
    1, 'insert-components')

open(P, 'w', encoding='utf-8').write(s)
print('batch1b OK 长度', len(s))
