# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

def show(anchor, before=100, after=320, tag=''):
    i = s.find(anchor)
    print('==', tag or anchor[:40], '@', i, '==')
    if i >= 0:
        print(s[max(0,i-before):i+after].replace('\n', '⏎'))
    print()

show('结论取最差档：任一项')
show('暂无待采集记录')
show('form-hin')
show('label(')
show('未识别公差')
show('数据录入方式')
# 全部 label 双参调用（desc）
for m in re.finditer(r"label\('([^']{2,60})',\s*'([^']{2,80})'\)", s):
    print('label-desc:', m.group(1)[:40], '||', m.group(2)[:60])
print()
# AnlDetail 说明段
for m in re.finditer(r'<div className="tiny mt8">', s):
    print('mt8 @', m.start(), '::', s[m.start():m.start()+150].replace('\n','⏎')[:150])
