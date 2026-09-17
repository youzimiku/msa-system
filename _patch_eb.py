# -*- coding: utf-8 -*-
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()

anchor = 'const NavAPI = { go:()=>{}, openGrr:()=>{}, openKappa:()=>{}, openAnl:()=>{}, openInst:()=>{}, openCalibInst:()=>{} };'
eb = anchor + '''
class EB extends React.Component {
  constructor(p){super(p); this.state={err:null};}
  static getDerivedStateFromError(e){ return {err:e}; }
  componentDidCatch(e){ try{ window.__errs=(window.__errs||[]).concat([String(e&&e.stack||e)]); }catch(_){} }
  render(){ if(this.state.err) return <div style={{color:'#c00',padding:24,whiteSpace:'pre-wrap',fontFamily:'monospace',fontSize:12}}>ERR: {String(this.state.err&&this.state.err.stack||this.state.err)}</div>; return this.props.children; }
}'''
assert anchor in s, 'anchor1 missing'
s = s.replace(anchor, eb, 1)

old = '<Content className="app-content">{renderPage()}</Content>'
new = '<Content className="app-content"><EB>{renderPage()}</EB></Content>'
assert old in s, 'anchor2 missing'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
