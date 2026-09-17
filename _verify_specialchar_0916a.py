# -*- coding: utf-8 -*-
import io, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page, open_modal=False):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    if open_modal:
        c = c.replace("const [batchModal,setBatchModal]=useState(null);",
                      "const [batchModal,setBatchModal]=useState({mode:'inst'});")
    io.open(path, 'w', encoding='utf-8').write(c)
    try:
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        return out[out.find('<body'):] if '<body' in out else out
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

b = render('char')
print('=== 被测参数维护 ===')
print('被测参数列表-特殊特性表头:', '特殊特性' in b)
print('特殊特性值 SC-001:', 'SC-001' in b and '轴径 φ50' in b)
print('检验标准列表-绑定器具组表头(应无):', '绑定器具组' not in b)
print('检验标准操作列-器具组按钮:', '器具组' in b)
print('详情-特殊特性:', b.count('特殊特性') >= 2)

b2 = render('plan', open_modal=True)
print('=== MSA计划(弹窗打开) ===')
print('弹窗-质量特性字段:', '质量特性' in b2)
print('弹窗-质量特性选项 SC-001 轴径 φ50:', 'SC-001' in b2 and '轴径 φ50' in b2)
print('弹窗-零件名称存在:', '零件名称' in b2)
print('RESTORED')
