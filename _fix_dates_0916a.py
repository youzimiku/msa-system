# -*- coding: utf-8 -*-
import io

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
c = io.open(path, encoding='utf-8').read()

def rep(old, new, tag):
    global c
    n = c.count(old)
    assert n == 1, f'{tag}: found {n}'
    c = c.replace(old, new)
    print('OK', tag)

# ===== 公共 FDate/FDateTime 组件（antd 解构与 NOW 之后） =====
anchor = "const NOW = (window.dayjs && dayjs().format('YYYY-MM-DD HH:mm:ss')) || TODAY+' 09:00:00';"
assert c.count(anchor) == 1
comp = anchor + """

/* 日期/日期时间输入控件：内部完成 dayjs<->字符串转换（Form 与行内编辑均存字符串） */
const _toD = v => (v && v!=='—' && v!=='暂无' && v!=='待维护' && v!=='-' && dayjs(v).isValid()) ? dayjs(v) : null;
function FDate({value,onChange,showTime,format,...rest}){
  return <DatePicker {...rest} showTime={showTime} format={format||(showTime?'YYYY-MM-DD HH:mm:ss':'YYYY-MM-DD')} value={_toD(value)} onChange={(d)=>onChange(d ? (showTime? d.format('YYYY-MM-DD HH:mm:ss') : d.format('YYYY-MM-DD')) : '')}/>;
}"""
c = c.replace(anchor, comp)
print('OK FDate 组件')

# ===== A. 器具台账新增弹窗 =====
rep('<Col span={6}><Form.Item name="buy" label="购置年月日"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="buy" label="购置年月日"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'buy')
rep('<Col span={6}><Form.Item name="ledgerDate" label="入账时间"><Input placeholder="YYYY-MM-DD 或 YYYY-MM-DD HH:mm"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="ledgerDate" label="入账时间"><FDate showTime style={{width:\'100%\'}}/></Form.Item></Col>', 'ledgerDate')
rep('<Col span={6}><Form.Item name="ymd" label="年月日"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="ymd" label="年月日"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'ymd')
rep('<Col span={6}><Form.Item name="lastCal" label="校准时间"><Input placeholder="上次校准 YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="lastCal" label="校准时间"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'lastCal')
rep('<Col span={6}><Form.Item name="nextCal" label="下次校准日期"><Input placeholder="自动=上次+周期"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="nextCal" label="下次校准日期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'nextCal')

# ===== B. 登记校准弹窗 =====
rep('<Col span={12}><Form.Item name="calDate" label="校准日期" rules={[{required:true}]}><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={12}><Form.Item name="calDate" label="校准日期" rules={[{required:true}]}><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'calDate')

# ===== C. 器具组列表行内（新增/编辑） =====
rep('render:(v,r)=>isNew(r)?<Input size="small" value={draft.lastExec||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setDraft(d=>({...d,lastExec:e.target.value}))}/>:<Input size="small" value={r.lastExec||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setF(r,\'lastExec\',e.target.value)}/>',
    'render:(v,r)=>isNew(r)?<FDate size="small" style={{width:110}} value={draft.lastExec||\'\'} onChange={x=>setDraft(d=>({...d,lastExec:x}))}/>:<FDate size="small" style={{width:110}} value={r.lastExec||\'\'} onChange={x=>setF(r,\'lastExec\',x)}/>', 'lastExec 行内')
rep('render:(v,r)=>isNew(r)?<Input size="small" value={draft.nextPlanDate||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setDraft(d=>({...d,nextPlanDate:e.target.value}))}/>:<Input size="small" value={r.nextPlanDate||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setF(r,\'nextPlanDate\',e.target.value)}/>',
    'render:(v,r)=>isNew(r)?<FDate size="small" style={{width:110}} value={draft.nextPlanDate||\'\'} onChange={x=>setDraft(d=>({...d,nextPlanDate:x}))}/>:<FDate size="small" style={{width:110}} value={r.nextPlanDate||\'\'} onChange={x=>setF(r,\'nextPlanDate\',x)}/>', 'nextPlanDate 行内')
rep('render:(v,r)=>isNew(r)?<Input size="small" value={draft.nextRemind||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setDraft(d=>({...d,nextRemind:e.target.value}))}/>:<Input size="small" value={r.nextRemind||\'\'} placeholder="YYYY-MM-DD" onChange={e=>setF(r,\'nextRemind\',e.target.value)}/>',
    'render:(v,r)=>isNew(r)?<FDate size="small" style={{width:110}} value={draft.nextRemind||\'\'} onChange={x=>setDraft(d=>({...d,nextRemind:x}))}/>:<FDate size="small" style={{width:110}} value={r.nextRemind||\'\'} onChange={x=>setF(r,\'nextRemind\',x)}/>', 'nextRemind 行内')

# ===== D. 器具组弹窗 =====
rep('<Col span={6}><Form.Item name="lastExec" label="上次执行时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="lastExec" label="上次执行时间"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'lastExec 弹窗')
rep('<Col span={6}><Form.Item name="nextPlanDate" label="下次计划日期"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="nextPlanDate" label="下次计划日期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'nextPlanDate 弹窗')
rep('<Col span={6}><Form.Item name="nextRemind" label="下次提醒时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="nextRemind" label="下次提醒时间"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'nextRemind 弹窗')

# ===== E. MSA计划弹窗 =====
rep('<Col span={6}><Form.Item name="planDate" label="计划完成日期"><Input/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="planDate" label="计划完成日期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'planDate 计划弹窗')
rep('<Col span={8}><Form.Item name="actualDate" label="实际检期"><Input placeholder="实际完成分析日期 YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={8}><Form.Item name="actualDate" label="实际检期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'actualDate')
rep('<Col span={12}><Form.Item name="planDate" label="计划完成日期" initialValue={TODAY}><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={12}><Form.Item name="planDate" label="计划完成日期" initialValue={TODAY}><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'planDate 人员计划弹窗')

# ===== F. 检验标准弹窗 =====
rep('<Col span={8}><Form.Item name="effDate" label="生效日期"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={8}><Form.Item name="effDate" label="生效日期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'effDate')

# ===== G. 样本库行内 + 弹窗 =====
rep('render:(_,r)=><Input size="small" className="mono" value={r.expireDate||\'\'} onChange={e=>setF(r,\'expireDate\',e.target.value)}/>',
    'render:(_,r)=><FDate size="small" className="mono" style={{width:104}} value={r.expireDate||\'\'} onChange={x=>setF(r,\'expireDate\',x)}/>', 'expireDate 行内')
rep('<Col span={6}><Form.Item name="expireDate" label="有效期至"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={6}><Form.Item name="expireDate" label="有效期至"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'expireDate 弹窗')

# ===== H. 台账弹窗（选取日期） =====
rep('<Col span={12}><Form.Item name="pickDate" label="选取日期"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>',
    '<Col span={12}><Form.Item name="pickDate" label="选取日期"><FDate style={{width:\'100%\'}}/></Form.Item></Col>', 'pickDate')

io.open(path, 'w', encoding='utf-8').write(c)
print('ALL DONE')
