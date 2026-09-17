# -*- coding: utf-8 -*-
"""① 创建弹窗：分计划预览条 → 层级预览树（总计划/分计划）
② 器具筛选：加「部门」列（对齐纪要：生产部设备按台账隶属部门识别、全部检测）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:100])
    s = s.replace(old, new, cnt)

# ① 筛选 state 加 fDept
rep("""  const [fVendor,setFVendor]=useState(); const [fModel,setFModel]=useState(); const [fProd,setFProd]=useState(); const [fProcess,setFProcess]=useState();""",
    """  const [fVendor,setFVendor]=useState(); const [fModel,setFModel]=useState(); const [fProd,setFProd]=useState(); const [fProcess,setFProcess]=useState(); const [fDept,setFDept]=useState();""",
    1, 'fdept-state')

# ② 过滤链加部门
rep("""    .filter(i=> !fProcess || i.process===fProcess)""",
    """    .filter(i=> !fProcess || i.process===fProcess)
    .filter(i=> !fDept || i.dept===fDept)""",
    1, 'fdept-filter')

# ③ 筛选区加「部门」列（全部器具时显示，放在工序后）
rep("""          <Col xs={24} sm={12} lg={4}><span className="flt-label">工序（用途）</span><Select size="small" allowClear style={{width:140}} placeholder="工序（用途）" value={fProcess} options={[...new Set(d.instruments.map(i=>i.process).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProcess}/></Col>
        </>}""",
    """          <Col xs={24} sm={12} lg={4}><span className="flt-label">工序（用途）</span><Select size="small" allowClear style={{width:140}} placeholder="工序（用途）" value={fProcess} options={[...new Set(d.instruments.map(i=>i.process).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProcess}/></Col>
          <Col xs={24} sm={12} lg={4}><span className="flt-label">部门</span><Select size="small" allowClear style={{width:140}} placeholder="使用部门" value={fDept} options={[...new Set(d.instruments.map(i=>i.dept).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFDept}/></Col>
        </>}""",
    1, 'fdept-col')

# ④ 层级预览树替换原 Alert
rep("""        {mMethods.length>0 && <Col span={24}><Alert type="info" showIcon message={'将生成 '+mMethods.length+' 个分计划（取样计划）：'+mMethods.map(an=>ANAL_SHORT[an]+'（'+subRuleBrief(an)+'）').join(' / ')} style={{marginTop:8}}/></Col>}""",
    """        {mMethods.length>0 && <Col span={24}>
          <div style={{border:'1px solid #b7eb8f', background:'#f6ffed', borderRadius:6, padding:'8px 10px', marginTop:6}}>
            <div style={{fontWeight:600, fontSize:13, marginBottom:6}}>计划层级预览（1 总计划 = N 分计划）</div>
            <div style={{padding:'5px 8px', border:'1px solid #91caff', background:'#e6f4ff', borderRadius:5, fontSize:13, marginBottom:4}}>
              📋 总计划 × {(selKeys.length>0? selKeys.length : 1)}（每台器具 1 个总计划）{selKeys.length>0? '｜已选 '+selKeys.length+' 台器具' : '｜尚未勾选器具'}
            </div>
            <div style={{marginLeft:16, borderLeft:'2px solid #d9d9d9', paddingLeft:12}}>
              {mMethods.map(an=>(
                <div key={an} style={{padding:'4px 8px', border:'1px solid #e8e8e8', background:'#fff', borderRadius:5, marginBottom:4, fontSize:13, display:'flex', gap:8, alignItems:'center', flexWrap:'wrap'}}>
                  <Tag color={ANAL_COLOR[an]} style={{marginRight:0}}>{ANAL_SHORT[an]}</Tag>
                  <span>取样：{subRuleBrief(an)}</span>
                  <span style={{color:'#8c8c8c'}}>→ 生成 {ANAL_SHORT[an]} 台账「待采集」分析单</span>
                </div>
              ))}
            </div>
          </div>
        </Col>}""",
    1, 'level-preview')

open(P, 'w', encoding='utf-8').write(s)
print('level-preview OK 长度', len(s))
