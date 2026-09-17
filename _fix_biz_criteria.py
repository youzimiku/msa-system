# -*- coding: utf-8 -*-
"""按业务材料对齐 MSA 系统判定准则与口径"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# 1) verdictColor 改关键词匹配（支持新判定文本配色）
rep("function verdictColor(c){ return ENUM.verdictTagColor[c]||'default'; }",
    "function verdictColor(c){ if(!c) return 'default'; if(c.indexOf('不可接受')>=0) return 'red'; if(c.indexOf('有条件')>=0||c.indexOf('边缘')>=0||c.indexOf('较理想')>=0) return 'orange'; if(c.indexOf('可接受')>=0||c.indexOf('优秀')>=0||c.indexOf('理想')>=0||c.indexOf('好')>=0) return 'green'; return ENUM.verdictTagColor[c]||'default'; }")

# 2) calcLinear 重写：业务「线性+偏倚」4 条判定（"0"水平线 vs 95% 置信区间 + 回归常量/斜率）
rep("""function calcLinear(rec){
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
}""",
"""function calcLinear(rec){
  if(!rec.raw) return null;
  const rows=[], xs=[], ys=[], offs=[];
  for(let i=0;i<rec.stds;i++){
    const row=rec.raw[i]; if(!row||!row.length) return null;
    const ref=Number(rec.refs[i]); if(!(ref>0)) return null;
    const m=mean(row), sd=stdev(row), n=row.length;
    xs.push(ref); ys.push(m); offs.push(m-ref);
    const tcrit = n>20?1.96:(n>15?2.13:(n>10?2.26:2.31)); // t(0.975, n-1) 近似
    const se=sd/Math.sqrt(n);
    rows.push({ref, mean:m, off:m-ref, sd, n, ciLo:m-tcrit*se, ciHi:m+tcrit*se, zeroIn:(0>=m-tcrit*se&&0<=m+tcrit*se)});
  }
  const maxOff=Math.max.apply(null, offs.map(Math.abs));
  const refMax=Math.max.apply(null, xs.map(Math.abs));
  const maxOffPct=100*maxOff/(refMax||1);
  const xb=mean(xs), yb=mean(ys);
  let sxy=0, sxx=0; for(let i=0;i<xs.length;i++){ sxy+=(xs[i]-xb)*(ys[i]-yb); sxx+=(xs[i]-xb)*(xs[i]-xb); }
  const slope=sxx? sxy/sxx : 0;          // 线性回归斜率（业务：回归"斜率"显著性）
  const intercept=yb-slope*xb;           // 回归"常量"（业务：固定偏倚）
  const r2 = sxx&&ys.length>1? (()=>{ let sst=0; ys.forEach(y=>sst+=(y-yb)*(y-yb)); return sst? (1 - ((sxy*sxy/sxx)/sst)) : 1; })() : 1;
  const slopePct=100*Math.abs(slope)/(refMax||1); // 斜率占量程比
  const zeroOut=rows.filter(r=>!r.zeroIn).length; // 偏倚为 0 的水平线落在 95% 置信区间外的点数
  const bothSides = (()=>{ const out=rows.filter(r=>!r.zeroIn); if(!out.length) return false; return out.some(r=>r.ciLo>0)&&out.some(r=>r.ciHi<0); })(); // 出界点是否位于不同侧
  const slopeSig = slopePct>5;           // 简化显著性：斜率 >5% 量程视为显著
  let verdict, level, reasons=[];
  if(zeroOut===0){ verdict='非常理想可接受'; level=0; reasons.push('偏倚为 0 的水平线完全包围在 95% 置信区间内，且各点平均偏倚均落在置信区间内，测量系统非常理想可接受'); }
  else if(!slopeSig&&!bothSides){ verdict='理想可接受（固定偏倚可修正）'; level=0; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，回归方程"常量"显著不为 0、"斜率"显著为 0 → 量程范围内有固定偏倚（常量），很容易通过纠偏加以修正'); }
  else if(slopeSig&&!bothSides){ verdict='较理想可接受（线性偏倚可修正）'; level=1; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，且回归效果显著（斜率显著不为 0），同时各点平均偏倚值皆落在置信区间内 → 存在非"常量"线性偏倚，可按回归结果修正'); }
  else { verdict='不可接受'; level=2; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，又不能拒绝回归斜率为 0，且有若干点平均偏移值落在置信区间外且位于不同侧 → 测量系统有偏倚，且因没有线性而无法修正'); }
  reasons.push('最大偏移 '+fmt(maxOff,3)+'（'+fmt(maxOffPct,1)+'%）');
  reasons.push('线性回归：斜率='+fmt(slope,4)+'、常量='+fmt(intercept,4)+'、R²='+fmt(r2,3));
  reasons.push('偏倚 95% 置信区间外点数 '+zeroOut+'/'+rows.length);
  return {rows, offs, maxOff, maxOffPct, slope, slopePct, intercept, r2, xs, ys, zeroOut, verdict, level, reasons};
}""")

# 3) calcCgCgk 增强：业务 5 条判定 + 6σ/T
rep("""  const Cg = sd? (0.2*T)/(6*sd) : 0;
  const Cgk = sd? Math.min(usl-m, m-lsl)/(3*sd) : 0;
  const verdict = (Cg>=1.33 && Cgk>=1.33)? '可接受' : ((Cg>=1.00 && Cgk>=1.00)? '有条件接受':'不可接受');
  const level = verdict==='可接受'?0:(verdict==='有条件接受'?1:2);
  const reasons=[];
  reasons.push('测量 '+a.length+' 次，均值 '+fmt(m,4)+'，σ='+fmt(sd,4));
  reasons.push('控制线 USL='+fmt(usl,4)+' / LSL='+fmt(lsl,4)+'（参考值±10%公差）');
  reasons.push('Cg='+fmt(Cg,2)+(Cg>=1.33?' ≥1.33':'')+'，Cgk='+fmt(Cgk,2)+(Cgk>=1.33?' ≥1.33':''));
  return {m, sd, usl, lsl, T, Cg, Cgk, verdict, level, reasons};""",
"""  const Cg = sd? (0.2*T)/(6*sd) : 0;
  const Cgk = sd? Math.min(usl-m, m-lsl)/(3*sd) : 0;
  const sgT = sd&&T? 100*6*sd/T : null; // 重复性误差占比 6σ/T
  let verdict, level, reasons=[];
  if(Cgk<0){ verdict='不可接受'; level=2; reasons.push('Cgk='+fmt(Cgk,2)+' <0：偏倚超出 10% 公差，量具不可使用，必须立即整改复测'); }
  else if(Cg>=1.33 && Cgk>=1.33){ verdict='可接受'; level=0; reasons.push('Cg、Cgk 均 ≥1.33：该量具重复性、偏倚满足 AIAG MSA-4 要求，量具能力充足，可用于该尺寸日常检验与量产判定'); }
  else if(Cg<1.33){ verdict='不可接受'; level=2; reasons.push('Cg='+fmt(Cg,2)+' 偏小：量具重复性差、波动大，需检修、清洁、更换量具或提升装夹稳定性'); }
  else { verdict='有条件接受'; level=1; reasons.push('Cg 合格、Cgk='+fmt(Cgk,2)+' 偏小：量具存在系统性偏倚，需重新校准、修正补偿、核对标准件真值'); }
  reasons.push('测量 '+a.length+' 次，均值 '+fmt(m,4)+'，σ='+fmt(sd,4));
  reasons.push('控制线 USL='+fmt(usl,4)+' / LSL='+fmt(lsl,4)+'（参考值±10%公差）');
  reasons.push('Cg='+fmt(Cg,2)+(Cg>=1.33?' ≥1.33':'')+'，Cgk='+fmt(Cgk,2));
  reasons.push('重复性误差占比 6σ/T='+(sgT!=null?fmt(sgT,1)+'%':'待补充')+(sgT!=null?(sgT<=15?'（≤15% 优秀）':(sgT<=20?'（≤20% 可接受）':'（＞20% 需改进）')):''));
  return {m, sd, usl, lsl, T, Cg, Cgk, sgT, verdict, level, reasons};""")

# 4) calcKappaRec 判定：业务三档判定表（Kappa/有效性/错误率/错误警报率）
rep("""  // 判定（STD-MSA-003/004）
  let verdict, level=0, reasons=[];
  if(kappa>0.75){verdict='优秀(可接受)';}
  else if(kappa>=0.40){verdict='良好(有条件接受)'; level=1; reasons.push('总体KAPPA处于 0.40~0.75 有条件区间');}
  else {verdict='不可接受'; level=2; reasons.push('总体KAPPA<0.40，一致性差');}
  if(overall.effectiveness<90){ if(level<1)level=1; verdict=level===2?verdict:'良好(有条件接受)'; reasons.push('整体有效性 '+r2(overall.effectiveness)+'% < 90%'); }
  if(overall.missRate>2){ level=2; verdict='不可接受'; reasons.push('漏判率 '+r2(overall.missRate)+'% > 2%（顾客风险，从严判定）'); }
  if(overall.falseAlarm>5){ if(level<1)level=1; verdict=level===2?verdict:'良好(有条件接受)'; reasons.push('误判率 '+r2(overall.falseAlarm)+'% > 5%'); }
  if(level===0) verdict='优秀(可接受)';
  return {per,pairs,overall,verdict,level,reasons};""",
"""  // 判定（业务计数型三档判定表：Kappa / 有效性 / 错误率 / 错误警报率，取最差档）
  const eff=overall.effectiveness, miss=overall.missRate, fa=overall.falseAlarm;
  const lvK = kappa>=0.75?0:(kappa>=0.40?1:2);
  const lvE = eff>=90?0:(eff>=80?1:2);
  const lvM = miss<=2?0:(miss<=5?1:2);
  const lvF = fa<=5?0:(fa<=10?1:2);
  let verdict, level=Math.max(lvK,lvE,lvM,lvF), reasons=[];
  if(level===0) verdict='可接受';
  else if(level===1) verdict='可接受边缘-可能需改进';
  else verdict='不可接受-需改进';
  reasons.push('总体KAPPA='+r2(kappa)+(lvK===0?'（≥0.75）':lvK===1?'（0.40~0.75）':'（<0.40）'));
  if(lvE>0) reasons.push('有效性 '+r2(eff)+'%'+(lvE===1?'（80%~90% 边缘）':'（<80% 不可接受）'));
  if(lvM>0) reasons.push('错误率(漏判) '+r2(miss)+'%'+(lvM===1?'（2%~5% 边缘）':'（>5% 不可接受）'));
  if(lvF>0) reasons.push('错误警报率(误判) '+r2(fa)+'%'+(lvF===1?'（5%~10% 边缘）':'（>10% 不可接受）'));
  return {per,pairs,overall,verdict,level,reasons};""")

# 5) TYPE_PARAMS.KAPPA：零件数 30→50（业务样例）
rep("'KAPPA':{ops:3,trials:1,parts:30},", "'KAPPA':{ops:3,trials:1,parts:50},")

# 6) SAMPLING 文案：linear / KAPPA 按业务口径
rep("'linear':'线性+偏移性合并取样：5 个标准件（具鉴定证书/高等级量具真值）覆盖 0/25/50/75/100% 量程点，每件测 10~12 次（共 50~60 组）',",
    "'linear':'线性+偏倚合并取样：线性取 5 个标准件（鉴定证书/高等级量具真值）覆盖 0/25/50/75/100% 量程点、每件测 10~12 次；偏倚分析以标准件为对象重复测 15 次，先正态性检验（P>0.05）再判\"0\"是否落在 95% 置信区间',")
rep("'KAPPA':'与 GRR 相同取样（计数型）：检验员×参考值交叉表 + 检验员间交叉 + 漏发/误发判定 + 有效性（报告格式待万工确认）',",
    "'KAPPA':'KAPPA（计数型）取样：50 个零件 × 3 人盲测判定（业务报告样例 50 件/3 人/每件 3 次，系统演示为每件 1 次二分类判定），与参考值交叉表 + 检验员间交叉 + 有效性/错误率/错误警报率判定',")

# 7) KappaPage 列表列名：漏判率→错误率、误判率→错误警报率
rep("{title:'漏判率', width:80, render:(_,r)=>{const c=calcKappaRec(r);return c?fmt(c.overall.missRate,1)+'%':'-'}},",
    "{title:'错误率', width:80, render:(_,r)=>{const c=calcKappaRec(r);return c?fmt(c.overall.missRate,1)+'%':'-'}},")
rep("{title:'误判率', width:80, render:(_,r)=>{const c=calcKappaRec(r);return c?fmt(c.overall.falseAlarm,1)+'%':'-'}},",
    "{title:'错误警报率', width:92, render:(_,r)=>{const c=calcKappaRec(r);return c?fmt(c.overall.falseAlarm,1)+'%':'-'}},")

# 8) KappaPage 操作区说明文案
rep("判定标准：KAPPA&gt;0.75 优秀；0.40~0.75 良好（有条件）；&lt;0.40 不可接受；有效性≥90%、漏判≤2%、误判≤5%。",
    "判定标准（业务三档）：Kappa≥0.75 且有效性≥90%、错误率≤2%、错误警报率≤5% → 可接受；Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10% → 边缘；Kappa&lt;0.40 或有效性&lt;80% 或错误率&gt;5% 或错误警报率&gt;10% → 不可接受-需改进。")

# 9) KappaDetail：level 推导 + banner 文案
rep("  const level = calc.verdict.indexOf('优秀')>=0?0: calc.verdict.indexOf('不可接受')>=0?2:1;\n  const banner = {0:{t:'测量系统一致性优秀',c:'accept',desc:'总体 KAPPA>0.75，有效性/漏判/误判满足要求，可接受'},1:{t:'有条件接受',c:'cond',desc:'需对缺陷/边界样本加强培训，重点控制漏判风险，并复测验证'},2:{t:'不可接受',c:'reject',desc:'判定一致性差，须重新培训/更换判定标准后复测'}}[level];",
    "  const level = calc.level;\n  const banner = {0:{t:'测量系统一致性可接受',c:'accept',desc:'总体 KAPPA≥0.75，有效性≥90%、错误率≤2%、错误警报率≤5%，满足要求'},1:{t:'可接受边缘-可能需改进',c:'cond',desc:'存在单项落入边缘区间（Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10%），需加强培训并复测验证'},2:{t:'不可接受-需改进',c:'reject',desc:'存在单项不可接受（Kappa<0.40 / 有效性<80% / 错误率>5% / 错误警报率>10%），须重新培训/更换判定标准后复测'}}[level];")

# 10) KappaDetail perCols：列名 + 三档判定
rep("{title:'漏判率', width:90, render:(_,r)=><span style={{color:r.missRate>2?'#dc2626':'inherit'}}>{fmt(r.missRate,1)}%</span>},",
    "{title:'错误率(漏判)', width:100, render:(_,r)=><span style={{color:r.missRate>5?'#dc2626':r.missRate>2?'#d97706':'inherit'}}>{fmt(r.missRate,1)}%</span>},")
rep("{title:'误判率', width:90, render:(_,r)=><span style={{color:r.falseAlarm>5?'#dc2626':'inherit'}}>{fmt(r.falseAlarm,1)}%</span>},",
    "{title:'错误警报率(误判)', width:120, render:(_,r)=><span style={{color:r.falseAlarm>10?'#dc2626':r.falseAlarm>5?'#d97706':'inherit'}}>{fmt(r.falseAlarm,1)}%</span>},")
rep("{title:'判定', width:90, render:(_,r)=><Tag color={r.kappa>0.75?'green':r.kappa>=0.4?'orange':'red'}>{r.kappa>0.75?'优秀':r.kappa>=0.4?'良好':'差'}</Tag>}",
    "{title:'判定', width:90, render:(_,r)=><Tag color={r.kappa>=0.75?'green':r.kappa>=0.4?'orange':'red'}>{r.kappa>=0.75?'可接受':r.kappa>=0.4?'边缘':'差'}</Tag>}")

# 11) KappaDetail KPI：三档阈值
rep("""          <div className="kpi-item"><div className="k">总体 KAPPA</div><div className="v" style={{color:calc.overall.kappa>0.75?'#16a34a':calc.overall.kappa>=0.4?'#d97706':'#dc2626'}}>{fmt(calc.overall.kappa,2)}</div></div>
          <div className="kpi-item"><div className="k">总体有效性</div><div className="v">{fmt(calc.overall.effectiveness,1)}%</div><div className="tiny">≥90%</div></div>
          <div className="kpi-item"><div className="k">漏判率</div><div className="v" style={{color:calc.overall.missRate>2?'#dc2626':'inherit'}}>{fmt(calc.overall.missRate,1)}%</div><div className="tiny">≤2%（从严）</div></div>
          <div className="kpi-item"><div className="k">误判率</div><div className="v" style={{color:calc.overall.falseAlarm>5?'#dc2626':'inherit'}}>{fmt(calc.overall.falseAlarm,1)}%</div><div className="tiny">≤5%</div></div>""",
"""          <div className="kpi-item"><div className="k">总体 KAPPA</div><div className="v" style={{color:calc.overall.kappa>=0.75?'#16a34a':calc.overall.kappa>=0.4?'#d97706':'#dc2626'}}>{fmt(calc.overall.kappa,2)}</div><div className="tiny">≥0.75 可接受</div></div>
          <div className="kpi-item"><div className="k">总体有效性</div><div className="v" style={{color:calc.overall.effectiveness>=90?'inherit':calc.overall.effectiveness>=80?'#d97706':'#dc2626'}}>{fmt(calc.overall.effectiveness,1)}%</div><div className="tiny">≥90% 可接受</div></div>
          <div className="kpi-item"><div className="k">错误率(漏判)</div><div className="v" style={{color:calc.overall.missRate>5?'#dc2626':calc.overall.missRate>2?'#d97706':'inherit'}}>{fmt(calc.overall.missRate,1)}%</div><div className="tiny">≤2% 可接受</div></div>
          <div className="kpi-item"><div className="k">错误警报率(误判)</div><div className="v" style={{color:calc.overall.falseAlarm>10?'#dc2626':calc.overall.falseAlarm>5?'#d97706':'inherit'}}>{fmt(calc.overall.falseAlarm,1)}%</div><div className="tiny">≤5% 可接受</div></div>""")

# 12) KappaDetail 汇总评估后插入业务判定准则表（三档）
rep("""      <div className="grp-label">检验员间两两一致性</div>
      <Table size="small" rowKey="label" dataSource={calc.pairs} columns={pairCols} pagination={false}/>
    </div>}""",
"""      <div className="grp-label">检验员间两两一致性</div>
      <Table size="small" rowKey="label" dataSource={calc.pairs} columns={pairCols} pagination={false}/>
    </div>}
    {calc && <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>判定准则（业务计数型三档表）</span></div>
      <Table size="small" rowKey="d" pagination={false} dataSource={[
        {d:'评价人可接受', k:'Kappa ≥0.75', e:'有效性 ≥90%', m:'错误率 ≤2%', f:'错误警报率 ≤5%'},
        {d:'可接受边缘-可能需改进', k:'Kappa 0.40~0.75', e:'有效性 80%~90%', m:'错误率 2%~5%', f:'错误警报率 5%~10%'},
        {d:'不可接受-需改进', k:'Kappa <0.40', e:'有效性 <80%', m:'错误率 >5%', f:'错误警报率 >10%'}
      ]} columns={[
        {title:'判定档位', dataIndex:'d', width:220},
        {title:'Kappa', dataIndex:'k', width:140},
        {title:'有效性', dataIndex:'e', width:130},
        {title:'错误率(漏判)', dataIndex:'m', width:120},
        {title:'错误警报率(误判)', dataIndex:'f', width:140}
      ]}/>
      <div className="tiny mt8">结论取最差档：任一项落入不可接受区间即整体「不可接受-需改进」；Kappa&gt;0.75 满足一致性要求（业务《MCU6焊接KAPPA报告》样例：Kappa=1.00/0.94，判定「好」）。</div>
    </div>}""")

# 13) AnlDetail KPI：linear 加 95%CI 外点数、cgcgk 加 6σ/T
rep("{k:'最大偏移',v:fmt(calc.maxOff,3)},{k:'偏移%',v:fmt(calc.maxOffPct,1)+'%'},{k:'线性斜率',v:fmt(calc.slope,4)},{k:'R²',v:fmt(calc.r2,3)}]",
    "{k:'最大偏移',v:fmt(calc.maxOff,3)},{k:'偏移%',v:fmt(calc.maxOffPct,1)+'%'},{k:'线性斜率',v:fmt(calc.slope,4)},{k:'R²',v:fmt(calc.r2,3)},{k:'95%CI外点数',v:calc.zeroOut+'/'+(calc.rows?calc.rows.length:calc.stds||5)}]")
rep("{k:'均值',v:fmt(calc.m,4)},{k:'σ',v:fmt(calc.sd,4)},{k:'Cg',v:fmt(calc.Cg,2)},{k:'Cgk',v:fmt(calc.Cgk,2)},{k:'控制线',v:fmt(calc.usl,4)+'/'+fmt(calc.lsl,4)}]",
    "{k:'均值',v:fmt(calc.m,4)},{k:'σ',v:fmt(calc.sd,4)},{k:'Cg',v:fmt(calc.Cg,2)},{k:'Cgk',v:fmt(calc.Cgk,2)},{k:'6σ/T',v:calc.sgT!=null?fmt(calc.sgT,1)+'%':'-'},{k:'控制线',v:fmt(calc.usl,4)+'/'+fmt(calc.lsl,4)}]")

# 14) 创建 MSA 计划弹窗：分析方法说明与选项按业务「五性一力 + Cg/Cgk」口径
rep("<span className=\"flt-label\">分析方法（勾选本次要生成的分析计划；一器一计划一方法，GRR 与 KAPPA 不同时勾选）</span><Checkbox.Group size=\"small\" value={mMethods} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'resolution',label:'分辨率'}]} onChange={setMMethods}/>",
    "<span className=\"flt-label\">分析方法（五性一力 + Cg/Cgk：重复性、再现性、线性、偏倚、稳定性、分辨力、能力；勾选后按器具批量生成分析任务，一个计划可触发多个任务，计划未完成期间同器具禁止新建计划）</span><Checkbox.Group size=\"small\" value={mMethods} options={[{value:'GRR',label:'GRR（重复性+再现性）'},{value:'KAPPA',label:'KAPPA（计数型一致性）'},{value:'linear',label:'线性/偏移（线性+偏倚）'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk（能力）'},{value:'resolution',label:'分辨率（分辨力）'}]} onChange={setMMethods}/>")

open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len:', len(s))
