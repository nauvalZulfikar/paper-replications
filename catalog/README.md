# Replication Ladder

Katalog gabungan **519 paper landmark** (Quant Finance + AI) buat direplikasi jadi portfolio, tiap bidang disusun dari **paling gampang ke paling susah**.

- **Live**: https://ai-ladder-lab.vercel.app
- **5 bidang**: **Quant Finance (119)** · Data Science / ML Klasik (100) · LLM (100) · Computer Vision (100) · Reinforcement Learning (100)
- **4 tier per card** (urutan easy→hard): Intro → Core → Advanced → Frontier
- ★ = flagship paling ikonik per bidang; bidang **Quant** punya **Ringkasan** expandable per card
- Link **Baca →** nunjuk ke papernya. AI: 0 search-page. Quant: mayoritas PDF gratis, sebagian paywall, 4 fallback Scholar (badge "cari").

> Gabungan dari 2 situs lama: **ai-ladder-lab** (400 AI) + **quant-ladder-lab** (119 Quant, dulu di ladder-sand-five.vercel.app — deployment itu udah dihapus, digabung ke sini).

## Struktur

```
ai-ladder-lab/
├── build.py          # generator — baca data/*.json, dedupe + cap per-bidang, emit ladder/index.html
├── extract_quant.py  # sekali-pakai: parse P/U/S dari quant-ladder-lab/ladder/index.html → data/quant_1.json
├── data/             # <field>_<band>.json — quant_1 + ds/llm/cv/rl_1..4 (+rl_5)
└── ladder/
    ├── index.html    # katalog statis self-contained (vanilla JS, 0 dependency)
    └── vercel.json    # {} — static hosting
```

Data 400 paper ada di **band JSON** di scratchpad: `<field>_<band>.json` (ds/llm/cv/rl × 1..4, plus rl_5 top-up). `build.py` konstanta `PAPERS_DIR` nunjuk ke situ. Tiap band = 1 tier (1=Intro, 2=Core, 3=Advanced, 4=Frontier).

## Edit / redeploy

1. Ubah/ tambah paper di band JSON (`PAPERS_DIR`), atau flagship di `STAR_TITLES` di `build.py`.
2. `python3 build.py` → regen `ladder/index.html` (auto dedupe by-title + trim 100/bidang + buang URL search-page).
3. `cd ladder && vercel --prod --yes` → deploy ke ai-ladder-lab.vercel.app.

## Catatan kurasi

- 400 paper dikurasi 17 agen paralel (4 bidang × 4 band + 1 RL top-up), tiap URL diverifikasi web-search nunjuk langsung ke paper. 0 search-page.
- RL band 2&3 sempet overlap (DDPG/A3C/GAE/distributional) → dedupe by-title + top-up band (Munchausen/CURL/DrQ/REDQ/PPG/MPO/NGU/Agent57/Go-Explore) buat genepin 100.

## TODO

- Folder replikasi per bidang (mirror pola quant-ladder-lab `tiers/`) — belum dibikin.
- Isi kode replikasi tiap paper.
- Beberapa link `paywall` (IEEE/Springer/JSTOR klasik) — cari mirror kalau perlu.
