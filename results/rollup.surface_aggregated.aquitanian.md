# Per-surface aggregation by median pmcd — pool: aquitanian

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | aquitanian | `alaba` | 50 | +172.0000 | +166.2400 | 104.5926 | 0.940 | +448.0000 | ARKH 2 | +0.4450 |
| 2 | aquitanian | `atta` | 50 | +160.0000 | +152.4800 | 97.4479 | 0.920 | +328.0000 | HT 108 | +0.4000 |
| 3 | aquitanian | `ama` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.4000 |
| 4 | aquitanian | `ere` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 5 | aquitanian | `etxe` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.4000 |
| 6 | aquitanian | `iri` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 7 | aquitanian | `non` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 8 | aquitanian | `hanna` | 50 | +72.0000 | +82.2400 | 94.6849 | 0.800 | +400.0000 | KN Zc 6 | +0.4450 |
| 9 | aquitanian | `arrain` | 24 | +48.0000 | +39.3333 | 113.6760 | 0.708 | +264.0000 | KN Zf 13 | +0.3563 |
| 10 | aquitanian | `arreba` | 24 | +40.0000 | +31.0000 | 105.0793 | 0.625 | +312.0000 | KN Zc 6 | +0.4625 |
| 11 | aquitanian | `senben` | 24 | +24.0000 | +43.0000 | 91.9656 | 0.667 | +336.0000 | KN Zc 6 | +0.4625 |
| 12 | aquitanian | `umme` | 50 | +16.0000 | +13.2800 | 72.2416 | 0.540 | +168.0000 | ARKH 2 | +0.4000 |
| 13 | aquitanian | `anai` | 50 | +0.0000 | +2.4000 | 75.7300 | 0.440 | +168.0000 | HT 117a | +0.4000 |
| 14 | aquitanian | `bere` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5500 |
| 15 | aquitanian | `bizi` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5500 |
| 16 | aquitanian | `buru` | 50 | +0.0000 | +1.1200 | 85.5515 | 0.460 | +184.0000 | HT 128a | +0.4000 |
| 17 | aquitanian | `hara` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.4000 |
| 18 | aquitanian | `mihi` | 50 | +0.0000 | +1.2800 | 86.9812 | 0.440 | +184.0000 | HT 128a | +0.4000 |
| 19 | aquitanian | `seme` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.4000 |
| 20 | aquitanian | `txiki` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.2500 |
| 21 | aquitanian | `odol` | 50 | -4.0000 | +2.4000 | 77.0371 | 0.440 | +168.0000 | HT 117a | +0.4000 |
| 22 | aquitanian | `aita` | 50 | -8.0000 | -2.2400 | 92.6901 | 0.460 | +248.0000 | HT 110a | +0.4000 |
| 23 | aquitanian | `ibai` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.4000 |
| 24 | aquitanian | `olio` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.5500 |
| 25 | aquitanian | `esne` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5500 |
| 26 | aquitanian | `ur` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.4000 |
| 27 | aquitanian | `bi` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.7000 |
| 28 | aquitanian | `ez` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5500 |
| 29 | aquitanian | `lo` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5500 |
| 30 | aquitanian | `su` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.4000 |
| 31 | aquitanian | `bai` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 32 | aquitanian | `bat` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.7000 |
| 33 | aquitanian | `eta` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 34 | aquitanian | `gatz` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 35 | aquitanian | `gau` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.4000 |
| 36 | aquitanian | `hau` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 37 | aquitanian | `idiar` | 50 | -48.0000 | -52.3200 | 73.6384 | 0.160 | +120.0000 | HT 95a | +0.4000 |
| 38 | aquitanian | `ile` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.4000 |
| 39 | aquitanian | `jan` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 40 | aquitanian | `lan` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 41 | aquitanian | `lau` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.7000 |
| 42 | aquitanian | `aho` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.4000 |
| 43 | aquitanian | `aitz` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.4000 |
| 44 | aquitanian | `ako` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.2500 |
| 45 | aquitanian | `ate` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.4000 |
| 46 | aquitanian | `eki` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.4000 |
| 47 | aquitanian | `hil` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 48 | aquitanian | `hox` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.2500 |
| 49 | aquitanian | `lur` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.4000 |
| 50 | aquitanian | `nor` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |

_(50 of 153 surfaces shown.)_
