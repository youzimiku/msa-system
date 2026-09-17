# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page, mode='inst', withRows=False):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    c = c.replace("const [batchModal,setBatchModal]=useState(null);",
                  "const [batchModal,setBatchModal]=useState({mode:'" + mode + "'});")
    c = c.replace("const [charSel,setCharSel]=useState('');",
                  "const [charSel,setCharSel]=useState('CHAR-2026-001');")
    if withRows:
        c = c.replace("const [methodRows,setMethodRows]=useState([]);",
                      "const [methodRows,setMethodRows]=useState([{method:'GRR',std:'STD-MSA-001',ops:3,trials:3,parts:10,saved:true}]);")
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

b  = strip_scripts(render('plan'))
b3 = strip_scripts(render('plan', withRows=True))

print('确定按钮(span包裹):', '确定</span>' in b)
# 分析方法模块区域：定位“分析方法”标题到表格结束，检查该区域 disabled 勾选框
def modal_method_area(dom):
    i = dom.find('分析方法')
    j = dom.find('未添加分析方法')
    if j < 0: j = dom.find('样本数')
    if j < 0: return dom[i:i+4000]
    return dom[i:j+2000]

a0 = modal_method_area(b)
a1 = modal_method_area(b3)
print('未入列表时 方法区 disabled 勾选框数:', a0.count('ant-checkbox-wrapper-disabled'))
print('GRR 已入列表时 方法区 disabled 勾选框数:', a1.count('ant-checkbox-wrapper-disabled'))
print('方法区 GRR checkbox:', 'GRR' in a0, '| linear checkbox:', 'LINEAR' in a0, '| Cg/Cgk:', 'CG/CGK' in a0)
print('RESTORED')
