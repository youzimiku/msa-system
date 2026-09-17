# -*- coding: utf-8 -*-
import io, re, subprocess, sys
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

def strip_scripts(s):
    return re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)

b = render('char')
b2 = strip_scripts(b)
print('=== 被测参数维护（剔除 script 后） ===')
print('操作列「器具组」按钮:', '>器具组<' in b2)
print('特殊特性列已选值 SC-001:', 'SC-001' in b2)
# 找 ant-select-selection-item 里的值
for m in re.finditer(r'ant-select-selection-item[^>]*>([^<]*)<', b2):
    if 'SC' in m.group(1): print('Select 已选值:', m.group(1))
print('详情「特殊特性」行:', '>特殊特性<' in b2)
print('检验标准「绑定器具组」表头(应无):', '>绑定器具组<' in b2)

b3 = render('plan', open_modal=True)
b4 = strip_scripts(b3)
print('=== MSA计划弹窗（剔除 script 后） ===')
print('质量特性字段:', '>质量特性<' in b4)
print('质量特性下拉渲染:', 'ant-select' in b4)
print('RESTORED')
