# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

# 语法粗查：括号配平（跳过字符串/模板字符串/注释）
def rough_balance(s):
    depth = 0; i = 0; n = len(s); in_str=None; esc=False; line=1
    while i < n:
        ch = s[i]
        if ch == '\n': line += 1
        if in_str:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == in_str: in_str = None
            i += 1; continue
        if ch in ('"', "'", '`'):
            in_str = ch; i += 1; continue
        if s.startswith('//', i):
            j = s.find('\n', i); i = n if j < 0 else j; continue
        if s.startswith('/*', i):
            j = s.find('*/', i+2); i = n if j < 0 else j+2; continue
        if ch in '({[': depth += 1
        elif ch in ')}]':
            depth -= 1
            if depth < 0: return False, line, 'unbalanced close'
        i += 1
    return depth == 0, line, 'depth=%d' % depth

ok, ln, msg = rough_balance(t)
print('括号配平:', ok, msg)

# 断言关键修改存在
checks = [
    ("specialChars=[", "特殊特性 seed"),
    ("if(!c.specialCharId)", "被测参数迁移 specialCharId"),
    ("{title:'特殊特性', width:176", "被测参数列表特殊特性列"),
    ("{key:'specialChar',label:'特殊特性'", "详情特殊特性行"),
    ("const [groupView,setGroupView]=useState(null);", "groupView state"),
    ("onClick={()=>setGroupView(r)}>器具组", "器具组按钮"),
    ("检验标准 '+groupView.id+' · 绑定的器具组", "器具组弹窗"),
    ("const [qualityChar,setQualityChar]=useState('');", "质量特性 state"),
    ("<span className=\"flt-label\">质量特性</span>", "质量特性下拉"),
]
for k, name in checks:
    print('断言', name, ':', '存在' if k in t else '缺失!!')
# 确认绑定器具组列已从 stdCols 移除（仅剩 StandardPage 的一处）
print('stdCols 绑定器具组列剩余出现次数:', t.count("render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className=\"tiny\">{gs.map(g=>g.name).join('、')}</span> : <span className=\"tiny\">暂无</span>; },"))
