# Per-surface aggregation by median pmcd — pool: toponym

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
| 4 | toponym | `lasaia` | 24 | +124.0000 | +101.3333 | 96.4895 | 0.750 | +264.0000 | KN Zc 6 | +0.7188 |
| 5 | toponym | `ala` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5500 |
| 6 | toponym | `sos` | 50 | +84.0000 | +84.3200 | 83.6635 | 0.860 | +312.0000 | ARKH 2 | +0.5500 |
| 7 | toponym | `aptara` | 24 | +80.0000 | +104.3333 | 115.7579 | 0.792 | +368.0000 | KN Zc 6 | +0.7188 |
| 8 | toponym | `tarra` | 50 | +72.0000 | +82.4000 | 95.4149 | 0.800 | +400.0000 | KN Zc 6 | +0.7660 |
| 9 | toponym | `iassos` | 24 | +60.0000 | +95.3333 | 126.1727 | 0.625 | +424.0000 | KN Zc 6 | +0.7188 |
| 10 | toponym | `ikaria` | 24 | +36.0000 | +30.3333 | 93.3803 | 0.583 | +304.0000 | KN Zc 6 | +0.7188 |
| 11 | toponym | `ttos` | 50 | +12.0000 | +3.2000 | 83.4305 | 0.520 | +208.0000 | ARKH 2 | +0.5500 |
| 12 | toponym | `ephesos` | 13 | +0.0000 | +8.6154 | 86.3032 | 0.462 | +200.0000 | KN Zc 6 | +0.7000 |
| 13 | toponym | `efe` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5500 |
| 14 | toponym | `hua` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 15 | toponym | `ina` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 16 | toponym | `lem` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 17 | toponym | `les` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 18 | toponym | `mna` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 19 | toponym | `ntha` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 20 | toponym | `nthe` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 21 | toponym | `olu` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 22 | toponym | `par` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 23 | toponym | `per` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 24 | toponym | `smu` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 25 | toponym | `tul` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5500 |
| 26 | toponym | `ami` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 27 | toponym | `aso` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 28 | toponym | `gor` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 29 | toponym | `hum` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 30 | toponym | `ida` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.8500 |
| 31 | toponym | `kno` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 32 | toponym | `kor` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5500 |
| 33 | toponym | `lab` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5500 |
| 34 | toponym | `ter` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5500 |
| 35 | toponym | `ther` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5500 |
| 36 | toponym | `tos` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5500 |
| 37 | toponym | `olous` | 50 | -56.0000 | -53.7600 | 74.2931 | 0.200 | +120.0000 | HT 95a | +0.7660 |
| 38 | toponym | `tegea` | 50 | -56.0000 | -60.9600 | 82.4565 | 0.200 | +168.0000 | HT Wc 3017a | +0.7660 |
| 39 | toponym | `krete` | 50 | -64.0000 | -65.2800 | 67.0352 | 0.120 | +80.0000 | KN Zc 6 | +0.7660 |
| 40 | toponym | `samos` | 50 | -64.0000 | -60.3200 | 95.2935 | 0.240 | +200.0000 | ARKH 2 | +0.7660 |
| 41 | toponym | `aksos` | 50 | -72.0000 | -65.6000 | 67.1428 | 0.120 | +80.0000 | KN Zc 6 | +0.7660 |
| 42 | toponym | `athenai` | 24 | -92.0000 | -112.6667 | 75.1502 | 0.042 | +16.0000 | KN Zc 6 | +0.7188 |
| 43 | toponym | `lebena` | 24 | -112.0000 | -109.3333 | 71.2429 | 0.083 | +16.0000 | KN Zc 6 | +0.7188 |
| 44 | toponym | `praisos` | 13 | -112.0000 | -135.3846 | 62.8717 | 0.000 | -24.0000 | KN Zc 6 | +0.7000 |
| 45 | toponym | `sparta` | 24 | -116.0000 | -108.0000 | 91.5059 | 0.042 | +136.0000 | KN Zc 6 | +0.7188 |
| 46 | toponym | `amnisos` | 13 | -120.0000 | -136.0000 | 63.7688 | 0.000 | -32.0000 | KN Zc 6 | +0.7000 |
| 47 | toponym | `lesbos` | 24 | -120.0000 | -108.6667 | 93.0066 | 0.083 | +152.0000 | KN Zc 6 | +0.7188 |
| 48 | toponym | `tulisos` | 13 | -128.0000 | -136.6154 | 59.8222 | 0.000 | -40.0000 | KN Zc 6 | +0.7000 |
| 49 | toponym | `priene` | 24 | -132.0000 | -116.3333 | 77.0447 | 0.125 | +32.0000 | KN Zc 6 | +0.7188 |
| 50 | toponym | `kuzikos` | 13 | -136.0000 | -162.4615 | 69.6989 | 0.000 | -48.0000 | KN Zf 13 | +0.7000 |

_(50 of 88 surfaces shown.)_
