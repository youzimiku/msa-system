# -*- coding: utf-8 -*-
"""修复 VerdictTag 损坏行"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

broken = '''function VerdictTag({v}){ const vv=(!v||v==='-')?'待采集':v; return <Tooltip title={TIPS.verdict[vv]||TIPS.verdict[v]||vv}><Tag color={verdictColor(vv)} className="spec-tag">{vv}</Tag></Tooltip>; } className="spec-tag" style={{minWidth:84,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{v}</Tag>; }'''
fixed = '''function VerdictTag({v}){ const vv=(!v||v==='-')?'待采集':v; return <Tooltip title={TIPS.verdict[vv]||TIPS.verdict[v]||vv}><Tag color={verdictColor(vv)} className="spec-tag" style={{minWidth:84,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{vv}</Tag></Tooltip>; }'''
n = s.count(broken)
print('broken x', n)
s = s.replace(broken, fixed)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
