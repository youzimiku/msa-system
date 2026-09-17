# -*- coding: utf-8 -*-
"""multi1: BatchPlanModal submit 改为一计划多方法"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

start = s.find('const submit=()=>{')
end = s.find('const cols=[', start)
assert start > 0 and end > start, (start, end)

new_submit = '''  const submit=()=>{
    if(!partSel){ toast.warn('请先选择零件/工序（检验标准定义在零件上）'); return; }
    if(!stdSel){ toast.warn('请为该零件选择检验标准（一个计划一个检验标准）'); return; }
    if(!selKeys.length){ toast.warn('请至少选择一个计量器具'); return; }
    const t=stdTypeOf(stdSel);
    const baseParams={ops:cfg._ops||TYPE_PARAMS[t].ops, trials:cfg._trials||TYPE_PARAMS[t].trials, parts:cfg._parts||TYPE_PARAMS[t].parts};
    // 会议口径（2026-09-08）：一个计划可对应多个分析方法（一计划多任务）。勾选 N 个分析方法 → 每台器具生成 1 个计划，计划下按方法各生成 1 条台账「待采集」记录；未勾选 → 生成 1 个「未定型」计划（待转）
    const meths = mMethods.length? mMethods : [];
    let created=0, skipped=0;
    mut(s=>{
      selKeys.forEach(id=>{
        if(instHasActivePlan(s, id)){ skipped++; return; }
        const it=s.instruments.find(i=>i.id===id); if(!it) return;
        const fullName=(it.range&&it.range!=='-'&&it.range!=='计数型'&&it.range!=='通端/止端')?(it.name+' '+it.range):it.name;
        const c=cfg[id]||{};
        const pid=nextPlanId(s);
        const firstAn=meths[0]||'';
        const singleM=meths.length===1;
        const tparams=TYPE_PARAMS[firstAn||'GRR']||{};
        const D0=SMP_DEF[(firstAn==='GRR'||firstAn==='KAPPA'||!firstAn)?(firstAn||'GRR'):(singleM?firstAn:'GRR')]||SMP_DEF.GRR;
        const rowOps=Number(c.ops)||D0.ops, rowTrials=Number(c.trials)||D0.trials, rowParts=Number(c.parts)||D0.parts;
        const pParamsOf=(an)=>{
          if(an==='GRR'||an==='KAPPA') return {ops:rowOps, trials:rowTrials, parts:rowParts};
          if(an==='linear') return singleM? {stds:rowParts||5, per:rowTrials||12, points:rowParts||5, biasRuns:tparams.biasRuns||15} : {stds:tparams.stds||5, per:tparams.per||12, points:tparams.points||5, biasRuns:tparams.biasRuns||15};
          if(an==='stability') return singleM? {groups:rowParts||25, per:rowTrials||5, span:'4周~3个月'} : {groups:tparams.groups||25, per:tparams.per||5, span:'4周~3个月'};
          if(an==='cgcgk') return singleM? {runs:rowTrials||50, parts:1} : {runs:tparams.runs||50, parts:1};
          return {none:1};
        };
        const nameAn=meths.length? ('·'+meths.map(x=>ANAL_SHORT[x]).join('/')) : '';
        const dataType=(meths.indexOf('KAPPA')>=0||stdTypeOf(stdSel)==='KAPPA')?'计数型':'计量型';
        const method=firstAn? ENUM.taskMethod[firstAn][0] : '';
        s.plans.unshift({ id:pid, name:(nameTpl||'{inst} MSA 分析计划').replace('{inst}', fullName+nameAn), instId:id, instName:fullName, instIds:[id], cat:it.cat,
          type:firstAn, method, methods:meths.slice(), standard:stdSel, params:meths.length? pParamsOf(firstAn) : {},
          object:c.object||'待定义', feature:'', owner:c.owner||s.me.name, editor:s.me.name, editorDate:TODAY,
          planDate, trigger, status: meths.length? '待采集':'未定型', recordId:'', result:'',
          note: meths.length? ('创建时勾选分析方法 '+meths.map(x=>ANAL_SHORT[x]).join('、')+'，已生成 '+meths.length+' 条台账待采集记录') : ('创建时选定零件 '+partSel.split(' / ')[0]+'、检验标准 '+stdSel+'，未勾选分析方法，可在列表勾选后转分析方法定型'),
          partNo:meta.partNo, partName:partSel.split(' / ')[0], qcArea:meta.qcArea, plant:meta.plant, subplant:meta.subplant, observer:meta.observer, measurers:Array.isArray(meta.measurers)? meta.measurers.join('、') : (meta.measurers||''),
          dept:meta.dept, dataType, msaMethods: meths.reduce((a,x)=>a.concat(msaExcelMap(x)),[]), opMethod:'《测量系统分析操作指导书》' });
        meths.forEach(an=>{ spawnRecord(s, pid, {type:an, instId:id, instName:fullName, object:c.object||'待定义', standard:stdSel, method:ENUM.taskMethod[an][0], params:pParamsOf(an), note:'创建时按分析方法 '+ANAL_SHORT[an]+' 生成'}); });
        syncPlanFromRecord(s,pid);
        created++;
      });
      logAction(s.me.name,'计划编制','MSAP-批量','按器具创建 '+created+' 个 MSA 计划（勾选分析方法：'+(meths.length?meths.map(x=>ANAL_SHORT[x]).join('、'):'未定型')+'，单一标准 '+stdSel+'）'+(skipped?('，跳过 '+skipped+' 台（已有未闭环计划）'):''));
    });
    if(created) toast.ok('已创建 '+created+' 个 MSA 计划'+(meths.length?('（'+meths.map(x=>ANAL_SHORT[x]).join('/')+'，共生成 '+created*meths.length+' 条台账待采集记录）'):'（未定型，待转）')+',单一检验标准 '+stdSel+(skipped?('；跳过 '+skipped+' 台（已有未闭环计划）'):''));
    else toast.warn('所选器具均已存在未闭环计划，未创建新计划');
    onClose();
  };
'''
old = s[start:end]
assert old.count('meths.forEach') >= 0
s = s[:start] + new_submit + s[end:]
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('submit 替换完成, old len', len(old), 'new len', len(new_submit))
print('残留旧标记:', s.count('一器一计划一方法。勾选 N 个分析方法 → 每台器具生成 N 个计划'))
