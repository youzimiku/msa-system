# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# AnlPage: add anlRec state
a1 = '''  const [detail,setDetail]=useState(null);
  const [entryRec,setEntryRec]=useState(null);
  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);'''
b1 = '''  const [detail,setDetail]=useState(null);
  const [entryRec,setEntryRec]=useState(null);
  const [anlRec,setAnlRec]=useState(null);
  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);'''
assert src.count(a1) == 1, 'a1=%d' % src.count(a1)
src = src.replace(a1, b1, 1)

# AnlPage: operation column
a2 = '''    {title:'操作', width:200, fixed:'left', render:(_,r)=><Space size={0}>
      {(r.reviewStatus==='待采集'||r.reviewStatus==='待分析') && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind); }}>{r.reviewStatus==='待分析'?'修改数据':'去录入'}</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},'''
b2 = '''    {title:'操作', width:260, fixed:'left', render:(_,r)=><Space size={0}>
      {r.reviewStatus==='待采集' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind); }}>去录入</Button>}
      {r.reviewStatus==='待分析' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>setAnlRec(r)}>手动分析</Button>}
      {r.reviewStatus==='待分析' && <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>{ DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind); }}>修改数据</Button>}
      <Button size="small" type="link" onClick={()=>doImport(r,kind)}>导入</Button>
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},'''
assert src.count(a2) == 1, 'a2=%d' % src.count(a2)
src = src.replace(a2, b2, 1)

# AnlPage: render AnalyzeModal
a3 = '''    {detail && <AnlDetail rec={detail} kind={kind} onClose={()=>setDetail(null)}/>}
  </div>;
}'''
b3 = '''    {detail && <AnlDetail rec={detail} kind={kind} onClose={()=>setDetail(null)}/>}
    {anlRec && <AnalyzeModal rec={anlRec} kind={kind} onClose={()=>setAnlRec(null)}/>}
  </div>;
}'''
assert src.count(a3) == 1, 'a3=%d' % src.count(a3)
src = src.replace(a3, b3, 1)

open(p, 'w', encoding='utf-8').write(src)
print('anl ok')
