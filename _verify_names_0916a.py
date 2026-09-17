# -*- coding: utf-8 -*-
import io, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    io.open(path, 'w', encoding='utf-8').write(c)
    try:
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        return out[out.find('<body'):] if '<body' in out else out
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

b = render('char')
print('被测参数维护 | 分析方法列名:', '分析方法' in b and '检验方法' not in b.split('记录列表')[0].replace('检验方法(',''))
b2 = render('sampling')
print('抽样方法维护 | LIN_BIAS:', 'LIN_BIAS' in b2)
b3 = render('entry_linear')
print('线性/偏倚台账 | 台账名:', '线性/偏倚台账' in b3, '| 旧名残留:', '线性/偏移台账' in b3)
b4 = render('data_linear')
print('线性/偏倚录入 | 页面标题:', '线性/偏倚' in b4)
# 菜单检查（所有页面共用菜单，取任意一次渲染）
print('菜单线性/偏倚台账:', '线性/偏倚台账' in b2, '| 菜单线性/偏倚录入数据:', '线性/偏倚录入数据' in b2, '| 菜单旧名残留:', '线性/偏移台账' in b2 or '线性/偏移录入数据' in b2)
print('RESTORED')
