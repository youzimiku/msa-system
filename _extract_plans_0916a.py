# -*- coding: utf-8 -*-
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'

def html2text(path, out):
    t = io.open(path, encoding='utf-8').read()
    # 去掉 script/style
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    # 表格换行标记
    t = t.replace('</tr>', '\n').replace('</div>', '\n').replace('</p>', '\n').replace('</li>', '\n').replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    t = re.sub(r'<t[dh][^>]*>', ' | ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'&nbsp;', ' ', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    lines = [l.strip() for l in t.split('\n')]
    lines = [l for l in lines if l]
    io.open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(out, len(lines), '行')

html2text(os.path.join(BASE, 'MSA系统页面调整方案及比对报告_20260916.html'), r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_plan_tencent.txt')
html2text(os.path.join(BASE, 'MSA系统_9月14日业务会议调整方案及比对报告_20260916.html'), r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_plan_feishu.txt')
