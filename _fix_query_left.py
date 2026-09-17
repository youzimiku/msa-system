# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(old, new, desc, expect=1):
    global src
    n = src.count(old)
    ok = (n == expect)
    print(f'{desc}: 出现 {n} 次 (期望 {expect})', '-> 替换' if ok else '!!跳过')
    if ok:
        src = src.replace(old, new)

# LedgerPage
rep("""        <Input.Search allowClear placeholder="编号 / 名称 / 型号 / 序列号 / 责任人" style={{width:140}} value={kw} onChange={e=>setKw(e.target.value)}/>
        <Select allowClear placeholder="工厂" style={{width:140}} value={fPlant} options={PLANTS_OPT} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} value={fSub} options={SUBPLANTS_OPT} onChange={setFSub}/>""",
"""        <Select allowClear placeholder="工厂" style={{width:140}} value={fPlant} options={PLANTS_OPT} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} value={fSub} options={SUBPLANTS_OPT} onChange={setFSub}/>
        <Input.Search allowClear placeholder="编号 / 名称 / 型号 / 序列号 / 责任人" style={{width:140}} value={kw} onChange={e=>setKw(e.target.value)}/>""",
'Q1 LedgerPage')

# CharPage
rep("""        <Input allowClear placeholder="被测参数编号 / 名称 / 零件 / 工序" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>
        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>""",
"""        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>
        <Input allowClear placeholder="被测参数编号 / 名称 / 零件 / 工序" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>""",
'Q2 CharPage')

# SamplingPage
rep("""        <Input allowClear placeholder="规则编号 / 方法 / 说明" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>
        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>""",
"""        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>
        <Input allowClear placeholder="规则编号 / 方法 / 说明" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>""",
'Q3 SamplingPage')

# SampleLibPage
rep("""        <Input.Search allowClear placeholder="样本编号 / 名称 / 零件号 / 特性维度" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>
        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>""",
"""        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>
        <Input.Search allowClear placeholder="样本编号 / 名称 / 零件号 / 特性维度" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>""",
'Q4 SampleLibPage')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
