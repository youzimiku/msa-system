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

op = slice_(old, 'PlanPage')
np_ = slice_(new, 'PlanPage')
# 提取 columns 数组里的 title 顺序
def colseq(src):
    seq=[]
    # title: 'x' 或 title:'x'（含动态 title: ...）
    for m in re.finditer(r"title:\s*'([^']{2,30})'", src):
        seq.append(m.group(1))
    return seq
print('旧 MSA计划列序:', ' → '.join(colseq(op)))
print('新 MSA计划列序:', ' → '.join(colseq(np_)))
print()
print('旧含CG/CGK:', 'CG/CGK' in op, '| 新含CG/CGK:', 'CG/CGK' in np_)
print('旧含分计划:', '分计划' in op, '| 新含分计划:', '分计划' in np_)
print('旧含分析方法:', '分析方法' in op, '| 新含分析方法:', '分析方法' in np_)
print('旧含判定结果:', '判定结果' in op, '| 新含判定结果:', '判定结果' in np_)
