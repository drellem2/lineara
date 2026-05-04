# Per-surface aggregation by median pmcd — all pools

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | toponym | `ssos` | 50 | +240.0000 | +210.4000 | 133.1009 | 0.900 | +520.0000 | HT 110a | +0.5500 |
| 2 | toponym | `knossos` | 13 | +184.0000 | +201.2308 | 138.2385 | 0.923 | +536.0000 | KN Zc 6 | +0.7000 |
| 3 | toponym | `assos` | 50 | +180.0000 | +165.9200 | 116.1936 | 0.940 | +480.0000 | KN Zc 6 | +0.7660 |
| 4 | aquitanian | `alaba` | 50 | +172.0000 | +166.2400 | 104.5926 | 0.940 | +448.0000 | ARKH 2 | +0.4450 |
| 5 | etruscan | `nene` | 50 | +172.0000 | +149.2800 | 86.3498 | 0.920 | +288.0000 | HT 117a | +0.5000 |
| 6 | etruscan | `papa` | 50 | +172.0000 | +149.2800 | 86.3498 | 0.920 | +288.0000 | HT 117a | +0.5000 |
| 7 | aquitanian | `atta` | 50 | +160.0000 | +152.4800 | 97.4479 | 0.920 | +328.0000 | HT 108 | +0.4000 |
| 8 | toponym | `lasaia` | 24 | +124.0000 | +101.3333 | 96.4895 | 0.750 | +264.0000 | KN Zc 6 | +0.7188 |
| 9 | aquitanian | `ama` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.4000 |
| 10 | aquitanian | `ere` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 11 | aquitanian | `etxe` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.4000 |
| 12 | aquitanian | `iri` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 13 | aquitanian | `non` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 14 | etruscan | `ana` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 15 | etruscan | `apa` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 16 | toponym | `ala` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 17 | toponym | `sos` | 50 | +84.0000 | +84.3200 | 83.6635 | 0.860 | +312.0000 | ARKH 2 | +0.5500 |
| 18 | toponym | `aptara` | 24 | +80.0000 | +104.3333 | 115.7579 | 0.792 | +368.0000 | KN Zc 6 | +0.7188 |
| 19 | etruscan | `matam` | 50 | +76.0000 | +82.2400 | 100.1636 | 0.740 | +288.0000 | GO Wc 1a | +0.5660 |
| 20 | aquitanian | `hanna` | 50 | +72.0000 | +82.2400 | 94.6849 | 0.800 | +400.0000 | KN Zc 6 | +0.4450 |
| 21 | toponym | `tarra` | 50 | +72.0000 | +82.4000 | 95.4149 | 0.800 | +400.0000 | KN Zc 6 | +0.7660 |
| 22 | toponym | `iassos` | 24 | +60.0000 | +95.3333 | 126.1727 | 0.625 | +424.0000 | KN Zc 6 | +0.7188 |
| 23 | etruscan | `papals` | 24 | +52.0000 | +49.0000 | 98.3955 | 0.667 | +240.0000 | KN Zc 6 | +0.5625 |
| 24 | aquitanian | `arrain` | 24 | +48.0000 | +39.3333 | 113.6760 | 0.708 | +264.0000 | KN Zf 13 | +0.3563 |
| 25 | aquitanian | `arreba` | 24 | +40.0000 | +31.0000 | 105.0793 | 0.625 | +312.0000 | KN Zc 6 | +0.4625 |
| 26 | toponym | `ikaria` | 24 | +36.0000 | +30.3333 | 93.3803 | 0.583 | +304.0000 | KN Zc 6 | +0.7188 |
| 27 | aquitanian | `senben` | 24 | +24.0000 | +43.0000 | 91.9656 | 0.667 | +336.0000 | KN Zc 6 | +0.4625 |
| 28 | etruscan | `trutnu` | 24 | +20.0000 | +42.0000 | 108.0802 | 0.542 | +336.0000 | KN Zc 6 | +0.5000 |
| 29 | aquitanian | `umme` | 50 | +16.0000 | +13.2800 | 72.2416 | 0.540 | +168.0000 | ARKH 2 | +0.4000 |
| 30 | toponym | `ttos` | 50 | +12.0000 | +3.2000 | 83.4305 | 0.520 | +208.0000 | ARKH 2 | +0.5500 |
| 31 | aquitanian | `anai` | 50 | +0.0000 | +2.4000 | 75.7300 | 0.440 | +168.0000 | HT 117a | +0.4000 |
| 32 | aquitanian | `bere` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5500 |
| 33 | aquitanian | `bizi` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5500 |
| 34 | aquitanian | `buru` | 50 | +0.0000 | +1.1200 | 85.5515 | 0.460 | +184.0000 | HT 128a | +0.4000 |
| 35 | aquitanian | `hara` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.4000 |
| 36 | aquitanian | `mihi` | 50 | +0.0000 | +1.2800 | 86.9812 | 0.440 | +184.0000 | HT 128a | +0.4000 |
| 37 | aquitanian | `seme` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.4000 |
| 38 | aquitanian | `txiki` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.2500 |
| 39 | etruscan | `catha` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.5000 |
| 40 | etruscan | `mini` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.6500 |
| 41 | etruscan | `tece` | 50 | +0.0000 | +1.2800 | 86.9812 | 0.440 | +184.0000 | HT 128a | +0.6500 |
| 42 | etruscan | `thana` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.5000 |
| 43 | toponym | `ephesos` | 13 | +0.0000 | +8.6154 | 86.3032 | 0.462 | +200.0000 | KN Zc 6 | +0.7000 |
| 44 | aquitanian | `odol` | 50 | -4.0000 | +2.4000 | 77.0371 | 0.440 | +168.0000 | HT 117a | +0.4000 |
| 45 | aquitanian | `aita` | 50 | -8.0000 | -2.2400 | 92.6901 | 0.460 | +248.0000 | HT 110a | +0.4000 |
| 46 | aquitanian | `ibai` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.4000 |
| 47 | aquitanian | `olio` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.5500 |
| 48 | etruscan | `ipei` | 50 | -8.0000 | -0.8000 | 93.8185 | 0.460 | +256.0000 | HT 110a | +0.6500 |
| 49 | aquitanian | `esne` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5500 |
| 50 | toponym | `efe` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5500 |

_(50 of 379 surfaces shown.)_
