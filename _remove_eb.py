# -*- coding: utf-8 -*-
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()

# 1) 删除 EB class 定义
eb = '''class EB extends React.Component {
  constructor(p){super(p); this.state={err:null};}
  static getDerivedStateFromError(e){ return {err:e}; }
  componentDidCatch(e){ try{ window.__errs=(window.__errs||[]).concat([String(e&&e.stack||e)]); }catch(_){} }
  render(){ if(this.state.err) return <div style={{color:'#c00',padding:24,whiteSpace:'pre-wrap',fontFamily:'monospace',fontSize:12}}>ERR: {String(this.state.err&&this.state.err.stack||this.state.err)}</div>; return this.props.children; }
}
'''
anchor = 'const NavAPI = { go:()=>{}, openGrr:()=>{}, openKappa:()=>{}, openAnl:()=>{}, openInst:()=>{}, openCalibInst:()=>{} };'
assert s.count(eb) == 1, 'EB block not found: %d' % s.count(eb)
s = s.replace(eb, '', 1)

# 2) 恢复 renderPage 直接调用
old = '<Content className="app-content"><EB>{renderPage()}</EB></Content>'
new = '<Content className="app-content">{renderPage()}</Content>'
assert s.count(old) == 1, 'EB wrapper not found'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('EB removed, len', len(s))
