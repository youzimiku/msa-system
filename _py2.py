# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 1) 页面末尾渲染日志弹窗
a1 = '''    {modal && <SampleLibModal value={modal} onClose={()=>setModal(null)}/>}
  </div>;
}
function SampleLibModal({value,onClose}){'''
b1 = '''    {modal && <SampleLibModal value={modal} onClose={()=>setModal(null)}/>}
    {logOpen && <SampleLibLogModal onClose={()=>setLogOpen(false)}/>}
  </div>;
}
function SampleLibLogModal({onClose}){
  const d=Store.get();
  const logs=(d.sampleLibLogs||[]).slice();
  const cols=[
    {title:'日志编号', dataIndex:'id', width:110, render:v=><span className="mono">{v}</span>},
    {title:'变更时间', dataIndex:'time', width:150},
    {title:'样本编号', dataIndex:'sampleId', width:100, render:v=><span className="mono">{v}</span>},
    {title:'样本名称', width:180, render:(_,r)=>{ const s=(d.sampleLib||[]).find(x=>x.id===r.sampleId); return <span>{s? s.name : '暂无'}</span>; }},
    {title:'变更字段', dataIndex:'field', width:130},
    {title:'变更前', dataIndex:'before', width:110, render:v=><span className="mono">{v||'—'}</span>},
    {title:'变更后', dataIndex:'after', width:110, render:v=><span className="mono">{v||'—'}</span>},
    {title:'操作人', dataIndex:'actor', width:100},
    {title:'说明', dataIndex:'note', width:280, ellipsis:true}
  ];
  return <Modal title="样本库变更日志" open width={1180} footer={null} onCancel={onClose} destroyOnClose>
    <Table size="small" rowKey="id" dataSource={logs} columns={cols} scroll={{x:1100}} pagination={false}/>
  </Modal>;
}
function SampleLibModal({value,onClose}){'''
assert src.count(a1) == 1, 'a1 count=%d' % src.count(a1)
src = src.replace(a1, b1, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
