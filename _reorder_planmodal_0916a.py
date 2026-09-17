# -*- coding: utf-8 -*-
import datetime, io, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
t = io.open(P, encoding='utf-8').read()

# 1) 改动前快照
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
snap = ROOT + r'\index_备份_' + ts + '_模块顺序换位前.html'
shutil.copy2(P, snap)
print('快照:', snap)

# 2) 切出三个模块并换位：器具选择(C) -> 计划填写信息(A) -> 分析方法(B)
A_head = "    <div style={{flexShrink:0, border:'1px solid #e3eaf3', borderRadius:6, padding:'8px 10px 10px', marginBottom:8, background:'#fafcff'}}>\n      <div className=\"grp-label\" style={{marginBottom:6}}>计划填写信息</div>"
B_head = "    <div style={{flexShrink:0, border:'1px solid #e3eaf3', borderRadius:6, padding:'8px 10px 10px', marginBottom:8, background:'#fafcff', maxHeight:230, overflow:'auto'}}>\n      <div className=\"grp-label\" style={{marginBottom:6}}>分析方法</div>"
C_head = "    <div style={{flex:1, minHeight:0, border:'1px solid #e3eaf3', borderRadius:6, padding:'8px 10px 10px', background:'#fafcff', display:'flex', flexDirection:'column'}}>\n      <div className=\"grp-label\" style={{marginBottom:6, flexShrink:0}}>器具选择</div>"

iA = t.index(A_head)
iB = t.index(B_head)
iC = t.index(C_head)
assert iA < iB < iC, '模块顺序异常'

blockA = t[iA:iB]          # 计划填写信息
blockB = t[iB:iC]          # 分析方法
blockC_end = t.index('\n    </div>\n  </Modal>;', iC)
blockC = t[iC:blockC_end]  # 器具选择（含闭合 </div>）
tail = t[blockC_end:]

new = t[:iA] + blockC + blockA + blockB + tail
io.open(P, 'w', encoding='utf-8').write(new)
print('换位完成：器具选择 -> 计划填写信息 -> 分析方法')

# 3) 断言新顺序
chk = io.open(P, encoding='utf-8').read()
o1 = chk.index('>器具选择<')
o2 = chk.index('>计划填写信息<')
o3 = chk.index('>分析方法<')
print('DOM/源码顺序 器具选择(%d) < 计划填写信息(%d) < 分析方法(%d):' % (o1, o2, o3), o1 < o2 < o3)
print('模块数量：计划填写信息', chk.count('>计划填写信息<'), '| 分析方法', chk.count('>分析方法<'), '| 器具选择', chk.count('>器具选择<'))
