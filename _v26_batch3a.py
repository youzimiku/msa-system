# -*- coding: utf-8 -*-
"""v2.6 第三批 a（按行号）：清理说明性文字 + KappaEntry 保留三维原始数据"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(P, encoding='utf-8').read().split('\n')

def drop(pred, tag):
    global lines
    hit = [i for i, l in enumerate(lines) if pred(l)]
    assert len(hit) == 1, 'FAIL %s: 命中 %d' % (tag, len(hit))
    del lines[hit[0]]
    print(tag, '删除行', hit[0]+1)

# 1. 校准登记说明
drop(lambda l: '登记后：台账自动更新' in l, 'calib-hint')
# 2. ConvertModal 取样策略说明
drop(lambda l: '取样策略（业务确认默认值' in l, 'convert-hint')
# 3. GRR 提交说明
drop(lambda l: '提交后自动完成变差分解与判定' in l, 'grr-submit-hint')
# 4. KAPPA 录入说明 → 替换为只保留检验标准动态行
hit = [i for i, l in enumerate(lines) if '每行首列为样本参考判定' in l]
assert len(hit) == 1, 'kappa-hint 命中 %d' % len(hit)
lines[hit[0]] = '        <div className="form-hint">检验标准：<span className="mono">{rec.standard||\'暂无\'}</span></div>'
print('kappa-hint 替换行', hit[0]+1)

# 5. KappaEntry 提交：存三维原始数据 rawData + 二维 appData
s = '\n'.join(lines)
old = "k.reference=ref; k.appData=judg; k.appNames=appNames; k.analysisDate=TODAY; k.analyst=s.me.name;"
new = "k.reference=ref; k.appData=appData; k.rawData=judg; k.numTrials=numTrials; k.numApp=numApp; k.numSamples=numSamples; k.appNames=appNames; k.analysisDate=TODAY; k.analyst=s.me.name;"
assert s.count(old) == 1, 'kappa-rawdata 命中 %d' % s.count(old)
s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s)
print('batch3a OK 长度', len(s))
