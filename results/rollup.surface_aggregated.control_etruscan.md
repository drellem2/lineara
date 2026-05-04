# Per-surface aggregation by median pmcd — pool: control_etruscan

Per-surface aggregation of `partial_mapping_compression_delta_v0` (pmcd) over candidates that share a (pool, surface) pair. Surfaces with fewer than 10 candidates are dropped; only the latest row per (hypothesis_path, hash) is counted (so post-fix rescores from mg-c2af replace prior runs).

Columns:
- **n_candidates**: number of candidates with this surface in this pool
- **median_pmcd / mean_pmcd / sd_pmcd**: per-surface aggregates of pmcd
- **frac_positive**: fraction of candidates with pmcd > 0 (i.e. the partial mapping compresses the corpus)
- **best_inscription**: inscription on which this surface scored its highest pmcd
- **geographic_mean**: per-surface mean of geographic_genre_fit_v1

| rank | pool | surface | n | median_pmcd | mean_pmcd | sd_pmcd | frac_positive | best_pmcd | best_inscription | geo_mean |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | control_etruscan | `aasaas` | 24 | +512.0000 | +534.0000 | 177.4373 | 1.000 | +912.0000 | KN Zc 6 | +0.5000 |
| 2 | control_etruscan | `iilie` | 50 | +184.0000 | +176.8000 | 124.9256 | 0.920 | +440.0000 | KN Zc 6 | +0.5000 |
| 3 | control_etruscan | `aeana` | 50 | +168.0000 | +166.2400 | 104.0159 | 0.940 | +448.0000 | ARKH 2 | +0.5000 |
| 4 | control_etruscan | `zlull` | 50 | +136.0000 | +146.8800 | 129.1326 | 0.860 | +544.0000 | KN Zc 6 | +0.5000 |
| 5 | control_etruscan | `uaeapa` | 24 | +112.0000 | +103.6667 | 94.0490 | 0.833 | +264.0000 | KN Zc 6 | +0.5000 |
| 6 | control_etruscan | `miiier` | 24 | +100.0000 | +103.3333 | 135.1131 | 0.792 | +312.0000 | KN Zc 6 | +0.5000 |
| 7 | control_etruscan | `aan` | 50 | +96.0000 | +100.4800 | 84.2877 | 0.880 | +288.0000 | ARKH 4b | +0.5000 |
| 8 | control_etruscan | `laaeca` | 24 | +88.0000 | +119.6667 | 130.9754 | 0.833 | +472.0000 | KN Zc 6 | +0.5000 |
| 9 | control_etruscan | `uuaapee` | 13 | +48.0000 | +81.2308 | 120.6687 | 0.769 | +392.0000 | KN Zc 6 | +0.5000 |
| 10 | control_etruscan | `ctiuci` | 24 | +32.0000 | +31.3333 | 92.7769 | 0.625 | +304.0000 | KN Zc 6 | +0.5000 |
| 11 | control_etruscan | `luua` | 50 | +16.0000 | +10.0800 | 71.2640 | 0.520 | +160.0000 | ARKH 2 | +0.5000 |
| 12 | control_etruscan | `atti` | 50 | +12.0000 | +8.8000 | 71.5050 | 0.540 | +160.0000 | ARKH 2 | +0.5000 |
| 13 | control_etruscan | `mmaz` | 50 | +12.0000 | +3.6800 | 82.6011 | 0.540 | +208.0000 | ARKH 2 | +0.5000 |
| 14 | control_etruscan | `nmmp` | 50 | +12.0000 | +9.4400 | 71.0640 | 0.520 | +168.0000 | ARKH 2 | +0.5000 |
| 15 | control_etruscan | `pcmm` | 50 | +8.0000 | -2.4000 | 80.7049 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 16 | control_etruscan | `sann` | 50 | +8.0000 | -2.4000 | 80.7049 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 17 | control_etruscan | `ssri` | 50 | +8.0000 | +4.6400 | 81.3972 | 0.520 | +208.0000 | ARKH 2 | +0.5000 |
| 18 | control_etruscan | `hsaa` | 50 | +4.0000 | -3.0400 | 79.4040 | 0.500 | +232.0000 | HT 128a | +0.5000 |
| 19 | control_etruscan | `etut` | 50 | +0.0000 | -0.3200 | 86.9017 | 0.440 | +184.0000 | HT 128a | +0.5000 |
| 20 | control_etruscan | `ichcch` | 50 | +0.0000 | +1.2800 | 86.9812 | 0.440 | +184.0000 | HT 128a | +0.5000 |
| 21 | control_etruscan | `neie` | 50 | +0.0000 | +2.2400 | 85.4172 | 0.460 | +184.0000 | HT 128a | +0.5000 |
| 22 | control_etruscan | `sata` | 50 | +0.0000 | +1.6000 | 85.2817 | 0.460 | +176.0000 | HT 110a | +0.5000 |
| 23 | control_etruscan | `uchu` | 50 | -4.0000 | -1.6000 | 92.3714 | 0.420 | +240.0000 | HT 110a | +0.5000 |
| 24 | control_etruscan | `inmi` | 50 | -12.0000 | -2.0800 | 91.0428 | 0.440 | +240.0000 | HT 110a | +0.5000 |
| 25 | control_etruscan | `caailui` | 13 | -16.0000 | -33.2308 | 122.4507 | 0.308 | +216.0000 | KN Zc 6 | +0.5000 |
| 26 | control_etruscan | `chischeaa` | 13 | -16.0000 | -21.5385 | 89.1055 | 0.462 | +168.0000 | KN Zc 6 | +0.5000 |
| 27 | control_etruscan | `la` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.5000 |
| 28 | control_etruscan | `sa` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.5000 |
| 29 | control_etruscan | `thi` | 50 | -24.0000 | -31.6800 | 55.4709 | 0.280 | +88.0000 | ARKH 5 | +0.5000 |
| 30 | control_etruscan | `ci` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 31 | control_etruscan | `el` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 32 | control_etruscan | `np` | 50 | -28.0000 | -31.8400 | 54.8567 | 0.240 | +88.0000 | ARKH 5 | +0.5000 |
| 33 | control_etruscan | `amiphnai` | 13 | -32.0000 | -20.9231 | 94.5292 | 0.385 | +184.0000 | KN Zc 6 | +0.5000 |
| 34 | control_etruscan | `muuavthth` | 13 | -32.0000 | -32.6154 | 66.5242 | 0.231 | +120.0000 | KN Zc 6 | +0.5000 |
| 35 | control_etruscan | `ththmrc` | 50 | -40.0000 | -49.7600 | 95.0121 | 0.320 | +168.0000 | KH 10 | +0.5000 |
| 36 | control_etruscan | `uruitie` | 13 | -40.0000 | -28.3077 | 100.5886 | 0.385 | +160.0000 | KN Zc 6 | +0.5000 |
| 37 | control_etruscan | `chsa` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 38 | control_etruscan | `elc` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 39 | control_etruscan | `iat` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 40 | control_etruscan | `ichr` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 41 | control_etruscan | `iem` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 42 | control_etruscan | `laz` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 43 | control_etruscan | `nthi` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 44 | control_etruscan | `rcu` | 50 | -48.0000 | -56.3200 | 66.7405 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 45 | control_etruscan | `suc` | 50 | -48.0000 | -56.1600 | 66.0374 | 0.200 | +64.0000 | ARKH 2 | +0.5000 |
| 46 | control_etruscan | `ththavi` | 50 | -48.0000 | -52.6400 | 95.3456 | 0.300 | +160.0000 | KH 10 | +0.5000 |
| 47 | control_etruscan | `thzzvl` | 50 | -48.0000 | -52.1600 | 80.2275 | 0.200 | +120.0000 | HT Wc 3017a | +0.5000 |
| 48 | control_etruscan | `aht` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 49 | control_etruscan | `aiph` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 50 | control_etruscan | `arth` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 51 | control_etruscan | `aun` | 50 | -52.0000 | -59.3600 | 68.3912 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 52 | control_etruscan | `lnth` | 50 | -52.0000 | -57.4400 | 69.1283 | 0.200 | +56.0000 | ARKH 2 | +0.5000 |
| 53 | control_etruscan | `nai` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 54 | control_etruscan | `nil` | 50 | -52.0000 | -58.2400 | 68.9865 | 0.200 | +64.0000 | ARKH 4a | +0.5000 |
| 55 | control_etruscan | `ninre` | 50 | -52.0000 | -52.6400 | 73.3228 | 0.180 | +112.0000 | HT 95a | +0.5000 |
| 56 | control_etruscan | `rla` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 57 | control_etruscan | `thia` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 58 | control_etruscan | `ula` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 59 | control_etruscan | `uthm` | 50 | -52.0000 | -56.4800 | 69.8049 | 0.220 | +64.0000 | ARKH 2 | +0.5000 |
| 60 | control_etruscan | `annet` | 50 | -56.0000 | -54.5600 | 80.5372 | 0.200 | +120.0000 | HT Wc 3017a | +0.5000 |
| 61 | control_etruscan | `cscrn` | 50 | -56.0000 | -54.2400 | 73.2914 | 0.160 | +112.0000 | HT 95a | +0.5000 |
| 62 | control_etruscan | `narns` | 50 | -56.0000 | -57.2800 | 92.7912 | 0.200 | +168.0000 | HT 110a | +0.5000 |
| 63 | control_etruscan | `vnena` | 50 | -56.0000 | -60.4800 | 80.9885 | 0.200 | +160.0000 | HT Wc 3017a | +0.5000 |
| 64 | control_etruscan | `miphit` | 50 | -60.0000 | -63.3600 | 81.5818 | 0.180 | +168.0000 | HT Wc 3017a | +0.5000 |
| 65 | control_etruscan | `neeui` | 50 | -60.0000 | -54.5600 | 81.8457 | 0.220 | +120.0000 | HT Wc 3017a | +0.5000 |
| 66 | control_etruscan | `rmltl` | 50 | -60.0000 | -64.4800 | 67.7012 | 0.120 | +88.0000 | KN Zc 6 | +0.5000 |
| 67 | control_etruscan | `afita` | 50 | -64.0000 | -62.2400 | 94.7423 | 0.260 | +184.0000 | ARKH 2 | +0.5000 |
| 68 | control_etruscan | `iauri` | 50 | -64.0000 | -61.6000 | 93.2300 | 0.260 | +192.0000 | ARKH 2 | +0.5000 |
| 69 | control_etruscan | `nmlnv` | 50 | -64.0000 | -56.0000 | 92.0800 | 0.180 | +160.0000 | HT 110a | +0.5000 |
| 70 | control_etruscan | `thipti` | 50 | -68.0000 | -54.7200 | 93.0804 | 0.280 | +200.0000 | KN Zc 6 | +0.5000 |
| 71 | control_etruscan | `inathn` | 50 | -72.0000 | -56.3200 | 94.2638 | 0.300 | +208.0000 | KN Zc 6 | +0.5000 |
| 72 | control_etruscan | `mpiia` | 50 | -76.0000 | -71.0400 | 72.4190 | 0.140 | +104.0000 | HT Wc 3017a | +0.5000 |
| 73 | control_etruscan | `eahss` | 50 | -80.0000 | -80.4800 | 85.8562 | 0.200 | +120.0000 | HT 110a | +0.5000 |
| 74 | control_etruscan | `pheei` | 50 | -80.0000 | -69.6000 | 70.8395 | 0.160 | +120.0000 | HT Wc 3017a | +0.5000 |
| 75 | control_etruscan | `urenn` | 50 | -80.0000 | -78.8800 | 87.6211 | 0.200 | +128.0000 | HT 110a | +0.5000 |
| 76 | control_etruscan | `aalchci` | 24 | -88.0000 | -112.3333 | 93.7935 | 0.125 | +56.0000 | KN Zc 6 | +0.5000 |
| 77 | control_etruscan | `phtlleth` | 24 | -96.0000 | -121.6667 | 97.4332 | 0.125 | +32.0000 | KN Zc 6 | +0.5000 |
| 78 | control_etruscan | `aeauli` | 24 | -100.0000 | -97.3333 | 95.9907 | 0.208 | +88.0000 | HT 95a | +0.5000 |
| 79 | control_etruscan | `iuivrn` | 24 | -104.0000 | -99.0000 | 93.2899 | 0.167 | +88.0000 | HT 95a | +0.5000 |
| 80 | control_etruscan | `eciurc` | 24 | -108.0000 | -111.3333 | 63.1999 | 0.000 | -24.0000 | KN Zc 6 | +0.5000 |
| 81 | control_etruscan | `izththuch` | 24 | -108.0000 | -125.3333 | 94.5351 | 0.167 | +32.0000 | KN Zc 6 | +0.5000 |
| 82 | control_etruscan | `ithalam` | 24 | -112.0000 | -120.3333 | 72.1657 | 0.042 | +16.0000 | KN Zc 6 | +0.5000 |
| 83 | control_etruscan | `taurrv` | 24 | -116.0000 | -122.3333 | 87.0702 | 0.083 | +8.0000 | KN Zc 6 | +0.5000 |
| 84 | control_etruscan | `nuhuse` | 24 | -128.0000 | -112.6667 | 71.4392 | 0.083 | +8.0000 | KN Zc 6 | +0.5000 |
| 85 | control_etruscan | `aczf` | 50 | -132.0000 | -134.0800 | 72.3646 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 86 | control_etruscan | `suat` | 50 | -132.0000 | -135.8400 | 73.1550 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 87 | control_etruscan | `cchva` | 50 | -136.0000 | -133.6000 | 70.7310 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 88 | control_etruscan | `hcsm` | 50 | -136.0000 | -134.8800 | 72.0357 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 89 | control_etruscan | `iazs` | 50 | -136.0000 | -134.8800 | 72.0357 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 90 | control_etruscan | `lavm` | 50 | -136.0000 | -134.8800 | 72.0357 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 91 | control_etruscan | `saem` | 50 | -136.0000 | -133.2800 | 73.7322 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 92 | control_etruscan | `zltha` | 50 | -136.0000 | -131.3600 | 73.0254 | 0.000 | -8.0000 | HT 117a | +0.5000 |
| 93 | control_etruscan | `emis` | 50 | -140.0000 | -136.6400 | 74.6849 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 94 | control_etruscan | `ilthcnc` | 24 | -140.0000 | -119.0000 | 77.0909 | 0.083 | +32.0000 | KN Zc 6 | +0.5000 |
| 95 | control_etruscan | `nmhk` | 50 | -140.0000 | -134.4000 | 74.8588 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 96 | control_etruscan | `sicf` | 50 | -140.0000 | -134.4000 | 74.8588 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 97 | control_etruscan | `vumt` | 50 | -140.0000 | -134.4000 | 74.8588 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 98 | control_etruscan | `ireu` | 50 | -144.0000 | -136.3200 | 72.7421 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 99 | control_etruscan | `macp` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 100 | control_etruscan | `mechthsll` | 13 | -144.0000 | -155.0769 | 56.9621 | 0.000 | -32.0000 | KN Zc 6 | +0.5000 |
| 101 | control_etruscan | `mnsv` | 50 | -144.0000 | -136.1600 | 74.5245 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 102 | control_etruscan | `nuei` | 50 | -144.0000 | -135.6800 | 76.8493 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 103 | control_etruscan | `psach` | 50 | -144.0000 | -135.6800 | 76.8493 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 104 | control_etruscan | `senu` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 105 | control_etruscan | `ucli` | 50 | -144.0000 | -134.7200 | 76.0355 | 0.000 | -16.0000 | ARKH 2 | +0.5000 |
| 106 | control_etruscan | `unsz` | 50 | -144.0000 | -136.3200 | 74.4982 | 0.000 | -16.0000 | HT 117a | +0.5000 |
| 107 | control_etruscan | `cael` | 50 | -148.0000 | -136.0000 | 73.4782 | 0.000 | -24.0000 | ARKH 2 | +0.5000 |
| 108 | control_etruscan | `asanvum` | 13 | -152.0000 | -136.0000 | 83.9634 | 0.000 | -24.0000 | KN Zc 6 | +0.5000 |
| 109 | control_etruscan | `chnrlalth` | 13 | -160.0000 | -168.0000 | 87.2415 | 0.000 | -48.0000 | KN Zc 6 | +0.5000 |
| 110 | control_etruscan | `cvalthza` | 13 | -160.0000 | -155.0769 | 76.2531 | 0.000 | -24.0000 | KN Zf 13 | +0.5000 |
| 111 | control_etruscan | `uizrpmi` | 13 | -176.0000 | -164.9231 | 67.3389 | 0.000 | -16.0000 | KN Zc 6 | +0.5000 |
| 112 | control_etruscan | `irtam` | 50 | -188.0000 | -200.4800 | 72.4503 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 113 | control_etruscan | `escmr` | 50 | -192.0000 | -202.0800 | 72.1387 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 114 | control_etruscan | `ithalr` | 50 | -192.0000 | -202.0800 | 72.1387 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 115 | control_etruscan | `mialn` | 50 | -192.0000 | -199.8400 | 75.5480 | 0.000 | -72.0000 | HT Wc 3017a | +0.5000 |
| 116 | control_etruscan | `nthciu` | 50 | -192.0000 | -200.9600 | 74.7328 | 0.000 | -80.0000 | KN Zc 6 | +0.5000 |
| 117 | control_etruscan | `sueip` | 50 | -192.0000 | -199.3600 | 75.2993 | 0.000 | -48.0000 | KN Zc 7 | +0.5000 |
| 118 | control_etruscan | `cthpnr` | 50 | -196.0000 | -202.7200 | 74.0613 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 119 | control_etruscan | `mrnce` | 50 | -196.0000 | -202.0800 | 74.8897 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 120 | control_etruscan | `muthfl` | 50 | -196.0000 | -202.0800 | 74.8897 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 121 | control_etruscan | `suirc` | 50 | -196.0000 | -200.0000 | 73.6695 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 122 | control_etruscan | `thuera` | 50 | -196.0000 | -200.0000 | 73.6695 | 0.000 | -64.0000 | KN Zc 7 | +0.5000 |
| 123 | control_etruscan | `vsinc` | 50 | -196.0000 | -201.6000 | 73.5652 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 124 | control_etruscan | `relfp` | 50 | -204.0000 | -202.7200 | 73.8710 | 0.000 | -72.0000 | KN Zc 7 | +0.5000 |
| 125 | control_etruscan | `srchlcn` | 24 | -232.0000 | -243.0000 | 60.7426 | 0.000 | -128.0000 | HT 95a | +0.5000 |
| 126 | control_etruscan | `tthlain` | 24 | -232.0000 | -240.0000 | 60.7509 | 0.000 | -136.0000 | HT 95a | +0.5000 |
| 127 | control_etruscan | `paceun` | 24 | -236.0000 | -244.0000 | 62.6099 | 0.000 | -136.0000 | HT 95a | +0.5000 |
| 128 | control_etruscan | `lemsthu` | 24 | -240.0000 | -243.3333 | 62.1361 | 0.000 | -144.0000 | HT 122b | +0.5000 |
| 129 | control_etruscan | `chelnscr` | 13 | -288.0000 | -279.3846 | 53.1088 | 0.000 | -184.0000 | KN Zf 13 | +0.5000 |

_(129 of 129 surfaces shown.)_
