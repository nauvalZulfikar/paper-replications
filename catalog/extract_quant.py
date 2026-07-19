import json, re, pathlib
src = pathlib.Path("/Users/shaka-mac-mini/coding-projects/quant-ladder-lab/ladder/index.html").read_text()

def block(marker_open, close="\n};"):
    s = src.index(marker_open) + len(marker_open)
    e = src.index(close, s)
    return src[s:e]

def strip_comments(b):
    b = re.sub(r'^\s*//.*$', '', b, flags=re.M)      # full-line // comments only
    b = re.sub(r',\s*$', '', b.strip())               # trailing comma
    return b

P = json.loads('[' + strip_comments(block("const P = [", "\n];")) + ']')
U = json.loads('{' + strip_comments(block("const U = {")) + '}')
S = json.loads('{' + strip_comments(block("const S = {")) + '}')
print("P:", len(P), "U:", len(U), "S:", len(S))

# level -> tier (monotonic easy->hard)
LVL2TIER = {0:"Intro", 1:"Core", 2:"Core", 3:"Advanced", 4:"Frontier", 5:"Frontier"}
recs, missing = [], 0
for num, level, name, title, why, tag, star in P:
    if num not in U:
        missing += 1; continue
    url, access = U[num]
    recs.append({
        "author": name, "title": title, "why": why,
        "tier": LVL2TIER[level], "url": url, "access": access,
        "star": int(star), "summary": S.get(num, "")
    })
print("records:", len(recs), "missing-url:", missing)
# access breakdown
from collections import Counter
print("access:", Counter(r["access"] for r in recs))
print("tiers:", Counter(r["tier"] for r in recs))

out = pathlib.Path("/Users/shaka-mac-mini/coding-projects/ai-ladder-lab/data/quant_1.json")
out.write_text(json.dumps(recs, ensure_ascii=False, indent=0))
print("wrote", out)
