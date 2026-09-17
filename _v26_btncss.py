# -*- coding: utf-8 -*-
"""操作列文字按钮：覆盖 .ant-btn-link/.ant-btn-text 为透明无边框"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

OLD = """.ant-btn-link{background:#fff;border:1px solid #1677ff;color:#1677ff;border-radius:4px}
.ant-btn-link.ant-btn-sm{padding:0 8px;height:24px;line-height:22px;font-size:14px}
.ant-btn-link.ant-btn-dangerous{background:#fff;border:1px solid #1677ff;color:#1677ff}
.ant-btn-text{background:#fff;border:1px solid #1677ff;color:#1677ff;border-radius:4px}"""
NEW = """.ant-btn-link{background:transparent;border:none;color:#1677ff;border-radius:4px}
.ant-btn-link:not(:disabled):hover{background:rgba(22,119,255,.06);color:#4096ff}
.ant-btn-link:not(:disabled):active{background:rgba(22,119,255,.12);color:#0958d9}
.ant-btn-link.ant-btn-sm{padding:0 8px;height:24px;line-height:22px;font-size:14px}
.ant-btn-link.ant-btn-dangerous{background:transparent;border:none;color:#ff4d4f}
.ant-btn-link.ant-btn-dangerous:not(:disabled):hover{background:rgba(255,77,79,.06);color:#ff7875}
.ant-btn-link.ant-btn-dangerous:not(:disabled):active{background:rgba(255,77,79,.12);color:#d9363e}
.ant-btn-text{background:transparent;border:none;color:#1677ff;border-radius:4px}"""
assert s.count(OLD) == 1, 'CSS 定位失败 %d' % s.count(OLD)
s = s.replace(OLD, NEW, 1)
open(P, 'w', encoding='utf-8').write(s)
print('btn CSS fix OK 长度', len(s))
