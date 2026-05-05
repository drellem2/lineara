# CHIC substrate-consistency scoring under Eteocretan LM (chic-v5; mg-7c6d)

Per-unknown-sign substrate-consistency analysis. For every candidate phoneme value V drawn from the candidate-value pool (20 values), the Eteocretan-anchored partial mapping is extended with `(unknown_sign → V)` and scored under the v21 Eteocretan LM via `external_phoneme_perplexity_v0`. The control is the same mapping with V replaced by a deterministic class-disjoint value from the same pool (seed: sha256(sign_id || candidate)). The paired_diff (substrate − control) is the per-candidate substrate-consistency score; class-level scores aggregate per-candidate diffs.

## Candidate-value pool

Built from the union of (a) every Linear-B carryover value in the chic-v2 anchor pool and (b) bare vowels a/e/i/o/u so the vowel class is fully covered.

| value | class |
|---|---|
| `a` | vowel |
| `de` | stop |
| `e` | vowel |
| `i` | vowel |
| `ke` | stop |
| `ki` | stop |
| `ma` | nasal |
| `me` | nasal |
| `mu` | nasal |
| `ni` | nasal |
| `o` | vowel |
| `pa` | stop |
| `ra` | liquid |
| `ro` | liquid |
| `ta` | stop |
| `te` | stop |
| `ti` | stop |
| `to` | stop |
| `u` | vowel |
| `wa` | glide |

## Per-sign top-K candidates

Showing the top-5 candidates per unknown sign by paired_diff. Positive paired_diff means the candidate scored better under the Eteocretan LM than its class-disjoint control (i.e. the candidate value, when mixed with the anchor mapping, produces phoneme runs that look more Eteocretan-like than runs produced by a non-class-matched control).

| sign | freq | top-K candidates (value/class/paired_diff) |
|---|---:|---|
| `#001` | 4 | `wa` / glide / +0.002212 ; `me` / nasal / +0.002050 ; `ki` / stop / +0.001654 ; `e` / vowel / +0.001465 ; `i` / vowel / +0.001429 |
| `#002` | 7 | `te` / stop / +0.011829 ; `ni` / nasal / +0.010838 ; `me` / nasal / +0.005874 ; `ke` / stop / +0.005576 ; `wa` / glide / +0.004025 |
| `#003` | 4 | `ma` / nasal / +0.012636 ; `wa` / glide / +0.007581 ; `ki` / stop / +0.007077 ; `me` / nasal / +0.004963 ; `ti` / stop / +0.004551 |
| `#004` | 3 | `ma` / nasal / +0.003214 ; `te` / stop / +0.003084 ; `to` / stop / +0.003045 ; `ti` / stop / +0.002179 ; `pa` / stop / +0.002113 |
| `#005` | 48 | `te` / stop / +0.108741 ; `ni` / nasal / +0.074468 ; `de` / stop / +0.073716 ; `ma` / nasal / +0.059396 ; `me` / nasal / +0.042838 |
| `#006` | 13 | `ti` / stop / +0.019610 ; `me` / nasal / +0.018781 ; `ma` / nasal / +0.018612 ; `wa` / glide / +0.008725 ; `te` / stop / +0.001517 |
| `#007` | 8 | `me` / nasal / +0.013122 ; `ta` / stop / +0.011316 ; `ki` / stop / +0.010944 ; `ma` / nasal / +0.009418 ; `ni` / nasal / +0.008019 |
| `#008` | 7 | `me` / nasal / +0.020962 ; `te` / stop / +0.018639 ; `ma` / nasal / +0.007974 ; `ta` / stop / +0.007839 ; `ni` / nasal / +0.007165 |
| `#009` | 10 | `ni` / nasal / +0.016609 ; `ma` / nasal / +0.013972 ; `me` / nasal / +0.013821 ; `de` / stop / +0.008740 ; `i` / vowel / +0.008028 |
| `#011` | 24 | `de` / stop / +0.032966 ; `ma` / nasal / +0.032056 ; `ti` / stop / +0.031830 ; `i` / vowel / +0.031628 ; `me` / nasal / +0.030767 |
| `#012` | 5 | `ta` / stop / +0.010526 ; `me` / nasal / +0.009261 ; `ma` / nasal / +0.006138 ; `te` / stop / +0.005567 ; `wa` / glide / +0.005331 |
| `#014` | 4 | `te` / stop / +0.003084 ; `me` / nasal / +0.002896 ; `wa` / glide / +0.002687 ; `ta` / stop / +0.002296 ; `a` / vowel / +0.000942 |
| `#015` | 1 | `te` / stop / +0.002447 ; `de` / stop / +0.001081 ; `ma` / nasal / +0.001022 ; `i` / vowel / +0.000905 ; `me` / nasal / +0.000771 |
| `#017` | 6 | `me` / nasal / +0.014426 ; `ma` / nasal / +0.013285 ; `te` / stop / +0.011571 ; `ti` / stop / +0.009381 ; `ta` / stop / +0.007671 |
| `#018` | 12 | `ma` / nasal / +0.025129 ; `ke` / stop / +0.020583 ; `me` / nasal / +0.020122 ; `ki` / stop / +0.014693 ; `ta` / stop / +0.011280 |
| `#020` | 9 | `me` / nasal / +0.012794 ; `de` / stop / +0.010205 ; `te` / stop / +0.009640 ; `ni` / nasal / +0.009047 ; `pa` / stop / +0.007499 |
| `#021` | 3 | `ma` / nasal / +0.011269 ; `me` / nasal / +0.008078 ; `ke` / stop / +0.005061 ; `mu` / nasal / +0.004558 ; `wa` / glide / +0.004373 |
| `#022` | 1 | `me` / nasal / +0.002915 ; `wa` / glide / +0.002212 ; `ma` / nasal / +0.001647 ; `te` / stop / +0.001543 ; `de` / stop / +0.001515 |
| `#023` | 12 | `me` / nasal / +0.024272 ; `ni` / nasal / +0.022260 ; `to` / stop / +0.015493 ; `de` / stop / +0.015223 ; `te` / stop / +0.012701 |
| `#024` | 1 | `te` / stop / +0.003103 ; `ni` / nasal / +0.002507 ; `me` / nasal / +0.002011 ; `ki` / stop / +0.001654 ; `wa` / glide / +0.001347 |
| `#026` | 1 | `te` / stop / +0.002210 ; `wa` / glide / +0.001976 ; `me` / nasal / +0.001448 ; `e` / vowel / +0.001229 ; `ta` / stop / +0.001108 |
| `#027` | 3 | `me` / nasal / +0.010690 ; `te` / stop / +0.006686 ; `de` / stop / +0.004468 ; `ni` / nasal / +0.002239 ; `ki` / stop / +0.002084 |
| `#029` | 18 | `te` / stop / +0.026961 ; `me` / nasal / +0.025893 ; `ra` / liquid / +0.025432 ; `ni` / nasal / +0.021939 ; `ti` / stop / +0.020441 |
| `#030` | 1 | `ni` / nasal / +0.003162 ; `wa` / glide / +0.001347 ; `ki` / stop / +0.001221 ; `ta` / stop / +0.001150 ; `ti` / stop / +0.001090 |
| `#032` | 9 | `ki` / stop / +0.011024 ; `me` / nasal / +0.009562 ; `ta` / stop / +0.009349 ; `pa` / stop / +0.009144 ; `i` / vowel / +0.009127 |
| `#033` | 3 | `ta` / stop / +0.005040 ; `te` / stop / +0.004251 ; `ni` / nasal / +0.003695 ; `i` / vowel / +0.003245 ; `de` / stop / +0.002530 |
| `#034` | 41 | `te` / stop / +0.082605 ; `me` / nasal / +0.066421 ; `ti` / stop / +0.064786 ; `ma` / nasal / +0.063479 ; `ta` / stop / +0.051781 |
| `#035` | 2 | `to` / stop / +0.002093 ; `ta` / stop / +0.002001 ; `i` / vowel / +0.001732 ; `ro` / liquid / +0.001514 ; `ti` / stop / +0.001507 |
| `#036` | 28 | `de` / stop / +0.044674 ; `pa` / stop / +0.035069 ; `te` / stop / +0.032370 ; `mu` / nasal / +0.027518 ; `me` / nasal / +0.027242 |
| `#037` | 3 | `me` / nasal / +0.010694 ; `ti` / stop / +0.008389 ; `te` / stop / +0.006030 ; `ta` / stop / +0.004731 ; `ma` / nasal / +0.004367 |
| `#039` | 7 | `ma` / nasal / +0.021382 ; `ke` / stop / +0.012787 ; `me` / nasal / +0.007221 ; `ni` / nasal / +0.007149 ; `ki` / stop / +0.006944 |
| `#040` | 17 | `ma` / nasal / +0.027452 ; `ra` / liquid / +0.024007 ; `ki` / stop / +0.023893 ; `me` / nasal / +0.023241 ; `wa` / glide / +0.014980 |
| `#043` | 6 | `pa` / stop / +0.013517 ; `ni` / nasal / +0.013383 ; `de` / stop / +0.012820 ; `ti` / stop / +0.010397 ; `ma` / nasal / +0.010028 |
| `#045` | 4 | `me` / nasal / +0.004262 ; `ta` / stop / +0.003491 ; `ma` / nasal / +0.002546 ; `to` / stop / +0.002506 ; `de` / stop / +0.002135 |
| `#046` | 10 | `ma` / nasal / +0.009816 ; `pa` / stop / +0.008239 ; `te` / stop / +0.007979 ; `me` / nasal / +0.005771 ; `ta` / stop / +0.003767 |
| `#047` | 19 | `te` / stop / +0.028569 ; `me` / nasal / +0.017427 ; `ma` / nasal / +0.017044 ; `ra` / liquid / +0.015582 ; `pa` / stop / +0.013176 |
| `#048` | 1 | `ti` / stop / +0.003021 ; `ta` / stop / +0.002458 ; `ma` / nasal / +0.001764 ; `te` / stop / +0.001425 ; `ra` / liquid / +0.001075 |
| `#050` | 23 | `ti` / stop / +0.046737 ; `me` / nasal / +0.035913 ; `te` / stop / +0.034755 ; `wa` / glide / +0.028860 ; `ki` / stop / +0.025849 |
| `#051` | 9 | `ma` / nasal / +0.013706 ; `te` / stop / +0.012841 ; `de` / stop / +0.011203 ; `ta` / stop / +0.009223 ; `wa` / glide / +0.008583 |
| `#052` | 10 | `me` / nasal / +0.031359 ; `de` / stop / +0.014146 ; `ma` / nasal / +0.011238 ; `i` / vowel / +0.010082 ; `ti` / stop / +0.010047 |
| `#055` | 5 | `me` / nasal / +0.006045 ; `ma` / nasal / +0.004571 ; `te` / stop / +0.004181 ; `wa` / glide / +0.002773 ; `pa` / stop / +0.002329 |
| `#056` | 52 | `te` / stop / +0.071792 ; `ni` / nasal / +0.056547 ; `ma` / nasal / +0.039611 ; `ta` / stop / +0.039329 ; `me` / nasal / +0.034059 |
| `#058` | 5 | `me` / nasal / +0.011532 ; `ma` / nasal / +0.011116 ; `ki` / stop / +0.010093 ; `wa` / glide / +0.007954 ; `ti` / stop / +0.005703 |
| `#059` | 5 | `me` / nasal / +0.009438 ; `ma` / nasal / +0.006724 ; `ta` / stop / +0.006021 ; `ni` / nasal / +0.005818 ; `mu` / nasal / +0.005412 |
| `#060` | 8 | `te` / stop / +0.017635 ; `me` / nasal / +0.014666 ; `ma` / nasal / +0.009739 ; `ra` / liquid / +0.009203 ; `de` / stop / +0.005177 |
| `#062` | 11 | `ta` / stop / +0.016169 ; `ni` / nasal / +0.016104 ; `ma` / nasal / +0.012395 ; `me` / nasal / +0.005493 ; `de` / stop / +0.004510 |
| `#063` | 7 | `me` / nasal / +0.014522 ; `i` / vowel / +0.010960 ; `ta` / stop / +0.010599 ; `wa` / glide / +0.009684 ; `ki` / stop / +0.005964 |
| `#064` | 2 | `ni` / nasal / +0.006320 ; `de` / stop / +0.003888 ; `pa` / stop / +0.002113 ; `ki` / stop / +0.002062 ; `to` / stop / +0.001731 |
| `#065` | 3 | `me` / nasal / +0.001915 ; `ki` / stop / +0.001654 ; `ni` / nasal / +0.001471 ; `ma` / nasal / +0.001150 ; `wa` / glide / +0.001000 |
| `#066` | 3 | `ma` / nasal / +0.005699 ; `me` / nasal / +0.005566 ; `te` / stop / +0.003919 ; `ni` / nasal / +0.002510 ; `ra` / liquid / +0.002332 |
| `#067` | 1 | `te` / stop / +0.004279 ; `ni` / nasal / +0.002784 ; `ra` / liquid / +0.002105 ; `ti` / stop / +0.001762 ; `me` / nasal / +0.001324 |
| `#068` | 10 | `te` / stop / +0.025336 ; `ma` / nasal / +0.013347 ; `ta` / stop / +0.012776 ; `pa` / stop / +0.010749 ; `me` / nasal / +0.009432 |
| `#069` | 3 | `te` / stop / +0.009572 ; `pa` / stop / +0.006698 ; `ta` / stop / +0.004984 ; `ti` / stop / +0.004726 ; `ni` / nasal / +0.004060 |
| `#071` | 2 | `pa` / stop / +0.004039 ; `me` / nasal / +0.003300 ; `ti` / stop / +0.002964 ; `te` / stop / +0.002887 ; `ni` / nasal / +0.002525 |
| `#072` | 7 | `ma` / nasal / +0.011732 ; `wa` / glide / +0.009021 ; `i` / vowel / +0.008101 ; `ke` / stop / +0.006316 ; `ni` / nasal / +0.004669 |
| `#074` | 1 | `te` / stop / +0.003103 ; `ni` / nasal / +0.001640 ; `wa` / glide / +0.001308 ; `ta` / stop / +0.001150 ; `ti` / stop / +0.001090 |
| `#075` | 1 | `me` / nasal / +0.002048 ; `ma` / nasal / +0.001458 ; `i` / vowel / +0.001429 ; `ni` / nasal / +0.000925 ; `wa` / glide / +0.000747 |
| `#076` | 3 | `ti` / stop / +0.003649 ; `ni` / nasal / +0.003075 ; `de` / stop / +0.002652 ; `pa` / stop / +0.002546 ; `me` / nasal / +0.002314 |
| `#078` | 3 | `ma` / nasal / +0.003286 ; `pa` / stop / +0.002975 ; `me` / nasal / +0.002896 ; `te` / stop / +0.001962 ; `wa` / glide / +0.001260 |
| `#079` | 1 | `ki` / stop / +0.002741 ; `ke` / stop / +0.002044 ; `ma` / nasal / +0.001645 ; `ni` / nasal / +0.001642 ; `de` / stop / +0.001515 |
| `#080` | 2 | `te` / stop / +0.004888 ; `ma` / nasal / +0.003214 ; `ke` / stop / +0.002774 ; `de` / stop / +0.002160 ; `pa` / stop / +0.002113 |
| `#081` | 1 | `de` / stop / +0.001515 ; `ni` / nasal / +0.001453 ; `mu` / nasal / +0.001087 ; `me` / nasal / +0.000771 ; `wa` / glide / +0.000631 |
| `#082` | 1 | `ma` / nasal / +0.002512 ; `me` / nasal / +0.001861 ; `ni` / nasal / +0.001603 ; `ki` / stop / +0.001221 ; `wa` / glide / +0.001158 |
| `#083` | 1 | `ki` / stop / +0.001182 ; `ma` / nasal / +0.001123 ; `e` / vowel / +0.001033 ; `ni` / nasal / +0.000925 ; `me` / nasal / +0.000771 |
| `#084` | 1 | `ni` / nasal / +0.003252 ; `ma` / nasal / +0.002387 ; `me` / nasal / +0.001906 ; `pa` / stop / +0.001834 ; `ki` / stop / +0.001654 |
| `#085` | 2 | `ti` / stop / +0.002144 ; `ki` / stop / +0.002086 ; `me` / nasal / +0.002048 ; `te` / stop / +0.002015 ; `ma` / nasal / +0.001647 |
| `#087` | 1 | `de` / stop / +0.001435 ; `e` / vowel / +0.001114 ; `te` / stop / +0.000980 ; `ra` / liquid / +0.000968 ; `wa` / glide / +0.000871 |
| `#088` | 2 | `me` / nasal / +0.002915 ; `ma` / nasal / +0.002512 ; `te` / stop / +0.001543 ; `i` / vowel / +0.001429 ; `ni` / nasal / +0.000925 |
| `#089` | 1 | `ma` / nasal / +0.002016 ; `te` / stop / +0.001678 ; `to` / stop / +0.001386 ; `e` / vowel / +0.000736 ; `i` / vowel / +0.000708 |
| `#090` | 1 | `ni` / nasal / +0.002659 ; `wa` / glide / +0.002366 ; `me` / nasal / +0.001746 ; `ki` / stop / +0.001588 ; `te` / stop / +0.001553 |
| `#091` | 1 | `ti` / stop / +0.003612 ; `ta` / stop / +0.003050 ; `ma` / nasal / +0.002817 ; `me` / nasal / +0.002612 ; `de` / stop / +0.002450 |
| `#093` | 1 | `a` / vowel / +0.000000 ; `de` / stop / +0.000000 ; `e` / vowel / +0.000000 ; `i` / vowel / +0.000000 ; `ke` / stop / +0.000000 |
| `#094` | 3 | `ti` / stop / +0.002563 ; `i` / vowel / +0.001732 ; `me` / nasal / +0.001476 ; `ma` / nasal / +0.001303 ; `te` / stop / +0.000855 |
| `#095` | 6 | `ti` / stop / +0.011639 ; `ro` / liquid / +0.007310 ; `ki` / stop / +0.007066 ; `ra` / liquid / +0.006569 ; `ta` / stop / +0.005541 |
| `#096` | 1 | `ma` / nasal / +0.003168 ; `ti` / stop / +0.002800 ; `i` / vowel / +0.001862 ; `ki` / stop / +0.001654 ; `to` / stop / +0.001523 |
| `#100` | 1 | `a` / vowel / +0.000000 ; `de` / stop / +0.000000 ; `e` / vowel / +0.000000 ; `i` / vowel / +0.000000 ; `ke` / stop / +0.000000 |

## Per-sign class-mean paired_diff

Per-class aggregate: mean paired_diff over every candidate value in the class. The winning class for the substrate line of evidence is the one with the highest mean.

| sign | freq | vowel | stop | nasal | liquid | fricative | glide | winning class |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `#001` | 4 | -0.000429 | +0.000218 | +0.000626 | -0.002077 | — | +0.002212 | glide |
| `#002` | 7 | -0.004143 | +0.001679 | +0.004615 | -0.004650 | — | +0.004025 | nasal |
| `#003` | 4 | -0.002601 | +0.001130 | +0.003838 | -0.010098 | — | +0.007581 | glide |
| `#004` | 3 | -0.002011 | +0.000880 | +0.001233 | -0.001617 | — | -0.000470 | nasal |
| `#005` | 48 | -0.042446 | +0.008496 | +0.035490 | -0.048834 | — | +0.025132 | nasal |
| `#006` | 13 | -0.009917 | -0.001074 | +0.008004 | -0.012550 | — | +0.008725 | glide |
| `#007` | 8 | -0.008710 | +0.003279 | +0.007975 | -0.006907 | — | +0.003297 | nasal |
| `#008` | 7 | -0.003360 | +0.003030 | +0.007788 | -0.004883 | — | +0.004300 | nasal |
| `#009` | 10 | -0.006220 | +0.000449 | +0.007602 | -0.012956 | — | +0.007589 | nasal |
| `#011` | 24 | -0.000946 | +0.005239 | +0.024055 | -0.018894 | — | +0.028282 | glide |
| `#012` | 5 | -0.005831 | +0.000995 | +0.003529 | -0.004316 | — | +0.005331 | glide |
| `#014` | 4 | -0.002015 | -0.000113 | +0.000114 | -0.001511 | — | +0.002687 | glide |
| `#015` | 1 | -0.000952 | +0.000259 | +0.000050 | -0.001505 | — | +0.000266 | glide |
| `#017` | 6 | -0.006065 | +0.004332 | +0.007659 | -0.004350 | — | -0.001484 | nasal |
| `#018` | 12 | -0.009456 | +0.007356 | +0.004654 | -0.001609 | — | +0.010822 | glide |
| `#020` | 9 | -0.007734 | +0.001998 | +0.005446 | -0.010307 | — | +0.005846 | glide |
| `#021` | 3 | -0.000628 | +0.002757 | +0.004903 | -0.001127 | — | +0.004373 | nasal |
| `#022` | 1 | -0.000811 | +0.000583 | +0.001264 | -0.001582 | — | +0.002212 | glide |
| `#023` | 12 | -0.011568 | +0.008669 | +0.013135 | +0.003435 | — | -0.007494 | nasal |
| `#024` | 1 | -0.000638 | +0.000554 | +0.000946 | -0.000695 | — | +0.001347 | glide |
| `#026` | 1 | -0.000488 | -0.000080 | +0.000395 | -0.002462 | — | +0.001976 | glide |
| `#027` | 3 | -0.004076 | +0.000393 | +0.002004 | -0.004439 | — | -0.001395 | nasal |
| `#029` | 18 | -0.004547 | +0.003074 | +0.018490 | +0.003908 | — | +0.011443 | nasal |
| `#030` | 1 | -0.000838 | +0.000119 | +0.000601 | -0.001091 | — | +0.001347 | glide |
| `#032` | 9 | -0.005642 | +0.004579 | +0.002986 | -0.012112 | — | -0.001315 | stop |
| `#033` | 3 | -0.003163 | +0.001159 | +0.000437 | -0.002582 | — | +0.001566 | glide |
| `#034` | 41 | -0.030567 | +0.014766 | +0.035674 | -0.028348 | — | -0.036274 | nasal |
| `#035` | 2 | -0.001345 | +0.000391 | -0.000051 | +0.000592 | — | -0.000570 | liquid |
| `#036` | 28 | -0.019110 | +0.008451 | +0.026427 | -0.023117 | — | +0.019344 | nasal |
| `#037` | 3 | -0.003930 | +0.002626 | +0.003860 | -0.004738 | — | +0.004025 | glide |
| `#039` | 7 | -0.007746 | -0.000122 | +0.007269 | -0.003282 | — | -0.006241 | nasal |
| `#040` | 17 | -0.011623 | +0.000545 | +0.010590 | +0.018450 | — | +0.014980 | liquid |
| `#043` | 6 | -0.001799 | +0.005576 | +0.006070 | -0.007134 | — | +0.007414 | glide |
| `#045` | 4 | -0.003016 | +0.000821 | +0.001293 | -0.001406 | — | -0.001411 | nasal |
| `#046` | 10 | -0.004914 | +0.002803 | +0.003604 | -0.003745 | — | +0.003617 | glide |
| `#047` | 19 | -0.009544 | -0.001666 | +0.002317 | -0.004320 | — | +0.001614 | nasal |
| `#048` | 1 | -0.001223 | +0.000415 | +0.000623 | +0.000926 | — | +0.000845 | liquid |
| `#050` | 23 | -0.020568 | +0.014730 | +0.023199 | -0.018963 | — | +0.028860 | glide |
| `#051` | 9 | -0.007458 | +0.005775 | +0.004370 | -0.004069 | — | +0.008583 | glide |
| `#052` | 10 | -0.007416 | +0.002684 | +0.008630 | -0.001790 | — | -0.003283 | nasal |
| `#055` | 5 | -0.003906 | +0.000907 | +0.001679 | -0.003927 | — | +0.002773 | glide |
| `#056` | 52 | -0.042625 | -0.011274 | +0.021542 | -0.056979 | — | -0.014841 | nasal |
| `#058` | 5 | -0.006797 | +0.000315 | +0.004422 | -0.006634 | — | +0.007954 | glide |
| `#059` | 5 | -0.002942 | +0.000090 | +0.006848 | -0.007243 | — | +0.004685 | nasal |
| `#060` | 8 | -0.003354 | +0.001729 | +0.005466 | +0.001239 | — | +0.002824 | nasal |
| `#062` | 11 | -0.005541 | +0.002803 | +0.005906 | -0.006050 | — | +0.001380 | nasal |
| `#063` | 7 | -0.007335 | +0.002777 | +0.003224 | -0.003967 | — | +0.009684 | glide |
| `#064` | 2 | -0.002560 | +0.001381 | +0.001214 | -0.002446 | — | +0.001493 | glide |
| `#065` | 3 | -0.001268 | +0.000293 | +0.001359 | -0.001104 | — | +0.001000 | nasal |
| `#066` | 3 | -0.002228 | +0.000444 | +0.003152 | +0.000459 | — | +0.002164 | nasal |
| `#067` | 1 | -0.001683 | +0.001039 | +0.001015 | +0.000861 | — | +0.000356 | stop |
| `#068` | 10 | -0.010119 | +0.002740 | +0.003362 | -0.001299 | — | -0.002990 | nasal |
| `#069` | 3 | -0.006283 | +0.002601 | +0.002726 | +0.000611 | — | +0.003288 | glide |
| `#071` | 2 | -0.001826 | +0.000732 | +0.001121 | +0.000131 | — | -0.002832 | nasal |
| `#072` | 7 | -0.001518 | -0.000885 | +0.004359 | -0.003105 | — | +0.009021 | glide |
| `#074` | 1 | -0.001142 | +0.001106 | +0.000188 | -0.001137 | — | +0.001308 | glide |
| `#075` | 1 | -0.000642 | -0.000503 | +0.000990 | -0.002172 | — | +0.000747 | nasal |
| `#076` | 3 | -0.001112 | +0.001227 | +0.001631 | -0.001769 | — | -0.001041 | nasal |
| `#078` | 3 | -0.002070 | -0.000738 | +0.001047 | -0.003159 | — | +0.001260 | glide |
| `#079` | 1 | -0.000666 | +0.001210 | +0.000560 | -0.001515 | — | -0.000082 | stop |
| `#080` | 2 | -0.001007 | +0.001572 | +0.000950 | -0.001501 | — | -0.000163 | stop |
| `#081` | 1 | -0.000744 | -0.000163 | +0.000969 | -0.001062 | — | +0.000631 | nasal |
| `#082` | 1 | -0.000916 | -0.000210 | +0.001028 | -0.001166 | — | +0.001158 | glide |
| `#083` | 1 | -0.000670 | -0.000239 | +0.000277 | -0.001348 | — | -0.000295 | nasal |
| `#084` | 1 | -0.000096 | -0.000069 | +0.001654 | -0.001972 | — | -0.001471 | nasal |
| `#085` | 2 | +0.000004 | +0.000967 | +0.000750 | -0.001318 | — | +0.000631 | stop |
| `#087` | 1 | -0.000572 | -0.000109 | -0.000273 | -0.000433 | — | +0.000871 | glide |
| `#088` | 2 | -0.000612 | +0.000335 | +0.001330 | -0.001167 | — | -0.000295 | nasal |
| `#089` | 1 | -0.000166 | -0.000113 | +0.000766 | -0.000401 | — | -0.000300 | nasal |
| `#090` | 1 | -0.001228 | -0.000114 | +0.001270 | +0.000336 | — | +0.002366 | glide |
| `#091` | 1 | -0.001991 | +0.001008 | +0.001629 | +0.000667 | — | +0.001441 | nasal |
| `#093` | 1 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | — | +0.000000 | glide |
| `#094` | 3 | -0.001239 | -0.000355 | +0.000464 | +0.000024 | — | -0.000809 | nasal |
| `#095` | 6 | -0.005856 | +0.003139 | -0.000701 | +0.006939 | — | -0.002687 | liquid |
| `#096` | 1 | -0.000692 | +0.000914 | +0.000674 | -0.001863 | — | +0.001345 | glide |
| `#100` | 1 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | — | +0.000000 | glide |

## Methodology notes

- Target corpus: CHIC syllabographic-only stream (`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 / mg-9700). Same stream the chic-v3 substrate gate ran against.
- Mapping: chic-v2 anchor mapping (20 sign→Linear-B-value pairs) PLUS the candidate (or control) for the single unknown sign. Both the clean `#NNN` and uncertain `[?:#NNN]` corpus token forms are mapped to the same value.
- LM: `harness/external_phoneme_models/eteocretan.json` (v21 artifact, mg-6ccd). The chic-v3 right-tail bayesian gate PASSed for Eteocretan against CHIC at p=7.33e-04, which is the empirical justification for treating Eteocretan as the natural substrate-LM choice for chic-v5.
- Control selection is deterministic (sha256-keyed permutation of the candidate-value pool restricted to class-disjoint values); the brief's 'deterministic seed' specification is implemented as a pure hash function rather than a `random.Random(seed)` draw, eliminating any RNG dependency.
- Per-candidate `n_chars_scored` varies across candidates (the substrate run grows when the unknown sign is high-frequency); the metric's per-char normalization keeps the score comparable, but for very low-frequency unknowns the paired_diff signal is itself low-magnitude. The line-3 winning class is taken regardless of magnitude — the tier classification (line agreement) handles the noise floor.
