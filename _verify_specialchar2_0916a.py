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

b = render('char')
# 渲染出的表头 th 中是否还有 绑定器具组
ths = re.findall(r'<th[^>]*>(.*?)</th>', b, re.S)
th_texts = [re.sub(r'<[^>]+>', '', x).strip() for x in ths]
print('=== 被测参数维护 ===')
print('渲染表头含「特殊特性」:', any('特殊特性' in t for t in th_texts))
print('渲染表头含「绑定器具组」(应无):', any('绑定器具组' in t for t in th_texts))
print('渲染表头含「器具组」按钮列:', any(t.strip()=='器具组' for t in th_texts))
# 特殊特性下拉渲染出 SC-001 轴径 φ50
print('特殊特性选项 SC-001 轴径 φ50:', 'SC-001 轴径 φ50' in b)
# 检验标准列表操作列按钮
print('检验标准操作列「器具组」按钮(link):', '器具组' in b and b.count('<a class="ant-btn-link"')>0)
# 详情抽屉字段
print('详情特殊特性行:', '特殊特性' in b)

b2 = render('plan', open_modal=True)
print('=== MSA计划弹窗 ===')
print('质量特性字段:', '质量特性' in b2)
print('质量特性选项 SC-001 轴径 φ50:', 'SC-001 轴径 φ50' in b2)
print('RESTORED')
