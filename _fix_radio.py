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

RG = '<Radio.Group size="small" optionType="button" buttonStyle="solid"'
RE = ' options='
def rg(value, setter, opts):
    return f'{RG} value={{{value}||\'\'}} onChange={{e=>{setter}(e.target.value||undefined)}}{RE}{opts}/>'

# 1 Ledger 状态
rep("""<Select allowClear placeholder="状态" style={{width:140}} value={fStatus} options={ENUM.instStatus.map(c=>({value:c,label:c}))} onChange={setFStatus}/>""",
    rg('fStatus','setFStatus',"[{value:'',label:'全部'}].concat(ENUM.instStatus.map(c=>({value:c,label:c})))"),
    '1 Ledger 状态')

# 2 Char 状态
rep("""<Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fs2} onChange={setFs2}/>""",
    rg('fs2','setFs2',"[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]"),
    '2 Char 状态')

# 3 Sampling 状态
rep("""<Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fs2} onChange={setFs2}/>""",
    rg('fs2','setFs2',"[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]"),
    '3 Sampling 状态')

# 4 SampleLib 状态
rep("""<Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fst} onChange={setFst}/>""",
    rg('fst','setFst',"[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]"),
    '4 SampleLib 状态')

# 5 Plan 计划状态
rep("""<Select allowClear placeholder="计划状态" style={{width:140}} value={fstatus} options={[{value:'待开始',label:'待开始'},{value:'进行中',label:'进行中'},{value:'已完成',label:'已完成'}]} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'待开始',label:'待开始'},{value:'进行中',label:'进行中'},{value:'已完成',label:'已完成'}]"),
    '5 Plan 计划状态')

# 6 Entry 记录状态（7 项）
rep("""<Select allowClear placeholder="记录状态" style={{width:140}} value={fstatus} options={['待采集','待分析','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待分析',label:'待分析'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]"),
    '6 Entry 记录状态')

# 7 Grr 记录状态（6 项）
rep("""<Select allowClear placeholder="记录状态" style={{width:140}} value={fstatus} options={['待采集','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]"),
    '7 Grr 记录状态')

# 8 Kappa 记录状态（6 项）
rep("""<Select allowClear placeholder="记录状态" style={{width:140}} value={fstatus} options={['待采集','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]"),
    '8 Kappa 记录状态')

# 9 Calib 校准状态（菜单外）
rep("""<Select allowClear placeholder="校准状态" style={{width:140}} value={fstate} options={['正常','临期','超期'].map(c=>({value:c,label:c}))} onChange={setFstate}/>""",
    rg('fstate','setFstate',"[{value:'',label:'全部'},{value:'正常',label:'正常'},{value:'临期',label:'临期'},{value:'超期',label:'超期'}]"),
    '9 Calib 校准状态')

# 10 Standard 标准状态（菜单外）
rep("""<Select allowClear placeholder="标准状态" style={{width:140}} value={fstatus} options={['启用','停用'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]"),
    '10 Standard 标准状态')

# 11 Sample 样本状态（菜单外）
rep("""<Select allowClear placeholder="样本状态" style={{width:140}} value={fstatus} options={[{value:'待测量',label:'待测量'},{value:'已测量',label:'已测量'}]} onChange={setFstatus}/>""",
    rg('fstatus','setFstatus',"[{value:'',label:'全部'},{value:'待测量',label:'待测量'},{value:'已测量',label:'已测量'}]"),
    '11 Sample 样本状态')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
