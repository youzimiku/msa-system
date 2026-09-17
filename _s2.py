# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    cnt = s.count(old)
    if cnt != 1:
        print('WARN count=%d for: %s' % (cnt, old[:60])); return
    s = s.replace(old, new)
    print('OK:', old[:46])

old_spawn = """/* 由计划生成一条台账记录（GRR/KAPPA），返回记录 id；供「创建时选标准自动定型」与「计划定型」共用 */
function spawnRecord(s, planId, o){
  const p = s.plans.find(x=>x.id===planId); if(!p) return '';
  const inst = s.instruments.find(i=>i.id===o.instId);
  if(o.type==='GRR'){
    const rid = 'GRR-'+TODAY.slice(0,4)+'-'+String(s.grr.length+1).padStart(3,'0');
    const opsN=o.params?Number(o.params.ops)||3:3, trialsN=o.params?Number(o.params.trials)||3:3, partsN=o.params?Number(o.params.parts)||10:10;
    s.grr.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
      method:o.method||'', standard:o.standard||'', numOps:opsN, numTrials:trialsN, numParts:partsN,
      sampleGroup:findSampleGroupForPlan(s,planId), tolerance:parseTol(o.object||p.object),
      operators:Array.from({length:opsN},(_,i)=>['操作员A','操作员B','操作员C','操作员D','操作员E'][i]),
      raw:null, analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  const rid = 'KPA-'+TODAY.slice(0,4)+'-'+String(s.kappa.length+1).padStart(3,'0');
  const opsN=o.params?Number(o.params.ops)||3:3, partsN=o.params?Number(o.params.parts)||30:30;
  s.kappa.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, kind:'计数型(合格/不合格)',
    standard:o.standard||'', numApp:opsN, numSamples:partsN, sampleGroup:findSampleGroupForPlan(s,planId),
    appNames:Array.from({length:opsN},(_,i)=>['检验员甲','检验员乙','检验员丙','检验员丁','检验员戊'][i]),
    reference:[], appData:[], analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
  return rid;
}"""

new_spawn = """/* 分析类型显示名与配色（会议口径：特性-量具-方法） */
const ANAL_SHORT = { 'GRR':'GRR','KAPPA':'KAPPA','linear':'线性/偏移','stability':'稳定性','cgcgk':'Cg/Cgk','resolution':'分辨率' };
const ANAL_COLOR = { 'GRR':'blue','KAPPA':'green','linear':'cyan','stability':'purple','cgcgk':'gold','resolution':'geekblue' };
function anTag(t){ return t? <Tag color={ANAL_COLOR[t]||'default'}>{ANAL_SHORT[t]||t}</Tag> : <Tag>未定型</Tag>; }
/* 由计划生成一条台账记录（6 类分析方法），返回记录 id；供「创建时按方法生成」与「计划定型」共用 */
function spawnRecord(s, planId, o){
  const p = s.plans.find(x=>x.id===planId); if(!p) return '';
  const inst = s.instruments.find(i=>i.id===o.instId);
  if(o.type==='GRR'){
    const rid = 'GRR-'+TODAY.slice(0,4)+'-'+String(s.grr.length+1).padStart(3,'0');
    const opsN=o.params?Number(o.params.ops)||3:3, trialsN=o.params?Number(o.params.trials)||3:3, partsN=o.params?Number(o.params.parts)||10:10;
    s.grr.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
      method:o.method||'均值-极差法(Xbar-R)', standard:o.standard||'', numOps:opsN, numTrials:trialsN, numParts:partsN,
      sampleGroup:findSampleGroupForPlan(s,planId), tolerance:parseTol(o.object||p.object),
      operators:Array.from({length:opsN},(_,i)=>['操作员A','操作员B','操作员C','操作员D','操作员E'][i]),
      raw:null, analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  if(o.type==='KAPPA'){
    const rid = 'KPA-'+TODAY.slice(0,4)+'-'+String(s.kappa.length+1).padStart(3,'0');
    const opsN=o.params?Number(o.params.ops)||3:3, partsN=o.params?Number(o.params.parts)||30:30;
    s.kappa.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, kind:'计数型(合格/不合格)',
      standard:o.standard||'', numApp:opsN, numSamples:partsN, sampleGroup:findSampleGroupForPlan(s,planId),
      appNames:Array.from({length:opsN},(_,i)=>['检验员甲','检验员乙','检验员丙','检验员丁','检验员戊'][i]),
      reference:[], appData:[], analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  if(o.type==='linear'){
    const rid = 'LIN-'+TODAY.slice(0,4)+'-'+String(s.linear.length+1).padStart(3,'0');
    s.linear.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
      method:o.method||'线性回归+偏移t检验（5标准件覆盖量程）', standard:o.standard||'', stds:5, per:10, points:5,
      refs:['','','','',''], raw:null, tolerance:parseTol(o.object||p.object),
      analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  if(o.type==='stability'){
    const rid = 'STB-'+TODAY.slice(0,4)+'-'+String(s.stability.length+1).padStart(3,'0');
    s.stability.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
      method:o.method||'均值-极差控制图（SPC判异模型）', standard:o.standard||'', groups:25, per:3, span:'4周~3个月',
      raw:null, tolerance:parseTol(o.object||p.object),
      analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  if(o.type==='cgcgk'){
    const rid = 'CG-'+TODAY.slice(0,4)+'-'+String(s.cgcgk.length+1).padStart(3,'0');
    s.cgcgk.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
      method:o.method||'Type1 能力指数（VDA 参考值±10%标准误）', standard:o.standard||'', runs:50, refValue:'',
      raw:null, tolerance:parseTol(o.object||p.object),
      analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
    return rid;
  }
  const rid = 'RES-'+TODAY.slice(0,4)+'-'+String(s.resolution.length+1).padStart(3,'0');
  s.resolution.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, unit:inst?inst.unit:'',
    method:o.method||'直接录入（不取样）', standard:o.standard||'', resValue:'', tolerance:parseTol(o.object||p.object),
    analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'-', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:o.note||'' });
  return rid;
}"""

rep(old_spawn, new_spawn)

# 在 calcGRR 函数结束后（verdictTagColor 后）插入新计算引擎；锚点用 calcGRR 结尾 + 下一函数
anchor = "  return {EV,AV,GRR,PV,TV,Rbar,Xdiff,partMeans,Xbars,opStats,pctEv,pctAv,pctGrr,pctPv,ndc,pctGrrTol,verdict,level,reasons};"
assert s.count(anchor)==1, 'anchor calcGRR end not unique'

new_calc = anchor + """

/* ============================================================================
 * 新增分析方法计算引擎（会议口径）
 *  线性/偏移性：5 标准件覆盖 0/25/50/75/100% 量程，每件 10 次；偏移%=|均值-参考|/参考；线性最小二乘 R²
 *  稳定性：25 子组均值-极差控制图（SPC 判异，X̄±A2·R̄ / D4·R̄），无出界=稳定
 *  Cg/Cgk(VDA Type1)：标准件连续 50 次；USL/LSL=参考±10%公差，Cg=0.2T/6σ，Cgk=min(USL-x̄,x̄-LSL)/3σ
 *  分辨率：直接录入，分辨率 ≤ 1/10 过程公差
 * ==========================================================================*/
const SPC_A2 = {2:1.880,3:1.023,4:0.729,5:0.577};
const SPC_D4 = {2:3.267,3:2.574,4:2.282,5:2.114};
function stdev(a){ if(!a||a.length<2) return 0; const m=a.reduce((x,y)=>x+y,0)/a.length; return Math.sqrt(a.reduce((x,y)=>x+(y-m)*(y-m),0)/(a.length-1)); }
function mean(a){ return a&&a.length? a.reduce((x,y)=>x+y,0)/a.length : 0; }
/* 线性/偏移性 */
function calcLinear(rec){
  if(!rec.raw) return null;
  const xs=[], ys=[], offs=[];
  for(let i=0;i<rec.stds;i++){
    const row=rec.raw[i]; if(!row||!row.length) return null;
    const ref=Number(rec.refs[i]); if(!(ref>0)) return null;
    const m=mean(row); xs.push(ref); ys.push(m); offs.push(m-ref);
  }
  const maxOff=Math.max.apply(null, offs.map(Math.abs));
  const maxOffPct=100*maxOff/(Math.max.apply(null,xs.map(Math.abs))||1);
  const xb=mean(xs), yb=mean(ys);
  let sxy=0, sxx=0; for(let i=0;i<xs.length;i++){ sxy+=(xs[i]-xb)*(ys[i]-yb); sxx+=(xs[i]-xb)*(xs[i]-xb); }
  const slope=sxx? sxy/sxx : 0; // 线性斜率（越接近 0 越线性无偏）
  const r2 = sxx&&ys.length>1? (()=>{ let sst=0; ys.forEach(y=>sst+=(y-yb)*(y-yb)); return sst? (1 - ((sxy*sxy/sxx)/sst)) : 1; })() : 1;
  const slopePct=100*Math.abs(slope); // 斜率占比
  const verdict = (maxOffPct<=10 && r2>=0.90)? '可接受' : ((maxOffPct<=20 || r2>=0.70)? '有条件接受' : '不可接受');
  const level = verdict==='可接受'?0:(verdict==='有条件接受'?1:2);
  const reasons=[];
  reasons.push('最大偏移 '+fmt(maxOff,3)+'（'+fmt(maxOffPct,1)+'% ≤10% 可接受）');
  reasons.push('线性回归 R²='+fmt(r2,3)+(r2>=0.90?'（线性良好）':'（线性欠佳）'));
  if(verdict!=='可接受') reasons.push('判定：'+verdict);
  return {offs, maxOff, maxOffPct, slope, slopePct, r2, xs, ys, verdict, level, reasons};
}
/* 稳定性（Xbar-R 控制图判异） */
function calcStability(rec){
  if(!rec.raw) return null;
  const xbars=[], rs=[];
  for(const row of rec.raw){ if(!row||!row.length) return null; xbars.push(mean(row)); rs.push(Math.max.apply(null,row)-Math.min.apply(null,row)); }
  const xbarBar=mean(xbars), rbar=mean(rs);
  const n=rec.per||3, A2=SPC_A2[n]||1.023, D4=SPC_D4[n]||2.574;
  const ucl=xbarBar+A2*rbar, lcl=Math.max(0,xbarBar-A2*rbar), uclR=D4*rbar;
  const out=xbars.filter(x=>x>ucl||x<lcl).length + rs.filter(r=>r>uclR).length;
  const verdict = out===0? '可接受' : (out<=2? '有条件接受':'不可接受');
  const level = verdict==='可接受'?0:(verdict==='有条件接受'?1:2);
  const reasons=[];
  reasons.push('子组数 '+xbars.length+'，X̄='+fmt(xbarBar,3)+'，R̄='+fmt(rbar,3));
  reasons.push('控制限 UCL='+fmt(ucl,3)+' / LCL='+fmt(lcl,3)+'，R 控制限='+fmt(uclR,3));
  reasons.push(out===0?'无出界点，过程稳定':'出界点数 '+out+'（SPC 判异）');
  return {xbars, rs, xbarBar, rbar, ucl, lcl, uclR, out, verdict, level, reasons};
}
/* Cg/Cgk（VDA Type1） */
function calcCgCgk(rec){
  if(!rec.raw||!rec.raw.length) return null;
  const ref=Number(rec.refValue); if(!(ref>0)) return null;
  const a=rec.raw.filter(v=>v!==''&&v!=null).map(Number).filter(v=>!isNaN(v));
  if(a.length<5) return null;
  const m=mean(a), sd=stdev(a);
  const T = (rec.tolerance&&rec.tolerance.has)? (rec.tolerance.usl-rec.tolerance.lsl) : 0.2*ref; // 无公差时默认 ±10% 参考值窗口
  const usl=ref+0.1*T, lsl=ref-0.1*T;
  const Cg = sd? (0.2*T)/(6*sd) : 0;
  const Cgk = sd? Math.min(usl-m, m-lsl)/(3*sd) : 0;
  const verdict = (Cg>=1.33 && Cgk>=1.33)? '可接受' : ((Cg>=1.00 && Cgk>=1.00)? '有条件接受':'不可接受');
  const level = verdict==='可接受'?0:(verdict==='有条件接受'?1:2);
  const reasons=[];
  reasons.push('测量 '+a.length+' 次，均值 '+fmt(m,4)+'，σ='+fmt(sd,4));
  reasons.push('控制线 USL='+fmt(usl,4)+' / LSL='+fmt(lsl,4)+'（参考值±10%公差）');
  reasons.push('Cg='+fmt(Cg,2)+(Cg>=1.33?' ≥1.33':'')+'，Cgk='+fmt(Cgk,2)+(Cgk>=1.33?' ≥1.33':''));
  return {m, sd, usl, lsl, T, Cg, Cgk, verdict, level, reasons};
}
/* 分辨率 */
function calcResolution(rec){
  const rv=Number(rec.resValue); if(!(rv>0)) return null;
  const tol=rec.tolerance;
  const ratio = (tol&&tol.has)? rv/(tol.usl-tol.lsl) : null;
  const pct = ratio!=null? 100*ratio : null;
  const verdict = (pct!=null && pct<=10)? '可接受' : ((pct!=null && pct<=20)? '有条件接受':'不可接受');
  const level = verdict==='可接受'?0:(verdict==='有条件接受'?1:2);
  const reasons=[];
  reasons.push('分辨率 '+rv+' '+(rec.unit||'')+(pct!=null?('，占过程公差 '+fmt(pct,1)+'%'):'（未填公差，待补充）'));
  if(pct!=null) reasons.push(pct<=10?'≤1/10 公差，分辨率满足':'＞1/10 公差，分辨率不足');
  return {rv, pct, verdict, level, reasons};
}
function recKindId(r){
  if(r.id.indexOf('GRR')===0) return 'GRR'; if(r.id.indexOf('KPA')===0) return 'KAPPA';
  if(r.id.indexOf('LIN')===0) return 'linear'; if(r.id.indexOf('STB')===0) return 'stability';
  if(r.id.indexOf('CG')===0) return 'cgcgk'; if(r.id.indexOf('RES')===0) return 'resolution';
  return 'GRR';
}
function recCalc(r){ // 统一入口：返回 {calc, tag}
  const k=recKindId(r);
  if(k==='GRR') return calcGRR(r);
  if(k==='linear') return calcLinear(r);
  if(k==='stability') return calcStability(r);
  if(k==='cgcgk') return calcCgCgk(r);
  if(k==='resolution') return calcResolution(r);
  return null;
}"""

rep(anchor, new_calc)

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
