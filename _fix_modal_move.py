# -*- coding: utf-8 -*-
"""1) 测量人员移到复评提前提醒后面，占2列宽(lg=8, 宽度撑满)
2) 器具筛选（查询条件）每行6列（lg=4）"""
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:60], n, cnt)
    s = s.replace(old, new)

# 1) 测量人员 Col：从原位置删除，插到复评提前提醒后面（占2列 lg=8，宽度撑满）
old_measurer = """<Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">测量人员</span><Select mode="multiple" size="small" style={{width:140}} placeholder="选择测量人员（可多选）" value={meta.measurers||[]} options={['王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'].map(n=>({value:n,label:n}))} onChange={v=>setMetaK('measurers',v)}/></Col>"""
rep(old_measurer, "")

new_measurer = """<Col xs={24} sm={12} md={8} lg={8}><span className="flt-label">测量人员</span><Select mode="multiple" size="small" style={{width:'100%'}} placeholder="选择测量人员（可多选）" value={meta.measurers||[]} options={['王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'].map(n=>({value:n,label:n}))} onChange={v=>setMetaK('measurers',v)}/></Col>"""
anchor = """<Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">复评提前提醒（天）</span><InputNumber size="small" min={1} max={90} style={{width:140}} value={reviewAdvance} onChange={v=>setReviewAdvance(v||20)}/></Col>"""
rep(anchor, anchor + "\n        " + new_measurer)

# 2) 器具筛选区 6列：lg={6}→lg={4}（仅器具筛选区 5 个字段，无 md={8}）
n6 = s.count('<Col xs={24} sm={12} lg={6}>')
assert n6 == 5, n6
s = s.replace('<Col xs={24} sm={12} lg={6}>', '<Col xs={24} sm={12} lg={4}>')
print('filter cols ->6col:', n6)

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
