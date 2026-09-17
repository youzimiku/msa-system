# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read()
new = open(NEW, encoding='utf-8').read()

def cssblock(src):
    m = re.search(r'<style>(.*?)</style>', src, re.S)
    return m.group(1) if m else ''
oc = cssblock(old); nc = cssblock(new)
print('旧CSS长度', len(oc), '新CSS长度', len(nc))
# 提取 CSS 规则名
def rules(css):
    return re.findall(r'([.#][a-zA-Z0-9_\- ]+)\s*\{', css)
or_=rules(oc); nr_=rules(nc)
add=[x for x in nr_ if x not in or_]
rem=[x for x in or_ if x not in nr_]
print('新增CSS规则:', sorted(set(add)))
print('删除CSS规则:', sorted(set(rem)))
# 关键样式：字体字号颜色
print()
print('旧 font-size 定义:', sorted(set(re.findall(r'font-size:\s*([0-9.]+px)', oc))))
print('新 font-size 定义:', sorted(set(re.findall(r'font-size:\s*([0-9.]+px)', nc))))
print('旧颜色:', sorted(set(re.findall(r'color:\s*(#[0-9a-fA-F]{3,6})', oc))))
print('新颜色:', sorted(set(re.findall(r'color:\s*(#[0-9a-fA-F]{3,6})', nc))))
