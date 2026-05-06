# CHIC chic-v5 tier-3 candidates: cross-pool L3 robustness check (chic-v12; mg-2035)

## Method

Methodologically symmetric extension of chic-v11 (mg-d69c). chic-v11 ran the chic-v5 L3 substrate-consistency line under each of the 4 substrate-pool LMs on the 3 chic-v5 **tier-2** candidate proposals. chic-v12 scales the same robustness check to the **29 chic-v5 tier-3 candidates** — signs where exactly 2 of the 3 non-silent lines of evidence agree (line 4 cross-script paleographic is silent for all 76 chic-v5 unknowns by construction).

For each (tier-3 candidate, substrate pool) cell:

1. Rebuild the candidate-value pool from chic-v2 anchor LB-carryover values + bare vowels, filtered to values whose first character is in the substrate pool's phoneme inventory (chic-v5 convention).
2. For each candidate value V, score (chic-v2 anchors ∪ {sign → V}) against a deterministic class-disjoint sha256-keyed control under the substrate pool's LM via `external_phoneme_perplexity_v0`.
3. Per-class mean paired_diff picks the L3 winning class.

The 29 × 4 = 116 cells produce the per-candidate cross-pool L3 verdict. For each candidate, the chic-v5 proposed class is the reference; `corroborated_by` lists non-Eteocretan substrate LMs whose L3 vote matches the chic-v5 proposed class; `reclassification` is one of three bands per the chic-v12 brief.

## Acceptance bands (chic-v12 brief)

- **`tier-2-equivalent`** — ≥1 non-Eteocretan substrate LM corroborates the chic-v5 proposed class. Same evidence structure as the chic-v11 surviving tier-2 (`#032`): three independent lines of agreement (chic-v5 L1, L2 — or L1/L2 + Eteocretan L3 for the 6 L1+L2-disagree tier-3 cases) + ≥ 1 non-Eteocretan substrate LM.
- **`tier-3-corroborated`** — only Eteocretan-L3 corroborates the chic-v5 proposed class. For the 23 tier-3 candidates where L1+L2 agree this is structurally impossible (Eteocretan-L3 disagrees by chic-v5 construction — that is why they are tier-3 and not tier-2). For the 6 tier-3 candidates where L1+L2 disagree (#006/#017/#021/#033/#050/#063, consensus via L1-or-L2 + Eteocretan-L3 agreement) this is the chic-v5 baseline state by construction.
- **`tier-3-uncorroborated`** — no LM's L3 corroborates the chic-v5 proposed class. For the 23 L1+L2-agree tier-3 candidates this means the cross-pool extension produces no additional substrate-LM support beyond chic-v5's L1+L2 distributional agreement.

## Pool-LM dispatch table

| substrate pool | LM file | candidate-pool size |
|---|---|---:|
| aquitanian | `harness/external_phoneme_models/basque.json` | 21 |
| etruscan | `harness/external_phoneme_models/etruscan.json` | 18 |
| toponym | `harness/external_phoneme_models/basque.json` | 19 |
| eteocretan | `harness/external_phoneme_models/eteocretan.json` | 20 |

Per-pool candidate-value pool composition (each pool's filter differs because the substrate-pool phoneme inventories differ; byte-identical to chic-v11 since the chic-v2 anchor pool and the substrate-pool yamls are unchanged):

- **aquitanian** (21 values): `a` `de` `e` `i` `ja` `je` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **etruscan** (18 values): `a` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **toponym** (19 values): `a` `de` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **eteocretan** (20 values): `a` `de` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u` `wa`

## Headline reclassification counts

| reclassification | n |
|---|---:|
| tier-2-equivalent | **8** |
| tier-3-corroborated | 4 |
| tier-3-uncorroborated | 17 |
| **total tier-3** | **29** |

## Per-candidate cross-pool L3 verdict

Rows ordered by tier-3 leaderboard order. `L1+L2 consensus` is the class L1 and L2 agree on (`(disagree)` for the 6 cases where they differ; the chic-v5 proposed class for those rows comes from L1-or-L2 + Eteocretan-L3 agreement, listed in the per-LM Eteocretan column). `corroborated_by` lists non-Eteocretan LMs whose winning class matches the chic-v5 proposed class; an empty list means none of the 3 non-Eteocretan substrate LMs corroborates.

| sign | freq | L1 | L2 | L1+L2 consensus | chic-v5 proposed | Eteocretan-L3 | Aquitanian-L3 | Etruscan-L3 | toponym-L3 | corroborated_by | reclassification |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| `#002` | 7 | liquid | liquid | liquid | liquid | nasal | stop | nasal | nasal | — | tier-3-uncorroborated |
| `#005` | 48 | stop | stop | stop | stop | nasal | stop | nasal | stop | aquitanian, toponym | tier-2-equivalent |
| `#006` | 13 | glide | stop | (disagree) | glide | glide | stop | nasal | stop | — | tier-3-corroborated |
| `#007` | 8 | vowel | vowel | vowel | vowel | nasal | stop | stop | stop | — | tier-3-uncorroborated |
| `#008` | 7 | glide | glide | glide | glide | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#009` | 10 | stop | stop | stop | stop | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#011` | 24 | liquid | liquid | liquid | liquid | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#017` | 6 | stop | nasal | (disagree) | nasal | nasal | stop | nasal | stop | etruscan | tier-2-equivalent |
| `#020` | 9 | vowel | vowel | vowel | vowel | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#021` | 3 | glide | nasal | (disagree) | nasal | nasal | nasal | nasal | nasal | aquitanian, etruscan, toponym | tier-2-equivalent |
| `#027` | 3 | glide | glide | glide | glide | nasal | stop | nasal | nasal | — | tier-3-uncorroborated |
| `#033` | 3 | stop | glide | (disagree) | glide | glide | liquid | nasal | liquid | — | tier-3-corroborated |
| `#037` | 3 | liquid | liquid | liquid | liquid | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#039` | 7 | stop | stop | stop | stop | nasal | glide | nasal | stop | toponym | tier-2-equivalent |
| `#040` | 17 | stop | stop | stop | stop | liquid | liquid | nasal | liquid | — | tier-3-uncorroborated |
| `#043` | 6 | liquid | liquid | liquid | liquid | glide | stop | nasal | stop | — | tier-3-uncorroborated |
| `#045` | 4 | stop | stop | stop | stop | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#050` | 23 | glide | stop | (disagree) | glide | glide | nasal | nasal | nasal | — | tier-3-corroborated |
| `#055` | 5 | stop | stop | stop | stop | glide | stop | nasal | stop | aquitanian, toponym | tier-2-equivalent |
| `#056` | 52 | stop | stop | stop | stop | nasal | nasal | stop | nasal | etruscan | tier-2-equivalent |
| `#058` | 5 | stop | stop | stop | stop | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#059` | 5 | glide | glide | glide | glide | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#060` | 8 | stop | stop | stop | stop | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#063` | 7 | glide | liquid | (disagree) | glide | glide | stop | nasal | stop | — | tier-3-corroborated |
| `#065` | 3 | stop | stop | stop | stop | nasal | stop | nasal | stop | aquitanian, toponym | tier-2-equivalent |
| `#066` | 3 | stop | stop | stop | stop | nasal | liquid | nasal | liquid | — | tier-3-uncorroborated |
| `#069` | 3 | stop | stop | stop | stop | glide | liquid | nasal | liquid | — | tier-3-uncorroborated |
| `#072` | 7 | stop | stop | stop | stop | glide | nasal | stop | stop | etruscan, toponym | tier-2-equivalent |
| `#078` | 3 | stop | stop | stop | stop | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |

## Per-candidate per-pool per-class mean paired_diff

Detail-table view of the 116 cells. Each row is one (candidate, pool) cell; columns are per-class mean paired_diff over the surviving candidate values. `winning class` is the per-class argmax. `—` for a class indicates the class is empty in the rebuilt candidate-value pool for that substrate (e.g. `glide` for aquitanian/etruscan/toponym, since their candidate pools exclude `wa`/`ja`/`je` by inventory filter; this is a structural property of those pools, not an L3 finding).

### `#002` (chic-v5 proposed: liquid; L1=liquid, L2=liquid, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `te` | +0.003287 | -0.005638 | +0.003287 | +0.002688 | -0.002879 | — | -0.000876 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.009230 | -0.009471 | +0.006581 | +0.009230 | -0.006516 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.003659 | -0.005638 | +0.002588 | +0.003659 | -0.002879 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ni` | +0.004615 | -0.004143 | +0.001679 | +0.004615 | -0.004650 | — | +0.004025 |

### `#005` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `te` | +0.080098 | -0.056365 | +0.080098 | +0.021654 | +0.077819 | — | -0.057882 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.059113 | -0.055314 | +0.031627 | +0.059113 | -0.076994 | — | — |
| toponym | `basque.json` | stop | `te` | +0.065813 | -0.078986 | +0.065813 | +0.021654 | +0.021267 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ni` | +0.035490 | -0.042446 | +0.008496 | +0.035490 | -0.048834 | — | +0.025132 |

### `#006` (chic-v5 proposed: glide; L1=glide, L2=stop, L3-eteo=glide; reclassification: **tier-3-corroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.004862 | -0.013407 | +0.004862 | +0.000802 | +0.000614 | — | -0.004399 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.004646 | -0.022523 | +0.003700 | +0.004646 | -0.008529 | — | — |
| toponym | `basque.json` | stop | `de` | +0.008898 | -0.013407 | +0.008898 | +0.000802 | -0.003526 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.008725 | -0.009917 | -0.001074 | +0.008004 | -0.012550 | — | +0.008725 |

### `#007` (chic-v5 proposed: vowel; L1=vowel, L2=vowel, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.008414 | -0.009248 | +0.008414 | +0.002935 | +0.001460 | — | -0.009469 |
| etruscan | `etruscan.json` | stop | `te` | +0.009698 | -0.012666 | +0.009698 | +0.009388 | -0.009854 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.008880 | -0.009248 | +0.008880 | +0.002935 | +0.001460 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.007975 | -0.008710 | +0.003279 | +0.007975 | -0.006907 | — | +0.003297 |

### `#008` (chic-v5 proposed: glide; L1=glide, L2=glide, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `me` | +0.005612 | -0.006403 | +0.002096 | +0.005612 | -0.002953 | — | -0.006911 |
| etruscan | `etruscan.json` | nasal | `me` | +0.012653 | -0.014735 | +0.002488 | +0.012653 | -0.009371 | — | — |
| toponym | `basque.json` | nasal | `me` | +0.005612 | -0.006403 | +0.002096 | +0.005612 | -0.002953 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.007788 | -0.003360 | +0.003030 | +0.007788 | -0.004883 | — | +0.004300 |

### `#009` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.006762 | -0.001244 | +0.001502 | +0.006762 | +0.002464 | — | +0.002653 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.018572 | -0.017057 | +0.003012 | +0.018572 | -0.005962 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.006762 | -0.001923 | +0.003064 | +0.006762 | +0.002464 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ni` | +0.007602 | -0.006220 | +0.000449 | +0.007602 | -0.012956 | — | +0.007589 |

### `#011` (chic-v5 proposed: liquid; L1=liquid, L2=liquid, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.014924 | -0.014618 | +0.001758 | +0.014924 | +0.001617 | — | +0.013007 |
| etruscan | `etruscan.json` | nasal | `mu` | +0.013348 | -0.036985 | -0.003660 | +0.013348 | -0.025850 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.014924 | -0.014618 | +0.008744 | +0.014924 | +0.001617 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.028282 | -0.000946 | +0.005239 | +0.024055 | -0.018894 | — | +0.028282 |

### `#017` (chic-v5 proposed: nasal; L1=stop, L2=nasal, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.004742 | -0.007907 | +0.004742 | +0.000815 | +0.003783 | — | -0.006700 |
| etruscan | `etruscan.json` | nasal | `me` | +0.011940 | -0.010012 | +0.005876 | +0.011940 | -0.002656 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.003803 | -0.007907 | +0.003803 | +0.000577 | +0.003783 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.007659 | -0.006065 | +0.004332 | +0.007659 | -0.004350 | — | -0.001484 |

### `#020` (chic-v5 proposed: vowel; L1=vowel, L2=vowel, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `me` | +0.007194 | -0.003586 | +0.005289 | +0.007194 | -0.012892 | — | -0.005765 |
| etruscan | `etruscan.json` | nasal | `me` | +0.017042 | -0.012026 | +0.012534 | +0.017042 | -0.004878 | — | — |
| toponym | `basque.json` | nasal | `me` | +0.007194 | -0.003586 | +0.006497 | +0.007194 | -0.012892 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.005846 | -0.007734 | +0.001998 | +0.005446 | -0.010307 | — | +0.005846 |

### `#021` (chic-v5 proposed: nasal; L1=glide, L2=nasal, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.005516 | -0.002969 | +0.004180 | +0.005516 | +0.000043 | — | -0.005276 |
| etruscan | `etruscan.json` | nasal | `mu` | +0.005675 | -0.000075 | +0.004272 | +0.005675 | -0.004278 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.005516 | -0.002885 | +0.004636 | +0.005516 | +0.000043 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.004903 | -0.000628 | +0.002757 | +0.004903 | -0.001127 | — | +0.004373 |

### `#027` (chic-v5 proposed: glide; L1=glide, L2=glide, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `to` | +0.002524 | -0.002958 | +0.002524 | +0.002210 | -0.000277 | — | -0.000716 |
| etruscan | `etruscan.json` | nasal | `me` | +0.004064 | -0.007568 | +0.000784 | +0.004064 | -0.002950 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.002210 | -0.002958 | +0.001550 | +0.002210 | -0.000277 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.002004 | -0.004076 | +0.000393 | +0.002004 | -0.004439 | — | -0.001395 |

### `#033` (chic-v5 proposed: glide; L1=stop, L2=glide, L3-eteo=glide; reclassification: **tier-3-corroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.001886 | -0.002551 | +0.001321 | +0.000298 | +0.001886 | — | -0.001914 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.002297 | -0.004659 | +0.002261 | +0.002297 | -0.001532 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.001886 | -0.002719 | +0.001321 | +0.000298 | +0.001886 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.001566 | -0.003163 | +0.001159 | +0.000437 | -0.002582 | — | +0.001566 |

### `#037` (chic-v5 proposed: liquid; L1=liquid, L2=liquid, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.001567 | -0.002842 | +0.000445 | +0.001567 | -0.003905 | — | +0.000354 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.006042 | -0.007634 | +0.002814 | +0.006042 | -0.004267 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.001911 | -0.002842 | +0.001032 | +0.001911 | -0.003489 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.004025 | -0.003930 | +0.002626 | +0.003860 | -0.004738 | — | +0.004025 |

### `#039` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | glide | `ja` | +0.004402 | -0.004515 | +0.002006 | +0.003402 | -0.003860 | — | +0.004402 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.009867 | -0.019355 | +0.001457 | +0.009867 | -0.001340 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.004082 | -0.005093 | +0.004082 | +0.003402 | -0.003860 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.007269 | -0.007746 | -0.000122 | +0.007269 | -0.003282 | — | -0.006241 |

### `#040` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=liquid; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.019758 | -0.017715 | +0.015397 | +0.011614 | +0.019758 | — | -0.006840 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.020407 | -0.027164 | +0.004975 | +0.020407 | +0.011271 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.019758 | -0.017715 | +0.010739 | +0.006498 | +0.019758 | — | — |
| eteocretan | `eteocretan.json` | liquid | `ra` | +0.018450 | -0.011623 | +0.000545 | +0.010590 | +0.018450 | — | +0.014980 |

### `#043` (chic-v5 proposed: liquid; L1=liquid, L2=liquid, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.004418 | -0.002590 | +0.004418 | +0.004210 | -0.002569 | — | -0.000133 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.009438 | -0.008261 | +0.005821 | +0.009438 | -0.007028 | — | — |
| toponym | `basque.json` | stop | `de` | +0.005258 | -0.003843 | +0.005258 | +0.004210 | -0.002569 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.007414 | -0.001799 | +0.005576 | +0.006070 | -0.007134 | — | +0.007414 |

### `#045` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.002285 | -0.002307 | +0.000996 | +0.002285 | +0.000709 | — | -0.002128 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.005145 | -0.004480 | +0.002133 | +0.005145 | +0.000724 | — | — |
| toponym | `basque.json` | nasal | `ni` | +0.001040 | -0.002307 | +0.000996 | +0.001040 | +0.000709 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.001293 | -0.003016 | +0.000821 | +0.001293 | -0.001406 | — | -0.001411 |

### `#050` (chic-v5 proposed: glide; L1=glide, L2=stop, L3-eteo=glide; reclassification: **tier-3-corroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `mu` | +0.014867 | -0.021269 | +0.002376 | +0.014867 | -0.009318 | — | +0.003087 |
| etruscan | `etruscan.json` | nasal | `mu` | +0.030422 | -0.039581 | +0.027371 | +0.030422 | +0.010721 | — | — |
| toponym | `basque.json` | nasal | `mu` | +0.014867 | -0.023639 | +0.010840 | +0.014867 | -0.009318 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.028860 | -0.020568 | +0.014730 | +0.023199 | -0.018963 | — | +0.028860 |

### `#055` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=glide; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.002354 | -0.002253 | +0.002354 | -0.000746 | -0.006139 | — | -0.000966 |
| etruscan | `etruscan.json` | nasal | `me` | +0.005850 | -0.005700 | +0.003826 | +0.005850 | +0.000525 | — | — |
| toponym | `basque.json` | stop | `de` | +0.002840 | -0.003571 | +0.002840 | +0.001050 | -0.006139 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.002773 | -0.003906 | +0.000907 | +0.001679 | -0.003927 | — | +0.002773 |

### `#056` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.026934 | -0.045930 | +0.013878 | +0.026934 | -0.033453 | — | +0.003744 |
| etruscan | `etruscan.json` | stop | `ta` | +0.041778 | -0.109095 | +0.041778 | +0.034847 | -0.077910 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.014692 | -0.045930 | +0.007756 | +0.014692 | -0.033453 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ni` | +0.021542 | -0.042625 | -0.011274 | +0.021542 | -0.056979 | — | -0.014841 |

### `#058` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.001710 | -0.007553 | +0.001085 | +0.001710 | -0.005166 | — | -0.003200 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.007271 | -0.014111 | +0.000827 | +0.007271 | -0.006814 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.001710 | -0.007553 | +0.001667 | +0.001710 | -0.005166 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.007954 | -0.006797 | +0.000315 | +0.004422 | -0.006634 | — | +0.007954 |

### `#059` (chic-v5 proposed: glide; L1=glide, L2=glide, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `mu` | +0.005913 | -0.006071 | +0.003411 | +0.005913 | -0.004256 | — | -0.001076 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.011400 | -0.007311 | +0.004834 | +0.011400 | -0.010307 | — | — |
| toponym | `basque.json` | nasal | `mu` | +0.005913 | -0.006071 | +0.003357 | +0.005913 | -0.004256 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.006848 | -0.002942 | +0.000090 | +0.006848 | -0.007243 | — | +0.004685 |

### `#060` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.004775 | -0.003585 | +0.003651 | +0.004775 | +0.003699 | — | +0.000592 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.015736 | -0.002713 | +0.005250 | +0.015736 | -0.003033 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.005186 | -0.007460 | +0.004629 | +0.005186 | +0.003699 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.005466 | -0.003354 | +0.001729 | +0.005466 | +0.001239 | — | +0.002824 |

### `#063` (chic-v5 proposed: glide; L1=glide, L2=liquid, L3-eteo=glide; reclassification: **tier-3-corroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.003560 | -0.008778 | +0.003560 | +0.002762 | -0.001516 | — | +0.002183 |
| etruscan | `etruscan.json` | nasal | `me` | +0.008349 | -0.017972 | +0.007269 | +0.008349 | -0.000344 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.004825 | -0.007588 | +0.004825 | +0.002762 | -0.001516 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.009684 | -0.007335 | +0.002777 | +0.003224 | -0.003967 | — | +0.009684 |

### `#065` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `to` | +0.001823 | -0.001357 | +0.001823 | -0.000449 | +0.000883 | — | -0.001613 |
| etruscan | `etruscan.json` | nasal | `mu` | +0.001981 | -0.001855 | +0.000751 | +0.001981 | -0.002115 | — | — |
| toponym | `basque.json` | stop | `to` | +0.001511 | -0.001357 | +0.001511 | -0.000449 | +0.000883 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.001359 | -0.001268 | +0.000293 | +0.001359 | -0.001104 | — | +0.001000 |

### `#066` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=nasal; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.002460 | -0.003234 | +0.001428 | +0.001866 | +0.002460 | — | -0.002620 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.004855 | -0.003325 | +0.001178 | +0.004855 | -0.000043 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.002460 | -0.003234 | +0.001428 | +0.001866 | +0.002460 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.003152 | -0.002228 | +0.000444 | +0.003152 | +0.000459 | — | +0.002164 |

### `#069` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ro` | +0.004981 | -0.002916 | +0.002406 | +0.001896 | +0.004981 | — | -0.005986 |
| etruscan | `etruscan.json` | nasal | `mu` | +0.005395 | -0.008069 | +0.003475 | +0.005395 | +0.001939 | — | — |
| toponym | `basque.json` | liquid | `ro` | +0.004981 | -0.004921 | +0.002617 | +0.001896 | +0.004981 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.003288 | -0.006283 | +0.002601 | +0.002726 | +0.000611 | — | +0.003288 |

### `#072` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=glide; reclassification: **tier-2-equivalent**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.002013 | -0.002876 | +0.001424 | +0.002013 | -0.004017 | — | -0.000073 |
| etruscan | `etruscan.json` | stop | `ke` | +0.006089 | -0.008724 | +0.006089 | +0.005944 | -0.006655 | — | — |
| toponym | `basque.json` | stop | `ki` | +0.002594 | -0.002876 | +0.002594 | +0.001976 | -0.004017 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.009021 | -0.001518 | -0.000885 | +0.004359 | -0.003105 | — | +0.009021 |

### `#078` (chic-v5 proposed: stop; L1=stop, L2=stop, L3-eteo=glide; reclassification: **tier-3-uncorroborated**)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.000515 | -0.001907 | +0.000257 | +0.000515 | -0.002271 | — | -0.000682 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.001949 | -0.003856 | +0.001471 | +0.001949 | -0.004242 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.000515 | -0.001826 | -0.000052 | +0.000515 | -0.002271 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.001260 | -0.002070 | -0.000738 | +0.001047 | -0.003159 | — | +0.001260 |

## Within-window context inspection

**`tier-2-equivalent` count = 8 > 5; per the chic-v12 brief, the context inspection is bailed and the scale signal is surfaced instead.** A reclassification rate this large across the tier-3 set is itself a methodologically interesting observation: it would imply the cross-pool L3 axis is systematically more permissive than the Eteocretan-only L3 chic-v5 used, and that the tier-3 cutoff was conservative rather than exact. Pre-registered next step: a chic-v13 ticket that runs the same context inspection on a stratified sample of the 8 candidates and re-evaluates the per-candidate evidence weighting under the cross-pool L3 axis. Out of chic-v12's polecat budget.

## Discipline notes

- **Cross-pool L3 corroboration is a partial defence, not a positive validation** (chic-v11 framing carried over). chic-v9's leave-one-out test places the chic-v5 framework's mechanical recovery on known anchor classes at 20.0% aggregate / 0/3 on the tier-2 unanimity criterion when run blind. A `tier-2-equivalent` reclassification under chic-v12 means the candidate has the same evidence structure as `#032` (three independent lines + ≥ 1 non-Eteocretan substrate-LM corroboration), but the framework's framework-level validation accuracy is unchanged. Specialist review remains the load-bearing next step for any candidate.
- **The chic-v9 framework-level negative is unaffected.** chic-v12 is an axis-restricted re-test of L3 only on the tier-3 set; L1+L2 (distributional fingerprint) are not re-run. Even an all-3-non-Eteocretan-LMs-corroborate L3 verdict here does not lift the framework's chic-v9 LOO accuracy from 20.0% / 0/3 tier-2 correct.
- **No paleographic L4 work.** Line 4 (cross-script paleographic) is silent for all 76 unknowns in chic-v5 by construction (documented limitation; the chic-v1 PALEOGRAPHIC_CANDIDATES list is precisely the seed for the chic-v2 anchor pool). chic-v12 does not attempt to fill it; that is out of polecat scope.
- **`tier-3-corroborated` is a chic-v12 baseline-state label, not a positive verdict.** For the 6 L1+L2-disagree tier-3 candidates (#006, #017, #021, #033, #050, #063), the chic-v5 consensus class is precisely the class L1-or-L2 + Eteocretan-L3 agree on, so Eteocretan-L3 corroborating the chic-v5 proposed class is true by construction (just like cross-pool L3 stop on `#032` corroborating the chic-v5 stop class). The `tier-3-corroborated` band catches them as the inherited chic-v5 state and contrasts with `tier-2-equivalent` where additional non-Eteocretan substrate-LM corroboration is added.
- **`tier-3-uncorroborated` is the structurally expected verdict for the L1+L2-agree tier-3 majority** if the cross-pool L3 axis behaves like Eteocretan-L3 (which by chic-v5 construction disagrees with L1+L2 for these 23 candidates). A non-zero `tier-2-equivalent` count would indicate the cross-pool L3 axis is qualitatively different from Eteocretan-L3 for at least some tier-3 candidates.

## Determinism

- No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-keyed permutation construction.
- Same (CHIC syllabographic stream, chic-v2 anchor mapping, substrate-pool yamls, LM artifacts) → byte-identical output.

## Build provenance

- Generated by `scripts/build_chic_v12.py` (mg-2035).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs: `corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); `pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; `harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* Amsterdam: J. C. Gieben.
- Trask, R. L. (1997). *The History of Basque.* London: Routledge.
- Bonfante, G. & Bonfante, L. (2002). *The Etruscan Language: An Introduction* (revised ed.). Manchester / New York.
- Beekes, R. S. P. (2010). *Etymological Dictionary of Greek*, vol. 2 appendix on Pre-Greek substrate. Leiden: Brill.
