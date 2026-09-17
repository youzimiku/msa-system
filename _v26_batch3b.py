# -*- coding: utf-8 -*-
"""v2.6 第三批 b：calcKappaRec 兼容三维 rawData + 自评 self；seed KAPPA 补 rawData"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:90])
    s = s.replace(old, new, cnt)

# ---------- 1. calcKappaRec 新版（兼容 rawData 三维 + 自评 self + pairs 分级） ----------
OLD_CALC = """function calcKappaRec(rec){
  const per = rec.appData.map((app,i)=>Object.assign({name:rec.appNames[i]}, kappa2x2(rec.reference, app)));
  // 检验员间两两一致性
  const pairs=[];
  for(let i=0;i<rec.numApp;i++) for(let j=i+1;j<rec.numApp;j++){
    pairs.push(Object.assign({i,j,label:rec.appNames[i]+' ↔ '+rec.appNames[j]}, kappa2x2(rec.appData[i],rec.appData[j])));
  }
  // 汇总（所有检验员判定与参照合并）
  const n=rec.numSamples*rec.numApp; let a=0,b=0,c=0,d=0;
  rec.appData.forEach(app=>{const r=kappa2x2(rec.reference,app);a+=r.a;b+=r.b;c+=r.c;d+=r.d;});
  const po=(a+d)/n, pe=((a+b)*(a+c)+(c+d)*(b+d))/(n*n);
  const kappa=(1-pe===0)?1:(po-pe)/(1-pe);
  const overall={kappa, effectiveness:100*po, missRate:(b+d)>0?100*b/(b+d):0, falseAlarm:(a+c)>0?100*c/(a+c):0, a,b,c,d};
  // 判定（业务计数型三档判定表：Kappa / 有效性 / 错误率 / 错误警报率，取最差档）
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
  return {per,pairs,overall,verdict,level,reasons};
}"""

NEW_CALC = """function majority1(arr){ if(!arr||!arr.length) return 0; const ones=arr.filter(v=>v===1).length; return ones>arr.length/2?1:0; }
function calcKappaRec(rec){
  // 兼容：录入提交存 rawData（每件多次判定，三维）；旧数据仅 appData（二维，每件最终判定）
  const hasRaw = !!(rec.rawData && rec.rawData.length && rec.rawData[0] && Array.isArray(rec.rawData[0][0]));
  const finalData = hasRaw? rec.rawData.map(app=>app.map(s=>majority1(s))) : rec.appData;
  const per = finalData.map((app,i)=>Object.assign({name:rec.appNames[i]}, kappa2x2(rec.reference, app)));
  // 检验员间两两一致性（逐对 Kappa + 分级）
  const pairs=[];
  for(let i=0;i<rec.numApp;i++) for(let j=i+1;j<rec.numApp;j++){
    const r=kappa2x2(finalData[i],finalData[j]);
    pairs.push(Object.assign({i,j,label:rec.appNames[i]+' ↔ '+rec.appNames[j]}, r, {level: r.kappa>=0.75?0:(r.kappa>=0.4?1:2)}));
  }
  // 自评 Self（每人多次试验两两一致性，业务报告 %Appraiser 重复性）
  const self=[];
  if(hasRaw){ rec.rawData.forEach((app,ai)=>{
    const trials=(app[0]&&app[0].length)||0; const cons=[];
    for(let x=0;x<trials;x++) for(let y=x+1;y<trials;y++){ cons.push(Object.assign({t1:x+1,t2:y+1}, kappa2x2(app.map(s=>s[x]), app.map(s=>s[y])))); }
    self.push({name:rec.appNames[ai], trials, pairs:cons});
  }); }
  // 汇总（所有检验员最终判定与参照合并）
  const n=rec.numSamples*rec.numApp; let a=0,b=0,c=0,d=0;
  finalData.forEach(app=>{const r=kappa2x2(rec.reference,app);a+=r.a;b+=r.b;c+=r.c;d+=r.d;});
  const po=(a+d)/n, pe=((a+b)*(a+c)+(c+d)*(b+d))/(n*n);
  const kappa=(1-pe===0)?1:(po-pe)/(1-pe);
  const overall={kappa, effectiveness:100*po, missRate:(b+d)>0?100*b/(b+d):0, falseAlarm:(a+c)>0?100*c/(a+c):0, a,b,c,d};
  // 判定（业务计数型三档判定表：Kappa / 有效性 / 错误率 / 错误警报率，取最差档）
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
  return {per,pairs,self,overall,verdict,level,reasons};
}"""
rep(OLD_CALC, NEW_CALC, 1, 'calcKappaRec')

# ---------- 2. seed KAPPA-001 补 rawData / numTrials ----------
rep("""     appData:[
       kRef1.slice(),
       kRef1.slice(),
       kRef1.slice()
     ],
     analysisDate:'2026-04-22', analyst:'李工程师', reviewStatus:'已批准', conclusion:'优秀(可接受)',""",
    """     appData:[
       kRef1.slice(),
       kRef1.slice(),
       kRef1.slice()
     ],
     rawData:[
       kRef1.slice().map(v=>[v,v,v]),
       kRef1.slice().map(v=>[v,v,v]),
       kRef1.slice().map(v=>[v,v,v])
     ],
     numTrials:3,
     analysisDate:'2026-04-22', analyst:'李工程师', reviewStatus:'已批准', conclusion:'优秀(可接受)',""",
    1, 'seed-kpa1')

rep("""     appData:[
       judge(kRef1, [3,10,17]),
       judge(kRef1, [2,6,11,14,16])
     ],
     analysisDate:'2026-08-26', analyst:'李工程师', reviewStatus:'需整改', conclusion:'不可接受-需改进',""",
    """     appData:[
       judge(kRef1, [3,10,17]),
       judge(kRef1, [2,6,11,14,16])
     ],
     rawData:[
       judge(kRef1, [3,10,17]).map(v=>[v,v,v]),
       judge(kRef1, [2,6,11,14,16]).map(v=>[v,v,v])
     ],
     numTrials:3,
     analysisDate:'2026-08-26', analyst:'李工程师', reviewStatus:'需整改', conclusion:'不可接受-需改进',""",
    1, 'seed-kpa2')

open(P, 'w', encoding='utf-8').write(s)
print('batch3b OK 长度', len(s))
