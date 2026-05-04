# Per-surface aggregation by median pmcd — pool: control_toponym

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | control_toponym | `amrrrrh` | 13 | +320.0000 | +324.3077 | 184.9372 | 0.923 | +624.0000 | KN Zf 13 | +0.5000 |
| 2 | control_toponym | `osossa` | 24 | +240.0000 | +259.6667 | 127.3102 | 1.000 | +520.0000 | KN Zc 6 | +0.5000 |
| 3 | control_toponym | `ssoo` | 50 | +152.0000 | +142.4000 | 87.1082 | 0.900 | +320.0000 | HT 117a | +0.5000 |
| 4 | control_toponym | `aas` | 50 | +96.0000 | +100.4800 | 84.2877 | 0.880 | +288.0000 | ARKH 4b | +0.5000 |
| 5 | control_toponym | `ssn` | 50 | +96.0000 | +103.3600 | 83.5966 | 0.900 | +288.0000 | ARKH 4b | +0.5000 |
| 6 | control_toponym | `msssrap` | 13 | +88.0000 | +52.9231 | 163.2754 | 0.615 | +256.0000 | KN Zc 7 | +0.5000 |
| 7 | control_toponym | `ala` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 8 | control_toponym | `ana` | 50 | +84.0000 | +83.6800 | 82.7404 | 0.820 | +312.0000 | ARKH 2 | +0.5000 |
| 9 | control_toponym | `thnth` | 50 | +84.0000 | +84.3200 | 83.6635 | 0.860 | +312.0000 | ARKH 2 | +0.5000 |
| 10 | control_toponym | `sstsnhm` | 13 | +80.0000 | +48.0000 | 166.8680 | 0.538 | +280.0000 | KN Zf 13 | +0.5000 |
| 11 | control_toponym | `onn` | 50 | +72.0000 | +74.7200 | 85.7100 | 0.760 | +272.0000 | HT 103 | +0.5000 |
| 12 | control_toponym | `saenaa` | 24 | +60.0000 | +107.3333 | 104.1260 | 0.875 | +312.0000 | KN Zf 13 | +0.5000 |
| 13 | control_toponym | `hsrmsmh` | 13 | +56.0000 | +91.6923 | 96.0828 | 0.923 | +376.0000 | KN Zc 6 | +0.5000 |
| 14 | control_toponym | `ioonaol` | 13 | +32.0000 | +44.9231 | 123.9569 | 0.692 | +352.0000 | KN Zc 6 | +0.5000 |
| 15 | control_toponym | `ksuaas` | 24 | +20.0000 | +24.0000 | 81.7150 | 0.667 | +192.0000 | KN Zf 13 | +0.5000 |
| 16 | control_toponym | `aasn` | 50 | +8.0000 | +1.4400 | 83.7626 | 0.500 | +208.0000 | ARKH 2 | +0.5000 |
| 17 | control_toponym | `thkoo` | 50 | +8.0000 | -2.4000 | 80.7049 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 18 | control_toponym | `unss` | 50 | +8.0000 | -2.4000 | 80.7049 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 19 | control_toponym | `lnsn` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5000 |
| 20 | control_toponym | `rhsh` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.5000 |
| 21 | control_toponym | `sdas` | 50 | -8.0000 | -1.7600 | 93.3266 | 0.440 | +248.0000 | HT 110a | +0.5000 |
| 22 | control_toponym | `aathei` | 50 | -48.0000 | -53.2800 | 93.7825 | 0.280 | +152.0000 | KH 10 | +0.5000 |
| 23 | control_toponym | `das` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 24 | control_toponym | `eta` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 25 | control_toponym | `kho` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 26 | control_toponym | `kim` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 27 | control_toponym | `mpa` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 28 | control_toponym | `nul` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 29 | control_toponym | `oks` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 30 | control_toponym | `ore` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 31 | control_toponym | `rti` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 32 | control_toponym | `ssthka` | 50 | -48.0000 | -53.1200 | 94.0707 | 0.280 | +160.0000 | KH 10 | +0.5000 |
| 33 | control_toponym | `sto` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 34 | control_toponym | `tokobaa` | 13 | -48.0000 | -37.5385 | 71.2359 | 0.308 | +136.0000 | KN Zc 6 | +0.5000 |
| 35 | control_toponym | `aeth` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 36 | control_toponym | `hli` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 37 | control_toponym | `ors` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 38 | control_toponym | `rhi` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 39 | control_toponym | `sgo` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 40 | control_toponym | `sno` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 41 | control_toponym | `tea` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 42 | control_toponym | `rmioi` | 50 | -60.0000 | -63.5200 | 68.2660 | 0.120 | +80.0000 | KN Zc 6 | +0.5000 |
| 43 | control_toponym | `pseap` | 50 | -64.0000 | -61.7600 | 94.6578 | 0.260 | +192.0000 | ARKH 2 | +0.5000 |
| 44 | control_toponym | `sgaes` | 50 | -64.0000 | -59.3600 | 94.7126 | 0.260 | +192.0000 | ARKH 2 | +0.5000 |
| 45 | control_toponym | `teoit` | 50 | -64.0000 | -59.6800 | 97.1163 | 0.260 | +192.0000 | ARKH 2 | +0.5000 |
| 46 | control_toponym | `eonun` | 50 | -72.0000 | -66.7200 | 68.3822 | 0.120 | +88.0000 | KN Zc 6 | +0.5000 |
| 47 | control_toponym | `boraa` | 50 | -84.0000 | -79.5200 | 84.2307 | 0.200 | +120.0000 | HT 110a | +0.5000 |
| 48 | control_toponym | `kllzua` | 24 | -88.0000 | -110.6667 | 84.2430 | 0.083 | +48.0000 | KN Zc 6 | +0.5000 |
| 49 | control_toponym | `kolee` | 50 | -88.0000 | -80.0000 | 85.2366 | 0.200 | +128.0000 | HT 110a | +0.5000 |
| 50 | control_toponym | `eatpan` | 24 | -96.0000 | -108.0000 | 84.1586 | 0.083 | +96.0000 | KN Zc 6 | +0.5000 |
| 51 | control_toponym | `anealo` | 24 | -100.0000 | -106.6667 | 91.9903 | 0.125 | +72.0000 | KN Zf 13 | +0.5000 |
| 52 | control_toponym | `ismthus` | 24 | -100.0000 | -108.0000 | 61.9677 | 0.000 | -24.0000 | KN Zc 6 | +0.5000 |
| 53 | control_toponym | `iassrm` | 24 | -108.0000 | -124.3333 | 95.6376 | 0.167 | +40.0000 | KN Zc 6 | +0.5000 |
| 54 | control_toponym | `oiosur` | 24 | -112.0000 | -100.6667 | 98.3034 | 0.208 | +88.0000 | HT 95a | +0.5000 |
| 55 | control_toponym | `aesisuo` | 13 | -120.0000 | -153.8462 | 72.5893 | 0.000 | -64.0000 | KN Zf 13 | +0.5000 |
| 56 | control_toponym | `aoothhsp` | 13 | -120.0000 | -153.2308 | 88.5213 | 0.000 | -24.0000 | KN Zf 13 | +0.5000 |
| 57 | control_toponym | `irsthsm` | 24 | -120.0000 | -120.6667 | 71.5883 | 0.042 | +24.0000 | KN Zc 6 | +0.5000 |
| 58 | control_toponym | `kththotzd` | 13 | -120.0000 | -151.3846 | 90.7520 | 0.000 | -16.0000 | KN Zf 13 | +0.5000 |
| 59 | control_toponym | `riaumr` | 24 | -120.0000 | -108.0000 | 80.4322 | 0.125 | +72.0000 | KN Zc 6 | +0.5000 |
| 60 | control_toponym | `klus` | 50 | -132.0000 | -134.0800 | 72.3646 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 61 | control_toponym | `iksoeo` | 24 | -136.0000 | -116.6667 | 76.5216 | 0.083 | +24.0000 | KN Zc 6 | +0.5000 |
| 62 | control_toponym | `nlaisst` | 13 | -136.0000 | -136.6154 | 56.6956 | 0.000 | -32.0000 | KN Zf 13 | +0.5000 |
| 63 | control_toponym | `korn` | 50 | -140.0000 | -136.1600 | 74.3008 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 64 | control_toponym | `spku` | 50 | -140.0000 | -135.3600 | 76.1949 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 65 | control_toponym | `moap` | 50 | -144.0000 | -136.3200 | 72.7421 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 66 | control_toponym | `oans` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 67 | control_toponym | `tursabs` | 13 | -152.0000 | -160.6154 | 102.9036 | 0.077 | +64.0000 | KN Zc 6 | +0.5000 |
| 68 | control_toponym | `bminpss` | 13 | -168.0000 | -156.3077 | 54.6758 | 0.000 | -40.0000 | KN Zc 6 | +0.5000 |
| 69 | control_toponym | `ersath` | 50 | -192.0000 | -200.9600 | 72.8069 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 70 | control_toponym | `okthnl` | 50 | -192.0000 | -201.2800 | 74.2986 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 71 | control_toponym | `ansti` | 50 | -196.0000 | -203.2000 | 74.0162 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 72 | control_toponym | `klire` | 50 | -196.0000 | -201.2800 | 72.5730 | 0.000 | -80.0000 | KN Zc 7 | +0.5000 |
| 73 | control_toponym | `mitsa` | 50 | -196.0000 | -200.6400 | 72.0327 | 0.000 | -80.0000 | HT Wc 3017a | +0.5000 |
| 74 | control_toponym | `mslte` | 50 | -196.0000 | -201.2800 | 72.5730 | 0.000 | -80.0000 | KN Zc 7 | +0.5000 |
| 75 | control_toponym | `slnoh` | 50 | -196.0000 | -201.1200 | 73.7392 | 0.000 | -80.0000 | HT Wc 3017a | +0.5000 |
| 76 | control_toponym | `oaest` | 50 | -200.0000 | -203.0400 | 74.2388 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 77 | control_toponym | `soain` | 50 | -200.0000 | -202.0800 | 74.8042 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 78 | control_toponym | `gndlah` | 24 | -228.0000 | -242.3333 | 59.4858 | 0.000 | -128.0000 | HT 95a | +0.5000 |
| 79 | control_toponym | `mhoarth` | 24 | -232.0000 | -240.3333 | 63.3079 | 0.000 | -136.0000 | HT 122b | +0.5000 |
| 80 | control_toponym | `poitan` | 24 | -232.0000 | -243.0000 | 62.0886 | 0.000 | -136.0000 | HT 95a | +0.5000 |
| 81 | control_toponym | `dpeaok` | 24 | -240.0000 | -241.6667 | 61.6649 | 0.000 | -136.0000 | HT 95a | +0.5000 |
| 82 | control_toponym | `dtskan` | 24 | -244.0000 | -241.6667 | 60.1323 | 0.000 | -136.0000 | HT 95a | +0.5000 |
| 83 | control_toponym | `hdseol` | 24 | -244.0000 | -243.0000 | 59.8136 | 0.000 | -128.0000 | HT 95a | +0.5000 |
| 84 | control_toponym | `osumat` | 24 | -244.0000 | -242.6667 | 62.0394 | 0.000 | -136.0000 | HT 122b | +0.5000 |
| 85 | control_toponym | `thaonlsd` | 13 | -296.0000 | -279.3846 | 45.4136 | 0.000 | -200.0000 | KN Zf 13 | +0.5000 |

_(85 of 85 surfaces shown.)_
