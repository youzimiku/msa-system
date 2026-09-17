# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(old, new, desc, expect=1, replace_all=False):
    global src
    n = src.count(old)
    ok = (n == expect) if not replace_all else (n >= 1)
    print(f'{desc}: 出现 {n} 次 (期望 {expect})', '-> 替换' if ok else '!!跳过')
    if ok:
        src = src.replace(old, new)

# 1) LedgerPage 状态（动态）
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fStatus||''} onChange={e=>setFStatus(e.target.value||undefined)} options={[{value:'',label:'全部'}].concat(ENUM.instStatus.map(c=>({value:c,label:c})))}/>""",
"""<Radio.Group size="small" value={fStatus||''} onChange={e=>setFStatus(e.target.value||undefined)}><Radio value="">全部</Radio>{ENUM.instStatus.map(c=><Radio key={c} value={c}>{c}</Radio>)}</Radio.Group>""",
'R1 台账状态')

# 2) CalibPage 校准状态
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstate||''} onChange={e=>setFstate(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'正常',label:'正常'},{value:'临期',label:'临期'},{value:'超期',label:'超期'}]}/>""",
"""<Radio.Group size="small" value={fstate||''} onChange={e=>setFstate(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="正常">正常</Radio><Radio value="临期">临期</Radio><Radio value="超期">超期</Radio></Radio.Group>""",
'R2 校准状态')

# 3) PlanPage 计划状态
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待开始',label:'待开始'},{value:'进行中',label:'进行中'},{value:'已完成',label:'已完成'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待开始">待开始</Radio><Radio value="进行中">进行中</Radio><Radio value="已完成">已完成</Radio></Radio.Group>""",
'R3 计划状态')

# 4) StandardPage 标准状态
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="启用">启用</Radio><Radio value="停用">停用</Radio></Radio.Group>""",
'R4 标准状态')

# 5+6) CharPage / SamplingPage（相同，replace_all）
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fs2||''} onChange={e=>setFs2(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/>""",
"""<Radio.Group size="small" value={fs2||''} onChange={e=>setFs2(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="启用">启用</Radio><Radio value="停用">停用</Radio></Radio.Group>""",
'R5 被测参数/抽样方法状态', expect=2, replace_all=True)

# 7) SampleLibPage
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fst||''} onChange={e=>setFst(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/>""",
"""<Radio.Group size="small" value={fst||''} onChange={e=>setFst(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="启用">启用</Radio><Radio value="停用">停用</Radio></Radio.Group>""",
'R6 样本库状态')

# 8) SamplePage 样本状态
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待测量',label:'待测量'},{value:'已测量',label:'已测量'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待测量">待测量</Radio><Radio value="已测量">已测量</Radio></Radio.Group>""",
'R7 样本状态')

# 9) EntryPage GRR（7项）
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>""",
'R8 GRR录入状态')

# 10) EntryPage KAPPA（7项含待分析）
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待分析',label:'待分析'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>""",
'R9 KAPPA录入状态')

# 11+12) 线性/稳定性/CgCgk（6项，相同两处 replace_all）
rep("""<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]}/>""",
"""<Radio.Group size="small" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>""",
'R10 线性/稳定性/CgCgk状态', expect=3, replace_all=True)

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
