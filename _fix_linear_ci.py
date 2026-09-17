# -*- coding: utf-8 -*-
"""修正 calcLinear：回归对象=偏倚(测量-参考) vs 参考值；"0"是否落在偏倚 95%CI 内；斜率显著性用 F 检验"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

old = """function calcLinear(rec){
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
}"""

new = """function calcLinear(rec){
  if(!rec.raw) return null;
  const rows=[], xs=[], ys=[], offs=[];
  for(let i=0;i<rec.stds;i++){
    const row=rec.raw[i]; if(!row||!row.length) return null;
    const ref=Number(rec.refs[i]); if(!(ref>0)) return null;
    const m=mean(row), sd=stdev(row), n=row.length;
    const off=m-ref;                       // 该量程点的平均偏倚
    xs.push(ref); ys.push(off); offs.push(off);
    const tcrit = n>20?1.96:(n>15?2.13:(n>10?2.26:2.31)); // t(0.975, n-1) 近似
    const se=sd/Math.sqrt(n);
    rows.push({ref, mean:m, off, sd, n, ciLo:off-tcrit*se, ciHi:off+tcrit*se, zeroIn:(0>=off-tcrit*se&&0<=off+tcrit*se)});
  }
  const maxOff=Math.max.apply(null, offs.map(Math.abs));
  const refMax=Math.max.apply(null, xs.map(Math.abs));
  const maxOffPct=100*maxOff/(refMax||1);
  const xb=mean(xs), yb=mean(ys);
  let sxy=0, sxx=0; for(let i=0;i<xs.length;i++){ sxy+=(xs[i]-xb)*(ys[i]-yb); sxx+=(xs[i]-xb)*(xs[i]-xb); }
  const slope=sxx? sxy/sxx : 0;            // 回归"斜率"：偏倚随参考值的变化率（线性偏倚）
  const intercept=yb-slope*xb;             // 回归"常量"：固定偏倚
  const nPts=xs.length;
  let ssr=0, sse=0; for(let i=0;i<nPts;i++){ const fit=intercept+slope*xs[i]; sse+=(ys[i]-fit)*(ys[i]-fit); ssr+=(fit-yb)*(fit-yb); }
  const r2 = (ssr+sse)? (1-sse/(ssr+sse)) : 1;
  const F = (sse>0&&nPts>2)? (ssr/1)/(sse/(nPts-2)) : 0; // 回归显著性 F 检验（F(1,n-2)）
  const slopeSig = F>7.71;                 // α=0.05 临界近似
  const zeroOut=rows.filter(r=>!r.zeroIn).length; // 偏倚为 0 的水平线落在 95% 置信区间外的点数
  const bothSides = (()=>{ const out=rows.filter(r=>!r.zeroIn); if(!out.length) return false; return out.some(r=>r.ciLo>0)&&out.some(r=>r.ciHi<0); })(); // 出界点是否位于不同侧
  let verdict, level, reasons=[];
  if(zeroOut===0){ verdict='非常理想可接受'; level=0; reasons.push('偏倚为 0 的水平线完全包围在 95% 置信区间内，且各点平均偏倚均落在置信区间内，测量系统非常理想可接受'); }
  else if(!slopeSig&&!bothSides){ verdict='理想可接受（固定偏倚可修正）'; level=0; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，回归方程"常量"显著不为 0、"斜率"显著为 0 → 量程范围内有固定偏倚（常量），很容易通过纠偏加以修正'); }
  else if(slopeSig&&!bothSides){ verdict='较理想可接受（线性偏倚可修正）'; level=1; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，且回归效果显著（斜率显著不为 0），同时各点平均偏倚值皆落在置信区间内 → 存在非"常量"线性偏倚，可按回归结果修正'); }
  else { verdict='不可接受'; level=2; reasons.push('偏倚为 0 的水平线若干点落在置信区间外，又不能拒绝回归斜率为 0，且有若干点平均偏移值落在置信区间外且位于不同侧 → 测量系统有偏倚，且因没有线性而无法修正'); }
  reasons.push('最大偏移 '+fmt(maxOff,3)+'（'+fmt(maxOffPct,1)+'%）');
  reasons.push('线性回归：斜率='+fmt(slope,4)+'、常量='+fmt(intercept,4)+'、R²='+fmt(r2,3)+(slopeSig?'（斜率显著≠0）':'（斜率不显著）'));
  reasons.push('偏倚 95% 置信区间外点数 '+zeroOut+'/'+rows.length);
  return {rows, offs, maxOff, maxOffPct, slope, slopePct:100*Math.abs(slope), intercept, r2, xs, ys, zeroOut, verdict, level, reasons};
}"""

n = s.count(old)
assert n == 1, ('calcLinear not found, count=%d' % n)
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('calcLinear fixed OK, len:', len(s))
