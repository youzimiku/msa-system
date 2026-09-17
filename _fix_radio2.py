# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# Char + Sampling 状态（fs2，启用/停用）—— 全部替换
old1 = """<Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fs2} onChange={setFs2}/>"""
new1 = """<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fs2||''} onChange={e=>setFs2(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'启用',label:'启用'},{value:'停用',label:'停用'}]}/>"""
n1 = src.count(old1)
src = src.replace(old1, new1)
print('fs2 状态 Radio:', n1, '处替换')

# Grr + Kappa（及同款）记录状态（6 项）—— 全部替换
old2 = """<Select allowClear placeholder="记录状态" style={{width:140}} value={fstatus} options={['待采集','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>"""
new2 = """<Radio.Group size="small" optionType="button" buttonStyle="solid" value={fstatus||''} onChange={e=>setFstatus(e.target.value||undefined)} options={[{value:'',label:'全部'},{value:'待采集',label:'待采集'},{value:'待审核',label:'待审核'},{value:'已批准',label:'已批准'},{value:'需整改',label:'需整改'},{value:'已闭环',label:'已闭环'},{value:'已关闭',label:'已关闭'}]}/>"""
n2 = src.count(old2)
src = src.replace(old2, new2)
print('记录状态 Radio:', n2, '处替换')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
