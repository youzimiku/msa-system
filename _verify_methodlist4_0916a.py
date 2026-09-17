# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(withRows=False, mode='inst'):
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
    body = out[out.find('<body'):] if '<body' in out else out
    return re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.S)

b  = render()
b3 = render(withRows=True)

# 定位弹窗内方法区：从“未添加分析方法”(空态) 或 ant-table 往前找 grp-label
def area(dom):
    j = dom.find('未添加分析方法')
    if j < 0:
        j = dom.find('ant-table')  # 有行时
    if j < 0: return ''
    return dom[max(0,j-3000): j+2500]

a0 = area(b)
a1 = area(b3)
print('=== 未入列表 方法区 ===')
print('长度:', len(a0))
print('确定按钮:', '确定' in a0)
print('勾选框GRR/linear/cgcgk:', all(x in a0 for x in ['GRR','LINEAR','CG/CGK']))
print('方法区 disabled 勾选框数:', a0.count('ant-checkbox-wrapper-disabled'))

print('=== GRR已入列表 方法区 ===')
print('长度:', len(a1))
print('确定按钮:', '确定' in a1)
print('GRR行 + 保存/删除:', all(x in a1 for x in ['GRR','>保存<','>删除<']))
print('方法区 disabled 勾选框数:', a1.count('ant-checkbox-wrapper-disabled'))
# 找确定按钮上下文
k = b.find('确定')
print('全局“确定”上下文:', b[max(0,k-120):k+80])
