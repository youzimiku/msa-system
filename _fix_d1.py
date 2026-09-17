# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = """  return <Modal title={isEdit?'编辑器具组':'新增器具组'} open width={760} onCancel={onClose} onOk={onOk} okText="保存" destroyOnClose>
    <Form form={form} layout="vertical" size="small">"""
new = """  return <Modal title={isEdit?'编辑器具组':'新增器具组'} open width={760} onCancel={onClose} onOk={onOk} okText="保存" destroyOnClose>
    <Form form={form} layout="vertical" size="small" onValuesChange={onValuesChange}>"""
n = src.count(old)
print('D1 精确定位:', n, '次', '-> 替换' if n==1 else '!!跳过')
if n == 1:
    src = src.replace(old, new)
    open(p, 'w', encoding='utf-8').write(src)
    print('写入完成, 大小:', len(src))
