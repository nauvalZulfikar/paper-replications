# Paper Replications — katalog + ruang kerja

Satu repo buat dua hal: **milih** paper mana yang dikerjain (katalog), dan **ngerjain**-nya (notebook).

- 📚 **Katalog live**: [ai-ladder-lab.vercel.app](https://ai-ladder-lab.vercel.app) — 519 paper landmark, 5 bidang, urut gampang → susah.
- 🛠 **Ruang kerja**: folder `ds-01-.../` dst — notebook Colab tempat ngoding.

Fokus sekarang: **Data Science**, urut dari yang paling gampang.

## Cara mainnya (tiap paper)

1. **Brief + Rubric** ada di dalam notebook (target hasil ditentuin di depan).
2. Buka notebook di **Google Colab** (badge di bawah), baca papernya, **lu yang ngerjain**.
3. **Save a copy in GitHub** balik ke repo ini (`File → Save a copy in GitHub`).
4. Bilang *"<id> siap dicek"* — notebook dijalanin, dinilai vs rubric, lalu tanya-tanya pemahaman.
5. Lulus → status jadi ✅ di katalog + jadi isi portfolio.

**Aturan:** solusi jadi nggak dikasih. Konsep, rumus, dan langkah-langkah dijelasin sedetail mungkin — tapi baris kodenya tetap lu yang rakit.

## Progress — Data Science

| # | Paper | Tier | Status | Notebook |
|---|---|---|---|---|
| DS-01 | Galton (1886) — Regression to the Mean | Intro | 🟡 lagi dikerjain | [Open in Colab](https://colab.research.google.com/github/nauvalZulfikar/paper-replications/blob/main/ds-01-galton-regression/notebook.ipynb) |

Status: ⬜ belum · 🟡 dikerjain · ✅ lulus

## Struktur

```
paper-replications/
├── _template/notebook.ipynb          # template buat paper baru
├── ds-01-galton-regression/
│   └── notebook.ipynb                # Brief + Rubric + sel TODO  ← kerjaan lu
└── catalog/                          # situs katalog (dulu repo ai-ladder-lab)
    ├── build.py                      # generator: data/*.json → ladder/index.html
    ├── extract_quant.py
    ├── data/                         # <bidang>_<band>.json + status.json
    └── ladder/index.html             # situs statis (vanilla JS, 0 dependency)
```

Katalog & ruang kerja nyambung lewat **`catalog/data/status.json`** — keyed by judul paper
(`{status: reading|coding|done, url}`). Update status di situ → rebuild → kartu di situs
berubah jadi ✅ dan hitungan `X/100 ✓` naik.

## Update katalog / redeploy

```bash
# 1. edit paper di catalog/data/*.json  (atau status.json buat progress)
python3 catalog/build.py               # regen catalog/ladder/index.html
cd catalog/ladder && vercel --prod --yes   # deploy ke ai-ladder-lab.vercel.app
```

`build.py` otomatis dedupe by-title, trim 100/bidang, dan buang URL search-page.

## Catatan

- Katalog: 400 paper AI dikurasi 17 agen paralel (4 bidang × 4 band + 1 RL top-up), tiap URL
  diverifikasi nunjuk langsung ke paper — 0 search-page. Plus 119 paper Quant Finance.
- Repo `ai-ladder-lab` yang lama udah digabung ke sini (`catalog/`) lengkap dengan historinya.
