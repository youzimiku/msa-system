# -*- coding: utf-8 -*-
import io, subprocess, sys, re
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

for page, name in [('entry_grr','GRR台账'), ('entry_kappa','KAPPA台账'), ('entry_linear','线性/偏移台账'), ('entry_stability','稳定性台账'), ('entry_cgcgk','CG/CGK台账')]:
    b = render(page)
    has = '样本/人员选择' in b
    hasOp = '操作人' in b and '审核' in b
    hasErr = ('Uncaught' in b and 'body' in b) or 'throw new Error' in b
    print(name, '| 样本/人员选择按钮:', has, '| 操作列其他按钮存在:', hasOp, '| 渲染异常:', hasErr)
print('RESTORED')
