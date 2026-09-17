# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = io.open(P, encoding='utf-8').read().splitlines(keepends=True)

PLACEHOLDER = {
    1754: '支持：编号/名称/型号/出厂编号/领用人',
    2060: '支持：组编码/组名称/说明',
    2237: '支持：器具编号/器具名称/校准机构/证书编号',
    2374: '支持：计划号/器具编号/器具名称/零件号/零件名称',
    2912: '支持：标准编号/标准名称/零件名称/工序名称/检验依据',
    3108: '支持：参数编号/参数名称/零件号/零件名称/工序名称',
    3360: '支持：方法代码/方法名称（判断规则：规则编号/方法/结论）',
    3609: '支持：样本编号/样本名称/零件号/被测项目',
    3724: '支持：样本编号/样本名称/器具编号/计划号',
    3965: '支持：台账编号/计划号/器具编号/器具名称/测量对象',
    4250: '支持：台账编号/计划号/器具编号/器具名称/测量对象',
    4429: '支持：台账编号/计划号/器具编号/器具名称/测量对象',
    4593: '支持：台账编号/计划号/器具编号/器具名称/测量对象',
}

for ln, tip in PLACEHOLDER.items():
    i = ln - 1
    assert '>关键词</span><Input allowClear style={{width:140}}' in lines[i], '行 %d 锚点不符: %s' % (ln, lines[i].strip()[:120])
    old_line = lines[i]
    new_line = old_line.replace(
        '>关键词</span><Input allowClear style={{width:140}}',
        '>关键词</span><Input allowClear placeholder="%s" style={{width:220}}' % tip, 1)
    assert new_line != old_line
    lines[i] = new_line
    print('OK 行 %d' % ln)

io.open(P, 'w', encoding='utf-8').write(''.join(lines))
print('完成，共 %d 处' % len(PLACEHOLDER))
