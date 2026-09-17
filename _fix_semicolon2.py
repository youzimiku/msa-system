# -*- coding: utf-8 -*-
import io

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
c = io.open(path, encoding='utf-8').read()

def rep(old, new, tag):
    global c
    n = c.count(old)
    assert n == 1, f'{tag}: found {n}'
    c = c.replace(old, new)
    print('OK', tag)

# 1. 修正 CSS 选择器（antd 实际结构为 selection-overflow-item，无 selection-item 层）
rep(""".msa-method-select .ant-select-selection-item{background:transparent!important;border:none!important;padding:0!important;margin-inline-end:0!important;border-radius:0!important;height:auto!important;line-height:22px!important;font-size:13px;color:#333333}
.msa-method-select .ant-select-selection-item + .ant-select-selection-item::before{content:'；';margin-right:2px}""",
""".msa-method-select .ant-select-selection-overflow-item{margin-inline-end:0!important;padding:0!important}
.msa-method-select .ant-select-selection-overflow-item + .ant-select-selection-overflow-item::before{content:'；';margin-right:2px}
.msa-method-select .ant-select-selection-overflow-item.ant-select-selection-overflow-item-suffix{min-width:4px}""",
'修正分号 CSS 选择器')

# 2. 检验方法列 value 统一转大写，与 anMethods code 匹配（显示方法名称）
rep("""value={(r.methods||[]).map(m=>m.method)}""",
    """value={(r.methods||[]).map(m=>String(m.method).toUpperCase())}""",
    'value 转大写匹配')

io.open(path, 'w', encoding='utf-8').write(c)
print('ALL DONE')
