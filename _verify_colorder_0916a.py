# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('plan')")
c = c.replace("const [batchModal,setBatchModal]=useState(null);", "const [batchModal,setBatchModal]=useState({mode:'inst'});")
c = c.replace("const [charSel,setCharSel]=useState('');", "const [charSel,setCharSel]=useState('CHAR-2026-001');")
c = c.replace("const [methodRows,setMethodRows]=useState([]);", "const [methodRows,setMethodRows]=useState([{method:'GRR',std:'STD-MSA-001',ops:3,trials:3,parts:10,saved:true}]);")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
body = re.sub(r'<script[^>]*>.*?</script>', '', out, flags=re.S)
i = body.find('data-row-key="GRR"')
j = body.find('</tr>', i)
row = body[i:j]
# 行内第一列应为操作列（保存/删除按钮），且按钮在 Tag 之前
ops = row.find('ant-btn-link')
tag = row.find('ant-tag')
print('操作列在方法列之前:', 0 <= ops < tag)
print('GRR 行首列是操作按钮:', row.find('ant-btn-link') > 0)
th = body[body.find('<thead'): body.find('</thead>')]
titles = re.findall(r'<th[^>]*>(.*?)</th>', th, flags=re.S)
titles = [re.sub(r'<[^>]+>', '', x) for x in titles]
print('表头顺序:', titles)
