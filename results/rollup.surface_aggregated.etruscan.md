# Per-surface aggregation by median pmcd — pool: etruscan

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | etruscan | `nene` | 50 | +172.0000 | +149.2800 | 86.3498 | 0.920 | +288.0000 | HT 117a | +0.5000 |
| 2 | etruscan | `papa` | 50 | +172.0000 | +149.2800 | 86.3498 | 0.920 | +288.0000 | HT 117a | +0.5000 |
| 3 | etruscan | `ana` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 4 | etruscan | `apa` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 5 | etruscan | `matam` | 50 | +76.0000 | +82.2400 | 100.1636 | 0.740 | +288.0000 | GO Wc 1a | +0.5660 |
| 6 | etruscan | `papals` | 24 | +52.0000 | +49.0000 | 98.3955 | 0.667 | +240.0000 | KN Zc 6 | +0.5625 |
| 7 | etruscan | `trutnu` | 24 | +20.0000 | +42.0000 | 108.0802 | 0.542 | +336.0000 | KN Zc 6 | +0.5000 |
| 8 | etruscan | `catha` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.5000 |
| 9 | etruscan | `mini` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.6500 |
| 10 | etruscan | `tece` | 50 | +0.0000 | +1.2800 | 86.9812 | 0.440 | +184.0000 | HT 128a | +0.6500 |
| 11 | etruscan | `thana` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.5000 |
| 12 | etruscan | `ipei` | 50 | -8.0000 | -0.8000 | 93.8185 | 0.460 | +256.0000 | HT 110a | +0.6500 |
| 13 | etruscan | `ca` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.6500 |
| 14 | etruscan | `mi` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.6500 |
| 15 | etruscan | `sa` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.8000 |
| 16 | etruscan | `an` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.6500 |
| 17 | etruscan | `ar` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.6500 |
| 18 | etruscan | `ci` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.8000 |
| 19 | etruscan | `cn` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.6500 |
| 20 | etruscan | `in` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.6500 |
| 21 | etruscan | `thu` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.8000 |
| 22 | etruscan | `chia` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 23 | etruscan | `ipa` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 24 | etruscan | `ita` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 25 | etruscan | `leu` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 26 | etruscan | `sath` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 27 | etruscan | `thui` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 28 | etruscan | `tiu` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 29 | etruscan | `tul` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.6500 |
| 30 | etruscan | `ais` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 31 | etruscan | `ame` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.6500 |
| 32 | etruscan | `ati` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 33 | etruscan | `eis` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 34 | etruscan | `etera` | 50 | -52.0000 | -52.6400 | 74.1387 | 0.180 | +112.0000 | HT 95a | +0.5450 |
| 35 | etruscan | `huth` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.8000 |
| 36 | etruscan | `mach` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.8000 |
| 37 | etruscan | `nac` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.6500 |
| 38 | etruscan | `ril` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 39 | etruscan | `sar` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.8000 |
| 40 | etruscan | `sech` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 41 | etruscan | `tin` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 42 | etruscan | `uni` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 43 | etruscan | `vel` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 44 | etruscan | `zal` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.8000 |
| 45 | etruscan | `zich` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.3500 |
| 46 | etruscan | `lupum` | 50 | -56.0000 | -64.3200 | 82.8602 | 0.200 | +168.0000 | HT Wc 3017a | +0.5000 |
| 47 | etruscan | `tinia` | 50 | -56.0000 | -60.9600 | 82.4565 | 0.200 | +168.0000 | HT Wc 3017a | +0.5000 |
| 48 | etruscan | `alpan` | 50 | -60.0000 | -56.3200 | 92.0238 | 0.200 | +152.0000 | HT 110a | +0.5000 |
| 49 | etruscan | `cepen` | 50 | -60.0000 | -64.3200 | 82.2711 | 0.200 | +168.0000 | HT Wc 3017a | +0.5000 |
| 50 | etruscan | `nesna` | 50 | -60.0000 | -55.6800 | 91.9542 | 0.200 | +152.0000 | HT 110a | +0.5000 |

_(50 of 138 surfaces shown.)_
