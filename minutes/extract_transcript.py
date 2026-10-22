# -*- coding: utf-8 -*-
# 解析腾讯会议转写 JSON -> 时间[说话人]文本 纯文本
import io, json, os

src = r"C:\Users\youzi\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38440120376335362\agents\m_0cwEzAKMzjT\system\tool-results\bash_7C6DAE1D9A55.txt"
out_dir = r"C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\minutes"
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "tencent_20261021_1417_transcript.txt")

data = io.open(src, encoding="utf-8").read()
j = json.loads(data)
paras = j["data"]["minutes"]["paragraphs"]

lines = []
for p in paras:
    sp = (p.get("speaker") or {}).get("user_name", "未知")
    t = p.get("start_time", "")
    texts = []
    for s in p.get("sentences", []):
        for w in s.get("words", []):
            texts.append(w.get("text", ""))
    if not texts:
        continue
    line = "[%s] %s：%s" % (t, sp, "".join(texts))
    lines.append(line)

body = "\n".join(lines)
io.open(out, "w", encoding="utf-8").write(body)
print("paragraphs:", len(paras), "lines:", len(lines), "chars:", len(body))
print("out:", out)
