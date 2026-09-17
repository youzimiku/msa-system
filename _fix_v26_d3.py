# -*- coding: utf-8 -*-
"""Step4c：存量数据兜底补种 + 结果列结论显示检查"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# 1) 加载逻辑：saved 分支补种 4 类空数组演示数据
old = """  if(saved && saved.instruments && saved.instruments.length){ Store.data=saved; applyFieldDefaults(Store.data); }
  else { Store.data = buildSeed(); }"""
new = """  if(saved && saved.instruments && saved.instruments.length){
    Store.data=saved; applyFieldDefaults(Store.data);
    try{
      const sd = buildSeed();
      ['linear','stability','cgcgk','resolution'].forEach(k=>{ if(!Store.data[k] || !Store.data[k].length) Store.data[k]=(Store.data[k]||[]).concat(sd[k].slice()); });
    }catch(e){}
  }
  else { Store.data = buildSeed(); }"""
n = s.count(old)
print('加载逻辑 x%d' % n)
assert n == 1
s = s.replace(old, new)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))

# 2) 检查结果列结论显示残留
for m in re.finditer(r'conclusion\|\|', s):
    a = max(0, m.start()-60)
    print('结论列 @%d :: %s' % (m.start(), s[a:m.start()+40].replace('\n',' ')[-110:]))
