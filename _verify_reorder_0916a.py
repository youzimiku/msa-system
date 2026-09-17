# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page, mode='inst'):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    c = c.replace("const [batchModal,setBatchModal]=useState(null);",
                  "const [batchModal,setBatchModal]=useState({mode:'" + mode + "'});")
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
o1 = b.index('>器具选择<')
o2 = b.index('>计划填写信息<')
o3 = b.index('>分析方法<')
print('=== 器具弹窗 DOM 顺序 ===')
print('器具选择(%d) < 计划填写信息(%d) < 分析方法(%d):' % (o1, o2, o3), o1 < o2 < o3)
print('搜索框存在:', '搜索器具组名称' in b)
print('被测参数字段存在:', '被测参数' in b)

b2 = strip_scripts(render('plan', mode='person'))
p1 = b2.index('>器具选择<')
p2 = b2.index('>计划填写信息<')
p3 = b2.index('>分析方法<')
print('=== 人员弹窗 DOM 顺序 ===')
print('器具选择(%d) < 计划填写信息(%d) < 分析方法(%d):' % (p1, p2, p3), p1 < p2 < p3)
print('人员表格渲染:', '人员编号' in b2)
print('RESTORED')
