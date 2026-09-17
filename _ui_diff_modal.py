# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read().split('\n')
new = open(NEW, encoding='utf-8').read().split('\n')

def slice_(lines, name):
    start=None; depth=0
    for i,l in enumerate(lines):
        if re.search(r'function '+name+r'\(', l): start=i; depth=0
        if start is not None and i>=start:
            depth += l.count('{')-l.count('}')
            if depth==0 and i>start: return '\n'.join(lines[start:i+1])
    return ''

def fields(src):
    """提取表单字段 label + Input/Select/TreeSelect 等控件顺序"""
    out=[]
    for m in re.finditer(r'(?:<Form\.Item|label=|title=|placeholder=|<Input|<Select|<TreeSelect|<DatePicker|<InputNumber|<Radio|<Checkbox|dataIndex|key:)\s*(["\']?)([^"\'>]{2,40}?)\1', src):
        pass
    return out

# BatchPlanModal 对比：抓 Form.Item label 序列
ob = slice_(old, 'BatchPlanModal')
nb = slice_(new, 'BatchPlanModal')
def flabels(src):
    return re.findall(r'<Form\.Item[^>]*label="([^"]{2,40})"', src)
print('旧创建弹窗 Form.Item label:', ' | '.join(flabels(ob)))
print()
print('新创建弹窗 Form.Item label:', ' | '.join(flabels(nb)))
print()
# 新弹窗里出现的 Select/TreeSelect/Input 提示
print('新弹窗 placeholder:', set(re.findall(r'placeholder="([^"]{2,40})"', nb)))
print('旧弹窗 placeholder:', set(re.findall(r'placeholder="([^"]{2,40})"', ob)))
