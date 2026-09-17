# -*- coding: utf-8 -*-
"""压缩手册截图 → base64 内嵌，供手册 HTML 使用"""
import os, io, base64

SRC = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\manual-img'
OUT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\manual-img\b64.json'

try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

data = {}
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.png'):
        continue
    p = os.path.join(SRC, f)
    if HAS_PIL:
        im = Image.open(p).convert('RGB')
        w, h = im.size
        if w > 1500:
            im = im.resize((1500, int(h * 1500 / w)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=82, optimize=True)
        b = buf.getvalue()
    else:
        b = open(p, 'rb').read()
    key = f.replace('.png', '')
    data[key] = 'data:image/jpeg;base64,' + base64.b64encode(b).decode()
    print(key, len(b) // 1024, 'KB')

import json
with open(OUT, 'w', encoding='utf-8') as fp:
    json.dump(data, fp, ensure_ascii=False)
print('b64 saved', OUT, 'PIL:', HAS_PIL)
