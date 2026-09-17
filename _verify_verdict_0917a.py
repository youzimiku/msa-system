# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('samplelib')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=9000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=120)
    out = r.stdout or ''
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
body = re.sub(r'<script[^>]*>.*?</script>', '', out, flags=re.S)

# 表头顺序：全局收集 th 文本，定位 被测参数/判定状态/标准值/真值
titles = re.findall(r'<th[^>]*>(.*?)</th>', body, flags=re.S)
titles = [re.sub(r'<[^>]+>', '', x).strip() for x in titles]
titles = [x for x in titles if x]
print('表头:', titles)
assert '判定状态' in titles, '判定状态列缺失'
pos_char = titles.index('被测参数'); pos_v = titles.index('判定状态'); pos_n = titles.index('标准值')
print('判定状态在被测参数后:', pos_v == pos_char + 1)
print('标准值紧跟判定状态:', pos_n == pos_v + 1)

# SPL-004 行：标准值/真值应显示空（无 待维护 文字），判定状态=不合格
i4 = body.find('SPL-004')
row4 = body[i4: body.find('</tr>', i4)]
print('SPL-004 行无 待维护:', '待维护' not in row4)
print('SPL-004 判定状态不合格:', '不合格' in row4)

# SPL-005 行：标准值/真值应显示空（无 合格 文字作为值），但判定状态列有 合格
i5 = body.find('SPL-005')
row5 = body[i5: body.find('</tr>', i5)]
print('SPL-005 行仍有 合格(判定状态):', '合格' in row5)
print('SPL-005 无 placeholder 待维护:', '待维护' not in row5)
print('OK')
