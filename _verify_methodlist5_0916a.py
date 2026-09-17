# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(mode='inst', withRows=False):
    c = orig.replace("useState('instgroup')", "useState('plan')")
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
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)
    body = re.sub(r'<script[^>]*>.*?</script>', '', out, flags=re.S)
    i = body.find('分析方法</div>')
    return body[max(0,i-100): i+3500]

print('=== GRR 已入列表（联动禁用验证） ===')
a1 = render(withRows=True)
print('确定按钮:', '确 定</span>' in a1)
print('GRR 勾选框被禁用:', 'ant-checkbox-wrapper-disabled' in a1)
print('linear/cgcgk 未被禁用:', a1.count('ant-checkbox-wrapper-disabled') == 1)
# GRR 行渲染 + 行内输入框 + 保存/删除
print('GRR 表格行:', 'GRR' in a1 and '>保存<' in a1 and '>删除<' in a1)
print('行内数字输入框(人数/次数/样本数):', a1.count('ant-input-number') >= 3)
print()
print('=== 人员弹窗 KAPPA（未入列表，可手动勾选） ===')
b2 = render(mode='person')
print('KAPPA 勾选框存在:', 'KAPPA' in b2)
print('KAPPA 未被禁用(可手动勾选):', 'ant-checkbox-wrapper-disabled' not in b2)
print('确定按钮:', '确 定</span>' in b2)
print('RESTORED')
