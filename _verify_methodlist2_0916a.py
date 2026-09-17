# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page, mode='inst', withChar=True, withRows=False):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    c = c.replace("const [batchModal,setBatchModal]=useState(null);",
                  "const [batchModal,setBatchModal]=useState({mode:'" + mode + "'});")
    if withChar:
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

b = strip_scripts(render('plan'))
print('=== 器具弹窗（已选被测参数，未入列表） ===')
print('确定按钮:', '>确定<' in b)
print('表格表头齐全:', all(x in b for x in ['>分析方法<','>人数<','>次数<','>样本数<','>操作<']))
print('空态文案:', '未添加分析方法' in b)
print('GRR 勾选框未禁用:', 'ant-checkbox-wrapper-disabled' not in b)

b2 = strip_scripts(render('plan', mode='person'))
print('=== 人员弹窗（KAPPA 未入列表） ===')
print('KAPPA 勾选框存在:', 'KAPPA' in b2)
print('KAPPA 未禁用(可手动勾选):', 'ant-checkbox-wrapper-disabled' not in b2)

b3 = strip_scripts(render('plan', withRows=True))
print('=== 器具弹窗（GRR 已入列表） ===')
print('GRR 勾选框已禁用:', 'ant-checkbox-wrapper-disabled' in b3)
print('表格渲染一行 GRR:', 'GRR' in b3)
print('行内保存按钮:', '>保存<' in b3)
print('行内删除按钮:', '>删除<' in b3)
print('RESTORED')
