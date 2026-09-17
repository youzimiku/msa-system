# -*- coding: utf-8 -*-
import subprocess, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'

orig = io.open(path, encoding='utf-8').read()
pages = {
    'char': {
        'must': ['被测参数维护', '零件号', '零件名称', '数据类型', '被测参数名称', '特性类型'],
        'forbid': ['零件编号'],
    },
    'sampling': {
        'must': ['数据类型', '方法组', '样品数范围'],
        'forbid': ['默认适用'],
    },
    'samplelib': {
        'must': ['样本库管理', '被测参数', '零件号', '零件名称', '单位'],
        'forbid': ['对应被测项目'],
    },
    'plan': {
        'must': ['被测参数', '零件名称', '工厂', 'MSA计划号', '分析人'],
        'forbid': ['检验标准'],
    },
}
try:
    for key, rule in pages.items():
        c = orig.replace("useState('instgroup')", "useState('" + key + "')")
        assert c != orig
        io.open(path, 'w', encoding='utf-8').write(c)
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        miss = [m for m in rule['must'] if m not in out]
        extra = [f for f in rule['forbid'] if f in out]
        print(f"[{key}] dom长度={len(out)} 缺失={miss or '无'} 不应出现={extra or '无'}")
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
