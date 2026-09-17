# -*- coding: utf-8 -*-
"""生成可在线部署的单文件版本：把 lib/ 依赖内联进 index.html"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
html = open(os.path.join(base, 'index.html'), encoding='utf-8').read()

# 库文件清单（按原 script 顺序）
libs = ['react.production.min.js','react-dom.production.min.js','dayjs.min.js','antd.min.js','xlsx.full.min.js','babel.min.js']

def inline(src, path):
    content = open(path, encoding='utf-8').read()
    # 检查是否包含 </script（大小写不敏感），如有则转义
    if re.search(r'</script', content, re.I):
        content = re.sub(r'</script', r'<\\/script', content, flags=re.I)
    return src.replace('<script src="lib/%s"></script>' % path.split(os.sep)[-1],
                       '<script>/* inline:%s */\n' % path.split(os.sep)[-1] + content + '\n</script>', 1)

for lib in libs:
    p = os.path.join(base, 'lib', lib)
    if not os.path.exists(p):
        print('MISSING', p); sys.exit(1)
    html = inline(html, p)

# 确认没有残留的 src="lib/
rem = re.findall(r'src="lib/[^"]+"', html)
print('残留相对引用:', rem if rem else '无')

out = os.path.join(base, 'index_online.html')
open(out, 'w', encoding='utf-8').write(html)
print('生成:', out, '大小(字节):', os.path.getsize(out))
