#!/usr/bin/env python3
"""Generate ladder/index.html for ai-ladder-lab: 400 papers (100 per field),
ordered easy->hard across 4 tiers, every link direct to the paper.
Reads band JSON files from PAPERS_DIR. Run: python3 build.py"""
import json, html, pathlib, re, glob

PAPERS_DIR = pathlib.Path(__file__).parent / "data"

# field key -> (tag, css-color-var, display name, one-line desc)
FIELDS = [
    ("ds",  "DS",  "var(--dDS)",  "Data Science / ML Klasik",
     "Statistik → ensemble → boosting → causal → deep-tabular. 100 paper, gampang ke susah."),
    ("llm", "LLM", "var(--dLLM)", "Large Language Models",
     "word2vec → Transformer → BERT/GPT → scaling → RLHF → MoE/Mamba. 100 paper."),
    ("cv",  "CV",  "var(--dCV)",  "Computer Vision",
     "SIFT/CNN → ResNet/deteksi → GAN/ViT → diffusion/SAM/3DGS. 100 paper."),
    ("rl",  "RL",  "var(--dRL)",  "Reinforcement Learning",
     "MDP/Q-learning → DQN → PPO/SAC → AlphaZero/MuZero/offline. 100 paper."),
]
TARGET = 100
TIER_ORDER = {"Intro": 0, "Core": 1, "Advanced": 2, "Frontier": 3}
BAD = re.compile(r'scholar\.google|semanticscholar|duckduckgo|/search\?|google\.[a-z.]+/search')

def norm_title(t):
    return re.sub(r'[^a-z0-9]', '', html.unescape(t).lower())[:45]

def load_field(fk):
    """Concatenate the field's bands in tier order, dedupe by title, drop bad URLs."""
    rows, seen = [], set()
    files = sorted(glob.glob(str(PAPERS_DIR / f"{fk}_*.json")),
                   key=lambda p: int(re.search(r'_(\d+)\.json', p).group(1)))
    for f in files:
        for p in json.load(open(f)):
            if BAD.search(p["url"]):          # never a search page
                continue
            k = norm_title(p["title"])
            if k in seen:
                continue
            seen.add(k)
            rows.append(p)
    # stable-sort by tier so Intro->Core->Advanced->Frontier, preserving in-band order
    rows.sort(key=lambda p: TIER_ORDER.get(p["tier"], 9))
    return rows

# flagship picks (by normalized title) per field — the icons everyone knows
STAR_TITLES = {
    "ds":  {"randomforests","adamamethodforstochasticoptimization","xgboostascalabletreeboostingsystem",
            "aunifiedapproachtointerpretingmodelpredictions","regressionshrinkageandselectionviathelasso"},
    "llm": {"attentionisallyouneed","bertpretrainingofdeepbidirectionaltransformersforl",
            "languagemodelsarefewshotlearners","loralowrankadaptationoflargelanguagemodels",
            "traininglanguagemodelstofollowinstructionswithhuma"},
    "cv":  {"deepresiduallearningforimagerecognition","imagenetclassificationwithdeepconvolutionalneuraln",
            "generativeadversarialnetworks","animageisworth16x16wordstransformersforimagerec",
            "denoisingdiffusionprobabilisticmodels","segmentanything"},
    "rl":  {"qlearning","humanlevelcontrolthroughdeepreinforcementlearning",
            "proximalpolicyoptimizationalgorithms","softactorcriticoffpolicymaximumentropydeepreinfor",
            "masteringthegameofgowithdeepneuralnetworksandtree"},
}

def esc_js(s):
    return json.dumps(html.unescape(s), ensure_ascii=False)

P_rows, U_lines = [], []
counts = {}
for di, (fk, tag, color, name, desc) in enumerate(FIELDS):
    rows = load_field(fk)[:TARGET]
    counts[fk] = len(rows)
    stars = STAR_TITLES.get(fk, set())
    for i, p in enumerate(rows, start=1):
        pid = f"{fk}{i}"
        star = 1 if norm_title(p["title"]) in stars else 0
        access = "paywall" if p["access"] in ("paid", "paywall") else "free"
        P_rows.append(f'[{esc_js(pid)},{di},{esc_js(p["author"])},{esc_js(p["title"])},'
                      f'{esc_js(p["why"])},{esc_js(p["tier"])},{star}]')
        U_lines.append(f'{esc_js(pid)}:[{esc_js(p["url"])},{esc_js(access)}]')

TOTAL = len(P_rows)
FIELDS_JS = ",\n  ".join(
    f'{i}:{{tag:{esc_js(tag)},color:{json.dumps(color)},name:{esc_js(name)},d:{esc_js(desc)}}}'
    for i, (fk, tag, color, name, desc) in enumerate(FIELDS))

HTML = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Replication Ladder — {TOTAL} papers (DS · LLM · CV · RL)</title>
<link rel="icon" href="data:,">
<style>
  :root{{
    --bg:#0b0e14; --bg2:#11151f; --card:#151a26; --line:#232a3a;
    --tx:#e6e9f0; --mut:#8b93a7; --acc:#4fd1c5; --acc2:#f6c177;
    --dDS:#f6c177; --dLLM:#4fd1c5; --dCV:#63b3ff; --dRL:#a78bfa;
  }}
  *{{box-sizing:border-box}} html,body{{margin:0;padding:0}}
  body{{background:var(--bg);color:var(--tx);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
  a{{color:inherit}}
  .wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
  header{{padding:52px 0 28px;border-bottom:1px solid var(--line);background:radial-gradient(1200px 400px at 50% -120px,rgba(79,209,197,.10),transparent)}}
  h1{{margin:0 0 8px;font-size:30px;letter-spacing:-.4px}}
  h1 .g{{background:linear-gradient(90deg,var(--acc),var(--dCV),var(--dRL));-webkit-background-clip:text;background-clip:text;color:transparent}}
  .sub{{color:var(--mut);max-width:720px;font-size:15px}}
  .meta{{display:flex;gap:18px;flex-wrap:wrap;margin-top:16px;color:var(--mut);font-size:13px}}
  .meta b{{color:var(--tx)}}
  .controls{{position:sticky;top:0;z-index:20;background:rgba(11,14,20,.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:12px 0}}
  .controls .wrap{{display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
  #q{{flex:1;min-width:200px;background:var(--bg2);border:1px solid var(--line);color:var(--tx);padding:9px 13px;border-radius:10px;font-size:14px;outline:none}}
  #q:focus{{border-color:var(--acc)}}
  .chips{{display:flex;gap:6px;flex-wrap:wrap}}
  .chip{{cursor:pointer;user-select:none;border:1px solid var(--line);background:var(--bg2);color:var(--mut);padding:6px 11px;border-radius:999px;font-size:12.5px;font-weight:600;transition:.12s}}
  .chip:hover{{color:var(--tx)}}
  .chip.on{{background:var(--tx);color:#0b0e14;border-color:var(--tx)}}
  .count{{color:var(--mut);font-size:12.5px;margin-left:auto}}
  .level{{margin:40px 0 0}}
  .lvhead{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-bottom:10px;border-bottom:1px solid var(--line)}}
  .lvtag{{font-size:12px;font-weight:700;padding:3px 9px;border-radius:6px;color:#0b0e14}}
  .lvhead h2{{margin:0;font-size:19px;letter-spacing:-.2px}}
  .lvhead .d{{color:var(--mut);font-size:13.5px}}
  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}}
  @media(max-width:720px){{.grid{{grid-template-columns:1fr}}}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 15px;display:flex;flex-direction:column;gap:6px;transition:.12s}}
  .card:hover{{border-color:#33405a;transform:translateY(-1px)}}
  .card .top{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
  .num{{font-variant-numeric:tabular-nums;color:var(--mut);font-size:12px;font-weight:700;min-width:38px}}
  .nm{{font-weight:700;font-size:14.5px}}
  .star{{color:var(--acc2)}}
  .badge{{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:5px;letter-spacing:.3px}}
  .b-Intro{{background:rgba(139,147,167,.20);color:#c3c9d6}}
  .b-Core{{background:rgba(79,209,197,.16);color:#6fe3d7}}
  .b-Advanced{{background:rgba(99,179,255,.16);color:#8ec6ff}}
  .b-Frontier{{background:rgba(244,114,182,.16);color:#f9a8d4}}
  .title{{color:var(--mut);font-style:italic;font-size:12.5px}}
  .desc{{font-size:13.5px;color:#cfd4e0}}
  .foot{{margin-top:auto;display:flex;align-items:center;gap:8px;padding-top:5px;flex-wrap:wrap}}
  .card a.read{{font-size:12.5px;font-weight:700;color:var(--acc);text-decoration:none}}
  .card a.read:hover{{text-decoration:underline}}
  .acc{{font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;letter-spacing:.2px}}
  .a-free{{background:rgba(79,209,197,.16);color:#6fe3d7}}
  .a-paywall{{background:rgba(246,193,119,.16);color:#f6c177}}
  .empty{{color:var(--mut);text-align:center;padding:60px 0;display:none}}
  footer{{margin:56px 0 40px;color:var(--mut);font-size:12.5px;border-top:1px solid var(--line);padding-top:20px}}
  footer code{{background:var(--bg2);padding:1px 6px;border-radius:5px;color:#cfd4e0}}
  .menu-btn{{position:fixed;top:11px;left:14px;z-index:60;background:var(--card);border:1px solid var(--line);color:var(--tx);border-radius:9px;padding:7px 11px;font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:7px}}
  .menu-btn:hover{{border-color:#33405a}}
  .scrim{{position:fixed;inset:0;background:rgba(0,0,0,.5);opacity:0;pointer-events:none;transition:.18s;z-index:70}}
  .scrim.open{{opacity:1;pointer-events:auto}}
  .drawer{{position:fixed;top:0;left:0;bottom:0;width:270px;max-width:84vw;background:var(--bg2);border-right:1px solid var(--line);z-index:80;transform:translateX(-100%);transition:transform .2s ease;overflow-y:auto;padding:16px 0}}
  .drawer.open{{transform:none}}
  .drawer .dh{{display:flex;align-items:center;justify-content:space-between;padding:0 16px 10px;border-bottom:1px solid var(--line);margin-bottom:8px}}
  .drawer .dh b{{font-size:14px}}
  .drawer .dh .x{{cursor:pointer;color:var(--mut);font-size:20px;line-height:1;background:none;border:none}}
  .drawer .di{{padding:9px 16px;cursor:pointer;border-left:3px solid transparent}}
  .drawer .di:hover{{background:rgba(255,255,255,.04)}}
  .drawer .di.on{{background:rgba(255,255,255,.06)}}
  .drawer .di .row1{{display:flex;align-items:center;gap:9px}}
  .drawer .dot{{width:9px;height:9px;border-radius:50%;flex:0 0 9px}}
  .drawer .di .lv{{font-size:11px;font-weight:800;letter-spacing:.4px;color:var(--mut);min-width:26px}}
  .drawer .di .nm{{font-size:13.5px;font-weight:600}}
  .tierkey{{display:flex;gap:6px;flex-wrap:wrap;margin:14px 16px 4px;padding-top:12px;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<button class="menu-btn" id="menuBtn" aria-label="Menu">☰ Bidang</button>
<div class="scrim" id="scrim"></div>
<nav class="drawer" id="drawer" aria-label="Quick access bidang">
  <div class="dh"><b>Quick access</b><button class="x" id="drawerX" aria-label="Tutup">×</button></div>
  <div id="drawerList"></div>
</nav>
<header>
  <div class="wrap">
    <h1><span class="g">AI Replication</span> Ladder</h1>
    <div class="sub">{TOTAL} paper landmark di <b>Data Science, LLM, Computer Vision &amp; Reinforcement Learning</b> — <b>100 paper per bidang</b>, disusun dari paling gampang ke paling susah lewat 4 tier. Replikasi tiap paper pakai kode sendiri buat portfolio. Klik <b>Baca →</b> langsung ke papernya.</div>
    <div class="meta">
      <span><b>{TOTAL}</b> papers</span><span><b>4</b> bidang × 100</span>
      <span>Tier: <span class="badge b-Intro">Intro</span> <span class="badge b-Core">Core</span> <span class="badge b-Advanced">Advanced</span> <span class="badge b-Frontier">Frontier</span></span>
    </div>
  </div>
</header>

<div class="controls">
  <div class="wrap">
    <input id="q" placeholder="Cari judul / penulis / metode…" autocomplete="off">
    <div class="chips" id="chips">
      <span class="chip on" data-l="all">Semua</span>
      <span class="chip" data-l="0">DS</span>
      <span class="chip" data-l="1">LLM</span>
      <span class="chip" data-l="2">CV</span>
      <span class="chip" data-l="3">RL</span>
    </div>
    <span class="count" id="count"></span>
  </div>
</div>

<main class="wrap" id="main"></main>
<div class="empty" id="empty">Nggak ada paper yang cocok.</div>

<footer class="wrap">
  <p>Semua link <b>Baca →</b> nunjuk <b>langsung ke papernya</b> (arXiv/ACL/proceedings/author PDF), bukan halaman pencarian. <span class="acc a-free">PDF gratis</span> = full-text kebuka · <span class="acc a-paywall">paywall</span> = link resmi (mungkin bayar; cari mirror). ★ = flagship paling ikonik per bidang. Urutan tiap bidang: <b>Intro → Core → Advanced → Frontier</b>.</p>
  <p>Repo: <code>~/coding-projects/ai-ladder-lab</code> · regen: <code>python3 build.py</code></p>
</footer>

<script>
const DOMAINS = {{
  {FIELDS_JS}
}};
const NDOM = {len(FIELDS)};
const P = [
{",".join(chr(10) + r for r in P_rows)}
];
const main=document.getElementById('main'), empty=document.getElementById('empty'),
      countEl=document.getElementById('count'), qEl=document.getElementById('q');
let curDom='all', curQ='';
const U = {{
{",".join(chr(10) + u for u in U_lines)}
}};
const ACCLBL={{free:"PDF gratis",paywall:"paywall"}};
function render(){{
  main.innerHTML='';
  let shown=0;
  for(let d=0; d<NDOM; d++){{
    if(curDom!=='all' && String(d)!==curDom) continue;
    const rows=P.filter(p=>p[1]===d).filter(p=>{{
      if(!curQ) return true;
      const h=(p[2]+" "+p[3]+" "+p[4]+" "+p[5]).toLowerCase();
      return h.includes(curQ);
    }});
    if(!rows.length) continue;
    shown+=rows.length;
    const L=DOMAINS[d];
    const sec=document.createElement('section'); sec.className='level';
    sec.innerHTML=`<div class="lvhead">
        <span class="lvtag" style="background:${{L.color}}">${{L.tag}}</span>
        <h2>${{L.name}}</h2><span class="d">${{L.d}}</span>
      </div><div class="grid"></div>`;
    const grid=sec.querySelector('.grid');
    rows.forEach((p,idx)=>{{
      const [num,,name,title,desc,tier,star]=p;
      const lnk=U[num]||["#","free"];
      const c=document.createElement('div'); c.className='card';
      c.innerHTML=`<div class="top">
          <span class="num">${{L.tag}}${{idx+1}}</span>
          <span class="nm">${{name}}${{star?' <span class="star">★</span>':''}}</span>
          <span class="badge b-${{tier}}">${{tier}}</span>
        </div>
        <div class="title">${{title}}</div>
        <div class="desc">${{desc}}</div>
        <div class="foot">
          <a class="read" href="${{lnk[0]}}" target="_blank" rel="noopener">Baca →</a>
          <span class="acc a-${{lnk[1]}}">${{ACCLBL[lnk[1]]}}</span>
        </div>`;
      grid.appendChild(c);
    }});
    main.appendChild(sec);
  }}
  empty.style.display = shown?'none':'block';
  countEl.textContent = shown+" / "+P.length+" papers";
}}
document.getElementById('chips').addEventListener('click',e=>{{
  const c=e.target.closest('.chip'); if(!c) return;
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
  c.classList.add('on'); curDom=c.dataset.l; render();
}});
qEl.addEventListener('input',()=>{{curQ=qEl.value.trim().toLowerCase(); render();}});

const drawer=document.getElementById('drawer'), scrim=document.getElementById('scrim'), dList=document.getElementById('drawerList');
function openDrawer(v){{drawer.classList.toggle('open',v);scrim.classList.toggle('open',v);}}
document.getElementById('menuBtn').onclick=()=>openDrawer(true);
document.getElementById('drawerX').onclick=()=>openDrawer(false);
scrim.onclick=()=>openDrawer(false);
document.addEventListener('keydown',e=>{{if(e.key==='Escape')openDrawer(false);}});
let dHTML=`<div class="di" data-l="all"><div class="row1"><span class="lv">·</span><span class="nm">Semua bidang</span></div></div>`;
for(let d=0;d<NDOM;d++){{const L=DOMAINS[d];
  dHTML+=`<div class="di" data-l="${{d}}">
    <div class="row1"><span class="dot" style="background:${{L.color}}"></span><span class="lv">${{L.tag}}</span><span class="nm">${{L.name}}</span></div>
  </div>`;}}
dHTML+=`<div class="tierkey"><span class="badge b-Intro">Intro</span><span class="badge b-Core">Core</span><span class="badge b-Advanced">Advanced</span><span class="badge b-Frontier">Frontier</span></div>`;
dList.innerHTML=dHTML;
function syncSide(){{dList.querySelectorAll('.di').forEach(x=>x.classList.toggle('on',x.dataset.l===curDom));}}
dList.addEventListener('click',e=>{{
  const x=e.target.closest('.di'); if(!x) return;
  document.querySelector('.chip[data-l="'+x.dataset.l+'"]').click();
  syncSide(); openDrawer(false); window.scrollTo({{top:0,behavior:'smooth'}});
}});
document.getElementById('chips').addEventListener('click',syncSide);
syncSide();
render();
</script>
</body>
</html>
'''

out = pathlib.Path(__file__).parent / "ladder" / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out} — {TOTAL} papers")
for fk, n in counts.items():
    flag = "OK" if n == TARGET else f"!! only {n}"
    print(f"  {fk}: {n} {flag}")
