# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = """  if(saved && saved.instruments && saved.instruments.length){
    Store.data=saved; applyFieldDefaults(Store.data);
    try{
      const sd = buildSeed();
      ['linear','stability','cgcgk','resolution','characteristics','anMethods','samplingRules'].forEach(k=>{ if(!Store.data[k] || !Store.data[k].length) Store.data[k]=(Store.data[k]||[]).concat(sd[k].slice()); });
    }catch(e){}
  }"""
new = """  if(saved && saved.instruments && saved.instruments.length){
    Store.data=saved;
    try{
      const sd = buildSeed();
      ['linear','stability','cgcgk','resolution','characteristics','anMethods','samplingRules'].forEach(k=>{ if(!Store.data[k] || !Store.data[k].length) Store.data[k]=(Store.data[k]||[]).concat(sd[k].slice()); });
    }catch(e){}
    applyFieldDefaults(Store.data);
  }"""
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
