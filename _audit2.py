# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()

def show(kw, label, limit=30, start=0):
    print('==== ' + label + ' ====')
    n = 0
    for i, l in enumerate(lines):
        if i < start:
            continue
        s = l.strip()
        if kw in s:
            print(i + 1, s[:240])
            n += 1
            if n >= limit:
                break
    print()

show('ANAL_SHORT', 'ANAL_SHORT定义', 8)
show('去录入', '台账操作列-去录入', 20)
show('>分析</Button>', '台账-分析按钮', 20)
show('ImportBtn', '导入按钮使用', 25)
show('setLibModal', '样本库弹窗', 12)
show('sampleLibModal', '样本库弹窗2', 12)
show('sampleMin', '取样范围字段使用', 20)
show('form.setFieldsValue({charId', '样本库编辑', 6)
show('有效', '样本库有效期', 20)
show('真值', '样本库真值', 20)
show('refValue', 'refValue', 20)
