# Per-surface aggregation by median pmcd — pool: control_aquitanian

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | control_aquitanian | `ehaahee` | 13 | +264.0000 | +294.1538 | 134.1651 | 1.000 | +728.0000 | KN Zc 6 | +0.5000 |
| 2 | control_aquitanian | `aatzasl` | 24 | +136.0000 | +110.0000 | 127.8176 | 0.875 | +328.0000 | KN Zc 6 | +0.5000 |
| 3 | control_aquitanian | `eez` | 50 | +96.0000 | +100.4800 | 84.2877 | 0.880 | +288.0000 | ARKH 4b | +0.5000 |
| 4 | control_aquitanian | `rru` | 50 | +96.0000 | +100.4800 | 84.2877 | 0.880 | +288.0000 | ARKH 4b | +0.5000 |
| 5 | control_aquitanian | `hah` | 50 | +84.0000 | +84.3200 | 83.6635 | 0.860 | +312.0000 | ARKH 2 | +0.5000 |
| 6 | control_aquitanian | `tit` | 50 | +84.0000 | +84.3200 | 83.6635 | 0.860 | +312.0000 | ARKH 2 | +0.5000 |
| 7 | control_aquitanian | `rlili` | 50 | +80.0000 | +80.3200 | 87.3864 | 0.840 | +320.0000 | KN Zc 6 | +0.5000 |
| 8 | control_aquitanian | `hii` | 50 | +76.0000 | +74.4000 | 87.6539 | 0.760 | +272.0000 | HT 103 | +0.5000 |
| 9 | control_aquitanian | `arzaeai` | 13 | +72.0000 | +43.6923 | 132.4464 | 0.692 | +288.0000 | KN Zc 6 | +0.5000 |
| 10 | control_aquitanian | `ornro` | 50 | +72.0000 | +83.0400 | 100.0466 | 0.720 | +296.0000 | GO Wc 1a | +0.5000 |
| 11 | control_aquitanian | `raiia` | 50 | +72.0000 | +82.4000 | 95.4149 | 0.800 | +400.0000 | KN Zc 6 | +0.5000 |
| 12 | control_aquitanian | `zaa` | 50 | +72.0000 | +74.7200 | 85.7100 | 0.760 | +272.0000 | HT 103 | +0.5000 |
| 13 | control_aquitanian | `riieen` | 24 | +32.0000 | +29.3333 | 104.2731 | 0.583 | +232.0000 | KN Zc 6 | +0.5000 |
| 14 | control_aquitanian | `okka` | 50 | +16.0000 | +13.2800 | 72.2416 | 0.540 | +168.0000 | ARKH 2 | +0.5000 |
| 15 | control_aquitanian | `txnnc` | 50 | +16.0000 | +13.2800 | 72.2416 | 0.540 | +168.0000 | ARKH 2 | +0.5000 |
| 16 | control_aquitanian | `usnsub` | 24 | +16.0000 | +30.0000 | 90.8992 | 0.500 | +216.0000 | KN Zc 6 | +0.5000 |
| 17 | control_aquitanian | `cuug` | 50 | +12.0000 | +8.8000 | 71.5050 | 0.540 | +160.0000 | ARKH 2 | +0.5000 |
| 18 | control_aquitanian | `drre` | 50 | +12.0000 | +8.8000 | 71.5050 | 0.540 | +160.0000 | ARKH 2 | +0.5000 |
| 19 | control_aquitanian | `llatz` | 50 | +12.0000 | +3.6800 | 82.6011 | 0.540 | +208.0000 | ARKH 2 | +0.5000 |
| 20 | control_aquitanian | `tztzan` | 50 | +12.0000 | +3.2000 | 83.4305 | 0.520 | +208.0000 | ARKH 2 | +0.5000 |
| 21 | control_aquitanian | `aaer` | 50 | +8.0000 | +2.7200 | 81.7976 | 0.520 | +208.0000 | ARKH 2 | +0.5000 |
| 22 | control_aquitanian | `anao` | 50 | +8.0000 | +2.8800 | 74.6835 | 0.520 | +168.0000 | HT 117a | +0.5000 |
| 23 | control_aquitanian | `iihe` | 50 | +8.0000 | +4.6400 | 81.3972 | 0.520 | +208.0000 | ARKH 2 | +0.5000 |
| 24 | control_aquitanian | `tznrr` | 50 | +8.0000 | -2.4000 | 80.7049 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 25 | control_aquitanian | `anii` | 50 | +4.0000 | -2.0800 | 80.2845 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 26 | control_aquitanian | `enaa` | 50 | +4.0000 | -3.0400 | 79.4040 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 27 | control_aquitanian | `aiab` | 50 | +0.0000 | +2.4000 | 75.7300 | 0.440 | +168.0000 | HT 117a | +0.5000 |
| 28 | control_aquitanian | `anai` | 50 | +0.0000 | +2.4000 | 75.7300 | 0.440 | +168.0000 | HT 117a | +0.5000 |
| 29 | control_aquitanian | `eass` | 50 | +0.0000 | -4.1600 | 78.8110 | 0.480 | +232.0000 | HT 128a | +0.5000 |
| 30 | control_aquitanian | `gara` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.5000 |
| 31 | control_aquitanian | `ioro` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5000 |
| 32 | control_aquitanian | `lalt` | 50 | -4.0000 | +3.0400 | 76.4641 | 0.440 | +168.0000 | HT 117a | +0.5000 |
| 33 | control_aquitanian | `edae` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.5000 |
| 34 | control_aquitanian | `aoba` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5000 |
| 35 | control_aquitanian | `arla` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5000 |
| 36 | control_aquitanian | `nbzzhh` | 24 | -16.0000 | +10.6667 | 102.8829 | 0.458 | +240.0000 | KN Zc 6 | +0.5000 |
| 37 | control_aquitanian | `an` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 38 | control_aquitanian | `in` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 39 | control_aquitanian | `itx` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 40 | control_aquitanian | `aarig` | 50 | -48.0000 | -53.6000 | 94.6742 | 0.280 | +152.0000 | KH 10 | +0.5000 |
| 41 | control_aquitanian | `eal` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 42 | control_aquitanian | `egb` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 43 | control_aquitanian | `gub` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 44 | control_aquitanian | `iel` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 45 | control_aquitanian | `iiemn` | 50 | -48.0000 | -51.5200 | 94.2122 | 0.340 | +152.0000 | KH 10 | +0.5000 |
| 46 | control_aquitanian | `irihu` | 50 | -48.0000 | -52.1600 | 74.4514 | 0.180 | +128.0000 | HT 95a | +0.5000 |
| 47 | control_aquitanian | `iud` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 48 | control_aquitanian | `lgs` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 49 | control_aquitanian | `lna` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 50 | control_aquitanian | `lsa` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 51 | control_aquitanian | `lzi` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 52 | control_aquitanian | `nte` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 53 | control_aquitanian | `oub` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 54 | control_aquitanian | `sru` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 55 | control_aquitanian | `aahzl` | 50 | -52.0000 | -53.9200 | 94.8843 | 0.300 | +160.0000 | KH 10 | +0.5000 |
| 56 | control_aquitanian | `arh` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 57 | control_aquitanian | `ehi` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 58 | control_aquitanian | `hnu` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 59 | control_aquitanian | `mlh` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 60 | control_aquitanian | `mzs` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 61 | control_aquitanian | `oru` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 62 | control_aquitanian | `osr` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 63 | control_aquitanian | `rrnsa` | 50 | -52.0000 | -52.3200 | 93.6815 | 0.320 | +160.0000 | KH 10 | +0.5000 |
| 64 | control_aquitanian | `uoh` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 65 | control_aquitanian | `eimeh` | 50 | -56.0000 | -56.6400 | 94.0718 | 0.200 | +168.0000 | HT 110a | +0.5000 |
| 66 | control_aquitanian | `leerh` | 50 | -60.0000 | -54.5600 | 81.8457 | 0.220 | +120.0000 | HT Wc 3017a | +0.5000 |
| 67 | control_aquitanian | `lhhoi` | 50 | -60.0000 | -54.5600 | 81.8457 | 0.220 | +120.0000 | HT Wc 3017a | +0.5000 |
| 68 | control_aquitanian | `luaha` | 50 | -60.0000 | -65.1200 | 68.8560 | 0.140 | +88.0000 | KN Zc 6 | +0.5000 |
| 69 | control_aquitanian | `nhhul` | 50 | -60.0000 | -54.5600 | 81.8457 | 0.220 | +120.0000 | HT Wc 3017a | +0.5000 |
| 70 | control_aquitanian | `rtsarx` | 50 | -60.0000 | -56.8000 | 92.7621 | 0.200 | +168.0000 | HT 110a | +0.5000 |
| 71 | control_aquitanian | `azebe` | 50 | -64.0000 | -66.0800 | 69.9405 | 0.140 | +88.0000 | KN Zc 6 | +0.5000 |
| 72 | control_aquitanian | `ezlal` | 50 | -64.0000 | -64.3200 | 68.7434 | 0.160 | +80.0000 | KN Zc 6 | +0.5000 |
| 73 | control_aquitanian | `rehor` | 50 | -64.0000 | -60.3200 | 95.2935 | 0.240 | +200.0000 | ARKH 2 | +0.5000 |
| 74 | control_aquitanian | `erizr` | 50 | -68.0000 | -58.2400 | 93.0485 | 0.300 | +200.0000 | KN Zc 6 | +0.5000 |
| 75 | control_aquitanian | `irhar` | 50 | -68.0000 | -54.5600 | 91.6856 | 0.300 | +200.0000 | KN Zc 6 | +0.5000 |
| 76 | control_aquitanian | `ealdd` | 50 | -84.0000 | -80.1600 | 87.4673 | 0.200 | +120.0000 | HT 110a | +0.5000 |
| 77 | control_aquitanian | `ueinn` | 50 | -84.0000 | -80.1600 | 86.1253 | 0.220 | +120.0000 | HT 110a | +0.5000 |
| 78 | control_aquitanian | `ntsilai` | 24 | -116.0000 | -101.3333 | 88.8944 | 0.042 | +144.0000 | KN Zc 6 | +0.5000 |
| 79 | control_aquitanian | `lasizhz` | 13 | -120.0000 | -136.0000 | 58.7878 | 0.000 | -24.0000 | KN Zc 6 | +0.5000 |
| 80 | control_aquitanian | `aninze` | 24 | -124.0000 | -111.6667 | 69.4158 | 0.083 | +8.0000 | KN Zc 6 | +0.5000 |
| 81 | control_aquitanian | `dblhaa` | 24 | -124.0000 | -116.3333 | 74.2960 | 0.083 | +32.0000 | KN Zc 6 | +0.5000 |
| 82 | control_aquitanian | `udtxrhu` | 24 | -128.0000 | -112.3333 | 84.6476 | 0.125 | +88.0000 | KN Zc 6 | +0.5000 |
| 83 | control_aquitanian | `abnh` | 50 | -132.0000 | -134.0800 | 72.3646 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 84 | control_aquitanian | `egrl` | 50 | -132.0000 | -134.0800 | 72.3646 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 85 | control_aquitanian | `earl` | 50 | -136.0000 | -134.8800 | 72.0357 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 86 | control_aquitanian | `hina` | 50 | -136.0000 | -133.6000 | 70.7310 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 87 | control_aquitanian | `lgzu` | 50 | -136.0000 | -134.8800 | 72.0357 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 88 | control_aquitanian | `onia` | 50 | -136.0000 | -132.0000 | 73.4477 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 89 | control_aquitanian | `rahi` | 50 | -136.0000 | -133.2800 | 73.7322 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 90 | control_aquitanian | `rhia` | 50 | -136.0000 | -131.3600 | 73.0254 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 91 | control_aquitanian | `ronk` | 50 | -136.0000 | -132.0000 | 73.4477 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 92 | control_aquitanian | `uenr` | 50 | -136.0000 | -133.2800 | 73.7322 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 93 | control_aquitanian | `urie` | 50 | -136.0000 | -132.0000 | 73.4477 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 94 | control_aquitanian | `anuh` | 50 | -140.0000 | -136.1600 | 74.3008 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 95 | control_aquitanian | `aoel` | 50 | -140.0000 | -136.4800 | 73.8155 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 96 | control_aquitanian | `ashb` | 50 | -140.0000 | -136.3200 | 75.5051 | 0.000 | -16.0000 | HT 110a | +0.5000 |
| 97 | control_aquitanian | `bile` | 50 | -140.0000 | -136.1600 | 74.3008 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 98 | control_aquitanian | `ionm` | 50 | -140.0000 | -136.3200 | 75.5051 | 0.000 | -16.0000 | HT 110a | +0.5000 |
| 99 | control_aquitanian | `itre` | 50 | -140.0000 | -133.2800 | 72.9468 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 100 | control_aquitanian | `ngeo` | 50 | -140.0000 | -135.3600 | 76.1949 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 101 | control_aquitanian | `nhes` | 50 | -140.0000 | -135.3600 | 76.1949 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 102 | control_aquitanian | `ozti` | 50 | -140.0000 | -133.2800 | 72.9468 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 103 | control_aquitanian | `ribu` | 50 | -140.0000 | -135.3600 | 76.1949 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 104 | control_aquitanian | `txiah` | 50 | -140.0000 | -134.4000 | 74.8588 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 105 | control_aquitanian | `zihn` | 50 | -140.0000 | -134.2400 | 74.1767 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 106 | control_aquitanian | `enrt` | 50 | -144.0000 | -136.1600 | 74.5245 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 107 | control_aquitanian | `haib` | 50 | -144.0000 | -135.8400 | 76.4239 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 108 | control_aquitanian | `hesb` | 50 | -144.0000 | -133.6000 | 73.6739 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 109 | control_aquitanian | `iaem` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 110 | control_aquitanian | `igneitm` | 13 | -144.0000 | -165.5385 | 72.2651 | 0.000 | -48.0000 | KN Zf 13 | +0.5000 |
| 111 | control_aquitanian | `ikez` | 50 | -144.0000 | -136.3200 | 72.7421 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 112 | control_aquitanian | `ilae` | 50 | -144.0000 | -135.6800 | 76.8493 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 113 | control_aquitanian | `keho` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 114 | control_aquitanian | `mrgi` | 50 | -144.0000 | -135.6800 | 76.8493 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 115 | control_aquitanian | `oamb` | 50 | -144.0000 | -134.7200 | 76.0355 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 116 | control_aquitanian | `orgi` | 50 | -144.0000 | -135.6800 | 76.8493 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 117 | control_aquitanian | `ueih` | 50 | -144.0000 | -134.7200 | 76.0355 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 118 | control_aquitanian | `geil` | 50 | -148.0000 | -136.0000 | 73.4782 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 119 | control_aquitanian | `oarz` | 50 | -148.0000 | -136.0000 | 73.4782 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 120 | control_aquitanian | `brhai` | 50 | -192.0000 | -201.1200 | 72.5315 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 121 | control_aquitanian | `doazl` | 50 | -192.0000 | -201.7600 | 73.0815 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 122 | control_aquitanian | `hetbo` | 50 | -192.0000 | -201.1200 | 73.0941 | 0.000 | -72.0000 | HT Wc 3017a | +0.5000 |
| 123 | control_aquitanian | `ishlr` | 50 | -192.0000 | -202.0800 | 72.1387 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 124 | control_aquitanian | `iteos` | 50 | -192.0000 | -202.0800 | 72.1387 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 125 | control_aquitanian | `kertxl` | 50 | -192.0000 | -202.0800 | 71.9966 | 0.000 | -56.0000 | KN Zc 7 | +0.5000 |
| 126 | control_aquitanian | `loraz` | 50 | -192.0000 | -200.9600 | 72.8069 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 127 | control_aquitanian | `aeusi` | 50 | -196.0000 | -201.9200 | 72.6647 | 0.000 | -80.0000 | HT Wc 3017a | +0.5000 |
| 128 | control_aquitanian | `loear` | 50 | -196.0000 | -201.2800 | 74.2641 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 129 | control_aquitanian | `nrlat` | 50 | -196.0000 | -201.2800 | 74.2641 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 130 | control_aquitanian | `osmne` | 50 | -196.0000 | -200.0000 | 73.6695 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 131 | control_aquitanian | `taheg` | 50 | -196.0000 | -202.7200 | 74.0786 | 0.000 | -56.0000 | KN Zc 7 | +0.5000 |
| 132 | control_aquitanian | `tbaoi` | 50 | -196.0000 | -201.9200 | 74.7143 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 133 | control_aquitanian | `aedru` | 50 | -200.0000 | -203.6800 | 74.0371 | 0.000 | -80.0000 | KN Zc 7 | +0.5000 |
| 134 | control_aquitanian | `agbie` | 50 | -200.0000 | -203.5200 | 73.9325 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 135 | control_aquitanian | `auhis` | 50 | -200.0000 | -204.3200 | 74.1581 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 136 | control_aquitanian | `rneham` | 24 | -232.0000 | -243.0000 | 60.7426 | 0.000 | -128.0000 | HT 95a | +0.5000 |
| 137 | control_aquitanian | `rsntze` | 24 | -232.0000 | -241.0000 | 59.8359 | 0.000 | -136.0000 | HT 122b | +0.5000 |
| 138 | control_aquitanian | `abudpts` | 24 | -236.0000 | -244.6667 | 57.5461 | 0.000 | -144.0000 | HT 95a | +0.5000 |
| 139 | control_aquitanian | `tsshdri` | 24 | -244.0000 | -242.0000 | 62.1932 | 0.000 | -136.0000 | HT 95a | +0.5000 |

_(139 of 139 surfaces shown.)_
