# CHIC anchor-distance map for unknown syllabographic signs (chic-v5; mg-7c6d)

Per-unknown-sign top-3 nearest anchors by mean Bhattacharyya coefficient over four fingerprint dimensions (`left_neighbor`, `right_neighbor`, `position`, `support`). Each anchor proposes its phoneme class for the unknown sign. This is the input to lines 1 (distributional plurality vote) and 2 (anchor-distance / strict top-1) of the chic-v5 four-line evidence framework.

Distance is computed as 1 − BC; the table reports BC directly (higher = more distributionally similar).

## Coverage

- Unknown syllabographic signs (chic-v1 syllabographic minus chic-v2 anchor pool): **76**
- Unknowns with ≥1 fingerprint occurrence: **76**

## Per-sign top-3 nearest anchors

| sign | freq | top-1 anchor / value / class / BC | top-2 anchor / value / class / BC | top-3 anchor / value / class / BC |
|---|---:|---|---|---|
| `#001` | 4 | `#057` / `je` / glide / 0.5533 | `#070` / `ra` / liquid / 0.4941 | `#061` / `te` / stop / 0.4779 |
| `#002` | 7 | `#070` / `ra` / liquid / 0.5825 | `#054` / `mu` / nasal / 0.5435 | `#049` / `de` / stop / 0.5377 |
| `#003` | 4 | `#013` / `pa` / stop / 0.5056 | `#041` / `ni` / nasal / 0.4530 | `#031` / `ro` / liquid / 0.4363 |
| `#004` | 3 | `#061` / `te` / stop / 0.5619 | `#070` / `ra` / liquid / 0.5449 | `#016` / `a` / vowel / 0.5116 |
| `#005` | 48 | `#049` / `de` / stop / 0.8453 | `#031` / `ro` / liquid / 0.6974 | `#061` / `te` / stop / 0.6316 |
| `#006` | 13 | `#049` / `de` / stop / 0.7219 | `#057` / `je` / glide / 0.7053 | `#031` / `ro` / liquid / 0.6988 |
| `#007` | 8 | `#016` / `a` / vowel / 0.6511 | `#038` / `i` / vowel / 0.6273 | `#010` / `ja` / glide / 0.6032 |
| `#008` | 7 | `#042` / `wa` / glide / 0.7201 | `#053` / `me` / nasal / 0.6434 | `#016` / `a` / vowel / 0.6315 |
| `#009` | 10 | `#013` / `pa` / stop / 0.6274 | `#019` / `ke` / stop / 0.5992 | `#053` / `me` / nasal / 0.5979 |
| `#011` | 24 | `#070` / `ra` / liquid / 0.7126 | `#028` / `ti` / stop / 0.7121 | `#031` / `ro` / liquid / 0.6947 |
| `#012` | 5 | `#042` / `wa` / glide / 0.6611 | `#038` / `i` / vowel / 0.6529 | `#044` / `ki` / stop / 0.6298 |
| `#014` | 4 | `#031` / `ro` / liquid / 0.5377 | `#025` / `ta` / stop / 0.5186 | `#049` / `de` / stop / 0.5170 |
| `#015` | 1 | `#016` / `a` / vowel / 0.4296 | `#025` / `ta` / stop / 0.4259 | `#061` / `te` / stop / 0.3918 |
| `#017` | 6 | `#077` / `ma` / nasal / 0.6771 | `#013` / `pa` / stop / 0.6723 | `#019` / `ke` / stop / 0.6718 |
| `#018` | 12 | `#038` / `i` / vowel / 0.6381 | `#092` / `ke` / stop / 0.6350 | `#044` / `ki` / stop / 0.6110 |
| `#020` | 9 | `#016` / `a` / vowel / 0.6632 | `#049` / `de` / stop / 0.6614 | `#038` / `i` / vowel / 0.6561 |
| `#021` | 3 | `#054` / `mu` / nasal / 0.5354 | `#019` / `ke` / stop / 0.4711 | `#010` / `ja` / glide / 0.4275 |
| `#022` | 1 | `#042` / `wa` / glide / 0.4934 | `#028` / `ti` / stop / 0.4054 | `#044` / `ki` / stop / 0.3795 |
| `#023` | 12 | `#070` / `ra` / liquid / 0.6671 | `#061` / `te` / stop / 0.6404 | `#013` / `pa` / stop / 0.6282 |
| `#024` | 1 | `#031` / `ro` / liquid / 0.3936 | `#016` / `a` / vowel / 0.3156 | `#077` / `ma` / nasal / 0.3101 |
| `#026` | 1 | `#054` / `mu` / nasal / 0.4603 | `#070` / `ra` / liquid / 0.4270 | `#057` / `je` / glide / 0.3953 |
| `#027` | 3 | `#057` / `je` / glide / 0.6351 | `#028` / `ti` / stop / 0.6180 | `#070` / `ra` / liquid / 0.6156 |
| `#029` | 18 | `#049` / `de` / stop / 0.7028 | `#070` / `ra` / liquid / 0.7017 | `#038` / `i` / vowel / 0.6938 |
| `#030` | 1 | `#042` / `wa` / glide / 0.5265 | `#053` / `me` / nasal / 0.4994 | `#057` / `je` / glide / 0.4936 |
| `#032` | 9 | `#061` / `te` / stop / 0.6021 | `#013` / `pa` / stop / 0.5765 | `#070` / `ra` / liquid / 0.5740 |
| `#033` | 3 | `#057` / `je` / glide / 0.5559 | `#061` / `te` / stop / 0.5532 | `#044` / `ki` / stop / 0.5374 |
| `#034` | 41 | `#013` / `pa` / stop / 0.7182 | `#038` / `i` / vowel / 0.7121 | `#031` / `ro` / liquid / 0.6932 |
| `#035` | 2 | `#053` / `me` / nasal / 0.5571 | `#061` / `te` / stop / 0.5314 | `#042` / `wa` / glide / 0.5228 |
| `#036` | 28 | `#038` / `i` / vowel / 0.6960 | `#057` / `je` / glide / 0.6593 | `#044` / `ki` / stop / 0.6585 |
| `#037` | 3 | `#070` / `ra` / liquid / 0.5832 | `#061` / `te` / stop / 0.5402 | `#041` / `ni` / nasal / 0.5284 |
| `#039` | 7 | `#049` / `de` / stop / 0.6490 | `#031` / `ro` / liquid / 0.6457 | `#019` / `ke` / stop / 0.6405 |
| `#040` | 17 | `#049` / `de` / stop / 0.7174 | `#061` / `te` / stop / 0.6923 | `#019` / `ke` / stop / 0.6841 |
| `#043` | 6 | `#031` / `ro` / liquid / 0.5973 | `#010` / `ja` / glide / 0.5964 | `#070` / `ra` / liquid / 0.5622 |
| `#045` | 4 | `#061` / `te` / stop / 0.6130 | `#049` / `de` / stop / 0.6047 | `#019` / `ke` / stop / 0.5914 |
| `#046` | 10 | `#031` / `ro` / liquid / 0.6710 | `#049` / `de` / stop / 0.6613 | `#019` / `ke` / stop / 0.6591 |
| `#047` | 19 | `#070` / `ra` / liquid / 0.7609 | `#061` / `te` / stop / 0.7218 | `#028` / `ti` / stop / 0.7127 |
| `#048` | 1 | `#031` / `ro` / liquid / 0.5598 | `#025` / `ta` / stop / 0.5191 | `#061` / `te` / stop / 0.5160 |
| `#050` | 23 | `#049` / `de` / stop / 0.7246 | `#038` / `i` / vowel / 0.7237 | `#042` / `wa` / glide / 0.7173 |
| `#051` | 9 | `#016` / `a` / vowel / 0.6069 | `#070` / `ra` / liquid / 0.6055 | `#061` / `te` / stop / 0.5944 |
| `#052` | 10 | `#038` / `i` / vowel / 0.6353 | `#031` / `ro` / liquid / 0.6276 | `#019` / `ke` / stop / 0.6114 |
| `#055` | 5 | `#028` / `ti` / stop / 0.6565 | `#061` / `te` / stop / 0.6447 | `#070` / `ra` / liquid / 0.6228 |
| `#056` | 52 | `#019` / `ke` / stop / 0.7874 | `#070` / `ra` / liquid / 0.7698 | `#049` / `de` / stop / 0.7527 |
| `#058` | 5 | `#061` / `te` / stop / 0.6360 | `#031` / `ro` / liquid / 0.6354 | `#092` / `ke` / stop / 0.6222 |
| `#059` | 5 | `#010` / `ja` / glide / 0.5764 | `#070` / `ra` / liquid / 0.5656 | `#025` / `ta` / stop / 0.5626 |
| `#060` | 8 | `#028` / `ti` / stop / 0.6923 | `#061` / `te` / stop / 0.6719 | `#070` / `ra` / liquid / 0.6593 |
| `#062` | 11 | `#038` / `i` / vowel / 0.6690 | `#042` / `wa` / glide / 0.6515 | `#025` / `ta` / stop / 0.6226 |
| `#063` | 7 | `#070` / `ra` / liquid / 0.5904 | `#042` / `wa` / glide / 0.5744 | `#061` / `te` / stop / 0.5725 |
| `#064` | 2 | `#041` / `ni` / nasal / 0.4607 | `#016` / `a` / vowel / 0.4466 | `#042` / `wa` / glide / 0.4460 |
| `#065` | 3 | `#049` / `de` / stop / 0.5527 | `#042` / `wa` / glide / 0.5275 | `#044` / `ki` / stop / 0.5217 |
| `#066` | 3 | `#049` / `de` / stop / 0.5622 | `#028` / `ti` / stop / 0.5479 | `#031` / `ro` / liquid / 0.5441 |
| `#067` | 1 | `#092` / `ke` / stop / 0.3338 | `#031` / `ro` / liquid / 0.3275 | `#073` / `to` / stop / 0.3055 |
| `#068` | 10 | `#038` / `i` / vowel / 0.6977 | `#019` / `ke` / stop / 0.6286 | `#070` / `ra` / liquid / 0.6277 |
| `#069` | 3 | `#013` / `pa` / stop / 0.5871 | `#019` / `ke` / stop / 0.5792 | `#070` / `ra` / liquid / 0.5626 |
| `#071` | 2 | `#042` / `wa` / glide / 0.3907 | `#028` / `ti` / stop / 0.3806 | `#013` / `pa` / stop / 0.3724 |
| `#072` | 7 | `#028` / `ti` / stop / 0.7281 | `#044` / `ki` / stop / 0.6568 | `#042` / `wa` / glide / 0.6316 |
| `#074` | 1 | `#057` / `je` / glide / 0.3340 | `#070` / `ra` / liquid / 0.3278 | `#049` / `de` / stop / 0.3273 |
| `#075` | 1 | `#061` / `te` / stop / 0.3152 | `#070` / `ra` / liquid / 0.2755 | `#057` / `je` / glide / 0.2604 |
| `#076` | 3 | `#031` / `ro` / liquid / 0.5525 | `#010` / `ja` / glide / 0.5250 | `#044` / `ki` / stop / 0.4653 |
| `#078` | 3 | `#028` / `ti` / stop / 0.5310 | `#042` / `wa` / glide / 0.5011 | `#061` / `te` / stop / 0.4953 |
| `#079` | 1 | `#028` / `ti` / stop / 0.3429 | `#042` / `wa` / glide / 0.3267 | `#038` / `i` / vowel / 0.3191 |
| `#080` | 2 | `#041` / `ni` / nasal / 0.5096 | `#038` / `i` / vowel / 0.5084 | `#044` / `ki` / stop / 0.4947 |
| `#081` | 1 | `#070` / `ra` / liquid / 0.3964 | `#061` / `te` / stop / 0.3918 | `#016` / `a` / vowel / 0.3737 |
| `#082` | 1 | `#061` / `te` / stop / 0.4318 | `#041` / `ni` / nasal / 0.4198 | `#070` / `ra` / liquid / 0.3964 |
| `#083` | 1 | `#042` / `wa` / glide / 0.4797 | `#028` / `ti` / stop / 0.4054 | `#053` / `me` / nasal / 0.4049 |
| `#084` | 1 | `#019` / `ke` / stop / 0.2898 | `#013` / `pa` / stop / 0.2548 | `#016` / `a` / vowel / 0.2447 |
| `#085` | 2 | `#041` / `ni` / nasal / 0.4621 | `#013` / `pa` / stop / 0.4545 | `#070` / `ra` / liquid / 0.4481 |
| `#087` | 1 | `#042` / `wa` / glide / 0.3025 | `#028` / `ti` / stop / 0.2988 | `#073` / `to` / stop / 0.2699 |
| `#088` | 2 | `#028` / `ti` / stop / 0.4686 | `#042` / `wa` / glide / 0.4588 | `#057` / `je` / glide / 0.3907 |
| `#089` | 1 | `#073` / `to` / stop / 0.4173 | `#013` / `pa` / stop / 0.3528 | `#049` / `de` / stop / 0.3376 |
| `#090` | 1 | `#073` / `to` / stop / 0.4173 | `#070` / `ra` / liquid / 0.3278 | `#013` / `pa` / stop / 0.3085 |
| `#091` | 1 | `#019` / `ke` / stop / 0.4278 | `#041` / `ni` / nasal / 0.4198 | `#049` / `de` / stop / 0.4006 |
| `#093` | 1 | `#070` / `ra` / liquid / 0.2046 | `#061` / `te` / stop / 0.1951 | `#041` / `ni` / nasal / 0.1928 |
| `#094` | 3 | `#019` / `ke` / stop / 0.6177 | `#038` / `i` / vowel / 0.6076 | `#031` / `ro` / liquid / 0.6035 |
| `#095` | 6 | `#019` / `ke` / stop / 0.4875 | `#038` / `i` / vowel / 0.4663 | `#010` / `ja` / glide / 0.4597 |
| `#096` | 1 | `#041` / `ni` / nasal / 0.3817 | `#016` / `a` / vowel / 0.3697 | `#049` / `de` / stop / 0.3609 |
| `#100` | 1 | `#028` / `ti` / stop / 0.3429 | `#042` / `wa` / glide / 0.3267 | `#054` / `mu` / nasal / 0.3178 |

## Methodology notes

- Fingerprint dimensions are computed over the full CHIC corpus (`corpora/cretan_hieroglyphic/all.jsonl`, chic-v0): `left_neighbor` and `right_neighbor` count adjacent sign IDs in the sign-only sequence (DIV / `[?]` are skipped); `position` buckets per-sign occurrences into start/middle/end/single thirds of the sign-only block (chic-v1 convention); `support` is the inscription support type histogram.
- Bhattacharyya coefficient is computed per dimension over the union of observed keys, after L1-normalizing each side to a probability distribution. The four per-dimension BCs are averaged to produce the final similarity score.
- An unknown sign with no fingerprint occurrences (frequency = 0) is omitted; this only happens for syllabographic signs whose every corpus occurrence is an uncertain reading collapsed to [?] without a `[?:#NNN]` annotation, which doesn't occur in the current CHIC corpus.
- Anchor-distance is symmetric and absolute; we do not normalize by the anchor's own self-similarity (which is always 1.0 by construction).
