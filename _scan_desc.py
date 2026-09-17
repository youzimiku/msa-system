# -*- coding: utf-8 -*-
"""扫描全站说明性文字候选（只读）"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) tiny span 内文本（排除纯数据/占位）
print('==== <span className="tiny"> 内含说明性词 ====')
kw = ['查询 / 重置', '取样', '说明', '会议口径', '速查', '默认', '固化', '操作指导', '提示', '注意', '请先', '可调', '一器一计划', '按业务', '按方法', '映射', '待转', '跳转', '在最前', '一级', '二级', '策略', '规范', '口径', '流程', '步骤', '录入', '提交后', '审核', '闭环', '自动', '绑定', '复评', '生效', '挑样', '状态一致性', '辅助', '每行', '单方法', '多方法', '覆盖', '结果', '查看', '管理', '维护', '新增', '移除', '优先', '规划', '用于', '建议', '从 ', '从「', '在「']
lines = s.split('\n')
for i, ln in enumerate(lines):
    for m in re.finditer(r'<span className="tiny">([^<]+)</span>', ln):
        txt = m.group(1)
        if any(k in txt for k in kw):
            a = max(0, m.start()-70)
            print('L%d :: %s' % (i+1, ln[max(0,m.start()-55):m.end()+10].strip()[:220]))

print()
print('==== <div className="tiny ..."> 说明块 ====')
for i, ln in enumerate(lines):
    for m in re.finditer(r'<div className="tiny[^"]*">([^<]*)</div>', ln):
        txt = m.group(1)
        if txt and len(txt) > 6:
            print('L%d :: %s' % (i+1, ln[max(0,m.start()-40):m.end()+10].strip()[:220]))

print()
print('==== Alert type=info ====')
for m in re.finditer(r'<Alert type="info"[^>]*message=\{?\'?\"?([^\'}]{6,160})', s):
    print('@%d :: %s' % (m.start(), m.group(1)[:160]))

print()
print('==== 含「说明：」文本 ====')
for m in re.finditer(r'说明[：:]', s):
    a = max(0, m.start()-60)
    print('@%d :: %s' % (m.start(), s[a:m.start()+160].replace('\n', ' ')[:220]))
