# -*- coding: utf-8 -*-
"""修复：1) 样本页操作列加宽防遮挡；2) 全站输入控件宽度统一（关键词280/下拉140/数字140）"""
import io, re

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'expect %d of [%s...] got %d' % (n, old[:70], c)
    s = s.replace(old, new, n)

def rep_re(pat, repl, n=None, label=''):
    global s
    hits = len(re.findall(pat, s))
    if n is not None:
        assert hits == n, 'regex [%s] expect %d hits, got %d (%s)' % (pat, n, hits, label)
    elif hits == 0:
        assert False, 'regex [%s] no hit (%s)' % (pat, label)
    s = re.sub(pat, repl, s)

# ---------- 1) 样本页操作列 90 -> 150（防编辑按钮被编号列遮挡/覆盖） ----------
rep("{title:'操作', width:90, render:(_,r)=><Space size={2}><Button size=\"small\" type=\"link\" onClick={()=>setDetail(r)}>查看明细</Button>",
    "{title:'操作', width:150, render:(_,r)=><Space size={2}><Button size=\"small\" type=\"link\" onClick={()=>setDetail(r)}>查看明细</Button>", 1)

# ---------- 2) 查询关键词框统一 280 ----------
rep('style={{width:300}}', 'style={{width:280}}', 5)          # 标准/样本/AnlPage/GRR/KAPPA
rep('style={{width:320,marginBottom:14}}', 'style={{width:280,marginBottom:14}}', 1)  # 审计日志

# ---------- 3) Select 下拉统一 140 ----------
rep_re(r'(<Select[^>]*style=\{\{width:)130(\}\})', r'\g<1>140\g<2>', n=13, label='select-130')
rep_re(r'(<Select[^>]*style=\{\{width:)150(\}\})', r'\g<1>140\g<2>', n=3, label='select-150')
rep_re(r'(<Select[^>]*style=\{\{width:)120(\}\})', r'\g<1>140\g<2>', n=1, label='select-120')
# 台账页「当前器具组」选择器 230 -> 180（页内工具行，避免与其他输入框悬殊）
rep_re(r'(<Select[^>]*style=\{\{width:)230(\}\})', r'\g<1>180\g<2>', n=1, label='select-230')

# ---------- 4) 数字输入统一 140 ----------
rep_re(r'(<Input\s[^>]*style=\{\{width:)130(\}\})', r'\g<1>140\g<2>', n=1, label='input-130')   # 未来N天到期
rep_re(r'(<Input\s[^>]*style=\{\{width:)120(\}\})', r'\g<1>140\g<2>', n=1, label='input-120')   # 稳定性参考值

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
