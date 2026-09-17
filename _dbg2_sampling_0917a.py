# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('sampling')", 1)
inject = '<script>window.onerror=function(m,s,l,c){var d=document.createElement("div");d.id="JSE";d.textContent="ERR:"+m+" @"+l+":"+c;document.body.appendChild(d);};window.addEventListener("unhandledrejection",function(e){var d=document.createElement("div");d.id="JSE2";d.textContent="REJ:"+String(e.reason);document.body.appendChild(d);});</script>'
tmp = tmp.replace('</head>', inject + '</head>', 1)
tmp_path = os.path.join(tempfile.gettempdir(), 'msa_sampling_check.html')
io.open(tmp_path, 'w', encoding='utf-8').write(tmp)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=10000', '--dump-dom', url],
                   capture_output=True, timeout=120)
dom = r.stdout.decode('utf-8', errors='replace')
for tag in ['JSE', 'JSE2']:
    m = re.search(r'<div id="%s"[^>]*>([^<]*)</div>' % tag, dom)
    print(tag, '->', m.group(1)[:600] if m else 'NONE')
print('root children:', re.search(r'<div id="root">[\s\S]{0,200}', dom).group(0)[:200] if re.search(r'<div id="root">', dom) else 'no root open tag')
