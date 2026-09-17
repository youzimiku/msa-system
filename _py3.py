# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# ---- GrrPage: 手动分析 + 导入 ----
a1 = '''function GrrPage(){
  const d=Store.get();
  const [detail,setDetail]=useState(null);
  const [fkw,setFkw]=useState('');'''
b1 = '''function GrrPage(){
  const d=Store.get();
  const [detail,setDetail]=useState(null);
  const [anlRec,setAnlRec]=useState(null);
  const [fkw,setFkw]=useState('');'''
assert src.count(a1) == 1, 'a1=%d' % src.count(a1)
src = src.replace(a1, b1, 1)

a2 = '''    {title:'操作', width:200, fixed:'left', render:(_,r)=><Space size={0}>
      {r.reviewStatus==='待采集' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind:'grr',id:r.id}; NavAPI.go('data_grr'); }}>去录入</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button>
    </Space>},'''
b2 = '''    {title:'操作', width:260, fixed:'left', render:(_,r)=><Space size={0}>
      {r.reviewStatus==='待采集' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind:'grr',id:r.id}; NavAPI.go('data_grr'); }}>去录入</Button>}
      {r.reviewStatus==='待分析' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>setAnlRec(r)}>手动分析</Button>}
      {r.reviewStatus==='待分析' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind:'grr',id:r.id}; NavAPI.go('data_grr'); }}>修改数据</Button>}
      <Button size="small" type="link" onClick={()=>doImport(r,'grr')}>导入</Button>
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button>
    </Space>},'''
assert src.count(a2) == 1, 'a2=%d' % src.count(a2)
src = src.replace(a2, b2, 1)

a3 = '''    {detail && <GrrDetail rec={detail} onClose={()=>setDetail(null)}/>}
    
  </div>;
}'''
b3 = '''    {detail && <GrrDetail rec={detail} onClose={()=>setDetail(null)}/>}
    {anlRec && <AnalyzeModal rec={anlRec} kind="grr" onClose={()=>setAnlRec(null)}/>}
  </div>;
}'''
assert src.count(a3) == 1, 'a3=%d' % src.count(a3)
src = src.replace(a3, b3, 1)

open(p, 'w', encoding='utf-8').write(src)
print('grr ok')
