# AI Replication Ladder

Katalog **400 paper landmark AI** (100 per bidang) buat direplikasi jadi portfolio, disusun dari **paling gampang ke paling susah**. Tiap link nunjuk **langsung ke papernya** (arXiv/ACL/proceedings/author PDF), bukan halaman pencarian.

- **Live**: https://ai-ladder-lab.vercel.app
- **4 bidang × 100**: Data Science / ML Klasik · LLM · Computer Vision · Reinforcement Learning
- **4 tier per card** (urutan easy→hard): Intro → Core → Advanced → Frontier
- ★ = flagship paling ikonik per bidang

## Struktur

```
ai-ladder-lab/
├── build.py          # generator — baca band JSON, dedupe+trim-100, emit ladder/index.html
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
