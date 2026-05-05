# CHIC chic-v6 verification match rates (mg-a557)

Mechanical verification-rate report for chic-v5 candidate proposals, per the chic-v6 brief. Built by `scripts/build_chic_v6.py`. Discipline note: this is a verification-rate report against three external-scholarship sources, NOT a decipherment claim. Specialist judgment is still required to advance any matched candidate from `matched` to `decipherment`.

## Pre-registered match criteria

Match criteria fixed BEFORE computing match counts (per the chic-v6 brief, to prevent post-hoc relaxation). They are preserved verbatim in the `scripts/build_chic_v6.py` module-level docstring; the abbreviated form below mirrors the script.

- **Source A — scholar-proposed Linear-A reading match.** A scholar entry's `ab_sequence` (length k) matches a CHIC inscription iff there exists a contiguous run of k syllabographic-class tokens within a single DIV-bounded segment of the inscription such that for each position i: (a) the token is a tier-1/2 anchored sign whose literal first-phoneme equals the scholar's `scholarly_first_phoneme[i]`, OR (b) the token is a tier-3/4 class placeholder whose class equals `classify_value(scholarly_first_phoneme[i])`. All k positions must match.
- **Source B — toponym substring match.** For every toponym surface in `pools/toponym.yaml`, generate substrings of length L ∈ [3, 5]. Match in a single DIV-bounded phoneme stream, char-by-char: literal char matches by string equality; class-onset slot matches if the target char is in that class's consonant set; vowel slot matches if the target char is a vowel.
- **Source C — item-location consistency.** Per-inscription `site` field, lowercased (alphabetical chars only). Generate substrings of length 3–5 from the site surface; apply the source-B match procedure but only against the inscription's own phoneme stream and only against substrings of its own site name.

## Class → consonant set

| class | consonants |
|---|---|
| vowel | `aeiou` |
| stop | `bdgkpqt` |
| nasal | `mn` |
| liquid | `lr` |
| fricative | `fhsxz` |
| glide | `jwy` |

## Per-tier match-rate table

Inputs: 302 CHIC inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| tier | n_inscriptions | n_with_any_match | match_rate_any | n_with_a | n_with_b | n_with_c | total_a | total_b | total_c |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| tier-1 | 302 | 67 | 0.2219 | 30 | 48 | 0 | 216 | 74 | 0 |
| tier-2 | 302 | 70 | 0.2318 | 31 | 51 | 0 | 233 | 77 | 0 |
| tier-3 | 302 | 161 | 0.5331 | 96 | 154 | 12 | 828 | 1803 | 18 |
| tier-4 | 302 | 207 | 0.6854 | 111 | 202 | 23 | 1019 | 3957 | 40 |

## Tier-over-tier verification lift

The `lift` from tier-(N-1) to tier-N is the difference in `n_inscriptions_with_any_match`. A positive lift means the tier-N extension produced verification matches not attainable under tier-(N-1).

| from | to | lift (n_inscriptions_with_any_match) | lift (total a+b+c hits) |
|---|---|--:|--:|
| tier-1 | tier-2 | +3 | +20 |
| tier-2 | tier-3 | +91 | +2339 |
| tier-3 | tier-4 | +46 | +2367 |

## Per-match enumeration (tier-4, the maximally extended tier)

For each verified match at tier-4 (the strict superset of all earlier tiers), the inscription, source, matched signs, and matched substring/scholar reading are listed. This enumeration provides the concrete list of candidate-with-external-verification cases; specialist judgment is still required to elevate any of these from matched to decipherment.

### Source A enumeration (scholar-proposed reading hits)

| CHIC id | Site | Tier-4 reading (excerpt) | Scholar entry | Phonemes | AB-sequence | Matched CHIC signs | Match modes |
|---|---|---|---|---|---|---|---|
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #068` | class/class |
| CHIC #002 | Knossos | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #068` | class/class |
| CHIC #008 | Knossos | `ti i ki [?]` | tai_HT123a | `ta i` | `AB59 AB28` | `#028 #038` | literal/literal |
| CHIC #008 | Knossos | `ti i ki [?]` | tai_HT39 | `ta i` | `AB59 AB28` | `#028 #038` | literal/literal |
| CHIC #009 | Knossos | `[?:STOP:#065] [GLIDE:#063]` | paja_HT154A | `pa ja` | `AB03 AB57` | `#065 #063` | class/class |
| CHIC #009 | Knossos | `[?:STOP:#065] [GLIDE:#063]` | paja_HT29 | `pa ja` | `AB03 AB57` | `#065 #063` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | ara_ARKH1a | `a ra` | `AB08 AB60` | `#020 #047` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | ara_HT1 | `a ra` | `AB08 AB60` | `#020 #047` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#009 #056` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #018 | Knossos | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #021 | Knossos | `i [NASAL:#017] de [LIQUID:#034] / IDEO:#153` | dare_HT10a | `da re` | `AB01 AB27` | `#049 #034` | literal/class |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | dare_HT10a | `da re` | `AB01 AB27` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#055 #070` | class/literal |
| CHIC #022 | Knossos | `[STOP:#055] ra de [?] / [?] [?:ro]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#055 #070` | class/literal |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | dare_HT10a | `da re` | `AB01 AB27` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#045 #029` | class/class |
| CHIC #023 | Knossos | `wa [?:STOP:#045] [LIQUID:#029]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#045 #029` | class/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #055` | literal/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #055` | literal/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #055` | literal/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | dare_HT10a | `da re` | `AB01 AB27` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #055` | literal/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #055` | literal/class |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#060 #070` | class/literal |
| CHIC #029 | Knossos | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#060 #070` | class/literal |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #052` | class/class |
| CHIC #031 | Knossos | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #052` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #047` | class/class |
| CHIC #032 | Knossos | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #047` | class/class |
| CHIC #034 | Knossos | `mu te pa / [?] / [?] / [STOP:#072] de / NUM:10` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #034 | Knossos | `mu te pa / [?] / [?] / [STOP:#072] de / NUM:10` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #037 | Knossos | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #037 | Knossos | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` | mate_HT52a | `ma te` | `AB80 AB04` | `#017 #039` | class/class |
| CHIC #037 | Knossos | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #037 | Knossos | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` | mate_PH15a | `ma te` | `AB80 AB04` | `#017 #039` | class/class |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kira_HT103 | `ki ra` | `AB67 AB60` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | dare_HT10a | `da re` | `AB01 AB27` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | karu_HT2 | `ka ru` | `AB77 AB26` | `#069 #070` | class/literal |
| CHIC #038 | Knossos | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` | kira_HT85b | `ki ra` | `AB67 AB60` | `#069 #070` | class/literal |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #023` | class/class |
| CHIC #039 | Knossos | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #023` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#072 #039` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#072 #039` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#072 #039` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#072 #039` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#072 #039` | class/class |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #070` | literal/literal |
| CHIC #040 | Knossos | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LI...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #070` | literal/literal |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kira_HT103 | `ki ra` | `AB67 AB60` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | dare_HT10a | `da re` | `AB01 AB27` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | karu_HT2 | `ka ru` | `AB77 AB26` | `#069 #047` | class/class |
| CHIC #041 | Knossos | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` | kira_HT85b | `ki ra` | `AB67 AB60` | `#069 #047` | class/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #023` | literal/class |
| CHIC #046 | Knossos | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #023` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #040` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #040` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #040` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | dare_HT10a | `da re` | `AB01 AB27` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #040` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #040` | literal/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#040 #004` | class/class |
| CHIC #049 | Knossos | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#040 #004` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | dare_HT10a | `da re` | `AB01 AB27` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | dare_HT10a | `da re` | `AB01 AB27` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#058 #002` | class/class |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | dina_HT25a | `di na` | `AB07 AB06` | `#049 #041` | literal/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#058 #031` | class/literal |
| CHIC #053 | Knossos | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#16...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#058 #002` | class/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#032 #013` | literal/literal |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#032 #013` | literal/literal |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#032 #013` | literal/literal |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#032 #013` | literal/literal |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#032 #013` | literal/literal |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#032 #011` | literal/class |
| CHIC #057 | Knossos | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#032 #011` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | tai_HT123a | `ta i` | `AB59 AB28` | `#028 #038` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | tai_HT39 | `ta i` | `AB59 AB28` | `#028 #038` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#032 #034` | literal/class |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#032 #070` | literal/literal |
| CHIC #058 | Knossos | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#0...` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#060 #013` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#060 #013` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#060 #013` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | dare_HT10a | `da re` | `AB01 AB27` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#060 #013` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#060 #013` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | mate_HT52a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#066 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #059 | Knossos | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] ...` | mate_PH15a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #060 | Knossos | `ti de ni [GLIDE:#003] [?] / [?:STOP:#009] mu te [?]` | dina_HT25a | `di na` | `AB07 AB06` | `#049 #041` | literal/literal |
| CHIC #060 | Knossos | `ti de ni [GLIDE:#003] [?] / [?:STOP:#009] mu te [?]` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #060 | Knossos | `ti de ni [GLIDE:#003] [?] / [?:STOP:#009] mu te [?]` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #009` | literal/class |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #009` | literal/class |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #009` | literal/class |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #009` | literal/class |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #009` | literal/class |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #031` | class/literal |
| CHIC #061 | Knossos | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [S...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #062 | Knossos | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM...` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#005 #063` | class/class |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#005 #063` | class/class |
| CHIC #065 | Knossos | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #066 | Knossos | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:STOP:#005] [GLIDE:#063] / NUM:1 / [?:I...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#005 #063` | class/class |
| CHIC #066 | Knossos | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:STOP:#005] [GLIDE:#063] / NUM:1 / [?:I...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#005 #063` | class/class |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #067 | Knossos | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #071 | Mallia | `#022 [STOP:#056] ra te` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #075 | Mallia | `[STOP:#060] [STOP:#009]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#060 #009` | class/class |
| CHIC #075 | Mallia | `[STOP:#060] [STOP:#009]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#060 #009` | class/class |
| CHIC #075 | Mallia | `[STOP:#060] [STOP:#009]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#060 #009` | class/class |
| CHIC #075 | Mallia | `[STOP:#060] [STOP:#009]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#060 #009` | class/class |
| CHIC #075 | Mallia | `[STOP:#060] [STOP:#009]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#060 #009` | class/class |
| CHIC #076 | Mallia | `[GLIDE:#008] [STOP:#056] pa` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#056 #013` | class/literal |
| CHIC #076 | Mallia | `[GLIDE:#008] [STOP:#056] pa` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#056 #013` | class/literal |
| CHIC #076 | Mallia | `[GLIDE:#008] [STOP:#056] pa` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#056 #013` | class/literal |
| CHIC #076 | Mallia | `[GLIDE:#008] [STOP:#056] pa` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#056 #013` | class/literal |
| CHIC #076 | Mallia | `[GLIDE:#008] [STOP:#056] pa` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#056 #013` | class/literal |
| CHIC #089 | Mallia | `ki de [LIQUID:#023] / [LIQUID:#034] ni #084 / [GLIDE:#051] [GLIDE:#051] [GLID...` | dare_HT10a | `da re` | `AB01 AB27` | `#049 #023` | literal/class |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kira_HT103 | `ki ra` | `AB67 AB60` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | dare_HT10a | `da re` | `AB01 AB27` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | karu_HT2 | `ka ru` | `AB77 AB26` | `#040 #070` | class/literal |
| CHIC #097 | Mallia | `NUM:2 / [STOP:#040] ra i` | kira_HT85b | `ki ra` | `AB67 AB60` | `#040 #070` | class/literal |
| CHIC #098 | Mallia | `[?:STOP:#072] i [VOWEL:#007] a` | tai_HT123a | `ta i` | `AB59 AB28` | `#072 #038` | class/literal |
| CHIC #098 | Mallia | `[?:STOP:#072] i [VOWEL:#007] a` | tai_HT39 | `ta i` | `AB59 AB28` | `#072 #038` | class/literal |
| CHIC #103 | Mallia | `[?:ra] [STOP:#055] je [?:STOP:#056] [?] / [?:IDEO:#163] [?]` | paja_HT154A | `pa ja` | `AB03 AB57` | `#055 #057` | class/literal |
| CHIC #103 | Mallia | `[?:ra] [STOP:#055] je [?:STOP:#056] [?] / [?:IDEO:#163] [?]` | paja_HT29 | `pa ja` | `AB03 AB57` | `#055 #057` | class/literal |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#032 #009` | literal/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#032 #009` | literal/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#032 #009` | literal/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#009 #056` | class/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#032 #009` | literal/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#032 #009` | literal/class |
| CHIC #104 | Mallia | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #034` | literal/class |
| CHIC #109 | Mallia | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #034` | literal/class |
| CHIC #110 | Mallia | `ki [STOP:#040] [?] / [?:#085] / [?]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #040` | literal/class |
| CHIC #110 | Mallia | `ki [STOP:#040] [?] / [?:#085] / [?]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #040` | literal/class |
| CHIC #110 | Mallia | `ki [STOP:#040] [?] / [?:#085] / [?]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #040` | literal/class |
| CHIC #110 | Mallia | `ki [STOP:#040] [?] / [?:#085] / [?]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #040` | literal/class |
| CHIC #110 | Mallia | `ki [STOP:#040] [?] / [?:#085] / [?]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #040` | literal/class |
| CHIC #113 | Mallia | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / N...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#040 #013` | class/literal |
| CHIC #113 | Mallia | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / N...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#040 #013` | class/literal |
| CHIC #113 | Mallia | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / N...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#040 #013` | class/literal |
| CHIC #113 | Mallia | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / N...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#040 #013` | class/literal |
| CHIC #113 | Mallia | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / N...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#040 #013` | class/literal |
| CHIC #117 | Mallia | `[?:STOP:#055] [?:VOWEL:#020] [?] / [?:LIQUID:#011] [?:STOP:#040] / [?] / [?] ...` | tai_HT123a | `ta i` | `AB59 AB28` | `#055 #020` | class/class |
| CHIC #117 | Mallia | `[?:STOP:#055] [?:VOWEL:#020] [?] / [?:LIQUID:#011] [?:STOP:#040] / [?] / [?] ...` | tai_HT39 | `ta i` | `AB59 AB28` | `#055 #020` | class/class |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#040 #057` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#040 #057` | class/literal |
| CHIC #118 | Mallia | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #123 | Knossos | `ke [STOP:#058]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#092 #058` | literal/class |
| CHIC #123 | Knossos | `ke [STOP:#058]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#092 #058` | literal/class |
| CHIC #123 | Knossos | `ke [STOP:#058]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#092 #058` | literal/class |
| CHIC #123 | Knossos | `ke [STOP:#058]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#092 #058` | literal/class |
| CHIC #123 | Knossos | `ke [STOP:#058]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#092 #058` | literal/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | dare_HT10a | `da re` | `AB01 AB27` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#040 #029` | class/class |
| CHIC #124 | Knossos | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#040 #029` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#009 #056` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#009 #056` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | paja_HT154A | `pa ja` | `AB03 AB57` | `#056 #062` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#009 #056` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | paja_HT29 | `pa ja` | `AB03 AB57` | `#056 #062` | class/class |
| CHIC #126 | Mallia | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` | pitaja_HT6a | `pi ta ja` | `AB39 AB59 AB57` | `#009 #056 #062` | class/class/class |
| CHIC #128 | Mallia | `[?:GLIDE:#008] me [NASAL:#017] / NUM:0` | mina_HT115a | `mi na` | `AB73 AB06` | `#053 #017` | literal/class |
| CHIC #128 | Mallia | `[?:GLIDE:#008] me [NASAL:#017] / NUM:0` | mina_HT117a | `mi na` | `AB73 AB06` | `#053 #017` | literal/class |
| CHIC #133 | Pyrgos (Myrtos) | `ra ti ni / NUM:0` | tana_ARKH5 | `ta na` | `AB59 AB06` | `#028 #041` | literal/literal |
| CHIC #133 | Pyrgos (Myrtos) | `ra ti ni / NUM:0` | tana_HT108 | `ta na` | `AB59 AB06` | `#028 #041` | literal/literal |
| CHIC #138 | Zakros | `ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #138 | Zakros | `ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #138 | Zakros | `ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #138 | Zakros | `ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #138 | Zakros | `ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #140 | Knossos | `ki pa [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #013` | literal/literal |
| CHIC #140 | Knossos | `ki pa [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #013` | literal/literal |
| CHIC #140 | Knossos | `ki pa [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #013` | literal/literal |
| CHIC #140 | Knossos | `ki pa [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #013` | literal/literal |
| CHIC #140 | Knossos | `ki pa [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #013` | literal/literal |
| CHIC #142 | Knossos | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#039 #005` | class/class |
| CHIC #142 | Knossos | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#039 #005` | class/class |
| CHIC #142 | Knossos | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#039 #005` | class/class |
| CHIC #142 | Knossos | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#039 #005` | class/class |
| CHIC #142 | Knossos | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#039 #005` | class/class |
| CHIC #144 | Knossos | `[?:ki] [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #144 | Knossos | `[?:ki] [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #144 | Knossos | `[?:ki] [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #144 | Knossos | `[?:ki] [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #144 | Knossos | `[?:ki] [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #145 | Knossos | `ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #145 | Knossos | `ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #145 | Knossos | `ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #145 | Knossos | `ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #145 | Knossos | `ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #149 | Mallia | `ro [NASAL:#021] te` | mate_HT52a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #149 | Mallia | `ro [NASAL:#021] te` | mate_PH15a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #158 | Knossos | `ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #158 | Knossos | `ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #158 | Knossos | `ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #158 | Knossos | `ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #158 | Knossos | `ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #160 | Knossos | `[?:ti] [VOWEL:#020] ni` | tai_HT123a | `ta i` | `AB59 AB28` | `#028 #020` | literal/class |
| CHIC #160 | Knossos | `[?:ti] [VOWEL:#020] ni` | tai_HT39 | `ta i` | `AB59 AB28` | `#028 #020` | literal/class |
| CHIC #165 | Knossos | `[?:ki] [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #165 | Knossos | `[?:ki] [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #165 | Knossos | `[?:ki] [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #165 | Knossos | `[?:ki] [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #165 | Knossos | `[?:ki] [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #047` | class/class |
| CHIC #166 | Knossos | `[STOP:#056] [LIQUID:#047] ro` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #047` | class/class |
| CHIC #167 | Knossos | `de ra ra` | dare_HT10a | `da re` | `AB01 AB27` | `#049 #070` | literal/literal |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #065` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#065 #005` | class/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #065` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#065 #005` | class/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #065` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#065 #005` | class/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #065` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#065 #005` | class/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #065` | literal/class |
| CHIC #174 | Palaikastro | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#065 #005` | class/class |
| CHIC #184 | Crete (unprovenanced) | `ki pa ra` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #013` | literal/literal |
| CHIC #184 | Crete (unprovenanced) | `ki pa ra` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #013` | literal/literal |
| CHIC #184 | Crete (unprovenanced) | `ki pa ra` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #013` | literal/literal |
| CHIC #184 | Crete (unprovenanced) | `ki pa ra` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #013` | literal/literal |
| CHIC #184 | Crete (unprovenanced) | `ki pa ra` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #013` | literal/literal |
| CHIC #186 | Kalo Horio | `ti te de [LIQUID:#047] / NUM:0` | dare_HT10a | `da re` | `AB01 AB27` | `#049 #047` | literal/class |
| CHIC #193 | Ziros | `a ke [STOP:#056] / NUM:0` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #056` | literal/class |
| CHIC #193 | Ziros | `a ke [STOP:#056] / NUM:0` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #056` | literal/class |
| CHIC #193 | Ziros | `a ke [STOP:#056] / NUM:0` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #056` | literal/class |
| CHIC #193 | Ziros | `a ke [STOP:#056] / NUM:0` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #056` | literal/class |
| CHIC #193 | Ziros | `a ke [STOP:#056] / NUM:0` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #056` | literal/class |
| CHIC #194 | Crete (unprovenanced) | `ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #194 | Crete (unprovenanced) | `ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #194 | Crete (unprovenanced) | `ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #194 | Crete (unprovenanced) | `ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #194 | Crete (unprovenanced) | `ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #197 | Mallia | `ro [NASAL:#021] te` | mate_HT52a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #197 | Mallia | `ro [NASAL:#021] te` | mate_PH15a | `ma te` | `AB80 AB04` | `#021 #061` | class/literal |
| CHIC #200 | Mallia | `[LIQUID:#029] ni [STOP:#056] i [?:ma]` | tai_HT123a | `ta i` | `AB59 AB28` | `#056 #038` | class/literal |
| CHIC #200 | Mallia | `[LIQUID:#029] ni [STOP:#056] i [?:ma]` | tai_HT39 | `ta i` | `AB59 AB28` | `#056 #038` | class/literal |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | dare_HT10a | `da re` | `AB01 AB27` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#009 #011` | class/class |
| CHIC #225 | Crete (unprovenanced) | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#009 #011` | class/class |
| CHIC #242 | Crete (unprovenanced) | `[STOP:#056] [GLIDE:#059] / i ja ro` | paja_HT154A | `pa ja` | `AB03 AB57` | `#056 #059` | class/class |
| CHIC #242 | Crete (unprovenanced) | `[STOP:#056] [GLIDE:#059] / i ja ro` | paja_HT29 | `pa ja` | `AB03 AB57` | `#056 #059` | class/class |
| CHIC #246 | Kritsa | `ki [STOP:#005] / [GLIDE:#006] ni` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #246 | Kritsa | `ki [STOP:#005] / [GLIDE:#006] ni` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #246 | Kritsa | `ki [STOP:#005] / [GLIDE:#006] ni` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #246 | Kritsa | `ki [STOP:#005] / [GLIDE:#006] ni` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #246 | Kritsa | `ki [STOP:#005] / [GLIDE:#006] ni` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #247 | Mallia | `ki de / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #247 | Mallia | `ki de / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #247 | Mallia | `ki de / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #247 | Mallia | `ki de / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #247 | Mallia | `ki de / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #250 | Zakros | `ki [STOP:#005] / i ja ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #250 | Zakros | `ki [STOP:#005] / i ja ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #250 | Zakros | `ki [STOP:#005] / i ja ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #250 | Zakros | `ki [STOP:#005] / i ja ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #250 | Zakros | `ki [STOP:#005] / i ja ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #253 | Crete (unprovenanced) | `i ja / ki de / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #253 | Crete (unprovenanced) | `i ja / ki de / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #253 | Crete (unprovenanced) | `i ja / ki de / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #253 | Crete (unprovenanced) | `i ja / ki de / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #253 | Crete (unprovenanced) | `i ja / ki de / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #254 | Crete (unprovenanced) | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #255 | Crete (unprovenanced) | `ki [GLIDE:#036] [GLIDE:#018] / ti de wa ro [STOP:#056] [GLIDE:#036] / [GLIDE:...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#056 #036` | class/class |
| CHIC #255 | Crete (unprovenanced) | `ki [GLIDE:#036] [GLIDE:#018] / ti de wa ro [STOP:#056] [GLIDE:#036] / [GLIDE:...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#056 #036` | class/class |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #257 | Crete (unprovenanced) | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #258 | Crete (unprovenanced) | `i ja / [GLIDE:#036] ke ro / ki de` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #259 | Crete (unprovenanced) | `ki de / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #259 | Crete (unprovenanced) | `ki de / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #259 | Crete (unprovenanced) | `ki de / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #259 | Crete (unprovenanced) | `ki de / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #259 | Crete (unprovenanced) | `ki de / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #261 | Crete (unprovenanced) | `ki [STOP:#005] / i ja ro / ki de` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #261 | Crete (unprovenanced) | `ki [STOP:#005] / i ja ro / ki de` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #261 | Crete (unprovenanced) | `ki [STOP:#005] / i ja ro / ki de` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #261 | Crete (unprovenanced) | `ki [STOP:#005] / i ja ro / ki de` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #261 | Crete (unprovenanced) | `ki [STOP:#005] / i ja ro / ki de` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #262 | Crete (unprovenanced) | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #263 | Crete (unprovenanced) | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #263 | Crete (unprovenanced) | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #263 | Crete (unprovenanced) | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #263 | Crete (unprovenanced) | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #263 | Crete (unprovenanced) | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#013 #050` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #264 | Heraklion | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#013 #050` | literal/class |
| CHIC #266 | Kordakia | `ki [STOP:#005] / ki ta de / ki de` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #266 | Kordakia | `ki [STOP:#005] / ki ta de / ki de` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #266 | Kordakia | `ki [STOP:#005] / ki ta de / ki de` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #266 | Kordakia | `ki [STOP:#005] / ki ta de / ki de` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #266 | Kordakia | `ki [STOP:#005] / ki ta de / ki de` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #268 | Lakonia | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #268 | Lakonia | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #268 | Lakonia | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #268 | Lakonia | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #268 | Lakonia | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #271 | Mallia | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #056` | literal/class |
| CHIC #271 | Mallia | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #056` | literal/class |
| CHIC #271 | Mallia | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #056` | literal/class |
| CHIC #271 | Mallia | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #056` | literal/class |
| CHIC #271 | Mallia | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #056` | literal/class |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #272 | Mirabelo | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | paja_HT154A | `pa ja` | `AB03 AB57` | `#005 #050` | class/class |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | paja_HT154A | `pa ja` | `AB03 AB57` | `#005 #050` | class/class |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | paja_HT29 | `pa ja` | `AB03 AB57` | `#005 #050` | class/class |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | paja_HT29 | `pa ja` | `AB03 AB57` | `#005 #050` | class/class |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #005` | literal/class |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #031` | literal/literal |
| CHIC #273 | Mirabelo | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #005` | literal/class |
| CHIC #274 | Mirabelo | `ki de / ki [STOP:#005] / i ja ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #274 | Mirabelo | `ki de / ki [STOP:#005] / i ja ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #274 | Mirabelo | `ki de / ki [STOP:#005] / i ja ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #274 | Mirabelo | `ki de / ki [STOP:#005] / i ja ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #274 | Mirabelo | `ki de / ki [STOP:#005] / i ja ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #013` | literal/literal |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #013` | literal/literal |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #013` | literal/literal |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #013` | literal/literal |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #277 | Ziros | `ki [STOP:#005] / ke ke pa / ki de` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #013` | literal/literal |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#056 #013` | class/literal |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#056 #013` | class/literal |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#056 #013` | class/literal |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#056 #013` | class/literal |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #283 | Crete (unprovenanced) | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#056 #013` | class/literal |
| CHIC #287 | Crete (unprovenanced) | `ki de / ra te [STOP:#069] / ki [STOP:#005]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #287 | Crete (unprovenanced) | `ki de / ra te [STOP:#069] / ki [STOP:#005]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #287 | Crete (unprovenanced) | `ki de / ra te [STOP:#069] / ki [STOP:#005]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #287 | Crete (unprovenanced) | `ki de / ra te [STOP:#069] / ki [STOP:#005]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #287 | Crete (unprovenanced) | `ki de / ra te [STOP:#069] / ki [STOP:#005]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #288 | Mallia | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #288 | Mallia | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #288 | Mallia | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #288 | Mallia | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #288 | Mallia | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#092 #056` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#092 #056` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#092 #056` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#092 #056` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#092 #056` | literal/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #034` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #011` | class/class |
| CHIC #289 | Palaikastro | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #034` | class/class |
| CHIC #293 | Adromili | `[?:ma] i / i ja ro / wa mu te / ki de` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #293 | Adromili | `[?:ma] i / i ja ro / wa mu te / ki de` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #047` | literal/class |
| CHIC #294 | Crete (unprovenanced) | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #047` | literal/class |
| CHIC #295 | Crete (unprovenanced) | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005]...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #295 | Crete (unprovenanced) | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005]...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #295 | Crete (unprovenanced) | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005]...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #295 | Crete (unprovenanced) | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005]...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #295 | Crete (unprovenanced) | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005]...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #296 | Crete (unprovenanced) | `ti [VOWEL:#007] [GLIDE:#018] / me i [STOP:#039] / ki de / je [LIQUID:#034] [S...` | tai_HT123a | `ta i` | `AB59 AB28` | `#028 #007` | literal/class |
| CHIC #296 | Crete (unprovenanced) | `ti [VOWEL:#007] [GLIDE:#018] / me i [STOP:#039] / ki de / je [LIQUID:#034] [S...` | tai_HT39 | `ta i` | `AB59 AB28` | `#028 #007` | literal/class |
| CHIC #297 | Crete (unprovenanced) | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #297 | Crete (unprovenanced) | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #297 | Crete (unprovenanced) | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #297 | Crete (unprovenanced) | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #297 | Crete (unprovenanced) | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #045` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #045` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #045` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | dare_HT10a | `da re` | `AB01 AB27` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #045` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #045` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#045 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #298 | Crete (unprovenanced) | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#00...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#045 #070` | class/literal |
| CHIC #299 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #299 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #299 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #299 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #299 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kira_HT103 | `ki ra` | `AB67 AB60` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | karu_HT2 | `ka ru` | `AB77 AB26` | `#019 #031` | literal/literal |
| CHIC #301 | Crete (unprovenanced) | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` | kira_HT85b | `ki ra` | `AB67 AB60` | `#019 #031` | literal/literal |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#019 #039` | literal/class |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#019 #039` | literal/class |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#019 #039` | literal/class |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#019 #039` | literal/class |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | tai_HT123a | `ta i` | `AB59 AB28` | `#039 #038` | class/literal |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#019 #039` | literal/class |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | tai_HT39 | `ta i` | `AB59 AB28` | `#039 #038` | class/literal |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | mate_HT52a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #303 | Crete (unprovenanced) | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` | mate_PH15a | `ma te` | `AB80 AB04` | `#054 #061` | literal/literal |
| CHIC #304 | Crete (unprovenanced) | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#039 #013` | class/literal |
| CHIC #304 | Crete (unprovenanced) | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#039 #013` | class/literal |
| CHIC #304 | Crete (unprovenanced) | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#039 #013` | class/literal |
| CHIC #304 | Crete (unprovenanced) | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#039 #013` | class/literal |
| CHIC #304 | Crete (unprovenanced) | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#039 #013` | class/literal |
| CHIC #305 | Lastros | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #305 | Lastros | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #305 | Lastros | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #305 | Lastros | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #305 | Lastros | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#039 #056` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#039 #056` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#039 #056` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#039 #056` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | paja_HT154A | `pa ja` | `AB03 AB57` | `#056 #014` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#039 #056` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | paja_HT29 | `pa ja` | `AB03 AB57` | `#056 #014` | class/class |
| CHIC #306 | Mallia | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [...` | pitaja_HT6a | `pi ta ja` | `AB39 AB59 AB57` | `#039 #056 #014` | class/class/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #308 | Palaikastro | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STO...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | mina_HT115a | `mi na` | `AB73 AB06` | `#053 #041` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | mina_HT117a | `mi na` | `AB73 AB06` | `#053 #041` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kumina_HT54a | `ku mi na` | `AB81 AB73 AB06` | `#040 #053 #041` | class/literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #309 | Pyrgos (Myrtos) | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` | kumina_ZA10a | `ku mi na` | `AB81 AB73 AB06` | `#040 #053 #041` | class/literal/literal |
| CHIC #311 | Sitia | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #311 | Sitia | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #311 | Sitia | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #311 | Sitia | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #311 | Sitia | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #312 | Xida | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kupa3_HT1 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kupa3_HT101 | `ku pa3` | `AB81 AB56` | `#044 #005` | literal/class |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kapa_HT102 | `ka pa` | `AB77 AB03` | `#044 #005` | literal/class |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kupa_HT110a | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kupa_HT16 | `ku pa` | `AB81 AB03` | `#044 #005` | literal/class |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#092 #031` | literal/literal |
| CHIC #314 | Neapolis | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#092 #031` | literal/literal |
| CHIC #316 | Mallia | `de ni [GLIDE:#006] ta` | dina_HT25a | `di na` | `AB07 AB06` | `#049 #041` | literal/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #321 | Mallia | `[?:STOP:#056] ra` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #327 | Mallia | `de ni [GLIDE:#006] / NUM:57` | dina_HT25a | `di na` | `AB07 AB06` | `#049 #041` | literal/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kura_ARKH2 | `ku ra` | `AB81 AB60` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kiro_ARKH4b | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kiro_HT1 | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kuro_HT100 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kuro_HT102 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kira_HT103 | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kuro_HT104 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | dare_HT10a | `da re` | `AB01 AB27` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kiro_HT117a | `ki ro` | `AB67 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kuro_HT117a | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kuro_HT13 | `ku ro` | `AB81 AB02` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | karu_HT2 | `ka ru` | `AB77 AB26` | `#056 #070` | class/literal |
| CHIC #328 | Mallia | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ...` | kira_HT85b | `ki ra` | `AB67 AB60` | `#056 #070` | class/literal |

### Source B enumeration (toponym substring hits, tier-4)

Total source-B match cells (inscription × distinct toponym × distinct substring): **3957**.

| CHIC id | Site | Toponym | Substring | n match positions |
|---|---|---|---|--:|
| CHIC #001 | Knossos | hierapytna | `era` | 1 |
| CHIC #001 | Knossos | kuthera | `era` | 1 |
| CHIC #001 | Knossos | melitos | `eli` | 1 |
| CHIC #001 | Knossos | melitos | `mel` | 1 |
| CHIC #001 | Knossos | melitos | `meli` | 1 |
| CHIC #001 | Knossos | melos | `elo` | 1 |
| CHIC #001 | Knossos | melos | `mel` | 1 |
| CHIC #001 | Knossos | melos | `melo` | 1 |
| CHIC #001 | Knossos | paros | `aro` | 1 |
| CHIC #001 | Knossos | thera | `era` | 1 |
| CHIC #002 | Knossos | ala | `ala` | 1 |
| CHIC #002 | Knossos | aleksandros | `ale` | 1 |
| CHIC #002 | Knossos | aptara | `ara` | 1 |
| CHIC #002 | Knossos | aptara | `tar` | 1 |
| CHIC #002 | Knossos | aptara | `tara` | 1 |
| CHIC #002 | Knossos | gor | `gor` | 1 |
| CHIC #002 | Knossos | gortyn | `gor` | 1 |
| CHIC #002 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #002 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #002 | Knossos | hierapytna | `era` | 1 |
| CHIC #002 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #002 | Knossos | ikaria | `ari` | 1 |
| CHIC #002 | Knossos | ikaria | `kar` | 1 |
| CHIC #002 | Knossos | ikaria | `kari` | 1 |
| CHIC #002 | Knossos | kalumnos | `alu` | 1 |
| CHIC #002 | Knossos | kalumnos | `kal` | 1 |
| CHIC #002 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #002 | Knossos | kor | `kor` | 1 |
| CHIC #002 | Knossos | korinthos | `kor` | 1 |
| CHIC #002 | Knossos | korinthos | `kori` | 1 |
| CHIC #002 | Knossos | korinthos | `ori` | 1 |
| CHIC #002 | Knossos | kuthera | `era` | 1 |
| CHIC #002 | Knossos | lykabettos | `abe` | 1 |
| CHIC #002 | Knossos | melitos | `eli` | 1 |
| CHIC #002 | Knossos | melos | `elo` | 1 |
| CHIC #002 | Knossos | olous | `olo` | 1 |
| CHIC #002 | Knossos | olu | `olu` | 1 |
| CHIC #002 | Knossos | olunthos | `olu` | 1 |
| CHIC #002 | Knossos | par | `par` | 1 |
| CHIC #002 | Knossos | parnassos | `par` | 1 |
| CHIC #002 | Knossos | paros | `aro` | 1 |
| CHIC #002 | Knossos | paros | `par` | 1 |
| CHIC #002 | Knossos | paros | `paro` | 1 |
| CHIC #002 | Knossos | per | `per` | 1 |
| CHIC #002 | Knossos | pergamos | `per` | 1 |
| CHIC #002 | Knossos | phalasarna | `ala` | 1 |
| CHIC #002 | Knossos | poikilassos | `ila` | 1 |
| CHIC #002 | Knossos | poikilassos | `kil` | 1 |
| CHIC #002 | Knossos | poikilassos | `kila` | 1 |
| CHIC #002 | Knossos | probalinthos | `ali` | 1 |
| CHIC #002 | Knossos | probalinthos | `bal` | 1 |
| CHIC #002 | Knossos | probalinthos | `bali` | 1 |
| CHIC #002 | Knossos | pulos | `pul` | 1 |
| CHIC #002 | Knossos | pulos | `pulo` | 1 |
| CHIC #002 | Knossos | pulos | `ulo` | 1 |
| CHIC #002 | Knossos | salaminos | `ala` | 1 |
| CHIC #002 | Knossos | sparta | `par` | 1 |
| CHIC #002 | Knossos | tarra | `tar` | 1 |
| CHIC #002 | Knossos | tarsos | `tar` | 1 |
| CHIC #002 | Knossos | telmessos | `tel` | 1 |
| CHIC #002 | Knossos | ter | `ter` | 1 |
| CHIC #002 | Knossos | termessos | `ter` | 1 |
| CHIC #002 | Knossos | thera | `era` | 1 |
| CHIC #002 | Knossos | tirintha | `iri` | 1 |
| CHIC #002 | Knossos | tirintha | `tir` | 1 |
| CHIC #002 | Knossos | tirintha | `tiri` | 1 |
| CHIC #002 | Knossos | tiruns | `iru` | 1 |
| CHIC #002 | Knossos | tiruns | `tir` | 1 |
| CHIC #002 | Knossos | tiruns | `tiru` | 1 |
| CHIC #002 | Knossos | tul | `tul` | 1 |
| CHIC #002 | Knossos | tulisos | `tul` | 1 |
| CHIC #002 | Knossos | tulisos | `tuli` | 1 |
| CHIC #002 | Knossos | tulisos | `uli` | 1 |
| CHIC #002 | Knossos | tulissos | `tul` | 1 |
| CHIC #002 | Knossos | tulissos | `tuli` | 1 |
| CHIC #002 | Knossos | tulissos | `uli` | 1 |
| CHIC #002 | Knossos | zakuntos | `aku` | 1 |
| CHIC #003 | Knossos | pergamos | `gam` | 1 |
| CHIC #005 | Knossos | aleksandros | `lek` | 1 |
| CHIC #005 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #005 | Knossos | lukia | `luk` | 1 |
| CHIC #005 | Knossos | muke | `uke` | 1 |
| CHIC #005 | Knossos | mukenai | `uke` | 1 |
| CHIC #008 | Knossos | poikilassos | `iki` | 1 |
| CHIC #013 | Knossos | ala | `ala` | 1 |
| CHIC #013 | Knossos | aleksandros | `ale` | 1 |
| CHIC #013 | Knossos | aleksandros | `alek` | 1 |
| CHIC #013 | Knossos | aleksandros | `lek` | 1 |
| CHIC #013 | Knossos | aptara | `ara` | 1 |
| CHIC #013 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #013 | Knossos | halikarnassos | `alik` | 1 |
| CHIC #013 | Knossos | halikarnassos | `alika` | 1 |
| CHIC #013 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #013 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #013 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #013 | Knossos | hierapytna | `era` | 1 |
| CHIC #013 | Knossos | hierapytna | `erap` | 1 |
| CHIC #013 | Knossos | hierapytna | `rap` | 1 |
| CHIC #013 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #013 | Knossos | ida | `ida` | 1 |
| CHIC #013 | Knossos | ikaria | `ari` | 1 |
| CHIC #013 | Knossos | ikaria | `ika` | 1 |
| CHIC #013 | Knossos | itanos | `ita` | 1 |
| CHIC #013 | Knossos | kalumnos | `alu` | 1 |
| CHIC #013 | Knossos | korinthos | `ori` | 1 |
| CHIC #013 | Knossos | krete | `ete` | 1 |
| CHIC #013 | Knossos | krete | `ret` | 1 |
| CHIC #013 | Knossos | krete | `rete` | 1 |
| CHIC #013 | Knossos | kudonia | `udo` | 1 |
| CHIC #013 | Knossos | kuthera | `era` | 1 |
| CHIC #013 | Knossos | kuzikos | `iko` | 1 |
| CHIC #013 | Knossos | lab | `lab` | 1 |
| CHIC #013 | Knossos | lebena | `ebe` | 1 |
| CHIC #013 | Knossos | lebena | `leb` | 1 |
| CHIC #013 | Knossos | lebena | `lebe` | 1 |
| CHIC #013 | Knossos | lukia | `luk` | 1 |
| CHIC #013 | Knossos | lukia | `luki` | 1 |
| CHIC #013 | Knossos | lukia | `uki` | 1 |
| CHIC #013 | Knossos | lykabettos | `abe` | 1 |
| CHIC #013 | Knossos | melitos | `eli` | 1 |
| CHIC #013 | Knossos | melitos | `elit` | 1 |
| CHIC #013 | Knossos | melitos | `elito` | 1 |
| CHIC #013 | Knossos | melitos | `ito` | 1 |
| CHIC #013 | Knossos | melitos | `lit` | 1 |
| CHIC #013 | Knossos | melitos | `lito` | 1 |
| CHIC #013 | Knossos | melos | `elo` | 1 |
| CHIC #013 | Knossos | muke | `uke` | 1 |
| CHIC #013 | Knossos | mukenai | `uke` | 1 |
| CHIC #013 | Knossos | olous | `olo` | 1 |
| CHIC #013 | Knossos | olu | `olu` | 1 |
| CHIC #013 | Knossos | olunthos | `olu` | 1 |
| CHIC #013 | Knossos | paros | `aro` | 1 |
| CHIC #013 | Knossos | phalasarna | `ala` | 1 |
| CHIC #013 | Knossos | poikilassos | `iki` | 1 |
| CHIC #013 | Knossos | poikilassos | `ila` | 1 |
| CHIC #013 | Knossos | probalinthos | `ali` | 1 |
| CHIC #013 | Knossos | probalinthos | `oba` | 1 |
| CHIC #013 | Knossos | probalinthos | `rob` | 1 |
| CHIC #013 | Knossos | probalinthos | `roba` | 1 |
| CHIC #013 | Knossos | pulos | `ulo` | 1 |
| CHIC #013 | Knossos | salaminos | `ala` | 1 |
| CHIC #013 | Knossos | tegea | `ege` | 1 |
| CHIC #013 | Knossos | thebai | `eba` | 1 |
| CHIC #013 | Knossos | thera | `era` | 1 |
| CHIC #013 | Knossos | tirintha | `iri` | 1 |
| CHIC #013 | Knossos | tiruns | `iru` | 1 |
| CHIC #013 | Knossos | tulisos | `uli` | 1 |
| CHIC #013 | Knossos | tulissos | `uli` | 1 |
| CHIC #013 | Knossos | zakuntos | `aku` | 1 |
| CHIC #015 | Knossos | aleksandros | `lek` | 1 |
| CHIC #015 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #015 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #015 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #015 | Knossos | hierapytna | `rap` | 1 |
| CHIC #015 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #015 | Knossos | ida | `ida` | 1 |
| CHIC #015 | Knossos | ikaria | `ika` | 1 |
| CHIC #015 | Knossos | itanos | `ita` | 1 |
| CHIC #015 | Knossos | krete | `ete` | 1 |
| CHIC #015 | Knossos | krete | `ret` | 1 |
| CHIC #015 | Knossos | krete | `rete` | 1 |
| CHIC #015 | Knossos | kudonia | `udo` | 1 |
| CHIC #015 | Knossos | kuzikos | `iko` | 1 |
| CHIC #015 | Knossos | lab | `lab` | 1 |
| CHIC #015 | Knossos | lebena | `ebe` | 1 |
| CHIC #015 | Knossos | lebena | `leb` | 1 |
| CHIC #015 | Knossos | lebena | `lebe` | 1 |
| CHIC #015 | Knossos | lukia | `luk` | 1 |
| CHIC #015 | Knossos | lukia | `luki` | 1 |
| CHIC #015 | Knossos | lukia | `uki` | 1 |
| CHIC #015 | Knossos | lykabettos | `abe` | 1 |
| CHIC #015 | Knossos | melitos | `ito` | 1 |
| CHIC #015 | Knossos | melitos | `lit` | 1 |
| CHIC #015 | Knossos | melitos | `lito` | 1 |
| CHIC #015 | Knossos | muke | `uke` | 1 |
| CHIC #015 | Knossos | mukenai | `uke` | 1 |
| CHIC #015 | Knossos | poikilassos | `iki` | 1 |
| CHIC #015 | Knossos | probalinthos | `oba` | 1 |
| CHIC #015 | Knossos | probalinthos | `rob` | 1 |
| CHIC #015 | Knossos | probalinthos | `roba` | 1 |
| CHIC #015 | Knossos | tegea | `ege` | 1 |
| CHIC #015 | Knossos | thebai | `eba` | 1 |
| CHIC #015 | Knossos | zakuntos | `aku` | 1 |
| CHIC #016 | Knossos | ardettos | `det` | 1 |
| CHIC #016 | Knossos | krete | `ete` | 1 |
| CHIC #016 | Knossos | lebena | `ebe` | 1 |
| CHIC #016 | Knossos | tegea | `ege` | 1 |
| CHIC #016 | Knossos | thebai | `eba` | 1 |
| CHIC #017 | Knossos | smurna | `mur` | 1 |
| CHIC #018 | Knossos | ala | `ala` | 1 |
| CHIC #018 | Knossos | aleksandros | `ale` | 1 |
| CHIC #018 | Knossos | aptara | `ara` | 1 |
| CHIC #018 | Knossos | ardettos | `det` | 2 |
| CHIC #018 | Knossos | dikte | `dik` | 1 |
| CHIC #018 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #018 | Knossos | halikarnassos | `ika` | 2 |
| CHIC #018 | Knossos | hierapytna | `era` | 1 |
| CHIC #018 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #018 | Knossos | ida | `ida` | 2 |
| CHIC #018 | Knossos | ikaria | `ari` | 1 |
| CHIC #018 | Knossos | ikaria | `ika` | 2 |
| CHIC #018 | Knossos | itanos | `ita` | 2 |
| CHIC #018 | Knossos | kalumnos | `alu` | 1 |
| CHIC #018 | Knossos | korinthos | `ori` | 1 |
| CHIC #018 | Knossos | krete | `ete` | 2 |
| CHIC #018 | Knossos | kudonia | `kud` | 1 |
| CHIC #018 | Knossos | kudonia | `kudo` | 1 |
| CHIC #018 | Knossos | kudonia | `udo` | 1 |
| CHIC #018 | Knossos | kuthera | `era` | 1 |
| CHIC #018 | Knossos | kuthera | `kut` | 2 |
| CHIC #018 | Knossos | kuzikos | `iko` | 2 |
| CHIC #018 | Knossos | lebena | `ebe` | 1 |
| CHIC #018 | Knossos | lukia | `uki` | 1 |
| CHIC #018 | Knossos | lykabettos | `abe` | 1 |
| CHIC #018 | Knossos | lykabettos | `abet` | 1 |
| CHIC #018 | Knossos | lykabettos | `bet` | 2 |
| CHIC #018 | Knossos | lykabettos | `kab` | 1 |
| CHIC #018 | Knossos | lykabettos | `kabe` | 1 |
| CHIC #018 | Knossos | lykabettos | `kabet` | 1 |
| CHIC #018 | Knossos | melitos | `eli` | 1 |
| CHIC #018 | Knossos | melitos | `ito` | 2 |
| CHIC #018 | Knossos | melos | `elo` | 1 |
| CHIC #018 | Knossos | muke | `uke` | 1 |
| CHIC #018 | Knossos | mukenai | `uke` | 1 |
| CHIC #018 | Knossos | olous | `olo` | 1 |
| CHIC #018 | Knossos | olu | `olu` | 1 |
| CHIC #018 | Knossos | olunthos | `olu` | 1 |
| CHIC #018 | Knossos | paros | `aro` | 1 |
| CHIC #018 | Knossos | phalasarna | `ala` | 1 |
| CHIC #018 | Knossos | poikilassos | `iki` | 2 |
| CHIC #018 | Knossos | poikilassos | `ila` | 1 |
| CHIC #018 | Knossos | probalinthos | `ali` | 1 |
| CHIC #018 | Knossos | probalinthos | `oba` | 1 |
| CHIC #018 | Knossos | pulos | `ulo` | 1 |
| CHIC #018 | Knossos | salaminos | `ala` | 1 |
| CHIC #018 | Knossos | tegea | `ege` | 1 |
| CHIC #018 | Knossos | tegea | `teg` | 1 |
| CHIC #018 | Knossos | tegea | `tege` | 1 |
| CHIC #018 | Knossos | thebai | `eba` | 1 |
| CHIC #018 | Knossos | thera | `era` | 1 |
| CHIC #018 | Knossos | tirintha | `iri` | 1 |
| CHIC #018 | Knossos | tiruns | `iru` | 1 |
| CHIC #018 | Knossos | tulisos | `uli` | 1 |
| CHIC #018 | Knossos | tulissos | `uli` | 1 |
| CHIC #018 | Knossos | zakuntos | `aku` | 1 |
| CHIC #021 | Knossos | hierapytna | `era` | 1 |
| CHIC #021 | Knossos | ina | `ina` | 1 |
| CHIC #021 | Knossos | kuthera | `era` | 1 |
| CHIC #021 | Knossos | melitos | `eli` | 1 |
| CHIC #021 | Knossos | melos | `elo` | 1 |
| CHIC #021 | Knossos | minoa | `ino` | 1 |
| CHIC #021 | Knossos | salaminos | `ino` | 1 |
| CHIC #021 | Knossos | thera | `era` | 1 |
| CHIC #022 | Knossos | aptara | `ara` | 1 |
| CHIC #022 | Knossos | aptara | `tar` | 1 |
| CHIC #022 | Knossos | aptara | `tara` | 1 |
| CHIC #022 | Knossos | gor | `gor` | 1 |
| CHIC #022 | Knossos | gortyn | `gor` | 1 |
| CHIC #022 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #022 | Knossos | hierapytna | `era` | 1 |
| CHIC #022 | Knossos | ikaria | `kar` | 1 |
| CHIC #022 | Knossos | kor | `kor` | 1 |
| CHIC #022 | Knossos | korinthos | `kor` | 1 |
| CHIC #022 | Knossos | kuthera | `era` | 1 |
| CHIC #022 | Knossos | par | `par` | 1 |
| CHIC #022 | Knossos | parnassos | `par` | 1 |
| CHIC #022 | Knossos | paros | `par` | 1 |
| CHIC #022 | Knossos | per | `per` | 1 |
| CHIC #022 | Knossos | pergamos | `per` | 1 |
| CHIC #022 | Knossos | sparta | `par` | 1 |
| CHIC #022 | Knossos | tarra | `tar` | 1 |
| CHIC #022 | Knossos | tarsos | `tar` | 1 |
| CHIC #022 | Knossos | ter | `ter` | 1 |
| CHIC #022 | Knossos | termessos | `ter` | 1 |
| CHIC #022 | Knossos | thera | `era` | 1 |
| CHIC #022 | Knossos | tirintha | `tir` | 1 |
| CHIC #022 | Knossos | tiruns | `tir` | 1 |
| CHIC #023 | Knossos | ala | `ala` | 1 |
| CHIC #023 | Knossos | aleksandros | `ale` | 1 |
| CHIC #023 | Knossos | aptara | `ara` | 1 |
| CHIC #023 | Knossos | aptara | `tar` | 1 |
| CHIC #023 | Knossos | aptara | `tara` | 1 |
| CHIC #023 | Knossos | gor | `gor` | 1 |
| CHIC #023 | Knossos | gortyn | `gor` | 1 |
| CHIC #023 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #023 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #023 | Knossos | hierapytna | `era` | 1 |
| CHIC #023 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #023 | Knossos | ikaria | `ari` | 1 |
| CHIC #023 | Knossos | ikaria | `kar` | 1 |
| CHIC #023 | Knossos | ikaria | `kari` | 1 |
| CHIC #023 | Knossos | kalumnos | `alu` | 1 |
| CHIC #023 | Knossos | kalumnos | `kal` | 1 |
| CHIC #023 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #023 | Knossos | kor | `kor` | 1 |
| CHIC #023 | Knossos | korinthos | `kor` | 1 |
| CHIC #023 | Knossos | korinthos | `kori` | 1 |
| CHIC #023 | Knossos | korinthos | `ori` | 1 |
| CHIC #023 | Knossos | kuthera | `era` | 1 |
| CHIC #023 | Knossos | lykabettos | `abe` | 1 |
| CHIC #023 | Knossos | melitos | `eli` | 1 |
| CHIC #023 | Knossos | melos | `elo` | 1 |
| CHIC #023 | Knossos | olous | `olo` | 1 |
| CHIC #023 | Knossos | olu | `olu` | 1 |
| CHIC #023 | Knossos | olunthos | `olu` | 1 |
| CHIC #023 | Knossos | par | `par` | 1 |
| CHIC #023 | Knossos | parnassos | `par` | 1 |
| CHIC #023 | Knossos | paros | `aro` | 1 |
| CHIC #023 | Knossos | paros | `par` | 1 |
| CHIC #023 | Knossos | paros | `paro` | 1 |
| CHIC #023 | Knossos | per | `per` | 1 |
| CHIC #023 | Knossos | pergamos | `per` | 1 |
| CHIC #023 | Knossos | phalasarna | `ala` | 1 |
| CHIC #023 | Knossos | poikilassos | `ila` | 1 |
| CHIC #023 | Knossos | poikilassos | `kil` | 1 |
| CHIC #023 | Knossos | poikilassos | `kila` | 1 |
| CHIC #023 | Knossos | probalinthos | `ali` | 1 |
| CHIC #023 | Knossos | probalinthos | `bal` | 1 |
| CHIC #023 | Knossos | probalinthos | `bali` | 1 |
| CHIC #023 | Knossos | pulos | `pul` | 1 |
| CHIC #023 | Knossos | pulos | `pulo` | 1 |
| CHIC #023 | Knossos | pulos | `ulo` | 1 |
| CHIC #023 | Knossos | salaminos | `ala` | 1 |
| CHIC #023 | Knossos | sparta | `par` | 1 |
| CHIC #023 | Knossos | tarra | `tar` | 1 |
| CHIC #023 | Knossos | tarsos | `tar` | 1 |
| CHIC #023 | Knossos | telmessos | `tel` | 1 |
| CHIC #023 | Knossos | ter | `ter` | 1 |
| CHIC #023 | Knossos | termessos | `ter` | 1 |
| CHIC #023 | Knossos | thera | `era` | 1 |
| CHIC #023 | Knossos | tirintha | `iri` | 1 |
| CHIC #023 | Knossos | tirintha | `tir` | 1 |
| CHIC #023 | Knossos | tirintha | `tiri` | 1 |
| CHIC #023 | Knossos | tiruns | `iru` | 1 |
| CHIC #023 | Knossos | tiruns | `tir` | 1 |
| CHIC #023 | Knossos | tiruns | `tiru` | 1 |
| CHIC #023 | Knossos | tul | `tul` | 1 |
| CHIC #023 | Knossos | tulisos | `tul` | 1 |
| CHIC #023 | Knossos | tulisos | `tuli` | 1 |
| CHIC #023 | Knossos | tulisos | `uli` | 1 |
| CHIC #023 | Knossos | tulissos | `tul` | 1 |
| CHIC #023 | Knossos | tulissos | `tuli` | 1 |
| CHIC #023 | Knossos | tulissos | `uli` | 1 |
| CHIC #023 | Knossos | zakuntos | `aku` | 1 |
| CHIC #024 | Knossos | aleksandros | `lek` | 1 |
| CHIC #024 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #024 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #024 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #024 | Knossos | hierapytna | `rap` | 1 |
| CHIC #024 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #024 | Knossos | ida | `ida` | 1 |
| CHIC #024 | Knossos | ikaria | `ika` | 1 |
| CHIC #024 | Knossos | itanos | `ita` | 1 |
| CHIC #024 | Knossos | krete | `ete` | 1 |
| CHIC #024 | Knossos | krete | `ret` | 1 |
| CHIC #024 | Knossos | krete | `rete` | 1 |
| CHIC #024 | Knossos | kudonia | `udo` | 1 |
| CHIC #024 | Knossos | kuzikos | `iko` | 1 |
| CHIC #024 | Knossos | lab | `lab` | 1 |
| CHIC #024 | Knossos | lebena | `ebe` | 1 |
| CHIC #024 | Knossos | lebena | `leb` | 1 |
| CHIC #024 | Knossos | lebena | `lebe` | 1 |
| CHIC #024 | Knossos | lukia | `luk` | 1 |
| CHIC #024 | Knossos | lukia | `luki` | 1 |
| CHIC #024 | Knossos | lukia | `uki` | 1 |
| CHIC #024 | Knossos | lykabettos | `abe` | 1 |
| CHIC #024 | Knossos | melitos | `ito` | 1 |
| CHIC #024 | Knossos | melitos | `lit` | 1 |
| CHIC #024 | Knossos | melitos | `lito` | 1 |
| CHIC #024 | Knossos | muke | `uke` | 1 |
| CHIC #024 | Knossos | mukenai | `uke` | 1 |
| CHIC #024 | Knossos | poikilassos | `iki` | 1 |
| CHIC #024 | Knossos | probalinthos | `oba` | 1 |
| CHIC #024 | Knossos | probalinthos | `rob` | 1 |
| CHIC #024 | Knossos | probalinthos | `roba` | 1 |
| CHIC #024 | Knossos | tegea | `ege` | 1 |
| CHIC #024 | Knossos | thebai | `eba` | 1 |
| CHIC #024 | Knossos | zakuntos | `aku` | 1 |
| CHIC #025 | Knossos | poikilassos | `ila` | 1 |
| CHIC #025 | Knossos | tirintha | `iri` | 1 |
| CHIC #025 | Knossos | tiruns | `iru` | 1 |
| CHIC #026 | Knossos | aleksandros | `lek` | 1 |
| CHIC #026 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #026 | Knossos | lukia | `luk` | 1 |
| CHIC #026 | Knossos | muke | `uke` | 1 |
| CHIC #026 | Knossos | mukenai | `uke` | 1 |
| CHIC #027 | Knossos | ala | `ala` | 1 |
| CHIC #027 | Knossos | aleksandros | `ale` | 1 |
| CHIC #027 | Knossos | aptara | `ara` | 1 |
| CHIC #027 | Knossos | aptara | `tar` | 1 |
| CHIC #027 | Knossos | aptara | `tara` | 1 |
| CHIC #027 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #027 | Knossos | ikaria | `ari` | 1 |
| CHIC #027 | Knossos | kalumnos | `alu` | 1 |
| CHIC #027 | Knossos | paros | `aro` | 1 |
| CHIC #027 | Knossos | phalasarna | `ala` | 1 |
| CHIC #027 | Knossos | poikilassos | `ila` | 1 |
| CHIC #027 | Knossos | probalinthos | `ali` | 1 |
| CHIC #027 | Knossos | salaminos | `ala` | 1 |
| CHIC #027 | Knossos | tarra | `tar` | 1 |
| CHIC #027 | Knossos | tarsos | `tar` | 1 |
| CHIC #027 | Knossos | tirintha | `iri` | 1 |
| CHIC #027 | Knossos | tiruns | `iru` | 1 |
| CHIC #028 | Knossos | hyakinthos | `yak` | 1 |
| CHIC #028 | Knossos | krete | `ete` | 1 |
| CHIC #028 | Knossos | muke | `uke` | 1 |
| CHIC #028 | Knossos | mukenai | `uke` | 1 |
| CHIC #029 | Knossos | aptara | `ara` | 1 |
| CHIC #029 | Knossos | aptara | `tar` | 1 |
| CHIC #029 | Knossos | aptara | `tara` | 1 |
| CHIC #029 | Knossos | gor | `gor` | 1 |
| CHIC #029 | Knossos | gortyn | `gor` | 1 |
| CHIC #029 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #029 | Knossos | hierapytna | `era` | 1 |
| CHIC #029 | Knossos | ikaria | `kar` | 1 |
| CHIC #029 | Knossos | kor | `kor` | 1 |
| CHIC #029 | Knossos | korinthos | `kor` | 1 |
| CHIC #029 | Knossos | krete | `ete` | 1 |
| CHIC #029 | Knossos | kuthera | `era` | 1 |
| CHIC #029 | Knossos | lebena | `ebe` | 1 |
| CHIC #029 | Knossos | par | `par` | 1 |
| CHIC #029 | Knossos | parnassos | `par` | 1 |
| CHIC #029 | Knossos | paros | `par` | 1 |
| CHIC #029 | Knossos | per | `per` | 1 |
| CHIC #029 | Knossos | pergamos | `per` | 1 |
| CHIC #029 | Knossos | sparta | `par` | 1 |
| CHIC #029 | Knossos | tarra | `tar` | 1 |
| CHIC #029 | Knossos | tarsos | `tar` | 1 |
| CHIC #029 | Knossos | tegea | `ege` | 1 |
| CHIC #029 | Knossos | ter | `ter` | 1 |
| CHIC #029 | Knossos | termessos | `ter` | 1 |
| CHIC #029 | Knossos | thebai | `eba` | 1 |
| CHIC #029 | Knossos | thera | `era` | 1 |
| CHIC #029 | Knossos | tirintha | `tir` | 1 |
| CHIC #029 | Knossos | tiruns | `tir` | 1 |
| CHIC #030 | Knossos | hyakinthos | `yak` | 1 |
| CHIC #030 | Knossos | muke | `uke` | 1 |
| CHIC #030 | Knossos | mukenai | `uke` | 1 |
| CHIC #031 | Knossos | ala | `ala` | 1 |
| CHIC #031 | Knossos | aleksandros | `ale` | 1 |
| CHIC #031 | Knossos | aptara | `ara` | 1 |
| CHIC #031 | Knossos | aptara | `tar` | 1 |
| CHIC #031 | Knossos | aptara | `tara` | 1 |
| CHIC #031 | Knossos | ardettos | `det` | 1 |
| CHIC #031 | Knossos | gor | `gor` | 1 |
| CHIC #031 | Knossos | gortyn | `gor` | 1 |
| CHIC #031 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #031 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #031 | Knossos | hierapytna | `era` | 1 |
| CHIC #031 | Knossos | ikaria | `ari` | 1 |
| CHIC #031 | Knossos | ikaria | `kar` | 1 |
| CHIC #031 | Knossos | ikaria | `kari` | 1 |
| CHIC #031 | Knossos | kalumnos | `alu` | 1 |
| CHIC #031 | Knossos | kalumnos | `kal` | 1 |
| CHIC #031 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #031 | Knossos | kor | `kor` | 1 |
| CHIC #031 | Knossos | korinthos | `kor` | 1 |
| CHIC #031 | Knossos | korinthos | `kori` | 1 |
| CHIC #031 | Knossos | korinthos | `ori` | 1 |
| CHIC #031 | Knossos | krete | `ete` | 1 |
| CHIC #031 | Knossos | kuthera | `era` | 1 |
| CHIC #031 | Knossos | lebena | `ebe` | 1 |
| CHIC #031 | Knossos | melitos | `eli` | 1 |
| CHIC #031 | Knossos | melos | `elo` | 1 |
| CHIC #031 | Knossos | olous | `olo` | 1 |
| CHIC #031 | Knossos | olu | `olu` | 1 |
| CHIC #031 | Knossos | olunthos | `olu` | 1 |
| CHIC #031 | Knossos | par | `par` | 1 |
| CHIC #031 | Knossos | parnassos | `par` | 1 |
| CHIC #031 | Knossos | paros | `aro` | 1 |
| CHIC #031 | Knossos | paros | `par` | 1 |
| CHIC #031 | Knossos | paros | `paro` | 1 |
| CHIC #031 | Knossos | per | `per` | 1 |
| CHIC #031 | Knossos | pergamos | `per` | 1 |
| CHIC #031 | Knossos | phalasarna | `ala` | 1 |
| CHIC #031 | Knossos | poikilassos | `ila` | 1 |
| CHIC #031 | Knossos | poikilassos | `kil` | 1 |
| CHIC #031 | Knossos | poikilassos | `kila` | 1 |
| CHIC #031 | Knossos | probalinthos | `ali` | 1 |
| CHIC #031 | Knossos | probalinthos | `bal` | 1 |
| CHIC #031 | Knossos | probalinthos | `bali` | 1 |
| CHIC #031 | Knossos | pulos | `pul` | 1 |
| CHIC #031 | Knossos | pulos | `pulo` | 1 |
| CHIC #031 | Knossos | pulos | `ulo` | 1 |
| CHIC #031 | Knossos | salaminos | `ala` | 1 |
| CHIC #031 | Knossos | sparta | `par` | 1 |
| CHIC #031 | Knossos | tarra | `tar` | 1 |
| CHIC #031 | Knossos | tarsos | `tar` | 1 |
| CHIC #031 | Knossos | tegea | `ege` | 1 |
| CHIC #031 | Knossos | telmessos | `tel` | 1 |
| CHIC #031 | Knossos | ter | `ter` | 1 |
| CHIC #031 | Knossos | termessos | `ter` | 1 |
| CHIC #031 | Knossos | thebai | `eba` | 1 |
| CHIC #031 | Knossos | thera | `era` | 1 |
| CHIC #031 | Knossos | tirintha | `iri` | 1 |
| CHIC #031 | Knossos | tirintha | `tir` | 1 |
| CHIC #031 | Knossos | tirintha | `tiri` | 1 |
| CHIC #031 | Knossos | tiruns | `iru` | 1 |
| CHIC #031 | Knossos | tiruns | `tir` | 1 |
| CHIC #031 | Knossos | tiruns | `tiru` | 1 |
| CHIC #031 | Knossos | tul | `tul` | 1 |
| CHIC #031 | Knossos | tulisos | `tul` | 1 |
| CHIC #031 | Knossos | tulisos | `tuli` | 1 |
| CHIC #031 | Knossos | tulisos | `uli` | 1 |
| CHIC #031 | Knossos | tulissos | `tul` | 1 |
| CHIC #031 | Knossos | tulissos | `tuli` | 1 |
| CHIC #031 | Knossos | tulissos | `uli` | 1 |
| CHIC #032 | Knossos | ala | `ala` | 1 |
| CHIC #032 | Knossos | aleksandros | `ale` | 1 |
| CHIC #032 | Knossos | aptara | `ara` | 1 |
| CHIC #032 | Knossos | aptara | `tar` | 1 |
| CHIC #032 | Knossos | aptara | `tara` | 1 |
| CHIC #032 | Knossos | gor | `gor` | 1 |
| CHIC #032 | Knossos | gortyn | `gor` | 1 |
| CHIC #032 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #032 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #032 | Knossos | hierapytna | `era` | 2 |
| CHIC #032 | Knossos | ikaria | `ari` | 1 |
| CHIC #032 | Knossos | ikaria | `kar` | 1 |
| CHIC #032 | Knossos | ikaria | `kari` | 1 |
| CHIC #032 | Knossos | kalumnos | `alu` | 1 |
| CHIC #032 | Knossos | kalumnos | `kal` | 1 |
| CHIC #032 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #032 | Knossos | kor | `kor` | 1 |
| CHIC #032 | Knossos | korinthos | `kor` | 1 |
| CHIC #032 | Knossos | korinthos | `kori` | 1 |
| CHIC #032 | Knossos | korinthos | `ori` | 1 |
| CHIC #032 | Knossos | krete | `ete` | 1 |
| CHIC #032 | Knossos | krete | `ret` | 1 |
| CHIC #032 | Knossos | krete | `rete` | 1 |
| CHIC #032 | Knossos | kuthera | `era` | 2 |
| CHIC #032 | Knossos | melitos | `eli` | 2 |
| CHIC #032 | Knossos | melitos | `elit` | 1 |
| CHIC #032 | Knossos | melitos | `lit` | 1 |
| CHIC #032 | Knossos | melos | `elo` | 2 |
| CHIC #032 | Knossos | olous | `olo` | 1 |
| CHIC #032 | Knossos | olu | `olu` | 1 |
| CHIC #032 | Knossos | olunthos | `olu` | 1 |
| CHIC #032 | Knossos | par | `par` | 1 |
| CHIC #032 | Knossos | parnassos | `par` | 1 |
| CHIC #032 | Knossos | paros | `aro` | 2 |
| CHIC #032 | Knossos | paros | `par` | 1 |
| CHIC #032 | Knossos | paros | `paro` | 1 |
| CHIC #032 | Knossos | per | `per` | 1 |
| CHIC #032 | Knossos | pergamos | `per` | 1 |
| CHIC #032 | Knossos | phalasarna | `ala` | 1 |
| CHIC #032 | Knossos | poikilassos | `ila` | 1 |
| CHIC #032 | Knossos | poikilassos | `kil` | 1 |
| CHIC #032 | Knossos | poikilassos | `kila` | 1 |
| CHIC #032 | Knossos | probalinthos | `ali` | 1 |
| CHIC #032 | Knossos | probalinthos | `bal` | 1 |
| CHIC #032 | Knossos | probalinthos | `bali` | 1 |
| CHIC #032 | Knossos | pulos | `pul` | 1 |
| CHIC #032 | Knossos | pulos | `pulo` | 1 |
| CHIC #032 | Knossos | pulos | `ulo` | 1 |
| CHIC #032 | Knossos | salaminos | `ala` | 1 |
| CHIC #032 | Knossos | sparta | `par` | 1 |
| CHIC #032 | Knossos | tarra | `tar` | 1 |
| CHIC #032 | Knossos | tarsos | `tar` | 1 |
| CHIC #032 | Knossos | telmessos | `tel` | 1 |
| CHIC #032 | Knossos | ter | `ter` | 1 |
| CHIC #032 | Knossos | termessos | `ter` | 1 |
| CHIC #032 | Knossos | thera | `era` | 2 |
| CHIC #032 | Knossos | tirintha | `iri` | 1 |
| CHIC #032 | Knossos | tirintha | `tir` | 1 |
| CHIC #032 | Knossos | tirintha | `tiri` | 1 |
| CHIC #032 | Knossos | tiruns | `iru` | 1 |
| CHIC #032 | Knossos | tiruns | `tir` | 1 |
| CHIC #032 | Knossos | tiruns | `tiru` | 1 |
| CHIC #032 | Knossos | tul | `tul` | 1 |
| CHIC #032 | Knossos | tulisos | `tul` | 1 |
| CHIC #032 | Knossos | tulisos | `tuli` | 1 |
| CHIC #032 | Knossos | tulisos | `uli` | 1 |
| CHIC #032 | Knossos | tulissos | `tul` | 1 |
| CHIC #032 | Knossos | tulissos | `tuli` | 1 |
| CHIC #032 | Knossos | tulissos | `uli` | 1 |
| CHIC #033 | Knossos | hyakinthos | `yak` | 1 |
| CHIC #033 | Knossos | muke | `uke` | 1 |
| CHIC #033 | Knossos | mukenai | `uke` | 1 |
| CHIC #034 | Knossos | kudonia | `kud` | 1 |
| CHIC #036 | Knossos | krete | `ete` | 1 |
| CHIC #036 | Knossos | krete | `ret` | 1 |
| CHIC #036 | Knossos | krete | `rete` | 1 |
| CHIC #036 | Knossos | melitos | `lit` | 1 |
| CHIC #037 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #037 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #037 | Knossos | hymettos | `met` | 1 |
| CHIC #037 | Knossos | ida | `ida` | 1 |
| CHIC #037 | Knossos | ikaria | `ika` | 1 |
| CHIC #037 | Knossos | itanos | `ita` | 1 |
| CHIC #037 | Knossos | krete | `ete` | 1 |
| CHIC #037 | Knossos | kudonia | `udo` | 1 |
| CHIC #037 | Knossos | kuzikos | `iko` | 1 |
| CHIC #037 | Knossos | lebena | `ebe` | 1 |
| CHIC #037 | Knossos | lukia | `uki` | 1 |
| CHIC #037 | Knossos | lykabettos | `abe` | 1 |
| CHIC #037 | Knossos | melitos | `ito` | 1 |
| CHIC #037 | Knossos | muke | `muk` | 1 |
| CHIC #037 | Knossos | muke | `muke` | 1 |
| CHIC #037 | Knossos | muke | `uke` | 1 |
| CHIC #037 | Knossos | mukenai | `muk` | 1 |
| CHIC #037 | Knossos | mukenai | `muke` | 1 |
| CHIC #037 | Knossos | mukenai | `uke` | 1 |
| CHIC #037 | Knossos | poikilassos | `iki` | 1 |
| CHIC #037 | Knossos | probalinthos | `oba` | 1 |
| CHIC #037 | Knossos | tegea | `ege` | 1 |
| CHIC #037 | Knossos | thebai | `eba` | 1 |
| CHIC #037 | Knossos | zakuntos | `aku` | 1 |
| CHIC #038 | Knossos | ala | `ala` | 1 |
| CHIC #038 | Knossos | aleksandros | `ale` | 1 |
| CHIC #038 | Knossos | aptara | `ara` | 2 |
| CHIC #038 | Knossos | aptara | `tar` | 1 |
| CHIC #038 | Knossos | aptara | `tara` | 1 |
| CHIC #038 | Knossos | gor | `gor` | 1 |
| CHIC #038 | Knossos | gortyn | `gor` | 1 |
| CHIC #038 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #038 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #038 | Knossos | hierapytna | `era` | 1 |
| CHIC #038 | Knossos | ikaria | `ari` | 1 |
| CHIC #038 | Knossos | ikaria | `kar` | 1 |
| CHIC #038 | Knossos | kalumnos | `alu` | 1 |
| CHIC #038 | Knossos | kor | `kor` | 1 |
| CHIC #038 | Knossos | korinthos | `kor` | 1 |
| CHIC #038 | Knossos | krete | `ete` | 1 |
| CHIC #038 | Knossos | kuthera | `era` | 1 |
| CHIC #038 | Knossos | lebena | `ebe` | 1 |
| CHIC #038 | Knossos | par | `par` | 1 |
| CHIC #038 | Knossos | parnassos | `par` | 1 |
| CHIC #038 | Knossos | paros | `aro` | 1 |
| CHIC #038 | Knossos | paros | `par` | 1 |
| CHIC #038 | Knossos | per | `per` | 1 |
| CHIC #038 | Knossos | pergamos | `per` | 1 |
| CHIC #038 | Knossos | phalasarna | `ala` | 1 |
| CHIC #038 | Knossos | probalinthos | `ali` | 1 |
| CHIC #038 | Knossos | salaminos | `ala` | 1 |
| CHIC #038 | Knossos | sparta | `par` | 1 |
| CHIC #038 | Knossos | tarra | `tar` | 1 |
| CHIC #038 | Knossos | tarsos | `tar` | 1 |
| CHIC #038 | Knossos | tegea | `ege` | 1 |
| CHIC #038 | Knossos | ter | `ter` | 1 |
| CHIC #038 | Knossos | termessos | `ter` | 1 |
| CHIC #038 | Knossos | thebai | `eba` | 1 |
| CHIC #038 | Knossos | thera | `era` | 1 |
| CHIC #038 | Knossos | tirintha | `tir` | 1 |
| CHIC #038 | Knossos | tiruns | `tir` | 1 |
| CHIC #039 | Knossos | ala | `ala` | 1 |
| CHIC #039 | Knossos | aleksandros | `ale` | 1 |
| CHIC #039 | Knossos | ami | `ami` | 1 |
| CHIC #039 | Knossos | aptara | `ara` | 2 |
| CHIC #039 | Knossos | aptara | `tar` | 1 |
| CHIC #039 | Knossos | aptara | `tara` | 1 |
| CHIC #039 | Knossos | gor | `gor` | 1 |
| CHIC #039 | Knossos | gortyn | `gor` | 1 |
| CHIC #039 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #039 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #039 | Knossos | hierapytna | `era` | 3 |
| CHIC #039 | Knossos | ikaria | `ari` | 1 |
| CHIC #039 | Knossos | ikaria | `kar` | 1 |
| CHIC #039 | Knossos | ikaria | `kari` | 1 |
| CHIC #039 | Knossos | itanos | `ano` | 1 |
| CHIC #039 | Knossos | kalumnos | `alu` | 1 |
| CHIC #039 | Knossos | kalumnos | `kal` | 1 |
| CHIC #039 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #039 | Knossos | kor | `kor` | 1 |
| CHIC #039 | Knossos | korinthos | `kor` | 1 |
| CHIC #039 | Knossos | korinthos | `kori` | 1 |
| CHIC #039 | Knossos | korinthos | `ori` | 1 |
| CHIC #039 | Knossos | kuthera | `era` | 3 |
| CHIC #039 | Knossos | melitos | `eli` | 2 |
| CHIC #039 | Knossos | melos | `elo` | 2 |
| CHIC #039 | Knossos | olous | `olo` | 1 |
| CHIC #039 | Knossos | olu | `olu` | 1 |
| CHIC #039 | Knossos | olunthos | `olu` | 1 |
| CHIC #039 | Knossos | par | `par` | 1 |
| CHIC #039 | Knossos | parnassos | `par` | 1 |
| CHIC #039 | Knossos | paros | `aro` | 1 |
| CHIC #039 | Knossos | paros | `par` | 1 |
| CHIC #039 | Knossos | paros | `paro` | 1 |
| CHIC #039 | Knossos | per | `per` | 1 |
| CHIC #039 | Knossos | pergamos | `amo` | 1 |
| CHIC #039 | Knossos | pergamos | `per` | 1 |
| CHIC #039 | Knossos | phalasarna | `ala` | 1 |
| CHIC #039 | Knossos | poikilassos | `ila` | 1 |
| CHIC #039 | Knossos | poikilassos | `kil` | 1 |
| CHIC #039 | Knossos | poikilassos | `kila` | 1 |
| CHIC #039 | Knossos | probalinthos | `ali` | 1 |
| CHIC #039 | Knossos | probalinthos | `bal` | 1 |
| CHIC #039 | Knossos | probalinthos | `bali` | 1 |
| CHIC #039 | Knossos | pulos | `pul` | 1 |
| CHIC #039 | Knossos | pulos | `pulo` | 1 |
| CHIC #039 | Knossos | pulos | `ulo` | 1 |
| CHIC #039 | Knossos | salaminos | `ala` | 1 |
| CHIC #039 | Knossos | salaminos | `ami` | 1 |
| CHIC #039 | Knossos | samos | `amo` | 1 |
| CHIC #039 | Knossos | sparta | `par` | 1 |
| CHIC #039 | Knossos | tarra | `tar` | 1 |
| CHIC #039 | Knossos | tarsos | `tar` | 1 |
| CHIC #039 | Knossos | telmessos | `tel` | 1 |
| CHIC #039 | Knossos | ter | `ter` | 1 |
| CHIC #039 | Knossos | termessos | `ter` | 1 |
| CHIC #039 | Knossos | thera | `era` | 3 |
| CHIC #039 | Knossos | tirintha | `iri` | 1 |
| CHIC #039 | Knossos | tirintha | `tir` | 1 |
| CHIC #039 | Knossos | tirintha | `tiri` | 1 |
| CHIC #039 | Knossos | tiruns | `iru` | 1 |
| CHIC #039 | Knossos | tiruns | `tir` | 1 |
| CHIC #039 | Knossos | tiruns | `tiru` | 1 |
| CHIC #039 | Knossos | tul | `tul` | 1 |
| CHIC #039 | Knossos | tulisos | `tul` | 1 |
| CHIC #039 | Knossos | tulisos | `tuli` | 1 |
| CHIC #039 | Knossos | tulisos | `uli` | 1 |
| CHIC #039 | Knossos | tulissos | `tul` | 1 |
| CHIC #039 | Knossos | tulissos | `tuli` | 1 |
| CHIC #039 | Knossos | tulissos | `uli` | 1 |
| CHIC #040 | Knossos | ardettos | `det` | 1 |
| CHIC #040 | Knossos | dikte | `dik` | 1 |
| CHIC #040 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #040 | Knossos | hierapytna | `era` | 1 |
| CHIC #040 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #040 | Knossos | ida | `ida` | 1 |
| CHIC #040 | Knossos | ikaria | `ika` | 1 |
| CHIC #040 | Knossos | itanos | `ita` | 1 |
| CHIC #040 | Knossos | krete | `ete` | 1 |
| CHIC #040 | Knossos | kudonia | `kud` | 1 |
| CHIC #040 | Knossos | kudonia | `kudo` | 1 |
| CHIC #040 | Knossos | kudonia | `udo` | 1 |
| CHIC #040 | Knossos | kuthera | `era` | 1 |
| CHIC #040 | Knossos | kuthera | `kut` | 1 |
| CHIC #040 | Knossos | kuzikos | `iko` | 1 |
| CHIC #040 | Knossos | lebena | `ebe` | 1 |
| CHIC #040 | Knossos | lukia | `uki` | 1 |
| CHIC #040 | Knossos | lykabettos | `abe` | 1 |
| CHIC #040 | Knossos | lykabettos | `bet` | 1 |
| CHIC #040 | Knossos | lykabettos | `kab` | 1 |
| CHIC #040 | Knossos | lykabettos | `kabe` | 1 |
| CHIC #040 | Knossos | melitos | `ito` | 1 |
| CHIC #040 | Knossos | muke | `uke` | 1 |
| CHIC #040 | Knossos | mukenai | `uke` | 1 |
| CHIC #040 | Knossos | paros | `aro` | 1 |
| CHIC #040 | Knossos | poikilassos | `iki` | 1 |
| CHIC #040 | Knossos | probalinthos | `oba` | 1 |
| CHIC #040 | Knossos | tegea | `ege` | 1 |
| CHIC #040 | Knossos | tegea | `teg` | 1 |
| CHIC #040 | Knossos | tegea | `tege` | 1 |
| CHIC #040 | Knossos | thebai | `eba` | 1 |
| CHIC #040 | Knossos | thera | `era` | 1 |
| CHIC #040 | Knossos | zakuntos | `aku` | 1 |
| CHIC #041 | Knossos | ala | `ala` | 1 |
| CHIC #041 | Knossos | aleksandros | `ale` | 1 |
| CHIC #041 | Knossos | aptara | `ara` | 1 |
| CHIC #041 | Knossos | aptara | `tar` | 1 |
| CHIC #041 | Knossos | aptara | `tara` | 1 |
| CHIC #041 | Knossos | gor | `gor` | 1 |
| CHIC #041 | Knossos | gortyn | `gor` | 1 |
| CHIC #041 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #041 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #041 | Knossos | hierapytna | `era` | 1 |
| CHIC #041 | Knossos | ikaria | `ari` | 1 |
| CHIC #041 | Knossos | ikaria | `kar` | 1 |
| CHIC #041 | Knossos | ikaria | `kari` | 1 |
| CHIC #041 | Knossos | kalumnos | `alu` | 1 |
| CHIC #041 | Knossos | kalumnos | `kal` | 1 |
| CHIC #041 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #041 | Knossos | kor | `kor` | 1 |
| CHIC #041 | Knossos | korinthos | `kor` | 1 |
| CHIC #041 | Knossos | korinthos | `kori` | 1 |
| CHIC #041 | Knossos | korinthos | `korin` | 1 |
| CHIC #041 | Knossos | korinthos | `ori` | 1 |
| CHIC #041 | Knossos | korinthos | `orin` | 1 |
| CHIC #041 | Knossos | korinthos | `rin` | 1 |
| CHIC #041 | Knossos | kudonia | `oni` | 1 |
| CHIC #041 | Knossos | kuthera | `era` | 1 |
| CHIC #041 | Knossos | melitos | `eli` | 1 |
| CHIC #041 | Knossos | melos | `elo` | 1 |
| CHIC #041 | Knossos | olous | `olo` | 1 |
| CHIC #041 | Knossos | olu | `olu` | 1 |
| CHIC #041 | Knossos | olunthos | `lun` | 1 |
| CHIC #041 | Knossos | olunthos | `olu` | 1 |
| CHIC #041 | Knossos | olunthos | `olun` | 1 |
| CHIC #041 | Knossos | par | `par` | 1 |
| CHIC #041 | Knossos | parnassos | `par` | 1 |
| CHIC #041 | Knossos | paros | `aro` | 1 |
| CHIC #041 | Knossos | paros | `par` | 1 |
| CHIC #041 | Knossos | paros | `paro` | 1 |
| CHIC #041 | Knossos | per | `per` | 1 |
| CHIC #041 | Knossos | pergamos | `per` | 1 |
| CHIC #041 | Knossos | phalasarna | `ala` | 1 |
| CHIC #041 | Knossos | poikilassos | `ila` | 1 |
| CHIC #041 | Knossos | poikilassos | `kil` | 1 |
| CHIC #041 | Knossos | poikilassos | `kila` | 1 |
| CHIC #041 | Knossos | probalinthos | `ali` | 1 |
| CHIC #041 | Knossos | probalinthos | `alin` | 1 |
| CHIC #041 | Knossos | probalinthos | `bal` | 1 |
| CHIC #041 | Knossos | probalinthos | `bali` | 1 |
| CHIC #041 | Knossos | probalinthos | `balin` | 1 |
| CHIC #041 | Knossos | probalinthos | `lin` | 1 |
| CHIC #041 | Knossos | pulos | `pul` | 1 |
| CHIC #041 | Knossos | pulos | `pulo` | 1 |
| CHIC #041 | Knossos | pulos | `ulo` | 1 |
| CHIC #041 | Knossos | salaminos | `ala` | 1 |
| CHIC #041 | Knossos | sparta | `par` | 1 |
| CHIC #041 | Knossos | tarra | `tar` | 1 |
| CHIC #041 | Knossos | tarsos | `tar` | 1 |
| CHIC #041 | Knossos | telmessos | `tel` | 1 |
| CHIC #041 | Knossos | ter | `ter` | 1 |
| CHIC #041 | Knossos | termessos | `ter` | 1 |
| CHIC #041 | Knossos | thera | `era` | 1 |
| CHIC #041 | Knossos | tirintha | `iri` | 1 |
| CHIC #041 | Knossos | tirintha | `irin` | 1 |
| CHIC #041 | Knossos | tirintha | `rin` | 1 |
| CHIC #041 | Knossos | tirintha | `tir` | 1 |
| CHIC #041 | Knossos | tirintha | `tiri` | 1 |
| CHIC #041 | Knossos | tirintha | `tirin` | 1 |
| CHIC #041 | Knossos | tiruns | `iru` | 1 |
| CHIC #041 | Knossos | tiruns | `irun` | 1 |
| CHIC #041 | Knossos | tiruns | `run` | 1 |
| CHIC #041 | Knossos | tiruns | `tir` | 1 |
| CHIC #041 | Knossos | tiruns | `tiru` | 1 |
| CHIC #041 | Knossos | tiruns | `tirun` | 1 |
| CHIC #041 | Knossos | tul | `tul` | 1 |
| CHIC #041 | Knossos | tulisos | `tul` | 1 |
| CHIC #041 | Knossos | tulisos | `tuli` | 1 |
| CHIC #041 | Knossos | tulisos | `uli` | 1 |
| CHIC #041 | Knossos | tulissos | `tul` | 1 |
| CHIC #041 | Knossos | tulissos | `tuli` | 1 |
| CHIC #041 | Knossos | tulissos | `uli` | 1 |
| CHIC #042 | Knossos | ala | `ala` | 2 |
| CHIC #042 | Knossos | aleksandros | `ale` | 2 |
| CHIC #042 | Knossos | aptara | `ara` | 3 |
| CHIC #042 | Knossos | halikarnassos | `ali` | 2 |
| CHIC #042 | Knossos | hierapytna | `era` | 3 |
| CHIC #042 | Knossos | ikaria | `ari` | 2 |
| CHIC #042 | Knossos | kalumnos | `alu` | 2 |
| CHIC #042 | Knossos | korinthos | `ori` | 2 |
| CHIC #042 | Knossos | kuthera | `era` | 3 |
| CHIC #042 | Knossos | melitos | `eli` | 2 |
| CHIC #042 | Knossos | melos | `elo` | 2 |
| CHIC #042 | Knossos | olous | `olo` | 2 |
| CHIC #042 | Knossos | olu | `olu` | 2 |
| CHIC #042 | Knossos | olunthos | `olu` | 2 |
| CHIC #042 | Knossos | paros | `aro` | 2 |
| CHIC #042 | Knossos | phalasarna | `ala` | 2 |
| CHIC #042 | Knossos | poikilassos | `ila` | 2 |
| CHIC #042 | Knossos | probalinthos | `ali` | 2 |
| CHIC #042 | Knossos | pulos | `ulo` | 2 |
| CHIC #042 | Knossos | salaminos | `ala` | 2 |
| CHIC #042 | Knossos | thera | `era` | 3 |
| CHIC #042 | Knossos | tirintha | `iri` | 2 |
| CHIC #042 | Knossos | tiruns | `iru` | 2 |
| CHIC #042 | Knossos | tulisos | `uli` | 2 |
| CHIC #042 | Knossos | tulissos | `uli` | 2 |
| CHIC #043 | Knossos | ala | `ala` | 3 |
| CHIC #043 | Knossos | aleksandros | `ale` | 3 |
| CHIC #043 | Knossos | aptara | `ara` | 3 |
| CHIC #043 | Knossos | halikarnassos | `ali` | 3 |
| CHIC #043 | Knossos | hierapytna | `era` | 2 |
| CHIC #043 | Knossos | ikaria | `ari` | 3 |
| CHIC #043 | Knossos | kalumnos | `alu` | 3 |
| CHIC #043 | Knossos | korinthos | `ori` | 2 |
| CHIC #043 | Knossos | kuthera | `era` | 2 |
| CHIC #043 | Knossos | melitos | `eli` | 2 |
| CHIC #043 | Knossos | melos | `elo` | 2 |
| CHIC #043 | Knossos | olous | `olo` | 2 |
| CHIC #043 | Knossos | olu | `olu` | 2 |
| CHIC #043 | Knossos | olunthos | `olu` | 2 |
| CHIC #043 | Knossos | paros | `aro` | 3 |
| CHIC #043 | Knossos | phalasarna | `ala` | 3 |
| CHIC #043 | Knossos | poikilassos | `ila` | 2 |
| CHIC #043 | Knossos | probalinthos | `ali` | 3 |
| CHIC #043 | Knossos | pulos | `ulo` | 2 |
| CHIC #043 | Knossos | salaminos | `ala` | 3 |
| CHIC #043 | Knossos | thera | `era` | 2 |
| CHIC #043 | Knossos | tirintha | `iri` | 2 |
| CHIC #043 | Knossos | tiruns | `iru` | 2 |
| CHIC #043 | Knossos | tulisos | `uli` | 2 |
| CHIC #043 | Knossos | tulissos | `uli` | 2 |
| CHIC #044 | Knossos | ala | `ala` | 1 |
| CHIC #044 | Knossos | aleksandros | `ale` | 1 |
| CHIC #044 | Knossos | aptara | `ara` | 1 |
| CHIC #044 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #044 | Knossos | ikaria | `ari` | 1 |
| CHIC #044 | Knossos | kalumnos | `alu` | 1 |
| CHIC #044 | Knossos | paros | `aro` | 1 |
| CHIC #044 | Knossos | phalasarna | `ala` | 1 |
| CHIC #044 | Knossos | probalinthos | `ali` | 1 |
| CHIC #044 | Knossos | salaminos | `ala` | 1 |
| CHIC #045 | Knossos | ala | `ala` | 1 |
| CHIC #045 | Knossos | aleksandros | `ale` | 1 |
| CHIC #045 | Knossos | aptara | `ara` | 1 |
| CHIC #045 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #045 | Knossos | ikaria | `ari` | 1 |
| CHIC #045 | Knossos | kalumnos | `alu` | 1 |
| CHIC #045 | Knossos | kalumnos | `lum` | 1 |
| CHIC #045 | Knossos | lem | `lem` | 1 |
| CHIC #045 | Knossos | lemnos | `lem` | 1 |
| CHIC #045 | Knossos | paros | `aro` | 1 |
| CHIC #045 | Knossos | phalasarna | `ala` | 1 |
| CHIC #045 | Knossos | probalinthos | `ali` | 1 |
| CHIC #045 | Knossos | salaminos | `ala` | 1 |
| CHIC #045 | Knossos | salaminos | `lam` | 1 |
| CHIC #046 | Knossos | hierapytna | `era` | 1 |
| CHIC #046 | Knossos | kuthera | `era` | 1 |
| CHIC #046 | Knossos | melitos | `eli` | 1 |
| CHIC #046 | Knossos | melos | `elo` | 1 |
| CHIC #046 | Knossos | thera | `era` | 1 |
| CHIC #049 | Knossos | ala | `ala` | 1 |
| CHIC #049 | Knossos | aleksandros | `ale` | 1 |
| CHIC #049 | Knossos | aleksandros | `lek` | 1 |
| CHIC #049 | Knossos | aptara | `ara` | 1 |
| CHIC #049 | Knossos | aptara | `tar` | 1 |
| CHIC #049 | Knossos | aptara | `tara` | 1 |
| CHIC #049 | Knossos | ardettos | `det` | 1 |
| CHIC #049 | Knossos | gor | `gor` | 1 |
| CHIC #049 | Knossos | gortyn | `gor` | 1 |
| CHIC #049 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #049 | Knossos | halikarnassos | `ika` | 2 |
| CHIC #049 | Knossos | halikarnassos | `ikar` | 1 |
| CHIC #049 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #049 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #049 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #049 | Knossos | hierapytna | `era` | 2 |
| CHIC #049 | Knossos | hierapytna | `rap` | 1 |
| CHIC #049 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #049 | Knossos | ida | `ida` | 2 |
| CHIC #049 | Knossos | ikaria | `ari` | 1 |
| CHIC #049 | Knossos | ikaria | `ika` | 2 |
| CHIC #049 | Knossos | ikaria | `ikar` | 1 |
| CHIC #049 | Knossos | ikaria | `ikari` | 1 |
| CHIC #049 | Knossos | ikaria | `kar` | 1 |
| CHIC #049 | Knossos | ikaria | `kari` | 1 |
| CHIC #049 | Knossos | itanos | `ita` | 2 |
| CHIC #049 | Knossos | kalumnos | `alu` | 1 |
| CHIC #049 | Knossos | kalumnos | `kal` | 1 |
| CHIC #049 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #049 | Knossos | kor | `kor` | 1 |
| CHIC #049 | Knossos | korinthos | `kor` | 1 |
| CHIC #049 | Knossos | korinthos | `kori` | 1 |
| CHIC #049 | Knossos | korinthos | `ori` | 1 |
| CHIC #049 | Knossos | krete | `ete` | 3 |
| CHIC #049 | Knossos | krete | `ret` | 1 |
| CHIC #049 | Knossos | krete | `rete` | 1 |
| CHIC #049 | Knossos | kudonia | `udo` | 1 |
| CHIC #049 | Knossos | kuthera | `era` | 2 |
| CHIC #049 | Knossos | kuthera | `kut` | 1 |
| CHIC #049 | Knossos | kuzikos | `iko` | 2 |
| CHIC #049 | Knossos | lab | `lab` | 1 |
| CHIC #049 | Knossos | lebena | `ebe` | 2 |
| CHIC #049 | Knossos | lebena | `leb` | 1 |
| CHIC #049 | Knossos | lebena | `lebe` | 1 |
| CHIC #049 | Knossos | lukia | `luk` | 1 |
| CHIC #049 | Knossos | lukia | `luki` | 1 |
| CHIC #049 | Knossos | lukia | `uki` | 1 |
| CHIC #049 | Knossos | lykabettos | `abe` | 1 |
| CHIC #049 | Knossos | lykabettos | `bet` | 1 |
| CHIC #049 | Knossos | melitos | `eli` | 2 |
| CHIC #049 | Knossos | melitos | `ito` | 2 |
| CHIC #049 | Knossos | melitos | `lit` | 1 |
| CHIC #049 | Knossos | melitos | `lito` | 1 |
| CHIC #049 | Knossos | melos | `elo` | 2 |
| CHIC #049 | Knossos | muke | `uke` | 1 |
| CHIC #049 | Knossos | mukenai | `uke` | 1 |
| CHIC #049 | Knossos | olous | `olo` | 1 |
| CHIC #049 | Knossos | olu | `olu` | 1 |
| CHIC #049 | Knossos | olunthos | `olu` | 1 |
| CHIC #049 | Knossos | par | `par` | 1 |
| CHIC #049 | Knossos | parnassos | `par` | 1 |
| CHIC #049 | Knossos | paros | `aro` | 1 |
| CHIC #049 | Knossos | paros | `par` | 1 |
| CHIC #049 | Knossos | paros | `paro` | 1 |
| CHIC #049 | Knossos | per | `per` | 1 |
| CHIC #049 | Knossos | pergamos | `per` | 1 |
| CHIC #049 | Knossos | phalasarna | `ala` | 1 |
| CHIC #049 | Knossos | poikilassos | `iki` | 2 |
| CHIC #049 | Knossos | poikilassos | `ikil` | 1 |
| CHIC #049 | Knossos | poikilassos | `ikila` | 1 |
| CHIC #049 | Knossos | poikilassos | `ila` | 1 |
| CHIC #049 | Knossos | poikilassos | `kil` | 1 |
| CHIC #049 | Knossos | poikilassos | `kila` | 1 |
| CHIC #049 | Knossos | probalinthos | `ali` | 1 |
| CHIC #049 | Knossos | probalinthos | `bal` | 1 |
| CHIC #049 | Knossos | probalinthos | `bali` | 1 |
| CHIC #049 | Knossos | probalinthos | `oba` | 1 |
| CHIC #049 | Knossos | probalinthos | `rob` | 1 |
| CHIC #049 | Knossos | probalinthos | `roba` | 1 |
| CHIC #049 | Knossos | pulos | `pul` | 1 |
| CHIC #049 | Knossos | pulos | `pulo` | 1 |
| CHIC #049 | Knossos | pulos | `ulo` | 1 |
| CHIC #049 | Knossos | salaminos | `ala` | 1 |
| CHIC #049 | Knossos | sparta | `par` | 1 |
| CHIC #049 | Knossos | tarra | `tar` | 1 |
| CHIC #049 | Knossos | tarsos | `tar` | 1 |
| CHIC #049 | Knossos | tegea | `ege` | 2 |
| CHIC #049 | Knossos | telmessos | `tel` | 1 |
| CHIC #049 | Knossos | ter | `ter` | 1 |
| CHIC #049 | Knossos | termessos | `ter` | 1 |
| CHIC #049 | Knossos | thebai | `eba` | 2 |
| CHIC #049 | Knossos | thera | `era` | 2 |
| CHIC #049 | Knossos | tirintha | `iri` | 1 |
| CHIC #049 | Knossos | tirintha | `tir` | 1 |
| CHIC #049 | Knossos | tirintha | `tiri` | 1 |
| CHIC #049 | Knossos | tiruns | `iru` | 1 |
| CHIC #049 | Knossos | tiruns | `tir` | 1 |
| CHIC #049 | Knossos | tiruns | `tiru` | 1 |
| CHIC #049 | Knossos | tul | `tul` | 1 |
| CHIC #049 | Knossos | tulisos | `tul` | 1 |
| CHIC #049 | Knossos | tulisos | `tuli` | 1 |
| CHIC #049 | Knossos | tulisos | `uli` | 1 |
| CHIC #049 | Knossos | tulissos | `tul` | 1 |
| CHIC #049 | Knossos | tulissos | `tuli` | 1 |
| CHIC #049 | Knossos | tulissos | `uli` | 1 |
| CHIC #049 | Knossos | zakuntos | `aku` | 1 |
| CHIC #052 | Knossos | ala | `ala` | 1 |
| CHIC #052 | Knossos | aleksandros | `ale` | 1 |
| CHIC #052 | Knossos | aptara | `ara` | 2 |
| CHIC #052 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #052 | Knossos | hierapytna | `era` | 2 |
| CHIC #052 | Knossos | ikaria | `ari` | 1 |
| CHIC #052 | Knossos | kalumnos | `alu` | 1 |
| CHIC #052 | Knossos | korinthos | `ori` | 1 |
| CHIC #052 | Knossos | krete | `ete` | 2 |
| CHIC #052 | Knossos | krete | `ret` | 1 |
| CHIC #052 | Knossos | krete | `rete` | 1 |
| CHIC #052 | Knossos | kuthera | `era` | 2 |
| CHIC #052 | Knossos | melitos | `eli` | 1 |
| CHIC #052 | Knossos | melitos | `elit` | 1 |
| CHIC #052 | Knossos | melitos | `lit` | 1 |
| CHIC #052 | Knossos | melos | `elo` | 1 |
| CHIC #052 | Knossos | olous | `olo` | 1 |
| CHIC #052 | Knossos | olu | `olu` | 1 |
| CHIC #052 | Knossos | olunthos | `olu` | 1 |
| CHIC #052 | Knossos | paros | `aro` | 1 |
| CHIC #052 | Knossos | phalasarna | `ala` | 1 |
| CHIC #052 | Knossos | poikilassos | `ila` | 1 |
| CHIC #052 | Knossos | probalinthos | `ali` | 1 |
| CHIC #052 | Knossos | pulos | `ulo` | 1 |
| CHIC #052 | Knossos | salaminos | `ala` | 1 |
| CHIC #052 | Knossos | ter | `ter` | 1 |
| CHIC #052 | Knossos | termessos | `ter` | 1 |
| CHIC #052 | Knossos | thera | `era` | 2 |
| CHIC #052 | Knossos | tirintha | `iri` | 1 |
| CHIC #052 | Knossos | tiruns | `iru` | 1 |
| CHIC #052 | Knossos | tulisos | `uli` | 1 |
| CHIC #052 | Knossos | tulissos | `uli` | 1 |
| CHIC #053 | Knossos | ala | `ala` | 1 |
| CHIC #053 | Knossos | aleksandros | `ale` | 1 |
| CHIC #053 | Knossos | aptara | `ara` | 1 |
| CHIC #053 | Knossos | aptara | `tar` | 2 |
| CHIC #053 | Knossos | aptara | `tara` | 1 |
| CHIC #053 | Knossos | gor | `gor` | 2 |
| CHIC #053 | Knossos | gortyn | `gor` | 2 |
| CHIC #053 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #053 | Knossos | halikarnassos | `kar` | 2 |
| CHIC #053 | Knossos | hierapytna | `era` | 1 |
| CHIC #053 | Knossos | ikaria | `ari` | 1 |
| CHIC #053 | Knossos | ikaria | `kar` | 2 |
| CHIC #053 | Knossos | ikaria | `kari` | 1 |
| CHIC #053 | Knossos | kalumnos | `alu` | 1 |
| CHIC #053 | Knossos | kalumnos | `kal` | 1 |
| CHIC #053 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #053 | Knossos | kor | `kor` | 2 |
| CHIC #053 | Knossos | korinthos | `kor` | 2 |
| CHIC #053 | Knossos | korinthos | `kori` | 1 |
| CHIC #053 | Knossos | korinthos | `ori` | 1 |
| CHIC #053 | Knossos | kuthera | `era` | 1 |
| CHIC #053 | Knossos | melitos | `eli` | 1 |
| CHIC #053 | Knossos | melos | `elo` | 1 |
| CHIC #053 | Knossos | olous | `olo` | 1 |
| CHIC #053 | Knossos | olu | `olu` | 1 |
| CHIC #053 | Knossos | olunthos | `olu` | 1 |
| CHIC #053 | Knossos | par | `par` | 2 |
| CHIC #053 | Knossos | parnassos | `par` | 2 |
| CHIC #053 | Knossos | paros | `aro` | 2 |
| CHIC #053 | Knossos | paros | `par` | 2 |
| CHIC #053 | Knossos | paros | `paro` | 2 |
| CHIC #053 | Knossos | per | `per` | 2 |
| CHIC #053 | Knossos | pergamos | `per` | 2 |
| CHIC #053 | Knossos | phalasarna | `ala` | 1 |
| CHIC #053 | Knossos | poikilassos | `ila` | 1 |
| CHIC #053 | Knossos | poikilassos | `kil` | 1 |
| CHIC #053 | Knossos | poikilassos | `kila` | 1 |
| CHIC #053 | Knossos | probalinthos | `ali` | 1 |
| CHIC #053 | Knossos | probalinthos | `bal` | 1 |
| CHIC #053 | Knossos | probalinthos | `bali` | 1 |
| CHIC #053 | Knossos | probalinthos | `oba` | 1 |
| CHIC #053 | Knossos | probalinthos | `rob` | 1 |
| CHIC #053 | Knossos | probalinthos | `roba` | 1 |
| CHIC #053 | Knossos | pulos | `pul` | 1 |
| CHIC #053 | Knossos | pulos | `pulo` | 1 |
| CHIC #053 | Knossos | pulos | `ulo` | 1 |
| CHIC #053 | Knossos | salaminos | `ala` | 1 |
| CHIC #053 | Knossos | sparta | `par` | 2 |
| CHIC #053 | Knossos | tarra | `tar` | 2 |
| CHIC #053 | Knossos | tarsos | `tar` | 2 |
| CHIC #053 | Knossos | telmessos | `tel` | 1 |
| CHIC #053 | Knossos | ter | `ter` | 2 |
| CHIC #053 | Knossos | termessos | `ter` | 2 |
| CHIC #053 | Knossos | thera | `era` | 1 |
| CHIC #053 | Knossos | tirintha | `iri` | 1 |
| CHIC #053 | Knossos | tirintha | `tir` | 2 |
| CHIC #053 | Knossos | tirintha | `tiri` | 1 |
| CHIC #053 | Knossos | tiruns | `iru` | 1 |
| CHIC #053 | Knossos | tiruns | `tir` | 2 |
| CHIC #053 | Knossos | tiruns | `tiru` | 1 |
| CHIC #053 | Knossos | tul | `tul` | 1 |
| CHIC #053 | Knossos | tulisos | `tul` | 1 |
| CHIC #053 | Knossos | tulisos | `tuli` | 1 |
| CHIC #053 | Knossos | tulisos | `uli` | 1 |
| CHIC #053 | Knossos | tulissos | `tul` | 1 |
| CHIC #053 | Knossos | tulissos | `tuli` | 1 |
| CHIC #053 | Knossos | tulissos | `uli` | 1 |
| CHIC #054 | Knossos | paros | `aro` | 1 |
| CHIC #055 | Knossos | aptara | `ara` | 1 |
| CHIC #055 | Knossos | hierapytna | `era` | 1 |
| CHIC #055 | Knossos | hierapytna | `rap` | 1 |
| CHIC #055 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #055 | Knossos | kuthera | `era` | 1 |
| CHIC #055 | Knossos | lykabettos | `abe` | 1 |
| CHIC #055 | Knossos | thera | `era` | 1 |
| CHIC #055 | Knossos | zakuntos | `aku` | 1 |
| CHIC #056 | Knossos | hierapytna | `era` | 1 |
| CHIC #056 | Knossos | kuthera | `era` | 1 |
| CHIC #056 | Knossos | paros | `aro` | 1 |
| CHIC #056 | Knossos | thera | `era` | 1 |
| CHIC #057 | Knossos | ala | `ala` | 3 |
| CHIC #057 | Knossos | aleksandros | `ale` | 3 |
| CHIC #057 | Knossos | aleksandros | `alek` | 1 |
| CHIC #057 | Knossos | aleksandros | `lek` | 1 |
| CHIC #057 | Knossos | aptara | `ara` | 3 |
| CHIC #057 | Knossos | halikarnassos | `ali` | 3 |
| CHIC #057 | Knossos | halikarnassos | `alik` | 1 |
| CHIC #057 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #057 | Knossos | hierapytna | `era` | 2 |
| CHIC #057 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #057 | Knossos | ikaria | `ari` | 3 |
| CHIC #057 | Knossos | kalumnos | `alu` | 3 |
| CHIC #057 | Knossos | korinthos | `ori` | 2 |
| CHIC #057 | Knossos | kuthera | `era` | 2 |
| CHIC #057 | Knossos | lukia | `luk` | 1 |
| CHIC #057 | Knossos | lukia | `luki` | 1 |
| CHIC #057 | Knossos | lukia | `uki` | 1 |
| CHIC #057 | Knossos | melitos | `eli` | 2 |
| CHIC #057 | Knossos | melos | `elo` | 2 |
| CHIC #057 | Knossos | olous | `olo` | 2 |
| CHIC #057 | Knossos | olu | `olu` | 2 |
| CHIC #057 | Knossos | olunthos | `olu` | 2 |
| CHIC #057 | Knossos | paros | `aro` | 3 |
| CHIC #057 | Knossos | phalasarna | `ala` | 3 |
| CHIC #057 | Knossos | poikilassos | `iki` | 1 |
| CHIC #057 | Knossos | poikilassos | `ikil` | 1 |
| CHIC #057 | Knossos | poikilassos | `ikila` | 1 |
| CHIC #057 | Knossos | poikilassos | `ila` | 3 |
| CHIC #057 | Knossos | poikilassos | `kil` | 1 |
| CHIC #057 | Knossos | poikilassos | `kila` | 1 |
| CHIC #057 | Knossos | probalinthos | `ali` | 3 |
| CHIC #057 | Knossos | pulos | `ulo` | 3 |
| CHIC #057 | Knossos | salaminos | `ala` | 3 |
| CHIC #057 | Knossos | smurna | `mur` | 1 |
| CHIC #057 | Knossos | thera | `era` | 2 |
| CHIC #057 | Knossos | tirintha | `iri` | 3 |
| CHIC #057 | Knossos | tiruns | `iru` | 3 |
| CHIC #057 | Knossos | tulisos | `uli` | 3 |
| CHIC #057 | Knossos | tulissos | `uli` | 3 |
| CHIC #058 | Knossos | ala | `ala` | 2 |
| CHIC #058 | Knossos | aleksandros | `ale` | 2 |
| CHIC #058 | Knossos | aleksandros | `alek` | 1 |
| CHIC #058 | Knossos | aleksandros | `lek` | 1 |
| CHIC #058 | Knossos | aptara | `ara` | 4 |
| CHIC #058 | Knossos | dikte | `dik` | 2 |
| CHIC #058 | Knossos | halikarnassos | `ali` | 2 |
| CHIC #058 | Knossos | halikarnassos | `alik` | 1 |
| CHIC #058 | Knossos | halikarnassos | `alika` | 1 |
| CHIC #058 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #058 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #058 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #058 | Knossos | hierapytna | `era` | 2 |
| CHIC #058 | Knossos | hierapytna | `rap` | 2 |
| CHIC #058 | Knossos | hyakinthos | `aki` | 4 |
| CHIC #058 | Knossos | ida | `ida` | 1 |
| CHIC #058 | Knossos | ikaria | `ari` | 2 |
| CHIC #058 | Knossos | ikaria | `ika` | 1 |
| CHIC #058 | Knossos | itanos | `ita` | 1 |
| CHIC #058 | Knossos | kalumnos | `alu` | 2 |
| CHIC #058 | Knossos | korinthos | `ori` | 1 |
| CHIC #058 | Knossos | krete | `ete` | 1 |
| CHIC #058 | Knossos | krete | `ret` | 1 |
| CHIC #058 | Knossos | krete | `rete` | 1 |
| CHIC #058 | Knossos | kudonia | `udo` | 1 |
| CHIC #058 | Knossos | kuthera | `era` | 2 |
| CHIC #058 | Knossos | kuzikos | `iko` | 1 |
| CHIC #058 | Knossos | lab | `lab` | 1 |
| CHIC #058 | Knossos | lebena | `ebe` | 1 |
| CHIC #058 | Knossos | lebena | `leb` | 1 |
| CHIC #058 | Knossos | lebena | `lebe` | 1 |
| CHIC #058 | Knossos | lukia | `luk` | 1 |
| CHIC #058 | Knossos | lukia | `luki` | 1 |
| CHIC #058 | Knossos | lukia | `uki` | 3 |
| CHIC #058 | Knossos | lykabettos | `abe` | 2 |
| CHIC #058 | Knossos | melitos | `eli` | 1 |
| CHIC #058 | Knossos | melitos | `ito` | 1 |
| CHIC #058 | Knossos | melitos | `lit` | 1 |
| CHIC #058 | Knossos | melitos | `lito` | 1 |
| CHIC #058 | Knossos | melos | `elo` | 1 |
| CHIC #058 | Knossos | muke | `uke` | 1 |
| CHIC #058 | Knossos | mukenai | `uke` | 1 |
| CHIC #058 | Knossos | olous | `olo` | 1 |
| CHIC #058 | Knossos | olu | `olu` | 1 |
| CHIC #058 | Knossos | olunthos | `olu` | 1 |
| CHIC #058 | Knossos | paros | `aro` | 3 |
| CHIC #058 | Knossos | phalasarna | `ala` | 2 |
| CHIC #058 | Knossos | poikilassos | `iki` | 3 |
| CHIC #058 | Knossos | poikilassos | `ikil` | 1 |
| CHIC #058 | Knossos | poikilassos | `ikila` | 1 |
| CHIC #058 | Knossos | poikilassos | `ila` | 3 |
| CHIC #058 | Knossos | poikilassos | `kil` | 1 |
| CHIC #058 | Knossos | poikilassos | `kila` | 1 |
| CHIC #058 | Knossos | probalinthos | `ali` | 2 |
| CHIC #058 | Knossos | probalinthos | `oba` | 1 |
| CHIC #058 | Knossos | probalinthos | `rob` | 1 |
| CHIC #058 | Knossos | probalinthos | `roba` | 1 |
| CHIC #058 | Knossos | pulos | `ulo` | 1 |
| CHIC #058 | Knossos | salaminos | `ala` | 2 |
| CHIC #058 | Knossos | tegea | `ege` | 1 |
| CHIC #058 | Knossos | thebai | `eba` | 1 |
| CHIC #058 | Knossos | thera | `era` | 2 |
| CHIC #058 | Knossos | tirintha | `iri` | 3 |
| CHIC #058 | Knossos | tiruns | `iru` | 3 |
| CHIC #058 | Knossos | tulisos | `uli` | 1 |
| CHIC #058 | Knossos | tulissos | `uli` | 1 |
| CHIC #058 | Knossos | zakuntos | `aku` | 2 |
| CHIC #059 | Knossos | ala | `ala` | 1 |
| CHIC #059 | Knossos | aleksandros | `ale` | 1 |
| CHIC #059 | Knossos | aptara | `ara` | 3 |
| CHIC #059 | Knossos | aptara | `tar` | 2 |
| CHIC #059 | Knossos | aptara | `tara` | 2 |
| CHIC #059 | Knossos | gor | `gor` | 2 |
| CHIC #059 | Knossos | gortyn | `gor` | 2 |
| CHIC #059 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #059 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #059 | Knossos | halikarnassos | `kar` | 2 |
| CHIC #059 | Knossos | hierapytna | `era` | 3 |
| CHIC #059 | Knossos | hymettos | `met` | 1 |
| CHIC #059 | Knossos | ida | `ida` | 1 |
| CHIC #059 | Knossos | ikaria | `ari` | 1 |
| CHIC #059 | Knossos | ikaria | `ika` | 1 |
| CHIC #059 | Knossos | ikaria | `kar` | 2 |
| CHIC #059 | Knossos | itanos | `ita` | 1 |
| CHIC #059 | Knossos | kalumnos | `alu` | 1 |
| CHIC #059 | Knossos | kor | `kor` | 2 |
| CHIC #059 | Knossos | korinthos | `kor` | 2 |
| CHIC #059 | Knossos | korinthos | `ori` | 1 |
| CHIC #059 | Knossos | krete | `ete` | 1 |
| CHIC #059 | Knossos | kudonia | `kud` | 1 |
| CHIC #059 | Knossos | kudonia | `oni` | 1 |
| CHIC #059 | Knossos | kuthera | `era` | 3 |
| CHIC #059 | Knossos | kuzikos | `iko` | 1 |
| CHIC #059 | Knossos | melitos | `eli` | 1 |
| CHIC #059 | Knossos | melitos | `ito` | 1 |
| CHIC #059 | Knossos | melos | `elo` | 1 |
| CHIC #059 | Knossos | olous | `olo` | 1 |
| CHIC #059 | Knossos | olu | `olu` | 1 |
| CHIC #059 | Knossos | olunthos | `olu` | 1 |
| CHIC #059 | Knossos | orchomenos | `ome` | 1 |
| CHIC #059 | Knossos | par | `par` | 2 |
| CHIC #059 | Knossos | parnassos | `par` | 2 |
| CHIC #059 | Knossos | paros | `aro` | 1 |
| CHIC #059 | Knossos | paros | `par` | 2 |
| CHIC #059 | Knossos | per | `per` | 2 |
| CHIC #059 | Knossos | pergamos | `per` | 2 |
| CHIC #059 | Knossos | phalasarna | `ala` | 1 |
| CHIC #059 | Knossos | poikilassos | `iki` | 1 |
| CHIC #059 | Knossos | poikilassos | `ila` | 2 |
| CHIC #059 | Knossos | probalinthos | `ali` | 1 |
| CHIC #059 | Knossos | pulos | `ulo` | 1 |
| CHIC #059 | Knossos | salaminos | `ala` | 1 |
| CHIC #059 | Knossos | sparta | `par` | 2 |
| CHIC #059 | Knossos | tarra | `tar` | 2 |
| CHIC #059 | Knossos | tarsos | `tar` | 2 |
| CHIC #059 | Knossos | ter | `ter` | 2 |
| CHIC #059 | Knossos | termessos | `ter` | 2 |
| CHIC #059 | Knossos | thera | `era` | 3 |
| CHIC #059 | Knossos | tirintha | `iri` | 2 |
| CHIC #059 | Knossos | tirintha | `tir` | 3 |
| CHIC #059 | Knossos | tirintha | `tiri` | 1 |
| CHIC #059 | Knossos | tiruns | `iru` | 2 |
| CHIC #059 | Knossos | tiruns | `tir` | 3 |
| CHIC #059 | Knossos | tiruns | `tiru` | 1 |
| CHIC #059 | Knossos | tulisos | `uli` | 1 |
| CHIC #059 | Knossos | tulissos | `uli` | 1 |
| CHIC #060 | Knossos | pergamos | `gam` | 1 |
| CHIC #061 | Knossos | ala | `ala` | 2 |
| CHIC #061 | Knossos | aleksandros | `ale` | 2 |
| CHIC #061 | Knossos | aleksandros | `lek` | 3 |
| CHIC #061 | Knossos | aptara | `ara` | 4 |
| CHIC #061 | Knossos | aptara | `tar` | 2 |
| CHIC #061 | Knossos | aptara | `tara` | 1 |
| CHIC #061 | Knossos | gor | `gor` | 2 |
| CHIC #061 | Knossos | gortyn | `gor` | 2 |
| CHIC #061 | Knossos | halikarnassos | `ali` | 2 |
| CHIC #061 | Knossos | halikarnassos | `ika` | 2 |
| CHIC #061 | Knossos | halikarnassos | `kar` | 2 |
| CHIC #061 | Knossos | halikarnassos | `lik` | 3 |
| CHIC #061 | Knossos | halikarnassos | `lika` | 2 |
| CHIC #061 | Knossos | hierapytna | `era` | 3 |
| CHIC #061 | Knossos | hierapytna | `rap` | 2 |
| CHIC #061 | Knossos | hyakinthos | `aki` | 4 |
| CHIC #061 | Knossos | ida | `ida` | 2 |
| CHIC #061 | Knossos | ikaria | `ari` | 2 |
| CHIC #061 | Knossos | ikaria | `ika` | 2 |
| CHIC #061 | Knossos | ikaria | `kar` | 2 |
| CHIC #061 | Knossos | itanos | `ita` | 2 |
| CHIC #061 | Knossos | kalumnos | `alu` | 2 |
| CHIC #061 | Knossos | kor | `kor` | 2 |
| CHIC #061 | Knossos | korinthos | `kor` | 2 |
| CHIC #061 | Knossos | korinthos | `ori` | 2 |
| CHIC #061 | Knossos | krete | `ete` | 3 |
| CHIC #061 | Knossos | krete | `ret` | 2 |
| CHIC #061 | Knossos | krete | `rete` | 2 |
| CHIC #061 | Knossos | kudonia | `udo` | 2 |
| CHIC #061 | Knossos | kuthera | `era` | 3 |
| CHIC #061 | Knossos | kuzikos | `iko` | 2 |
| CHIC #061 | Knossos | lab | `lab` | 2 |
| CHIC #061 | Knossos | lebena | `ebe` | 3 |
| CHIC #061 | Knossos | lebena | `leb` | 2 |
| CHIC #061 | Knossos | lebena | `lebe` | 2 |
| CHIC #061 | Knossos | lukia | `luk` | 3 |
| CHIC #061 | Knossos | lukia | `luki` | 3 |
| CHIC #061 | Knossos | lukia | `uki` | 3 |
| CHIC #061 | Knossos | lykabettos | `abe` | 3 |
| CHIC #061 | Knossos | melitos | `eli` | 2 |
| CHIC #061 | Knossos | melitos | `ito` | 2 |
| CHIC #061 | Knossos | melitos | `lit` | 2 |
| CHIC #061 | Knossos | melitos | `lito` | 2 |
| CHIC #061 | Knossos | melos | `elo` | 2 |
| CHIC #061 | Knossos | muke | `uke` | 2 |
| CHIC #061 | Knossos | mukenai | `uke` | 2 |
| CHIC #061 | Knossos | olous | `olo` | 2 |
| CHIC #061 | Knossos | olu | `olu` | 2 |
| CHIC #061 | Knossos | olunthos | `olu` | 2 |
| CHIC #061 | Knossos | par | `par` | 2 |
| CHIC #061 | Knossos | parnassos | `par` | 2 |
| CHIC #061 | Knossos | paros | `aro` | 3 |
| CHIC #061 | Knossos | paros | `par` | 2 |
| CHIC #061 | Knossos | paros | `paro` | 1 |
| CHIC #061 | Knossos | per | `per` | 2 |
| CHIC #061 | Knossos | pergamos | `per` | 2 |
| CHIC #061 | Knossos | phalasarna | `ala` | 2 |
| CHIC #061 | Knossos | poikilassos | `iki` | 3 |
| CHIC #061 | Knossos | poikilassos | `ila` | 2 |
| CHIC #061 | Knossos | probalinthos | `ali` | 2 |
| CHIC #061 | Knossos | probalinthos | `oba` | 2 |
| CHIC #061 | Knossos | probalinthos | `rob` | 2 |
| CHIC #061 | Knossos | probalinthos | `roba` | 2 |
| CHIC #061 | Knossos | pulos | `ulo` | 2 |
| CHIC #061 | Knossos | salaminos | `ala` | 2 |
| CHIC #061 | Knossos | sparta | `par` | 2 |
| CHIC #061 | Knossos | tarra | `tar` | 2 |
| CHIC #061 | Knossos | tarsos | `tar` | 2 |
| CHIC #061 | Knossos | tegea | `ege` | 3 |
| CHIC #061 | Knossos | ter | `ter` | 2 |
| CHIC #061 | Knossos | termessos | `ter` | 2 |
| CHIC #061 | Knossos | thebai | `eba` | 3 |
| CHIC #061 | Knossos | thera | `era` | 3 |
| CHIC #061 | Knossos | tirintha | `iri` | 2 |
| CHIC #061 | Knossos | tirintha | `tir` | 2 |
| CHIC #061 | Knossos | tiruns | `iru` | 2 |
| CHIC #061 | Knossos | tiruns | `tir` | 2 |
| CHIC #061 | Knossos | tulisos | `uli` | 2 |
| CHIC #061 | Knossos | tulissos | `uli` | 2 |
| CHIC #061 | Knossos | zakuntos | `aku` | 3 |
| CHIC #062 | Knossos | ala | `ala` | 1 |
| CHIC #062 | Knossos | aleksandros | `ale` | 1 |
| CHIC #062 | Knossos | aptara | `ara` | 1 |
| CHIC #062 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #062 | Knossos | ikaria | `ari` | 1 |
| CHIC #062 | Knossos | kalumnos | `alu` | 1 |
| CHIC #062 | Knossos | paros | `aro` | 1 |
| CHIC #062 | Knossos | phalasarna | `ala` | 1 |
| CHIC #062 | Knossos | probalinthos | `ali` | 1 |
| CHIC #062 | Knossos | salaminos | `ala` | 1 |
| CHIC #063 | Knossos | ardettos | `det` | 1 |
| CHIC #063 | Knossos | krete | `ete` | 1 |
| CHIC #065 | Knossos | ala | `ala` | 1 |
| CHIC #065 | Knossos | aleksandros | `ale` | 1 |
| CHIC #065 | Knossos | aptara | `ara` | 1 |
| CHIC #065 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #065 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #065 | Knossos | hierapytna | `era` | 1 |
| CHIC #065 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #065 | Knossos | hyakinthos | `yak` | 1 |
| CHIC #065 | Knossos | hyakinthos | `yaki` | 1 |
| CHIC #065 | Knossos | ida | `ida` | 1 |
| CHIC #065 | Knossos | ikaria | `ari` | 1 |
| CHIC #065 | Knossos | ikaria | `ika` | 1 |
| CHIC #065 | Knossos | itanos | `ita` | 1 |
| CHIC #065 | Knossos | kalumnos | `alu` | 1 |
| CHIC #065 | Knossos | kalumnos | `lum` | 1 |
| CHIC #065 | Knossos | korinthos | `ori` | 1 |
| CHIC #065 | Knossos | krete | `ete` | 1 |
| CHIC #065 | Knossos | kudonia | `kud` | 2 |
| CHIC #065 | Knossos | kudonia | `udo` | 1 |
| CHIC #065 | Knossos | kuthera | `era` | 1 |
| CHIC #065 | Knossos | kuzikos | `iko` | 1 |
| CHIC #065 | Knossos | lebena | `ebe` | 1 |
| CHIC #065 | Knossos | lem | `lem` | 1 |
| CHIC #065 | Knossos | lemnos | `lem` | 1 |
| CHIC #065 | Knossos | lukia | `uki` | 1 |
| CHIC #065 | Knossos | lykabettos | `abe` | 1 |
| CHIC #065 | Knossos | melitos | `eli` | 1 |
| CHIC #065 | Knossos | melitos | `ito` | 1 |
| CHIC #065 | Knossos | melos | `elo` | 1 |
| CHIC #065 | Knossos | muke | `uke` | 1 |
| CHIC #065 | Knossos | mukenai | `uke` | 1 |
| CHIC #065 | Knossos | olous | `olo` | 1 |
| CHIC #065 | Knossos | olu | `olu` | 1 |
| CHIC #065 | Knossos | olunthos | `olu` | 1 |
| CHIC #065 | Knossos | orchomenos | `ome` | 1 |
| CHIC #065 | Knossos | paros | `aro` | 1 |
| CHIC #065 | Knossos | phalasarna | `ala` | 1 |
| CHIC #065 | Knossos | poikilassos | `iki` | 1 |
| CHIC #065 | Knossos | poikilassos | `ila` | 1 |
| CHIC #065 | Knossos | probalinthos | `ali` | 1 |
| CHIC #065 | Knossos | probalinthos | `oba` | 1 |
| CHIC #065 | Knossos | pulos | `ulo` | 1 |
| CHIC #065 | Knossos | salaminos | `ala` | 1 |
| CHIC #065 | Knossos | salaminos | `lam` | 1 |
| CHIC #065 | Knossos | tegea | `ege` | 1 |
| CHIC #065 | Knossos | thebai | `eba` | 1 |
| CHIC #065 | Knossos | thera | `era` | 1 |
| CHIC #065 | Knossos | tirintha | `iri` | 1 |
| CHIC #065 | Knossos | tiruns | `iru` | 1 |
| CHIC #065 | Knossos | tulisos | `uli` | 1 |
| CHIC #065 | Knossos | tulissos | `uli` | 1 |
| CHIC #065 | Knossos | zakuntos | `aku` | 1 |
| CHIC #070 | Mallia | ala | `ala` | 1 |
| CHIC #070 | Mallia | aleksandros | `ale` | 1 |
| CHIC #070 | Mallia | aptara | `ara` | 1 |
| CHIC #070 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #070 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #070 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #070 | Mallia | ida | `ida` | 1 |
| CHIC #070 | Mallia | ikaria | `ari` | 1 |
| CHIC #070 | Mallia | ikaria | `aria` | 1 |
| CHIC #070 | Mallia | ikaria | `ika` | 1 |
| CHIC #070 | Mallia | ikaria | `ria` | 1 |
| CHIC #070 | Mallia | itanos | `ita` | 1 |
| CHIC #070 | Mallia | kalumnos | `alu` | 1 |
| CHIC #070 | Mallia | krete | `ete` | 1 |
| CHIC #070 | Mallia | kudonia | `udo` | 1 |
| CHIC #070 | Mallia | kuzikos | `iko` | 1 |
| CHIC #070 | Mallia | lebena | `ebe` | 1 |
| CHIC #070 | Mallia | lukia | `uki` | 1 |
| CHIC #070 | Mallia | lykabettos | `abe` | 1 |
| CHIC #070 | Mallia | melitos | `ito` | 1 |
| CHIC #070 | Mallia | muke | `uke` | 1 |
| CHIC #070 | Mallia | mukenai | `uke` | 1 |
| CHIC #070 | Mallia | olous | `lou` | 1 |
| CHIC #070 | Mallia | paros | `aro` | 1 |
| CHIC #070 | Mallia | phalasarna | `ala` | 1 |
| CHIC #070 | Mallia | poikilassos | `iki` | 1 |
| CHIC #070 | Mallia | poikilassos | `oik` | 1 |
| CHIC #070 | Mallia | poikilassos | `oiki` | 1 |
| CHIC #070 | Mallia | praisos | `rai` | 1 |
| CHIC #070 | Mallia | prie | `rie` | 1 |
| CHIC #070 | Mallia | priene | `rie` | 1 |
| CHIC #070 | Mallia | probalinthos | `ali` | 1 |
| CHIC #070 | Mallia | probalinthos | `oba` | 1 |
| CHIC #070 | Mallia | salaminos | `ala` | 1 |
| CHIC #070 | Mallia | tegea | `ege` | 1 |
| CHIC #070 | Mallia | thebai | `eba` | 1 |
| CHIC #070 | Mallia | zakuntos | `aku` | 1 |
| CHIC #071 | Mallia | aptara | `ara` | 1 |
| CHIC #071 | Mallia | aptara | `tar` | 1 |
| CHIC #071 | Mallia | aptara | `tara` | 1 |
| CHIC #071 | Mallia | gor | `gor` | 1 |
| CHIC #071 | Mallia | gortyn | `gor` | 1 |
| CHIC #071 | Mallia | halikarnassos | `kar` | 1 |
| CHIC #071 | Mallia | hierapytna | `era` | 1 |
| CHIC #071 | Mallia | ikaria | `kar` | 1 |
| CHIC #071 | Mallia | kor | `kor` | 1 |
| CHIC #071 | Mallia | korinthos | `kor` | 1 |
| CHIC #071 | Mallia | kuthera | `era` | 1 |
| CHIC #071 | Mallia | par | `par` | 1 |
| CHIC #071 | Mallia | parnassos | `par` | 1 |
| CHIC #071 | Mallia | paros | `par` | 1 |
| CHIC #071 | Mallia | per | `per` | 1 |
| CHIC #071 | Mallia | pergamos | `per` | 1 |
| CHIC #071 | Mallia | sparta | `par` | 1 |
| CHIC #071 | Mallia | tarra | `tar` | 1 |
| CHIC #071 | Mallia | tarsos | `tar` | 1 |
| CHIC #071 | Mallia | ter | `ter` | 1 |
| CHIC #071 | Mallia | termessos | `ter` | 1 |
| CHIC #071 | Mallia | thera | `era` | 1 |
| CHIC #071 | Mallia | tirintha | `tir` | 1 |
| CHIC #071 | Mallia | tiruns | `tir` | 1 |
| CHIC #072 | Mallia | praisos | `rai` | 1 |
| CHIC #073 | Mallia | ala | `ala` | 1 |
| CHIC #073 | Mallia | aleksandros | `ale` | 1 |
| CHIC #073 | Mallia | aptara | `ara` | 2 |
| CHIC #073 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #073 | Mallia | hierapytna | `era` | 2 |
| CHIC #073 | Mallia | ikaria | `ari` | 1 |
| CHIC #073 | Mallia | kalumnos | `alu` | 1 |
| CHIC #073 | Mallia | korinthos | `ori` | 1 |
| CHIC #073 | Mallia | kuthera | `era` | 2 |
| CHIC #073 | Mallia | melitos | `eli` | 1 |
| CHIC #073 | Mallia | melos | `elo` | 1 |
| CHIC #073 | Mallia | olous | `olo` | 1 |
| CHIC #073 | Mallia | olu | `olu` | 1 |
| CHIC #073 | Mallia | olunthos | `olu` | 1 |
| CHIC #073 | Mallia | paros | `aro` | 1 |
| CHIC #073 | Mallia | phalasarna | `ala` | 1 |
| CHIC #073 | Mallia | poikilassos | `ila` | 1 |
| CHIC #073 | Mallia | probalinthos | `ali` | 1 |
| CHIC #073 | Mallia | pulos | `ulo` | 1 |
| CHIC #073 | Mallia | salaminos | `ala` | 1 |
| CHIC #073 | Mallia | thera | `era` | 2 |
| CHIC #073 | Mallia | tirintha | `iri` | 1 |
| CHIC #073 | Mallia | tiruns | `iru` | 1 |
| CHIC #073 | Mallia | tulisos | `uli` | 1 |
| CHIC #073 | Mallia | tulissos | `uli` | 1 |
| CHIC #074 | Mallia | aptara | `ara` | 1 |
| CHIC #074 | Mallia | dikte | `dik` | 1 |
| CHIC #074 | Mallia | hierapytna | `rap` | 1 |
| CHIC #074 | Mallia | hyakinthos | `aki` | 2 |
| CHIC #074 | Mallia | lukia | `uki` | 1 |
| CHIC #074 | Mallia | lykabettos | `abe` | 1 |
| CHIC #074 | Mallia | poikilassos | `iki` | 1 |
| CHIC #074 | Mallia | zakuntos | `aku` | 1 |
| CHIC #075 | Mallia | ardettos | `det` | 1 |
| CHIC #075 | Mallia | dikte | `dik` | 1 |
| CHIC #075 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #075 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #075 | Mallia | ida | `ida` | 1 |
| CHIC #075 | Mallia | ikaria | `ika` | 1 |
| CHIC #075 | Mallia | itanos | `ita` | 1 |
| CHIC #075 | Mallia | krete | `ete` | 1 |
| CHIC #075 | Mallia | kudonia | `kud` | 1 |
| CHIC #075 | Mallia | kudonia | `kudo` | 1 |
| CHIC #075 | Mallia | kudonia | `udo` | 1 |
| CHIC #075 | Mallia | kuthera | `kut` | 1 |
| CHIC #075 | Mallia | kuzikos | `iko` | 1 |
| CHIC #075 | Mallia | lebena | `ebe` | 1 |
| CHIC #075 | Mallia | lukia | `uki` | 1 |
| CHIC #075 | Mallia | lykabettos | `abe` | 1 |
| CHIC #075 | Mallia | lykabettos | `bet` | 1 |
| CHIC #075 | Mallia | lykabettos | `kab` | 1 |
| CHIC #075 | Mallia | lykabettos | `kabe` | 1 |
| CHIC #075 | Mallia | melitos | `ito` | 1 |
| CHIC #075 | Mallia | muke | `uke` | 1 |
| CHIC #075 | Mallia | mukenai | `uke` | 1 |
| CHIC #075 | Mallia | poikilassos | `iki` | 1 |
| CHIC #075 | Mallia | probalinthos | `oba` | 1 |
| CHIC #075 | Mallia | tegea | `ege` | 1 |
| CHIC #075 | Mallia | tegea | `teg` | 1 |
| CHIC #075 | Mallia | tegea | `tege` | 1 |
| CHIC #075 | Mallia | thebai | `eba` | 1 |
| CHIC #075 | Mallia | zakuntos | `aku` | 1 |
| CHIC #076 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #076 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #076 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #076 | Mallia | hyakinthos | `yaki` | 1 |
| CHIC #076 | Mallia | ida | `ida` | 1 |
| CHIC #076 | Mallia | ikaria | `ika` | 1 |
| CHIC #076 | Mallia | itanos | `ita` | 1 |
| CHIC #076 | Mallia | krete | `ete` | 1 |
| CHIC #076 | Mallia | kudonia | `udo` | 1 |
| CHIC #076 | Mallia | kuzikos | `iko` | 1 |
| CHIC #076 | Mallia | lebena | `ebe` | 1 |
| CHIC #076 | Mallia | lukia | `uki` | 1 |
| CHIC #076 | Mallia | lykabettos | `abe` | 1 |
| CHIC #076 | Mallia | melitos | `ito` | 1 |
| CHIC #076 | Mallia | muke | `uke` | 1 |
| CHIC #076 | Mallia | mukenai | `uke` | 1 |
| CHIC #076 | Mallia | poikilassos | `iki` | 1 |
| CHIC #076 | Mallia | probalinthos | `oba` | 1 |
| CHIC #076 | Mallia | tegea | `ege` | 1 |
| CHIC #076 | Mallia | thebai | `eba` | 1 |
| CHIC #076 | Mallia | zakuntos | `aku` | 1 |
| CHIC #077 | Mallia | probalinthos | `oba` | 1 |
| CHIC #077 | Mallia | probalinthos | `rob` | 1 |
| CHIC #077 | Mallia | probalinthos | `roba` | 1 |
| CHIC #078 | Mallia | aleksandros | `lek` | 1 |
| CHIC #078 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #078 | Mallia | lukia | `luk` | 1 |
| CHIC #078 | Mallia | muke | `uke` | 1 |
| CHIC #078 | Mallia | mukenai | `uke` | 1 |
| CHIC #079 | Mallia | kalumnos | `lum` | 1 |
| CHIC #079 | Mallia | lem | `lem` | 1 |
| CHIC #079 | Mallia | lemnos | `lem` | 1 |
| CHIC #079 | Mallia | salaminos | `lam` | 1 |
| CHIC #080 | Mallia | paros | `aro` | 1 |
| CHIC #081 | Mallia | tirintha | `tir` | 1 |
| CHIC #081 | Mallia | tiruns | `tir` | 1 |
| CHIC #085 | Mallia | krete | `ete` | 1 |
| CHIC #085 | Mallia | krete | `ret` | 1 |
| CHIC #085 | Mallia | krete | `rete` | 1 |
| CHIC #085 | Mallia | melitos | `lit` | 1 |
| CHIC #086 | Mallia | ikaria | `ria` | 1 |
| CHIC #088 | Mallia | kudonia | `oni` | 1 |
| CHIC #089 | Mallia | hierapytna | `era` | 1 |
| CHIC #089 | Mallia | korinthos | `rin` | 1 |
| CHIC #089 | Mallia | kudonia | `oni` | 2 |
| CHIC #089 | Mallia | kuthera | `era` | 1 |
| CHIC #089 | Mallia | melitos | `eli` | 1 |
| CHIC #089 | Mallia | melos | `elo` | 1 |
| CHIC #089 | Mallia | olunthos | `lun` | 1 |
| CHIC #089 | Mallia | probalinthos | `lin` | 1 |
| CHIC #089 | Mallia | thera | `era` | 1 |
| CHIC #089 | Mallia | tirintha | `rin` | 1 |
| CHIC #089 | Mallia | tiruns | `run` | 1 |
| CHIC #090 | Mallia | aia | `aia` | 1 |
| CHIC #090 | Mallia | aios | `aio` | 1 |
| CHIC #090 | Mallia | lasaia | `aia` | 1 |
| CHIC #091 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #091 | Mallia | korinthos | `ori` | 1 |
| CHIC #091 | Mallia | lykabettos | `abe` | 1 |
| CHIC #091 | Mallia | olous | `olo` | 1 |
| CHIC #091 | Mallia | olu | `olu` | 1 |
| CHIC #091 | Mallia | olunthos | `olu` | 1 |
| CHIC #091 | Mallia | paros | `aro` | 1 |
| CHIC #091 | Mallia | zakuntos | `aku` | 1 |
| CHIC #097 | Mallia | aptara | `ara` | 1 |
| CHIC #097 | Mallia | aptara | `tar` | 1 |
| CHIC #097 | Mallia | aptara | `tara` | 1 |
| CHIC #097 | Mallia | gor | `gor` | 1 |
| CHIC #097 | Mallia | gortyn | `gor` | 1 |
| CHIC #097 | Mallia | halikarnassos | `kar` | 1 |
| CHIC #097 | Mallia | hierapytna | `era` | 1 |
| CHIC #097 | Mallia | ikaria | `kar` | 1 |
| CHIC #097 | Mallia | kor | `kor` | 1 |
| CHIC #097 | Mallia | korinthos | `kor` | 1 |
| CHIC #097 | Mallia | kuthera | `era` | 1 |
| CHIC #097 | Mallia | par | `par` | 1 |
| CHIC #097 | Mallia | parnassos | `par` | 1 |
| CHIC #097 | Mallia | paros | `par` | 1 |
| CHIC #097 | Mallia | per | `per` | 1 |
| CHIC #097 | Mallia | pergamos | `per` | 1 |
| CHIC #097 | Mallia | praisos | `rai` | 1 |
| CHIC #097 | Mallia | sparta | `par` | 1 |
| CHIC #097 | Mallia | tarra | `tar` | 1 |
| CHIC #097 | Mallia | tarsos | `tar` | 1 |
| CHIC #097 | Mallia | ter | `ter` | 1 |
| CHIC #097 | Mallia | termessos | `ter` | 1 |
| CHIC #097 | Mallia | thera | `era` | 1 |
| CHIC #097 | Mallia | tirintha | `tir` | 1 |
| CHIC #097 | Mallia | tiruns | `tir` | 1 |
| CHIC #098 | Mallia | aia | `aia` | 1 |
| CHIC #098 | Mallia | aios | `aio` | 1 |
| CHIC #098 | Mallia | lasaia | `aia` | 1 |
| CHIC #098 | Mallia | poikilassos | `poi` | 1 |
| CHIC #098 | Mallia | thebai | `bai` | 1 |
| CHIC #103 | Mallia | hierapytna | `rap` | 1 |
| CHIC #103 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #103 | Mallia | krete | `ete` | 1 |
| CHIC #103 | Mallia | lebena | `ebe` | 1 |
| CHIC #103 | Mallia | lykabettos | `abe` | 1 |
| CHIC #103 | Mallia | tegea | `ege` | 1 |
| CHIC #103 | Mallia | thebai | `eba` | 1 |
| CHIC #103 | Mallia | zakuntos | `aku` | 1 |
| CHIC #104 | Mallia | ardettos | `det` | 1 |
| CHIC #104 | Mallia | dikte | `dik` | 1 |
| CHIC #104 | Mallia | halikarnassos | `ika` | 2 |
| CHIC #104 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #104 | Mallia | ida | `ida` | 2 |
| CHIC #104 | Mallia | ikaria | `ika` | 2 |
| CHIC #104 | Mallia | itanos | `ita` | 2 |
| CHIC #104 | Mallia | krete | `ete` | 1 |
| CHIC #104 | Mallia | kudonia | `kud` | 1 |
| CHIC #104 | Mallia | kudonia | `kudo` | 1 |
| CHIC #104 | Mallia | kudonia | `udo` | 1 |
| CHIC #104 | Mallia | kuthera | `kut` | 1 |
| CHIC #104 | Mallia | kuzikos | `iko` | 2 |
| CHIC #104 | Mallia | lebena | `ebe` | 1 |
| CHIC #104 | Mallia | lukia | `uki` | 1 |
| CHIC #104 | Mallia | lykabettos | `abe` | 1 |
| CHIC #104 | Mallia | lykabettos | `bet` | 1 |
| CHIC #104 | Mallia | lykabettos | `kab` | 1 |
| CHIC #104 | Mallia | lykabettos | `kabe` | 1 |
| CHIC #104 | Mallia | melitos | `ito` | 2 |
| CHIC #104 | Mallia | muke | `uke` | 1 |
| CHIC #104 | Mallia | mukenai | `uke` | 1 |
| CHIC #104 | Mallia | poikilassos | `iki` | 2 |
| CHIC #104 | Mallia | probalinthos | `oba` | 1 |
| CHIC #104 | Mallia | tegea | `ege` | 1 |
| CHIC #104 | Mallia | tegea | `teg` | 1 |
| CHIC #104 | Mallia | tegea | `tege` | 1 |
| CHIC #104 | Mallia | thebai | `eba` | 1 |
| CHIC #104 | Mallia | zakuntos | `aku` | 1 |
| CHIC #109 | Mallia | hierapytna | `era` | 1 |
| CHIC #109 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #109 | Mallia | kuthera | `era` | 1 |
| CHIC #109 | Mallia | melitos | `eli` | 1 |
| CHIC #109 | Mallia | melos | `elo` | 1 |
| CHIC #109 | Mallia | muke | `uke` | 1 |
| CHIC #109 | Mallia | mukenai | `uke` | 1 |
| CHIC #109 | Mallia | thera | `era` | 1 |
| CHIC #110 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #110 | Mallia | ida | `ida` | 1 |
| CHIC #110 | Mallia | ikaria | `ika` | 1 |
| CHIC #110 | Mallia | itanos | `ita` | 1 |
| CHIC #110 | Mallia | kuzikos | `iko` | 1 |
| CHIC #110 | Mallia | melitos | `ito` | 1 |
| CHIC #110 | Mallia | poikilassos | `iki` | 1 |
| CHIC #113 | Mallia | ala | `ala` | 1 |
| CHIC #113 | Mallia | aleksandros | `ale` | 1 |
| CHIC #113 | Mallia | aptara | `ara` | 3 |
| CHIC #113 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #113 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #113 | Mallia | hierapytna | `era` | 4 |
| CHIC #113 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #113 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #113 | Mallia | hyakinthos | `yaki` | 1 |
| CHIC #113 | Mallia | ida | `ida` | 1 |
| CHIC #113 | Mallia | ikaria | `ari` | 1 |
| CHIC #113 | Mallia | ikaria | `ika` | 1 |
| CHIC #113 | Mallia | itanos | `ita` | 1 |
| CHIC #113 | Mallia | kalumnos | `alu` | 1 |
| CHIC #113 | Mallia | korinthos | `ori` | 1 |
| CHIC #113 | Mallia | krete | `ete` | 2 |
| CHIC #113 | Mallia | krete | `ret` | 1 |
| CHIC #113 | Mallia | krete | `rete` | 1 |
| CHIC #113 | Mallia | kudonia | `udo` | 1 |
| CHIC #113 | Mallia | kuthera | `era` | 4 |
| CHIC #113 | Mallia | kuzikos | `iko` | 1 |
| CHIC #113 | Mallia | lebena | `ebe` | 1 |
| CHIC #113 | Mallia | lukia | `uki` | 1 |
| CHIC #113 | Mallia | lykabettos | `abe` | 1 |
| CHIC #113 | Mallia | melitos | `eli` | 2 |
| CHIC #113 | Mallia | melitos | `elit` | 1 |
| CHIC #113 | Mallia | melitos | `ito` | 1 |
| CHIC #113 | Mallia | melitos | `lit` | 1 |
| CHIC #113 | Mallia | melos | `elo` | 2 |
| CHIC #113 | Mallia | muke | `uke` | 1 |
| CHIC #113 | Mallia | mukenai | `uke` | 1 |
| CHIC #113 | Mallia | olous | `olo` | 1 |
| CHIC #113 | Mallia | olu | `olu` | 1 |
| CHIC #113 | Mallia | olunthos | `olu` | 1 |
| CHIC #113 | Mallia | paros | `aro` | 1 |
| CHIC #113 | Mallia | pergamos | `gam` | 1 |
| CHIC #113 | Mallia | phalasarna | `ala` | 1 |
| CHIC #113 | Mallia | poikilassos | `iki` | 1 |
| CHIC #113 | Mallia | poikilassos | `ila` | 1 |
| CHIC #113 | Mallia | probalinthos | `ali` | 1 |
| CHIC #113 | Mallia | probalinthos | `oba` | 1 |
| CHIC #113 | Mallia | pulos | `ulo` | 1 |
| CHIC #113 | Mallia | salaminos | `ala` | 1 |
| CHIC #113 | Mallia | tegea | `ege` | 1 |
| CHIC #113 | Mallia | thebai | `eba` | 1 |
| CHIC #113 | Mallia | thera | `era` | 4 |
| CHIC #113 | Mallia | tirintha | `iri` | 1 |
| CHIC #113 | Mallia | tiruns | `iru` | 1 |
| CHIC #113 | Mallia | tulisos | `uli` | 1 |
| CHIC #113 | Mallia | tulissos | `uli` | 1 |
| CHIC #113 | Mallia | zakuntos | `aku` | 1 |
| CHIC #115 | Mallia | hierapytna | `era` | 1 |
| CHIC #115 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #115 | Mallia | kuthera | `era` | 1 |
| CHIC #115 | Mallia | lykabettos | `abe` | 1 |
| CHIC #115 | Mallia | melitos | `eli` | 1 |
| CHIC #115 | Mallia | melitos | `mel` | 1 |
| CHIC #115 | Mallia | melitos | `meli` | 1 |
| CHIC #115 | Mallia | melos | `elo` | 1 |
| CHIC #115 | Mallia | melos | `mel` | 1 |
| CHIC #115 | Mallia | melos | `melo` | 1 |
| CHIC #115 | Mallia | thera | `era` | 1 |
| CHIC #115 | Mallia | zakuntos | `aku` | 1 |
| CHIC #117 | Mallia | aleksandros | `lek` | 1 |
| CHIC #117 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #117 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #117 | Mallia | halikarnassos | `lika` | 1 |
| CHIC #117 | Mallia | hierapytna | `rap` | 1 |
| CHIC #117 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #117 | Mallia | ida | `ida` | 1 |
| CHIC #117 | Mallia | ikaria | `ika` | 1 |
| CHIC #117 | Mallia | itanos | `ita` | 1 |
| CHIC #117 | Mallia | keos | `keo` | 1 |
| CHIC #117 | Mallia | krete | `ete` | 1 |
| CHIC #117 | Mallia | krete | `ret` | 1 |
| CHIC #117 | Mallia | krete | `rete` | 1 |
| CHIC #117 | Mallia | kudonia | `udo` | 1 |
| CHIC #117 | Mallia | kuzikos | `iko` | 1 |
| CHIC #117 | Mallia | lab | `lab` | 1 |
| CHIC #117 | Mallia | lebena | `ebe` | 1 |
| CHIC #117 | Mallia | lebena | `leb` | 1 |
| CHIC #117 | Mallia | lebena | `lebe` | 1 |
| CHIC #117 | Mallia | lukia | `kia` | 1 |
| CHIC #117 | Mallia | lukia | `luk` | 1 |
| CHIC #117 | Mallia | lukia | `luki` | 1 |
| CHIC #117 | Mallia | lukia | `uki` | 1 |
| CHIC #117 | Mallia | lykabettos | `abe` | 1 |
| CHIC #117 | Mallia | melitos | `ito` | 1 |
| CHIC #117 | Mallia | melitos | `lit` | 1 |
| CHIC #117 | Mallia | melitos | `lito` | 1 |
| CHIC #117 | Mallia | muke | `uke` | 1 |
| CHIC #117 | Mallia | mukenai | `uke` | 1 |
| CHIC #117 | Mallia | poikilassos | `iki` | 1 |
| CHIC #117 | Mallia | poikilassos | `poi` | 1 |
| CHIC #117 | Mallia | probalinthos | `oba` | 1 |
| CHIC #117 | Mallia | probalinthos | `rob` | 1 |
| CHIC #117 | Mallia | probalinthos | `roba` | 1 |
| CHIC #117 | Mallia | rhytion | `tio` | 1 |
| CHIC #117 | Mallia | tegea | `ege` | 1 |
| CHIC #117 | Mallia | tegea | `gea` | 1 |
| CHIC #117 | Mallia | thebai | `bai` | 1 |
| CHIC #117 | Mallia | thebai | `eba` | 1 |
| CHIC #117 | Mallia | zakuntos | `aku` | 1 |
| CHIC #118 | Mallia | aptara | `ara` | 1 |
| CHIC #118 | Mallia | aptara | `tar` | 1 |
| CHIC #118 | Mallia | aptara | `tara` | 1 |
| CHIC #118 | Mallia | gor | `gor` | 1 |
| CHIC #118 | Mallia | gortyn | `gor` | 1 |
| CHIC #118 | Mallia | halikarnassos | `kar` | 1 |
| CHIC #118 | Mallia | hierapytna | `era` | 1 |
| CHIC #118 | Mallia | ikaria | `kar` | 1 |
| CHIC #118 | Mallia | kor | `kor` | 1 |
| CHIC #118 | Mallia | korinthos | `kor` | 1 |
| CHIC #118 | Mallia | kuthera | `era` | 1 |
| CHIC #118 | Mallia | par | `par` | 1 |
| CHIC #118 | Mallia | parnassos | `par` | 1 |
| CHIC #118 | Mallia | paros | `par` | 1 |
| CHIC #118 | Mallia | per | `per` | 1 |
| CHIC #118 | Mallia | pergamos | `per` | 1 |
| CHIC #118 | Mallia | sparta | `par` | 1 |
| CHIC #118 | Mallia | tarra | `tar` | 1 |
| CHIC #118 | Mallia | tarsos | `tar` | 1 |
| CHIC #118 | Mallia | ter | `ter` | 1 |
| CHIC #118 | Mallia | termessos | `ter` | 1 |
| CHIC #118 | Mallia | thera | `era` | 1 |
| CHIC #118 | Mallia | tirintha | `tir` | 1 |
| CHIC #118 | Mallia | tiruns | `tir` | 1 |
| CHIC #123 | Knossos | krete | `ete` | 1 |
| CHIC #123 | Knossos | lebena | `ebe` | 1 |
| CHIC #123 | Knossos | tegea | `ege` | 1 |
| CHIC #123 | Knossos | thebai | `eba` | 1 |
| CHIC #124 | Knossos | ala | `ala` | 2 |
| CHIC #124 | Knossos | aleksandros | `ale` | 2 |
| CHIC #124 | Knossos | aptara | `ara` | 2 |
| CHIC #124 | Knossos | aptara | `tar` | 1 |
| CHIC #124 | Knossos | aptara | `tara` | 1 |
| CHIC #124 | Knossos | gor | `gor` | 1 |
| CHIC #124 | Knossos | gortyn | `gor` | 1 |
| CHIC #124 | Knossos | halikarnassos | `ali` | 2 |
| CHIC #124 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #124 | Knossos | hierapytna | `era` | 2 |
| CHIC #124 | Knossos | ikaria | `ari` | 2 |
| CHIC #124 | Knossos | ikaria | `kar` | 1 |
| CHIC #124 | Knossos | ikaria | `kari` | 1 |
| CHIC #124 | Knossos | kalumnos | `alu` | 2 |
| CHIC #124 | Knossos | kalumnos | `kal` | 1 |
| CHIC #124 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #124 | Knossos | kor | `kor` | 1 |
| CHIC #124 | Knossos | korinthos | `kor` | 1 |
| CHIC #124 | Knossos | korinthos | `kori` | 1 |
| CHIC #124 | Knossos | korinthos | `ori` | 2 |
| CHIC #124 | Knossos | kuthera | `era` | 2 |
| CHIC #124 | Knossos | melitos | `eli` | 2 |
| CHIC #124 | Knossos | melos | `elo` | 2 |
| CHIC #124 | Knossos | olous | `olo` | 2 |
| CHIC #124 | Knossos | olu | `olu` | 2 |
| CHIC #124 | Knossos | olunthos | `olu` | 2 |
| CHIC #124 | Knossos | par | `par` | 1 |
| CHIC #124 | Knossos | parnassos | `par` | 1 |
| CHIC #124 | Knossos | paros | `aro` | 2 |
| CHIC #124 | Knossos | paros | `par` | 1 |
| CHIC #124 | Knossos | paros | `paro` | 1 |
| CHIC #124 | Knossos | per | `per` | 1 |
| CHIC #124 | Knossos | pergamos | `per` | 1 |
| CHIC #124 | Knossos | phalasarna | `ala` | 2 |
| CHIC #124 | Knossos | poikilassos | `ila` | 2 |
| CHIC #124 | Knossos | poikilassos | `kil` | 1 |
| CHIC #124 | Knossos | poikilassos | `kila` | 1 |
| CHIC #124 | Knossos | probalinthos | `ali` | 2 |
| CHIC #124 | Knossos | probalinthos | `bal` | 1 |
| CHIC #124 | Knossos | probalinthos | `bali` | 1 |
| CHIC #124 | Knossos | pulos | `pul` | 1 |
| CHIC #124 | Knossos | pulos | `pulo` | 1 |
| CHIC #124 | Knossos | pulos | `ulo` | 2 |
| CHIC #124 | Knossos | salaminos | `ala` | 2 |
| CHIC #124 | Knossos | sparta | `par` | 1 |
| CHIC #124 | Knossos | tarra | `tar` | 1 |
| CHIC #124 | Knossos | tarsos | `tar` | 1 |
| CHIC #124 | Knossos | telmessos | `tel` | 1 |
| CHIC #124 | Knossos | ter | `ter` | 1 |
| CHIC #124 | Knossos | termessos | `ter` | 1 |
| CHIC #124 | Knossos | thera | `era` | 2 |
| CHIC #124 | Knossos | tirintha | `iri` | 2 |
| CHIC #124 | Knossos | tirintha | `tir` | 1 |
| CHIC #124 | Knossos | tirintha | `tiri` | 1 |
| CHIC #124 | Knossos | tiruns | `iru` | 2 |
| CHIC #124 | Knossos | tiruns | `tir` | 1 |
| CHIC #124 | Knossos | tiruns | `tiru` | 1 |
| CHIC #124 | Knossos | tul | `tul` | 1 |
| CHIC #124 | Knossos | tulisos | `tul` | 1 |
| CHIC #124 | Knossos | tulisos | `tuli` | 1 |
| CHIC #124 | Knossos | tulisos | `uli` | 2 |
| CHIC #124 | Knossos | tulissos | `tul` | 1 |
| CHIC #124 | Knossos | tulissos | `tuli` | 1 |
| CHIC #124 | Knossos | tulissos | `uli` | 2 |
| CHIC #125 | Knossos | ala | `ala` | 2 |
| CHIC #125 | Knossos | aleksandros | `ale` | 2 |
| CHIC #125 | Knossos | aleksandros | `alek` | 1 |
| CHIC #125 | Knossos | aleksandros | `lek` | 1 |
| CHIC #125 | Knossos | aptara | `ara` | 2 |
| CHIC #125 | Knossos | halikarnassos | `ali` | 2 |
| CHIC #125 | Knossos | halikarnassos | `alik` | 1 |
| CHIC #125 | Knossos | halikarnassos | `alika` | 1 |
| CHIC #125 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #125 | Knossos | halikarnassos | `lik` | 1 |
| CHIC #125 | Knossos | halikarnassos | `lika` | 1 |
| CHIC #125 | Knossos | hierapytna | `era` | 1 |
| CHIC #125 | Knossos | hierapytna | `erap` | 1 |
| CHIC #125 | Knossos | hierapytna | `rap` | 1 |
| CHIC #125 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #125 | Knossos | ida | `ida` | 1 |
| CHIC #125 | Knossos | ikaria | `ari` | 2 |
| CHIC #125 | Knossos | ikaria | `ika` | 1 |
| CHIC #125 | Knossos | itanos | `ita` | 1 |
| CHIC #125 | Knossos | kalumnos | `alu` | 2 |
| CHIC #125 | Knossos | korinthos | `ori` | 1 |
| CHIC #125 | Knossos | krete | `ete` | 1 |
| CHIC #125 | Knossos | krete | `ret` | 1 |
| CHIC #125 | Knossos | krete | `rete` | 1 |
| CHIC #125 | Knossos | kudonia | `udo` | 1 |
| CHIC #125 | Knossos | kuthera | `era` | 1 |
| CHIC #125 | Knossos | kuzikos | `iko` | 1 |
| CHIC #125 | Knossos | lab | `lab` | 1 |
| CHIC #125 | Knossos | lebena | `ebe` | 1 |
| CHIC #125 | Knossos | lebena | `leb` | 1 |
| CHIC #125 | Knossos | lebena | `lebe` | 1 |
| CHIC #125 | Knossos | lukia | `luk` | 1 |
| CHIC #125 | Knossos | lukia | `luki` | 1 |
| CHIC #125 | Knossos | lukia | `uki` | 1 |
| CHIC #125 | Knossos | lykabettos | `abe` | 1 |
| CHIC #125 | Knossos | melitos | `eli` | 1 |
| CHIC #125 | Knossos | melitos | `elit` | 1 |
| CHIC #125 | Knossos | melitos | `elito` | 1 |
| CHIC #125 | Knossos | melitos | `ito` | 1 |
| CHIC #125 | Knossos | melitos | `lit` | 1 |
| CHIC #125 | Knossos | melitos | `lito` | 1 |
| CHIC #125 | Knossos | melos | `elo` | 1 |
| CHIC #125 | Knossos | muke | `uke` | 1 |
| CHIC #125 | Knossos | mukenai | `uke` | 1 |
| CHIC #125 | Knossos | olous | `olo` | 1 |
| CHIC #125 | Knossos | olu | `olu` | 1 |
| CHIC #125 | Knossos | olunthos | `olu` | 1 |
| CHIC #125 | Knossos | paros | `aro` | 2 |
| CHIC #125 | Knossos | phalasarna | `ala` | 2 |
| CHIC #125 | Knossos | poikilassos | `iki` | 1 |
| CHIC #125 | Knossos | poikilassos | `ila` | 1 |
| CHIC #125 | Knossos | probalinthos | `ali` | 2 |
| CHIC #125 | Knossos | probalinthos | `oba` | 1 |
| CHIC #125 | Knossos | probalinthos | `rob` | 1 |
| CHIC #125 | Knossos | probalinthos | `roba` | 1 |
| CHIC #125 | Knossos | pulos | `ulo` | 1 |
| CHIC #125 | Knossos | salaminos | `ala` | 2 |
| CHIC #125 | Knossos | tegea | `ege` | 1 |
| CHIC #125 | Knossos | thebai | `eba` | 1 |
| CHIC #125 | Knossos | thera | `era` | 1 |
| CHIC #125 | Knossos | tirintha | `iri` | 1 |
| CHIC #125 | Knossos | tiruns | `iru` | 1 |
| CHIC #125 | Knossos | tulisos | `uli` | 1 |
| CHIC #125 | Knossos | tulissos | `uli` | 1 |
| CHIC #125 | Knossos | zakuntos | `aku` | 1 |
| CHIC #126 | Mallia | ala | `ala` | 1 |
| CHIC #126 | Mallia | aleksandros | `ale` | 1 |
| CHIC #126 | Mallia | aleksandros | `alek` | 1 |
| CHIC #126 | Mallia | aleksandros | `lek` | 1 |
| CHIC #126 | Mallia | aptara | `ara` | 1 |
| CHIC #126 | Mallia | ardettos | `det` | 1 |
| CHIC #126 | Mallia | dikte | `dik` | 1 |
| CHIC #126 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #126 | Mallia | halikarnassos | `alik` | 1 |
| CHIC #126 | Mallia | halikarnassos | `alika` | 1 |
| CHIC #126 | Mallia | halikarnassos | `ika` | 2 |
| CHIC #126 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #126 | Mallia | halikarnassos | `lika` | 1 |
| CHIC #126 | Mallia | hierapytna | `era` | 1 |
| CHIC #126 | Mallia | hierapytna | `erap` | 1 |
| CHIC #126 | Mallia | hierapytna | `rap` | 1 |
| CHIC #126 | Mallia | hyakinthos | `aki` | 2 |
| CHIC #126 | Mallia | ida | `ida` | 2 |
| CHIC #126 | Mallia | ikaria | `ari` | 1 |
| CHIC #126 | Mallia | ikaria | `ika` | 2 |
| CHIC #126 | Mallia | itanos | `ita` | 2 |
| CHIC #126 | Mallia | kalumnos | `alu` | 1 |
| CHIC #126 | Mallia | korinthos | `ori` | 1 |
| CHIC #126 | Mallia | krete | `ete` | 2 |
| CHIC #126 | Mallia | krete | `ret` | 1 |
| CHIC #126 | Mallia | krete | `rete` | 1 |
| CHIC #126 | Mallia | kudonia | `kud` | 1 |
| CHIC #126 | Mallia | kudonia | `kudo` | 1 |
| CHIC #126 | Mallia | kudonia | `udo` | 2 |
| CHIC #126 | Mallia | kuthera | `era` | 1 |
| CHIC #126 | Mallia | kuthera | `kut` | 1 |
| CHIC #126 | Mallia | kuzikos | `iko` | 2 |
| CHIC #126 | Mallia | lab | `lab` | 1 |
| CHIC #126 | Mallia | lebena | `ebe` | 2 |
| CHIC #126 | Mallia | lebena | `leb` | 1 |
| CHIC #126 | Mallia | lebena | `lebe` | 1 |
| CHIC #126 | Mallia | lukia | `luk` | 1 |
| CHIC #126 | Mallia | lukia | `luki` | 1 |
| CHIC #126 | Mallia | lukia | `uki` | 2 |
| CHIC #126 | Mallia | lykabettos | `abe` | 2 |
| CHIC #126 | Mallia | lykabettos | `abet` | 1 |
| CHIC #126 | Mallia | lykabettos | `bet` | 1 |
| CHIC #126 | Mallia | lykabettos | `kab` | 1 |
| CHIC #126 | Mallia | lykabettos | `kabe` | 1 |
| CHIC #126 | Mallia | melitos | `eli` | 1 |
| CHIC #126 | Mallia | melitos | `elit` | 1 |
| CHIC #126 | Mallia | melitos | `elito` | 1 |
| CHIC #126 | Mallia | melitos | `ito` | 2 |
| CHIC #126 | Mallia | melitos | `lit` | 1 |
| CHIC #126 | Mallia | melitos | `lito` | 1 |
| CHIC #126 | Mallia | melos | `elo` | 1 |
| CHIC #126 | Mallia | muke | `uke` | 2 |
| CHIC #126 | Mallia | mukenai | `uke` | 2 |
| CHIC #126 | Mallia | olous | `olo` | 1 |
| CHIC #126 | Mallia | olu | `olu` | 1 |
| CHIC #126 | Mallia | olunthos | `olu` | 1 |
| CHIC #126 | Mallia | paros | `aro` | 1 |
| CHIC #126 | Mallia | phalasarna | `ala` | 1 |
| CHIC #126 | Mallia | poikilassos | `iki` | 2 |
| CHIC #126 | Mallia | poikilassos | `ila` | 1 |
| CHIC #126 | Mallia | probalinthos | `ali` | 1 |
| CHIC #126 | Mallia | probalinthos | `oba` | 2 |
| CHIC #126 | Mallia | probalinthos | `rob` | 1 |
| CHIC #126 | Mallia | probalinthos | `roba` | 1 |
| CHIC #126 | Mallia | pulos | `ulo` | 1 |
| CHIC #126 | Mallia | salaminos | `ala` | 1 |
| CHIC #126 | Mallia | tegea | `ege` | 2 |
| CHIC #126 | Mallia | tegea | `teg` | 1 |
| CHIC #126 | Mallia | tegea | `tege` | 1 |
| CHIC #126 | Mallia | thebai | `eba` | 2 |
| CHIC #126 | Mallia | thera | `era` | 1 |
| CHIC #126 | Mallia | tirintha | `iri` | 1 |
| CHIC #126 | Mallia | tiruns | `iru` | 1 |
| CHIC #126 | Mallia | tulisos | `uli` | 1 |
| CHIC #126 | Mallia | tulissos | `uli` | 1 |
| CHIC #126 | Mallia | zakuntos | `aku` | 2 |
| CHIC #127 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #127 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #127 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #127 | Mallia | hyakinthos | `yaki` | 1 |
| CHIC #127 | Mallia | ida | `ida` | 1 |
| CHIC #127 | Mallia | ikaria | `ika` | 1 |
| CHIC #127 | Mallia | itanos | `ita` | 1 |
| CHIC #127 | Mallia | krete | `ete` | 1 |
| CHIC #127 | Mallia | kudonia | `udo` | 1 |
| CHIC #127 | Mallia | kuzikos | `iko` | 1 |
| CHIC #127 | Mallia | lebena | `ebe` | 1 |
| CHIC #127 | Mallia | lukia | `uki` | 1 |
| CHIC #127 | Mallia | lykabettos | `abe` | 1 |
| CHIC #127 | Mallia | melitos | `ito` | 1 |
| CHIC #127 | Mallia | muke | `uke` | 1 |
| CHIC #127 | Mallia | mukenai | `uke` | 1 |
| CHIC #127 | Mallia | poikilassos | `iki` | 1 |
| CHIC #127 | Mallia | probalinthos | `oba` | 1 |
| CHIC #127 | Mallia | tegea | `ege` | 1 |
| CHIC #127 | Mallia | thebai | `eba` | 1 |
| CHIC #127 | Mallia | zakuntos | `aku` | 1 |
| CHIC #128 | Mallia | athenai | `ena` | 1 |
| CHIC #128 | Mallia | lebena | `ena` | 1 |
| CHIC #128 | Mallia | mukenai | `ena` | 1 |
| CHIC #128 | Mallia | orchomenos | `eno` | 1 |
| CHIC #128 | Mallia | orchomenos | `men` | 1 |
| CHIC #128 | Mallia | orchomenos | `meno` | 1 |
| CHIC #128 | Mallia | orchomenos | `ome` | 1 |
| CHIC #128 | Mallia | orchomenos | `omen` | 1 |
| CHIC #128 | Mallia | orchomenos | `omeno` | 1 |
| CHIC #128 | Mallia | priene | `ene` | 1 |
| CHIC #128 | Mallia | tenos | `eno` | 1 |
| CHIC #129 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #129 | Mallia | kudonia | `kud` | 1 |
| CHIC #129 | Mallia | lykabettos | `abe` | 1 |
| CHIC #129 | Mallia | zakuntos | `aku` | 1 |
| CHIC #130 | Mallia | kalumnos | `lum` | 1 |
| CHIC #130 | Mallia | lem | `lem` | 1 |
| CHIC #130 | Mallia | lemnos | `lem` | 1 |
| CHIC #130 | Mallia | salaminos | `lam` | 1 |
| CHIC #131 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #131 | Mallia | muke | `uke` | 1 |
| CHIC #131 | Mallia | mukenai | `uke` | 1 |
| CHIC #138 | Zakros | halikarnassos | `ika` | 1 |
| CHIC #138 | Zakros | ida | `ida` | 1 |
| CHIC #138 | Zakros | ikaria | `ika` | 1 |
| CHIC #138 | Zakros | itanos | `ita` | 1 |
| CHIC #138 | Zakros | kuzikos | `iko` | 1 |
| CHIC #138 | Zakros | melitos | `ito` | 1 |
| CHIC #138 | Zakros | poikilassos | `iki` | 1 |
| CHIC #140 | Knossos | hyakinthos | `aki` | 1 |
| CHIC #140 | Knossos | lykabettos | `abe` | 1 |
| CHIC #140 | Knossos | zakuntos | `aku` | 1 |
| CHIC #141 | Knossos | paros | `aro` | 1 |
| CHIC #142 | Knossos | ardettos | `det` | 1 |
| CHIC #142 | Knossos | dikte | `dik` | 1 |
| CHIC #142 | Knossos | halikarnassos | `ika` | 2 |
| CHIC #142 | Knossos | hyakinthos | `aki` | 2 |
| CHIC #142 | Knossos | hyakinthos | `yak` | 1 |
| CHIC #142 | Knossos | hyakinthos | `yaki` | 1 |
| CHIC #142 | Knossos | ida | `ida` | 2 |
| CHIC #142 | Knossos | ikaria | `ika` | 2 |
| CHIC #142 | Knossos | itanos | `ita` | 2 |
| CHIC #142 | Knossos | krete | `ete` | 2 |
| CHIC #142 | Knossos | kudonia | `kud` | 1 |
| CHIC #142 | Knossos | kudonia | `kudo` | 1 |
| CHIC #142 | Knossos | kudonia | `udo` | 2 |
| CHIC #142 | Knossos | kuthera | `kut` | 1 |
| CHIC #142 | Knossos | kuzikos | `iko` | 2 |
| CHIC #142 | Knossos | lebena | `ebe` | 2 |
| CHIC #142 | Knossos | lukia | `uki` | 2 |
| CHIC #142 | Knossos | lykabettos | `abe` | 2 |
| CHIC #142 | Knossos | lykabettos | `abet` | 1 |
| CHIC #142 | Knossos | lykabettos | `bet` | 1 |
| CHIC #142 | Knossos | lykabettos | `kab` | 1 |
| CHIC #142 | Knossos | lykabettos | `kabe` | 1 |
| CHIC #142 | Knossos | melitos | `ito` | 2 |
| CHIC #142 | Knossos | muke | `uke` | 2 |
| CHIC #142 | Knossos | mukenai | `uke` | 2 |
| CHIC #142 | Knossos | poikilassos | `iki` | 2 |
| CHIC #142 | Knossos | probalinthos | `oba` | 2 |
| CHIC #142 | Knossos | tegea | `ege` | 2 |
| CHIC #142 | Knossos | tegea | `teg` | 1 |
| CHIC #142 | Knossos | tegea | `tege` | 1 |
| CHIC #142 | Knossos | thebai | `eba` | 2 |
| CHIC #142 | Knossos | zakuntos | `aku` | 2 |
| CHIC #144 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #144 | Knossos | ida | `ida` | 1 |
| CHIC #144 | Knossos | ikaria | `ika` | 1 |
| CHIC #144 | Knossos | itanos | `ita` | 1 |
| CHIC #144 | Knossos | kuzikos | `iko` | 1 |
| CHIC #144 | Knossos | melitos | `ito` | 1 |
| CHIC #144 | Knossos | poikilassos | `iki` | 1 |
| CHIC #145 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #145 | Knossos | ida | `ida` | 1 |
| CHIC #145 | Knossos | ikaria | `ika` | 1 |
| CHIC #145 | Knossos | itanos | `ita` | 1 |
| CHIC #145 | Knossos | kuzikos | `iko` | 1 |
| CHIC #145 | Knossos | melitos | `ito` | 1 |
| CHIC #145 | Knossos | poikilassos | `iki` | 1 |
| CHIC #148 | Mallia | aia | `aia` | 1 |
| CHIC #148 | Mallia | lasaia | `aia` | 1 |
| CHIC #148 | Mallia | praisos | `rai` | 1 |
| CHIC #149 | Mallia | hymettos | `met` | 1 |
| CHIC #149 | Mallia | krete | `ete` | 1 |
| CHIC #149 | Mallia | kudonia | `oni` | 1 |
| CHIC #149 | Mallia | orchomenos | `ome` | 1 |
| CHIC #152 | Zakros | lukia | `uki` | 1 |
| CHIC #152 | Zakros | muke | `muk` | 1 |
| CHIC #152 | Zakros | mukenai | `muk` | 1 |
| CHIC #158 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #158 | Knossos | ida | `ida` | 1 |
| CHIC #158 | Knossos | ikaria | `ika` | 1 |
| CHIC #158 | Knossos | itanos | `ita` | 1 |
| CHIC #158 | Knossos | kuzikos | `iko` | 1 |
| CHIC #158 | Knossos | melitos | `ito` | 1 |
| CHIC #158 | Knossos | poikilassos | `iki` | 1 |
| CHIC #160 | Knossos | kudonia | `oni` | 1 |
| CHIC #160 | Knossos | priene | `ien` | 1 |
| CHIC #160 | Knossos | rhytion | `ion` | 1 |
| CHIC #160 | Knossos | rhytion | `tio` | 1 |
| CHIC #160 | Knossos | rhytion | `tion` | 1 |
| CHIC #162 | Knossos | paros | `aro` | 1 |
| CHIC #163 | Knossos | aptara | `ara` | 1 |
| CHIC #163 | Knossos | praisos | `rai` | 1 |
| CHIC #165 | Knossos | halikarnassos | `ika` | 1 |
| CHIC #165 | Knossos | ida | `ida` | 1 |
| CHIC #165 | Knossos | ikaria | `ika` | 1 |
| CHIC #165 | Knossos | itanos | `ita` | 1 |
| CHIC #165 | Knossos | kuzikos | `iko` | 1 |
| CHIC #165 | Knossos | melitos | `ito` | 1 |
| CHIC #165 | Knossos | poikilassos | `iki` | 1 |
| CHIC #166 | Knossos | ala | `ala` | 1 |
| CHIC #166 | Knossos | aleksandros | `ale` | 1 |
| CHIC #166 | Knossos | aptara | `ara` | 1 |
| CHIC #166 | Knossos | aptara | `tar` | 1 |
| CHIC #166 | Knossos | aptara | `tara` | 1 |
| CHIC #166 | Knossos | gor | `gor` | 1 |
| CHIC #166 | Knossos | gortyn | `gor` | 1 |
| CHIC #166 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #166 | Knossos | halikarnassos | `kar` | 1 |
| CHIC #166 | Knossos | hierapytna | `era` | 1 |
| CHIC #166 | Knossos | ikaria | `ari` | 1 |
| CHIC #166 | Knossos | ikaria | `kar` | 1 |
| CHIC #166 | Knossos | ikaria | `kari` | 1 |
| CHIC #166 | Knossos | kalumnos | `alu` | 1 |
| CHIC #166 | Knossos | kalumnos | `kal` | 1 |
| CHIC #166 | Knossos | kalumnos | `kalu` | 1 |
| CHIC #166 | Knossos | kor | `kor` | 1 |
| CHIC #166 | Knossos | korinthos | `kor` | 1 |
| CHIC #166 | Knossos | korinthos | `kori` | 1 |
| CHIC #166 | Knossos | korinthos | `ori` | 1 |
| CHIC #166 | Knossos | kuthera | `era` | 1 |
| CHIC #166 | Knossos | melitos | `eli` | 1 |
| CHIC #166 | Knossos | melos | `elo` | 1 |
| CHIC #166 | Knossos | olous | `olo` | 1 |
| CHIC #166 | Knossos | olu | `olu` | 1 |
| CHIC #166 | Knossos | olunthos | `olu` | 1 |
| CHIC #166 | Knossos | par | `par` | 1 |
| CHIC #166 | Knossos | parnassos | `par` | 1 |
| CHIC #166 | Knossos | paros | `aro` | 2 |
| CHIC #166 | Knossos | paros | `par` | 1 |
| CHIC #166 | Knossos | paros | `paro` | 1 |
| CHIC #166 | Knossos | per | `per` | 1 |
| CHIC #166 | Knossos | pergamos | `per` | 1 |
| CHIC #166 | Knossos | phalasarna | `ala` | 1 |
| CHIC #166 | Knossos | poikilassos | `ila` | 1 |
| CHIC #166 | Knossos | poikilassos | `kil` | 1 |
| CHIC #166 | Knossos | poikilassos | `kila` | 1 |
| CHIC #166 | Knossos | probalinthos | `ali` | 1 |
| CHIC #166 | Knossos | probalinthos | `bal` | 1 |
| CHIC #166 | Knossos | probalinthos | `bali` | 1 |
| CHIC #166 | Knossos | pulos | `pul` | 1 |
| CHIC #166 | Knossos | pulos | `pulo` | 1 |
| CHIC #166 | Knossos | pulos | `ulo` | 1 |
| CHIC #166 | Knossos | salaminos | `ala` | 1 |
| CHIC #166 | Knossos | sparta | `par` | 1 |
| CHIC #166 | Knossos | tarra | `tar` | 1 |
| CHIC #166 | Knossos | tarsos | `tar` | 1 |
| CHIC #166 | Knossos | telmessos | `tel` | 1 |
| CHIC #166 | Knossos | ter | `ter` | 1 |
| CHIC #166 | Knossos | termessos | `ter` | 1 |
| CHIC #166 | Knossos | thera | `era` | 1 |
| CHIC #166 | Knossos | tirintha | `iri` | 1 |
| CHIC #166 | Knossos | tirintha | `tir` | 1 |
| CHIC #166 | Knossos | tirintha | `tiri` | 1 |
| CHIC #166 | Knossos | tiruns | `iru` | 1 |
| CHIC #166 | Knossos | tiruns | `tir` | 1 |
| CHIC #166 | Knossos | tiruns | `tiru` | 1 |
| CHIC #166 | Knossos | tul | `tul` | 1 |
| CHIC #166 | Knossos | tulisos | `tul` | 1 |
| CHIC #166 | Knossos | tulisos | `tuli` | 1 |
| CHIC #166 | Knossos | tulisos | `uli` | 1 |
| CHIC #166 | Knossos | tulissos | `tul` | 1 |
| CHIC #166 | Knossos | tulissos | `tuli` | 1 |
| CHIC #166 | Knossos | tulissos | `uli` | 1 |
| CHIC #167 | Knossos | aptara | `ara` | 1 |
| CHIC #167 | Knossos | hierapytna | `era` | 1 |
| CHIC #167 | Knossos | kuthera | `era` | 1 |
| CHIC #167 | Knossos | thera | `era` | 1 |
| CHIC #168 | Knossos | aptara | `ara` | 1 |
| CHIC #169 | Knossos | paros | `aro` | 1 |
| CHIC #171 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #171 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #171 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #171 | Mallia | hyakinthos | `yaki` | 1 |
| CHIC #171 | Mallia | ida | `ida` | 1 |
| CHIC #171 | Mallia | ikaria | `ika` | 1 |
| CHIC #171 | Mallia | itanos | `ita` | 1 |
| CHIC #171 | Mallia | krete | `ete` | 1 |
| CHIC #171 | Mallia | kudonia | `udo` | 1 |
| CHIC #171 | Mallia | kuzikos | `iko` | 1 |
| CHIC #171 | Mallia | lebena | `ebe` | 1 |
| CHIC #171 | Mallia | lukia | `uki` | 1 |
| CHIC #171 | Mallia | lykabettos | `abe` | 1 |
| CHIC #171 | Mallia | melitos | `ito` | 1 |
| CHIC #171 | Mallia | muke | `uke` | 1 |
| CHIC #171 | Mallia | mukenai | `uke` | 1 |
| CHIC #171 | Mallia | poikilassos | `iki` | 1 |
| CHIC #171 | Mallia | probalinthos | `oba` | 1 |
| CHIC #171 | Mallia | tegea | `ege` | 1 |
| CHIC #171 | Mallia | thebai | `eba` | 1 |
| CHIC #171 | Mallia | zakuntos | `aku` | 1 |
| CHIC #173 | Mallia | aleksandros | `lek` | 1 |
| CHIC #173 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #173 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #173 | Mallia | halikarnassos | `lika` | 1 |
| CHIC #173 | Mallia | hierapytna | `era` | 1 |
| CHIC #173 | Mallia | hierapytna | `erap` | 1 |
| CHIC #173 | Mallia | hierapytna | `rap` | 1 |
| CHIC #173 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #173 | Mallia | ida | `ida` | 1 |
| CHIC #173 | Mallia | ikaria | `ika` | 1 |
| CHIC #173 | Mallia | itanos | `ita` | 1 |
| CHIC #173 | Mallia | krete | `ete` | 1 |
| CHIC #173 | Mallia | krete | `ret` | 1 |
| CHIC #173 | Mallia | krete | `rete` | 1 |
| CHIC #173 | Mallia | kudonia | `udo` | 1 |
| CHIC #173 | Mallia | kuthera | `era` | 1 |
| CHIC #173 | Mallia | kuzikos | `iko` | 1 |
| CHIC #173 | Mallia | lab | `lab` | 1 |
| CHIC #173 | Mallia | lebena | `ebe` | 1 |
| CHIC #173 | Mallia | lebena | `leb` | 1 |
| CHIC #173 | Mallia | lebena | `lebe` | 1 |
| CHIC #173 | Mallia | lukia | `luk` | 1 |
| CHIC #173 | Mallia | lukia | `luki` | 1 |
| CHIC #173 | Mallia | lukia | `uki` | 1 |
| CHIC #173 | Mallia | lykabettos | `abe` | 1 |
| CHIC #173 | Mallia | melitos | `eli` | 1 |
| CHIC #173 | Mallia | melitos | `elit` | 1 |
| CHIC #173 | Mallia | melitos | `elito` | 1 |
| CHIC #173 | Mallia | melitos | `ito` | 1 |
| CHIC #173 | Mallia | melitos | `lit` | 1 |
| CHIC #173 | Mallia | melitos | `lito` | 1 |
| CHIC #173 | Mallia | melos | `elo` | 1 |
| CHIC #173 | Mallia | muke | `uke` | 1 |
| CHIC #173 | Mallia | mukenai | `uke` | 1 |
| CHIC #173 | Mallia | poikilassos | `iki` | 1 |
| CHIC #173 | Mallia | probalinthos | `oba` | 1 |
| CHIC #173 | Mallia | probalinthos | `rob` | 1 |
| CHIC #173 | Mallia | probalinthos | `roba` | 1 |
| CHIC #173 | Mallia | tegea | `ege` | 1 |
| CHIC #173 | Mallia | thebai | `eba` | 1 |
| CHIC #173 | Mallia | thera | `era` | 1 |
| CHIC #173 | Mallia | zakuntos | `aku` | 1 |
| CHIC #174 | Palaikastro | ardettos | `det` | 1 |
| CHIC #174 | Palaikastro | dikte | `dik` | 1 |
| CHIC #174 | Palaikastro | halikarnassos | `ika` | 3 |
| CHIC #174 | Palaikastro | hyakinthos | `aki` | 1 |
| CHIC #174 | Palaikastro | ida | `ida` | 3 |
| CHIC #174 | Palaikastro | ikaria | `ika` | 3 |
| CHIC #174 | Palaikastro | itanos | `ita` | 3 |
| CHIC #174 | Palaikastro | krete | `ete` | 1 |
| CHIC #174 | Palaikastro | kudonia | `kud` | 1 |
| CHIC #174 | Palaikastro | kudonia | `kudo` | 1 |
| CHIC #174 | Palaikastro | kudonia | `udo` | 1 |
| CHIC #174 | Palaikastro | kuthera | `kut` | 1 |
| CHIC #174 | Palaikastro | kuzikos | `iko` | 3 |
| CHIC #174 | Palaikastro | lebena | `ebe` | 1 |
| CHIC #174 | Palaikastro | lukia | `uki` | 1 |
| CHIC #174 | Palaikastro | lykabettos | `abe` | 1 |
| CHIC #174 | Palaikastro | lykabettos | `bet` | 1 |
| CHIC #174 | Palaikastro | lykabettos | `kab` | 1 |
| CHIC #174 | Palaikastro | lykabettos | `kabe` | 1 |
| CHIC #174 | Palaikastro | melitos | `ito` | 3 |
| CHIC #174 | Palaikastro | muke | `uke` | 1 |
| CHIC #174 | Palaikastro | mukenai | `uke` | 1 |
| CHIC #174 | Palaikastro | poikilassos | `iki` | 3 |
| CHIC #174 | Palaikastro | probalinthos | `oba` | 1 |
| CHIC #174 | Palaikastro | tegea | `ege` | 1 |
| CHIC #174 | Palaikastro | tegea | `teg` | 1 |
| CHIC #174 | Palaikastro | tegea | `tege` | 1 |
| CHIC #174 | Palaikastro | thebai | `eba` | 1 |
| CHIC #174 | Palaikastro | zakuntos | `aku` | 1 |
| CHIC #180 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #180 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #180 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #180 | Crete (unprovenanced) | hyakinthos | `yaki` | 1 |
| CHIC #180 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #180 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #180 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #180 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #180 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #180 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #180 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #180 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #180 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #180 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #180 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #180 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #180 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #180 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #180 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #180 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #180 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #182 | Crete (unprovenanced) | ala | `ala` | 2 |
| CHIC #182 | Crete (unprovenanced) | aleksandros | `ale` | 2 |
| CHIC #182 | Crete (unprovenanced) | aptara | `ara` | 2 |
| CHIC #182 | Crete (unprovenanced) | aptara | `tar` | 1 |
| CHIC #182 | Crete (unprovenanced) | aptara | `tara` | 1 |
| CHIC #182 | Crete (unprovenanced) | ardettos | `det` | 1 |
| CHIC #182 | Crete (unprovenanced) | halikarnassos | `ali` | 2 |
| CHIC #182 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #182 | Crete (unprovenanced) | ikaria | `ari` | 2 |
| CHIC #182 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #182 | Crete (unprovenanced) | kalumnos | `alu` | 2 |
| CHIC #182 | Crete (unprovenanced) | korinthos | `ori` | 1 |
| CHIC #182 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #182 | Crete (unprovenanced) | kuthera | `kut` | 1 |
| CHIC #182 | Crete (unprovenanced) | lykabettos | `bet` | 1 |
| CHIC #182 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #182 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #182 | Crete (unprovenanced) | olous | `olo` | 1 |
| CHIC #182 | Crete (unprovenanced) | olu | `olu` | 1 |
| CHIC #182 | Crete (unprovenanced) | olunthos | `olu` | 1 |
| CHIC #182 | Crete (unprovenanced) | paros | `aro` | 2 |
| CHIC #182 | Crete (unprovenanced) | phalasarna | `ala` | 2 |
| CHIC #182 | Crete (unprovenanced) | poikilassos | `ila` | 1 |
| CHIC #182 | Crete (unprovenanced) | probalinthos | `ali` | 2 |
| CHIC #182 | Crete (unprovenanced) | pulos | `ulo` | 1 |
| CHIC #182 | Crete (unprovenanced) | salaminos | `ala` | 2 |
| CHIC #182 | Crete (unprovenanced) | tarra | `tar` | 1 |
| CHIC #182 | Crete (unprovenanced) | tarsos | `tar` | 1 |
| CHIC #182 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #182 | Crete (unprovenanced) | tirintha | `iri` | 1 |
| CHIC #182 | Crete (unprovenanced) | tiruns | `iru` | 1 |
| CHIC #182 | Crete (unprovenanced) | tulisos | `uli` | 1 |
| CHIC #182 | Crete (unprovenanced) | tulissos | `uli` | 1 |
| CHIC #183 | Crete (unprovenanced) | ala | `ala` | 1 |
| CHIC #183 | Crete (unprovenanced) | aleksandros | `ale` | 1 |
| CHIC #183 | Crete (unprovenanced) | aptara | `ara` | 1 |
| CHIC #183 | Crete (unprovenanced) | halikarnassos | `ali` | 1 |
| CHIC #183 | Crete (unprovenanced) | ikaria | `ari` | 1 |
| CHIC #183 | Crete (unprovenanced) | kalumnos | `alu` | 1 |
| CHIC #183 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #183 | Crete (unprovenanced) | phalasarna | `ala` | 1 |
| CHIC #183 | Crete (unprovenanced) | probalinthos | `ali` | 1 |
| CHIC #183 | Crete (unprovenanced) | salaminos | `ala` | 1 |
| CHIC #184 | Crete (unprovenanced) | aptara | `ara` | 1 |
| CHIC #184 | Crete (unprovenanced) | par | `par` | 1 |
| CHIC #184 | Crete (unprovenanced) | parnassos | `par` | 1 |
| CHIC #184 | Crete (unprovenanced) | paros | `par` | 1 |
| CHIC #184 | Crete (unprovenanced) | sparta | `par` | 1 |
| CHIC #186 | Kalo Horio | hierapytna | `era` | 1 |
| CHIC #186 | Kalo Horio | kuthera | `era` | 1 |
| CHIC #186 | Kalo Horio | melitos | `eli` | 1 |
| CHIC #186 | Kalo Horio | melos | `elo` | 1 |
| CHIC #186 | Kalo Horio | thera | `era` | 1 |
| CHIC #191 | Mochlos | halikarnassos | `ika` | 1 |
| CHIC #191 | Mochlos | hyakinthos | `aki` | 1 |
| CHIC #191 | Mochlos | hyakinthos | `yak` | 1 |
| CHIC #191 | Mochlos | hyakinthos | `yaki` | 1 |
| CHIC #191 | Mochlos | ida | `ida` | 1 |
| CHIC #191 | Mochlos | ikaria | `ika` | 1 |
| CHIC #191 | Mochlos | itanos | `ita` | 1 |
| CHIC #191 | Mochlos | krete | `ete` | 1 |
| CHIC #191 | Mochlos | kudonia | `udo` | 1 |
| CHIC #191 | Mochlos | kuzikos | `iko` | 1 |
| CHIC #191 | Mochlos | lebena | `ebe` | 1 |
| CHIC #191 | Mochlos | lukia | `uki` | 1 |
| CHIC #191 | Mochlos | lykabettos | `abe` | 1 |
| CHIC #191 | Mochlos | melitos | `ito` | 1 |
| CHIC #191 | Mochlos | muke | `uke` | 1 |
| CHIC #191 | Mochlos | mukenai | `uke` | 1 |
| CHIC #191 | Mochlos | poikilassos | `iki` | 1 |
| CHIC #191 | Mochlos | probalinthos | `oba` | 1 |
| CHIC #191 | Mochlos | tegea | `ege` | 1 |
| CHIC #191 | Mochlos | thebai | `eba` | 1 |
| CHIC #191 | Mochlos | zakuntos | `aku` | 1 |
| CHIC #193 | Ziros | krete | `ete` | 1 |
| CHIC #193 | Ziros | lebena | `ebe` | 1 |
| CHIC #193 | Ziros | tegea | `ege` | 1 |
| CHIC #193 | Ziros | thebai | `eba` | 1 |
| CHIC #194 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #194 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #194 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #194 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #194 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #194 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #194 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #195 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #196 | Gortys | krete | `ete` | 1 |
| CHIC #197 | Mallia | hymettos | `met` | 1 |
| CHIC #197 | Mallia | krete | `ete` | 1 |
| CHIC #197 | Mallia | kudonia | `oni` | 1 |
| CHIC #197 | Mallia | orchomenos | `ome` | 1 |
| CHIC #200 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #200 | Mallia | ida | `ida` | 1 |
| CHIC #200 | Mallia | ikaria | `ika` | 1 |
| CHIC #200 | Mallia | itanos | `ita` | 1 |
| CHIC #200 | Mallia | korinthos | `rin` | 1 |
| CHIC #200 | Mallia | kudonia | `oni` | 1 |
| CHIC #200 | Mallia | kuzikos | `iko` | 1 |
| CHIC #200 | Mallia | melitos | `ito` | 1 |
| CHIC #200 | Mallia | olunthos | `lun` | 1 |
| CHIC #200 | Mallia | poikilassos | `iki` | 1 |
| CHIC #200 | Mallia | poikilassos | `poi` | 1 |
| CHIC #200 | Mallia | probalinthos | `lin` | 1 |
| CHIC #200 | Mallia | thebai | `bai` | 1 |
| CHIC #200 | Mallia | tirintha | `rin` | 1 |
| CHIC #200 | Mallia | tiruns | `run` | 1 |
| CHIC #202 | Arkhanes | ala | `ala` | 1 |
| CHIC #202 | Arkhanes | aleksandros | `ale` | 1 |
| CHIC #202 | Arkhanes | aptara | `ara` | 1 |
| CHIC #202 | Arkhanes | halikarnassos | `ali` | 1 |
| CHIC #202 | Arkhanes | hierapytna | `era` | 1 |
| CHIC #202 | Arkhanes | ikaria | `ari` | 1 |
| CHIC #202 | Arkhanes | kalumnos | `alu` | 1 |
| CHIC #202 | Arkhanes | korinthos | `ori` | 1 |
| CHIC #202 | Arkhanes | kuthera | `era` | 1 |
| CHIC #202 | Arkhanes | melitos | `eli` | 1 |
| CHIC #202 | Arkhanes | melos | `elo` | 1 |
| CHIC #202 | Arkhanes | olous | `olo` | 1 |
| CHIC #202 | Arkhanes | olu | `olu` | 1 |
| CHIC #202 | Arkhanes | olunthos | `olu` | 1 |
| CHIC #202 | Arkhanes | paros | `aro` | 1 |
| CHIC #202 | Arkhanes | phalasarna | `ala` | 1 |
| CHIC #202 | Arkhanes | poikilassos | `ila` | 1 |
| CHIC #202 | Arkhanes | probalinthos | `ali` | 1 |
| CHIC #202 | Arkhanes | pulos | `ulo` | 1 |
| CHIC #202 | Arkhanes | salaminos | `ala` | 1 |
| CHIC #202 | Arkhanes | thera | `era` | 1 |
| CHIC #202 | Arkhanes | tirintha | `iri` | 1 |
| CHIC #202 | Arkhanes | tiruns | `iru` | 1 |
| CHIC #202 | Arkhanes | tulisos | `uli` | 1 |
| CHIC #202 | Arkhanes | tulissos | `uli` | 1 |
| CHIC #203 | Knossos | ala | `ala` | 1 |
| CHIC #203 | Knossos | aleksandros | `ale` | 1 |
| CHIC #203 | Knossos | aptara | `ara` | 1 |
| CHIC #203 | Knossos | halikarnassos | `ali` | 1 |
| CHIC #203 | Knossos | hierapytna | `era` | 1 |
| CHIC #203 | Knossos | ikaria | `ari` | 1 |
| CHIC #203 | Knossos | kalumnos | `alu` | 1 |
| CHIC #203 | Knossos | korinthos | `ori` | 1 |
| CHIC #203 | Knossos | kuthera | `era` | 1 |
| CHIC #203 | Knossos | melitos | `eli` | 1 |
| CHIC #203 | Knossos | melos | `elo` | 1 |
| CHIC #203 | Knossos | olous | `olo` | 1 |
| CHIC #203 | Knossos | olu | `olu` | 1 |
| CHIC #203 | Knossos | olunthos | `olu` | 1 |
| CHIC #203 | Knossos | paros | `aro` | 1 |
| CHIC #203 | Knossos | phalasarna | `ala` | 1 |
| CHIC #203 | Knossos | poikilassos | `ila` | 1 |
| CHIC #203 | Knossos | probalinthos | `ali` | 1 |
| CHIC #203 | Knossos | pulos | `ulo` | 1 |
| CHIC #203 | Knossos | salaminos | `ala` | 1 |
| CHIC #203 | Knossos | thera | `era` | 1 |
| CHIC #203 | Knossos | tirintha | `iri` | 1 |
| CHIC #203 | Knossos | tiruns | `iru` | 1 |
| CHIC #203 | Knossos | tulisos | `uli` | 1 |
| CHIC #203 | Knossos | tulissos | `uli` | 1 |
| CHIC #204 | Mallia | aleksandros | `lek` | 1 |
| CHIC #204 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #204 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #204 | Mallia | halikarnassos | `lika` | 1 |
| CHIC #204 | Mallia | hierapytna | `rap` | 1 |
| CHIC #204 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #204 | Mallia | ida | `ida` | 1 |
| CHIC #204 | Mallia | ikaria | `ika` | 1 |
| CHIC #204 | Mallia | itanos | `ita` | 1 |
| CHIC #204 | Mallia | krete | `ete` | 1 |
| CHIC #204 | Mallia | krete | `ret` | 1 |
| CHIC #204 | Mallia | krete | `rete` | 1 |
| CHIC #204 | Mallia | kudonia | `udo` | 1 |
| CHIC #204 | Mallia | kuzikos | `iko` | 1 |
| CHIC #204 | Mallia | lab | `lab` | 1 |
| CHIC #204 | Mallia | lebena | `ebe` | 1 |
| CHIC #204 | Mallia | lebena | `leb` | 1 |
| CHIC #204 | Mallia | lebena | `lebe` | 1 |
| CHIC #204 | Mallia | lukia | `luk` | 1 |
| CHIC #204 | Mallia | lukia | `luki` | 1 |
| CHIC #204 | Mallia | lukia | `uki` | 1 |
| CHIC #204 | Mallia | lykabettos | `abe` | 1 |
| CHIC #204 | Mallia | melitos | `ito` | 1 |
| CHIC #204 | Mallia | melitos | `lit` | 1 |
| CHIC #204 | Mallia | melitos | `lito` | 1 |
| CHIC #204 | Mallia | muke | `uke` | 1 |
| CHIC #204 | Mallia | mukenai | `uke` | 1 |
| CHIC #204 | Mallia | poikilassos | `iki` | 1 |
| CHIC #204 | Mallia | poikilassos | `ila` | 1 |
| CHIC #204 | Mallia | probalinthos | `oba` | 1 |
| CHIC #204 | Mallia | probalinthos | `rob` | 1 |
| CHIC #204 | Mallia | probalinthos | `roba` | 1 |
| CHIC #204 | Mallia | tegea | `ege` | 1 |
| CHIC #204 | Mallia | thebai | `eba` | 1 |
| CHIC #204 | Mallia | tirintha | `iri` | 1 |
| CHIC #204 | Mallia | tiruns | `iru` | 1 |
| CHIC #204 | Mallia | zakuntos | `aku` | 1 |
| CHIC #205 | Crete (unprovenanced) | ala | `ala` | 1 |
| CHIC #205 | Crete (unprovenanced) | aleksandros | `ale` | 1 |
| CHIC #205 | Crete (unprovenanced) | aptara | `ara` | 1 |
| CHIC #205 | Crete (unprovenanced) | halikarnassos | `ali` | 1 |
| CHIC #205 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #205 | Crete (unprovenanced) | ikaria | `ari` | 1 |
| CHIC #205 | Crete (unprovenanced) | kalumnos | `alu` | 1 |
| CHIC #205 | Crete (unprovenanced) | korinthos | `ori` | 1 |
| CHIC #205 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #205 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #205 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #205 | Crete (unprovenanced) | olous | `olo` | 1 |
| CHIC #205 | Crete (unprovenanced) | olu | `olu` | 1 |
| CHIC #205 | Crete (unprovenanced) | olunthos | `olu` | 1 |
| CHIC #205 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #205 | Crete (unprovenanced) | phalasarna | `ala` | 1 |
| CHIC #205 | Crete (unprovenanced) | poikilassos | `ila` | 1 |
| CHIC #205 | Crete (unprovenanced) | probalinthos | `ali` | 1 |
| CHIC #205 | Crete (unprovenanced) | pulos | `ulo` | 1 |
| CHIC #205 | Crete (unprovenanced) | salaminos | `ala` | 1 |
| CHIC #205 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #205 | Crete (unprovenanced) | tirintha | `iri` | 1 |
| CHIC #205 | Crete (unprovenanced) | tiruns | `iru` | 1 |
| CHIC #205 | Crete (unprovenanced) | tulisos | `uli` | 1 |
| CHIC #205 | Crete (unprovenanced) | tulissos | `uli` | 1 |
| CHIC #218 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #225 | Crete (unprovenanced) | ala | `ala` | 1 |
| CHIC #225 | Crete (unprovenanced) | aleksandros | `ale` | 1 |
| CHIC #225 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #225 | Crete (unprovenanced) | aptara | `ara` | 1 |
| CHIC #225 | Crete (unprovenanced) | aptara | `tar` | 1 |
| CHIC #225 | Crete (unprovenanced) | aptara | `tara` | 1 |
| CHIC #225 | Crete (unprovenanced) | gor | `gor` | 1 |
| CHIC #225 | Crete (unprovenanced) | gortyn | `gor` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `ali` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `ikar` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `kar` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #225 | Crete (unprovenanced) | halikarnassos | `likar` | 1 |
| CHIC #225 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #225 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #225 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #225 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `ari` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `ikar` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `ikari` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `kar` | 1 |
| CHIC #225 | Crete (unprovenanced) | ikaria | `kari` | 1 |
| CHIC #225 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #225 | Crete (unprovenanced) | kalumnos | `alu` | 1 |
| CHIC #225 | Crete (unprovenanced) | kalumnos | `kal` | 1 |
| CHIC #225 | Crete (unprovenanced) | kalumnos | `kalu` | 1 |
| CHIC #225 | Crete (unprovenanced) | kor | `kor` | 1 |
| CHIC #225 | Crete (unprovenanced) | korinthos | `kor` | 1 |
| CHIC #225 | Crete (unprovenanced) | korinthos | `kori` | 1 |
| CHIC #225 | Crete (unprovenanced) | korinthos | `ori` | 1 |
| CHIC #225 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #225 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #225 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #225 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #225 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #225 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #225 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #225 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #225 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #225 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #225 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #225 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #225 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #225 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #225 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #225 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #225 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #225 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #225 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #225 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #225 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #225 | Crete (unprovenanced) | olous | `olo` | 1 |
| CHIC #225 | Crete (unprovenanced) | olu | `olu` | 1 |
| CHIC #225 | Crete (unprovenanced) | olunthos | `olu` | 1 |
| CHIC #225 | Crete (unprovenanced) | par | `par` | 1 |
| CHIC #225 | Crete (unprovenanced) | parnassos | `par` | 1 |
| CHIC #225 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #225 | Crete (unprovenanced) | paros | `par` | 1 |
| CHIC #225 | Crete (unprovenanced) | paros | `paro` | 1 |
| CHIC #225 | Crete (unprovenanced) | per | `per` | 1 |
| CHIC #225 | Crete (unprovenanced) | pergamos | `per` | 1 |
| CHIC #225 | Crete (unprovenanced) | phalasarna | `ala` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `ikil` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `ikila` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `ila` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `kil` | 1 |
| CHIC #225 | Crete (unprovenanced) | poikilassos | `kila` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `ali` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `bal` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `bali` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `obal` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `obali` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #225 | Crete (unprovenanced) | probalinthos | `robal` | 1 |
| CHIC #225 | Crete (unprovenanced) | pulos | `pul` | 1 |
| CHIC #225 | Crete (unprovenanced) | pulos | `pulo` | 1 |
| CHIC #225 | Crete (unprovenanced) | pulos | `ulo` | 1 |
| CHIC #225 | Crete (unprovenanced) | salaminos | `ala` | 1 |
| CHIC #225 | Crete (unprovenanced) | sparta | `par` | 1 |
| CHIC #225 | Crete (unprovenanced) | tarra | `tar` | 1 |
| CHIC #225 | Crete (unprovenanced) | tarsos | `tar` | 1 |
| CHIC #225 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #225 | Crete (unprovenanced) | telmessos | `tel` | 1 |
| CHIC #225 | Crete (unprovenanced) | ter | `ter` | 1 |
| CHIC #225 | Crete (unprovenanced) | termessos | `ter` | 1 |
| CHIC #225 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #225 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #225 | Crete (unprovenanced) | tirintha | `iri` | 1 |
| CHIC #225 | Crete (unprovenanced) | tirintha | `tir` | 1 |
| CHIC #225 | Crete (unprovenanced) | tirintha | `tiri` | 1 |
| CHIC #225 | Crete (unprovenanced) | tiruns | `iru` | 1 |
| CHIC #225 | Crete (unprovenanced) | tiruns | `tir` | 1 |
| CHIC #225 | Crete (unprovenanced) | tiruns | `tiru` | 1 |
| CHIC #225 | Crete (unprovenanced) | tul | `tul` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulisos | `tul` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulisos | `tuli` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulisos | `uli` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulissos | `tul` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulissos | `tuli` | 1 |
| CHIC #225 | Crete (unprovenanced) | tulissos | `uli` | 1 |
| CHIC #225 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #229 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #229 | Mallia | muke | `uke` | 1 |
| CHIC #229 | Mallia | mukenai | `uke` | 1 |
| CHIC #236 | Mallia | aptara | `ara` | 1 |
| CHIC #238 | Mochlos | aleksandros | `lek` | 1 |
| CHIC #238 | Mochlos | halikarnassos | `ika` | 1 |
| CHIC #238 | Mochlos | halikarnassos | `lik` | 1 |
| CHIC #238 | Mochlos | halikarnassos | `lika` | 1 |
| CHIC #238 | Mochlos | hierapytna | `era` | 1 |
| CHIC #238 | Mochlos | hierapytna | `erap` | 1 |
| CHIC #238 | Mochlos | hierapytna | `rap` | 1 |
| CHIC #238 | Mochlos | hyakinthos | `aki` | 1 |
| CHIC #238 | Mochlos | ida | `ida` | 1 |
| CHIC #238 | Mochlos | ikaria | `ika` | 1 |
| CHIC #238 | Mochlos | itanos | `ita` | 1 |
| CHIC #238 | Mochlos | krete | `ete` | 1 |
| CHIC #238 | Mochlos | krete | `ret` | 1 |
| CHIC #238 | Mochlos | krete | `rete` | 1 |
| CHIC #238 | Mochlos | kudonia | `udo` | 1 |
| CHIC #238 | Mochlos | kuthera | `era` | 1 |
| CHIC #238 | Mochlos | kuzikos | `iko` | 1 |
| CHIC #238 | Mochlos | lab | `lab` | 1 |
| CHIC #238 | Mochlos | lebena | `ebe` | 1 |
| CHIC #238 | Mochlos | lebena | `leb` | 1 |
| CHIC #238 | Mochlos | lebena | `lebe` | 1 |
| CHIC #238 | Mochlos | lukia | `luk` | 1 |
| CHIC #238 | Mochlos | lukia | `luki` | 1 |
| CHIC #238 | Mochlos | lukia | `uki` | 1 |
| CHIC #238 | Mochlos | lykabettos | `abe` | 1 |
| CHIC #238 | Mochlos | melitos | `eli` | 1 |
| CHIC #238 | Mochlos | melitos | `elit` | 1 |
| CHIC #238 | Mochlos | melitos | `elito` | 1 |
| CHIC #238 | Mochlos | melitos | `ito` | 1 |
| CHIC #238 | Mochlos | melitos | `lit` | 1 |
| CHIC #238 | Mochlos | melitos | `lito` | 1 |
| CHIC #238 | Mochlos | melos | `elo` | 1 |
| CHIC #238 | Mochlos | muke | `uke` | 1 |
| CHIC #238 | Mochlos | mukenai | `uke` | 1 |
| CHIC #238 | Mochlos | poikilassos | `iki` | 1 |
| CHIC #238 | Mochlos | probalinthos | `oba` | 1 |
| CHIC #238 | Mochlos | probalinthos | `rob` | 1 |
| CHIC #238 | Mochlos | probalinthos | `roba` | 1 |
| CHIC #238 | Mochlos | tegea | `ege` | 1 |
| CHIC #238 | Mochlos | thebai | `eba` | 1 |
| CHIC #238 | Mochlos | thera | `era` | 1 |
| CHIC #238 | Mochlos | zakuntos | `aku` | 1 |
| CHIC #239 | Praisos | ala | `ala` | 1 |
| CHIC #239 | Praisos | aleksandros | `ale` | 1 |
| CHIC #239 | Praisos | aptara | `ara` | 1 |
| CHIC #239 | Praisos | halikarnassos | `ali` | 1 |
| CHIC #239 | Praisos | ikaria | `ari` | 1 |
| CHIC #239 | Praisos | kalumnos | `alu` | 1 |
| CHIC #239 | Praisos | paros | `aro` | 1 |
| CHIC #239 | Praisos | phalasarna | `ala` | 1 |
| CHIC #239 | Praisos | probalinthos | `ali` | 1 |
| CHIC #239 | Praisos | salaminos | `ala` | 1 |
| CHIC #242 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #243 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #243 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #243 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #243 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #243 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #244 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #244 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #244 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #244 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #244 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #244 | Crete (unprovenanced) | hierapytna | `erap` | 1 |
| CHIC #244 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #244 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #244 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #244 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #244 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #244 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #244 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #244 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #244 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #244 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #244 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #244 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #244 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #244 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #244 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #244 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #244 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #244 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #244 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `elit` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `elito` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #244 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #244 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #244 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #244 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #244 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #244 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #244 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #244 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #244 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #244 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #244 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #244 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #246 | Kritsa | halikarnassos | `ika` | 1 |
| CHIC #246 | Kritsa | ida | `ida` | 1 |
| CHIC #246 | Kritsa | ikaria | `ika` | 1 |
| CHIC #246 | Kritsa | itanos | `ita` | 1 |
| CHIC #246 | Kritsa | kudonia | `oni` | 1 |
| CHIC #246 | Kritsa | kuzikos | `iko` | 1 |
| CHIC #246 | Kritsa | melitos | `ito` | 1 |
| CHIC #246 | Kritsa | poikilassos | `iki` | 1 |
| CHIC #247 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #247 | Mallia | ida | `ida` | 1 |
| CHIC #247 | Mallia | ikaria | `ika` | 1 |
| CHIC #247 | Mallia | itanos | `ita` | 1 |
| CHIC #247 | Mallia | kuzikos | `iko` | 1 |
| CHIC #247 | Mallia | melitos | `ito` | 1 |
| CHIC #247 | Mallia | poikilassos | `iki` | 1 |
| CHIC #248 | Palaikastro | aleksandros | `lek` | 1 |
| CHIC #248 | Palaikastro | halikarnassos | `ika` | 1 |
| CHIC #248 | Palaikastro | halikarnassos | `lik` | 1 |
| CHIC #248 | Palaikastro | halikarnassos | `lika` | 1 |
| CHIC #248 | Palaikastro | hierapytna | `era` | 1 |
| CHIC #248 | Palaikastro | hierapytna | `erap` | 1 |
| CHIC #248 | Palaikastro | hierapytna | `rap` | 1 |
| CHIC #248 | Palaikastro | hyakinthos | `aki` | 1 |
| CHIC #248 | Palaikastro | ida | `ida` | 1 |
| CHIC #248 | Palaikastro | ikaria | `ika` | 1 |
| CHIC #248 | Palaikastro | itanos | `ita` | 1 |
| CHIC #248 | Palaikastro | krete | `ete` | 1 |
| CHIC #248 | Palaikastro | krete | `ret` | 1 |
| CHIC #248 | Palaikastro | krete | `rete` | 1 |
| CHIC #248 | Palaikastro | kudonia | `udo` | 1 |
| CHIC #248 | Palaikastro | kuthera | `era` | 1 |
| CHIC #248 | Palaikastro | kuzikos | `iko` | 1 |
| CHIC #248 | Palaikastro | lab | `lab` | 1 |
| CHIC #248 | Palaikastro | lebena | `ebe` | 1 |
| CHIC #248 | Palaikastro | lebena | `leb` | 1 |
| CHIC #248 | Palaikastro | lebena | `lebe` | 1 |
| CHIC #248 | Palaikastro | lukia | `luk` | 1 |
| CHIC #248 | Palaikastro | lukia | `luki` | 1 |
| CHIC #248 | Palaikastro | lukia | `uki` | 1 |
| CHIC #248 | Palaikastro | lykabettos | `abe` | 1 |
| CHIC #248 | Palaikastro | melitos | `eli` | 1 |
| CHIC #248 | Palaikastro | melitos | `elit` | 1 |
| CHIC #248 | Palaikastro | melitos | `elito` | 1 |
| CHIC #248 | Palaikastro | melitos | `ito` | 1 |
| CHIC #248 | Palaikastro | melitos | `lit` | 1 |
| CHIC #248 | Palaikastro | melitos | `lito` | 1 |
| CHIC #248 | Palaikastro | melos | `elo` | 1 |
| CHIC #248 | Palaikastro | muke | `uke` | 1 |
| CHIC #248 | Palaikastro | mukenai | `uke` | 1 |
| CHIC #248 | Palaikastro | paros | `aro` | 1 |
| CHIC #248 | Palaikastro | poikilassos | `iki` | 1 |
| CHIC #248 | Palaikastro | probalinthos | `oba` | 1 |
| CHIC #248 | Palaikastro | probalinthos | `rob` | 1 |
| CHIC #248 | Palaikastro | probalinthos | `roba` | 1 |
| CHIC #248 | Palaikastro | tegea | `ege` | 1 |
| CHIC #248 | Palaikastro | thebai | `eba` | 1 |
| CHIC #248 | Palaikastro | thera | `era` | 1 |
| CHIC #248 | Palaikastro | zakuntos | `aku` | 1 |
| CHIC #250 | Zakros | halikarnassos | `ika` | 1 |
| CHIC #250 | Zakros | ida | `ida` | 1 |
| CHIC #250 | Zakros | ikaria | `ika` | 1 |
| CHIC #250 | Zakros | itanos | `ita` | 1 |
| CHIC #250 | Zakros | kuzikos | `iko` | 1 |
| CHIC #250 | Zakros | melitos | `ito` | 1 |
| CHIC #250 | Zakros | paros | `aro` | 1 |
| CHIC #250 | Zakros | poikilassos | `iki` | 1 |
| CHIC #251 | Arkhanes | ala | `ala` | 1 |
| CHIC #251 | Arkhanes | aleksandros | `ale` | 1 |
| CHIC #251 | Arkhanes | aptara | `ara` | 1 |
| CHIC #251 | Arkhanes | halikarnassos | `ali` | 1 |
| CHIC #251 | Arkhanes | hierapytna | `era` | 1 |
| CHIC #251 | Arkhanes | ikaria | `ari` | 1 |
| CHIC #251 | Arkhanes | kalumnos | `alu` | 1 |
| CHIC #251 | Arkhanes | korinthos | `ori` | 1 |
| CHIC #251 | Arkhanes | kuthera | `era` | 1 |
| CHIC #251 | Arkhanes | melitos | `eli` | 1 |
| CHIC #251 | Arkhanes | melos | `elo` | 1 |
| CHIC #251 | Arkhanes | olous | `olo` | 1 |
| CHIC #251 | Arkhanes | olu | `olu` | 1 |
| CHIC #251 | Arkhanes | olunthos | `olu` | 1 |
| CHIC #251 | Arkhanes | paros | `aro` | 1 |
| CHIC #251 | Arkhanes | phalasarna | `ala` | 1 |
| CHIC #251 | Arkhanes | poikilassos | `ila` | 1 |
| CHIC #251 | Arkhanes | praisos | `rai` | 1 |
| CHIC #251 | Arkhanes | probalinthos | `ali` | 1 |
| CHIC #251 | Arkhanes | pulos | `ulo` | 1 |
| CHIC #251 | Arkhanes | salaminos | `ala` | 1 |
| CHIC #251 | Arkhanes | thera | `era` | 1 |
| CHIC #251 | Arkhanes | tirintha | `iri` | 1 |
| CHIC #251 | Arkhanes | tiruns | `iru` | 1 |
| CHIC #251 | Arkhanes | tulisos | `uli` | 1 |
| CHIC #251 | Arkhanes | tulissos | `uli` | 1 |
| CHIC #252 | Arkhanes | ala | `ala` | 1 |
| CHIC #252 | Arkhanes | aleksandros | `ale` | 1 |
| CHIC #252 | Arkhanes | aptara | `ara` | 1 |
| CHIC #252 | Arkhanes | halikarnassos | `ali` | 1 |
| CHIC #252 | Arkhanes | hierapytna | `era` | 1 |
| CHIC #252 | Arkhanes | ikaria | `ari` | 1 |
| CHIC #252 | Arkhanes | kalumnos | `alu` | 1 |
| CHIC #252 | Arkhanes | korinthos | `ori` | 1 |
| CHIC #252 | Arkhanes | kuthera | `era` | 1 |
| CHIC #252 | Arkhanes | melitos | `eli` | 1 |
| CHIC #252 | Arkhanes | melos | `elo` | 1 |
| CHIC #252 | Arkhanes | olous | `olo` | 1 |
| CHIC #252 | Arkhanes | olu | `olu` | 1 |
| CHIC #252 | Arkhanes | olunthos | `olu` | 1 |
| CHIC #252 | Arkhanes | paros | `aro` | 1 |
| CHIC #252 | Arkhanes | phalasarna | `ala` | 1 |
| CHIC #252 | Arkhanes | poikilassos | `ila` | 1 |
| CHIC #252 | Arkhanes | probalinthos | `ali` | 1 |
| CHIC #252 | Arkhanes | pulos | `ulo` | 1 |
| CHIC #252 | Arkhanes | salaminos | `ala` | 1 |
| CHIC #252 | Arkhanes | thera | `era` | 1 |
| CHIC #252 | Arkhanes | tirintha | `iri` | 1 |
| CHIC #252 | Arkhanes | tiruns | `iru` | 1 |
| CHIC #252 | Arkhanes | tulisos | `uli` | 1 |
| CHIC #252 | Arkhanes | tulissos | `uli` | 1 |
| CHIC #253 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #253 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #253 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #253 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #253 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #253 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #253 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #254 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #254 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #254 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #254 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #254 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #254 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #254 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #254 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #254 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #254 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #255 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #255 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #255 | Crete (unprovenanced) | hyakinthos | `yaki` | 1 |
| CHIC #255 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #255 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #255 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #255 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #255 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #255 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #256 | Crete (unprovenanced) | poikilassos | `ila` | 1 |
| CHIC #256 | Crete (unprovenanced) | tirintha | `iri` | 1 |
| CHIC #256 | Crete (unprovenanced) | tiruns | `iru` | 1 |
| CHIC #257 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #257 | Crete (unprovenanced) | hyakinthos | `yak` | 2 |
| CHIC #257 | Crete (unprovenanced) | hyakinthos | `yaki` | 1 |
| CHIC #257 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #257 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #257 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #257 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #257 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #258 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #258 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #258 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #259 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #259 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #259 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #259 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #259 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #259 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #259 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #260 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #260 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #260 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #260 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #260 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #260 | Crete (unprovenanced) | hierapytna | `erap` | 1 |
| CHIC #260 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #260 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #260 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #260 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #260 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #260 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #260 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #260 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #260 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #260 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #260 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #260 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #260 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #260 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #260 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #260 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #260 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #260 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #260 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `elit` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `elito` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #260 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #260 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #260 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #260 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #260 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #260 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #260 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #260 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #260 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #260 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #260 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #260 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #261 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #261 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #261 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #261 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #261 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #261 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #261 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #261 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #262 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #262 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #262 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #262 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #262 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #262 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #262 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #262 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #262 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #262 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #262 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #263 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #263 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #263 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #263 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #263 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #263 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #263 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #263 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #263 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #263 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #263 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #264 | Heraklion | halikarnassos | `ika` | 1 |
| CHIC #264 | Heraklion | ida | `ida` | 1 |
| CHIC #264 | Heraklion | ikaria | `ika` | 1 |
| CHIC #264 | Heraklion | itanos | `ita` | 1 |
| CHIC #264 | Heraklion | kuzikos | `iko` | 1 |
| CHIC #264 | Heraklion | melitos | `ito` | 1 |
| CHIC #264 | Heraklion | poikilassos | `iki` | 1 |
| CHIC #265 | Kasteli | aleksandros | `lek` | 1 |
| CHIC #265 | Kasteli | halikarnassos | `ika` | 1 |
| CHIC #265 | Kasteli | halikarnassos | `lik` | 1 |
| CHIC #265 | Kasteli | halikarnassos | `lika` | 1 |
| CHIC #265 | Kasteli | hierapytna | `rap` | 1 |
| CHIC #265 | Kasteli | hyakinthos | `aki` | 1 |
| CHIC #265 | Kasteli | hyakinthos | `yak` | 1 |
| CHIC #265 | Kasteli | ida | `ida` | 1 |
| CHIC #265 | Kasteli | ikaria | `ika` | 1 |
| CHIC #265 | Kasteli | itanos | `ita` | 1 |
| CHIC #265 | Kasteli | krete | `ete` | 1 |
| CHIC #265 | Kasteli | krete | `ret` | 1 |
| CHIC #265 | Kasteli | krete | `rete` | 1 |
| CHIC #265 | Kasteli | kudonia | `udo` | 1 |
| CHIC #265 | Kasteli | kuzikos | `iko` | 1 |
| CHIC #265 | Kasteli | lab | `lab` | 1 |
| CHIC #265 | Kasteli | lebena | `ebe` | 1 |
| CHIC #265 | Kasteli | lebena | `leb` | 1 |
| CHIC #265 | Kasteli | lebena | `lebe` | 1 |
| CHIC #265 | Kasteli | lukia | `luk` | 1 |
| CHIC #265 | Kasteli | lukia | `luki` | 1 |
| CHIC #265 | Kasteli | lukia | `uki` | 1 |
| CHIC #265 | Kasteli | lykabettos | `abe` | 1 |
| CHIC #265 | Kasteli | melitos | `ito` | 1 |
| CHIC #265 | Kasteli | melitos | `lit` | 1 |
| CHIC #265 | Kasteli | melitos | `lito` | 1 |
| CHIC #265 | Kasteli | muke | `uke` | 2 |
| CHIC #265 | Kasteli | mukenai | `uke` | 2 |
| CHIC #265 | Kasteli | poikilassos | `iki` | 1 |
| CHIC #265 | Kasteli | probalinthos | `oba` | 1 |
| CHIC #265 | Kasteli | probalinthos | `rob` | 1 |
| CHIC #265 | Kasteli | probalinthos | `roba` | 1 |
| CHIC #265 | Kasteli | tegea | `ege` | 1 |
| CHIC #265 | Kasteli | thebai | `eba` | 1 |
| CHIC #265 | Kasteli | zakuntos | `aku` | 1 |
| CHIC #266 | Kordakia | halikarnassos | `ika` | 1 |
| CHIC #266 | Kordakia | ida | `ida` | 1 |
| CHIC #266 | Kordakia | ikaria | `ika` | 1 |
| CHIC #266 | Kordakia | itanos | `ita` | 2 |
| CHIC #266 | Kordakia | kuzikos | `iko` | 1 |
| CHIC #266 | Kordakia | melitos | `ito` | 1 |
| CHIC #266 | Kordakia | poikilassos | `iki` | 1 |
| CHIC #267 | Kydonia | ala | `ala` | 1 |
| CHIC #267 | Kydonia | aleksandros | `ale` | 1 |
| CHIC #267 | Kydonia | aptara | `ara` | 1 |
| CHIC #267 | Kydonia | halikarnassos | `ali` | 1 |
| CHIC #267 | Kydonia | hierapytna | `era` | 1 |
| CHIC #267 | Kydonia | hyakinthos | `yak` | 1 |
| CHIC #267 | Kydonia | ikaria | `ari` | 1 |
| CHIC #267 | Kydonia | kalumnos | `alu` | 1 |
| CHIC #267 | Kydonia | korinthos | `ori` | 1 |
| CHIC #267 | Kydonia | kuthera | `era` | 1 |
| CHIC #267 | Kydonia | melitos | `eli` | 1 |
| CHIC #267 | Kydonia | melos | `elo` | 1 |
| CHIC #267 | Kydonia | muke | `uke` | 1 |
| CHIC #267 | Kydonia | mukenai | `uke` | 1 |
| CHIC #267 | Kydonia | olous | `olo` | 1 |
| CHIC #267 | Kydonia | olu | `olu` | 1 |
| CHIC #267 | Kydonia | olunthos | `olu` | 1 |
| CHIC #267 | Kydonia | paros | `aro` | 1 |
| CHIC #267 | Kydonia | phalasarna | `ala` | 1 |
| CHIC #267 | Kydonia | poikilassos | `ila` | 1 |
| CHIC #267 | Kydonia | probalinthos | `ali` | 1 |
| CHIC #267 | Kydonia | pulos | `ulo` | 1 |
| CHIC #267 | Kydonia | salaminos | `ala` | 1 |
| CHIC #267 | Kydonia | thera | `era` | 1 |
| CHIC #267 | Kydonia | tirintha | `iri` | 1 |
| CHIC #267 | Kydonia | tiruns | `iru` | 1 |
| CHIC #267 | Kydonia | tulisos | `uli` | 1 |
| CHIC #267 | Kydonia | tulissos | `uli` | 1 |
| CHIC #268 | Lakonia | aptara | `ara` | 1 |
| CHIC #268 | Lakonia | halikarnassos | `ika` | 1 |
| CHIC #268 | Lakonia | hierapytna | `era` | 1 |
| CHIC #268 | Lakonia | ida | `ida` | 1 |
| CHIC #268 | Lakonia | ikaria | `ika` | 1 |
| CHIC #268 | Lakonia | itanos | `ita` | 1 |
| CHIC #268 | Lakonia | kuthera | `era` | 1 |
| CHIC #268 | Lakonia | kuzikos | `iko` | 1 |
| CHIC #268 | Lakonia | melitos | `ito` | 1 |
| CHIC #268 | Lakonia | poikilassos | `iki` | 1 |
| CHIC #268 | Lakonia | thera | `era` | 1 |
| CHIC #269 | Lasithi | hyakinthos | `aki` | 1 |
| CHIC #269 | Lasithi | hyakinthos | `yak` | 1 |
| CHIC #269 | Lasithi | hyakinthos | `yaki` | 1 |
| CHIC #269 | Lasithi | lukia | `uki` | 1 |
| CHIC #269 | Lasithi | paros | `aro` | 1 |
| CHIC #269 | Lasithi | poikilassos | `iki` | 1 |
| CHIC #270 | Lasithi | praisos | `rai` | 1 |
| CHIC #271 | Mallia | dikte | `dik` | 1 |
| CHIC #271 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #271 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #271 | Mallia | ida | `ida` | 1 |
| CHIC #271 | Mallia | ikaria | `ika` | 1 |
| CHIC #271 | Mallia | itanos | `ita` | 1 |
| CHIC #271 | Mallia | korinthos | `ori` | 1 |
| CHIC #271 | Mallia | kuzikos | `iko` | 1 |
| CHIC #271 | Mallia | lukia | `uki` | 1 |
| CHIC #271 | Mallia | melitos | `ito` | 1 |
| CHIC #271 | Mallia | olous | `olo` | 1 |
| CHIC #271 | Mallia | olu | `olu` | 1 |
| CHIC #271 | Mallia | olunthos | `olu` | 1 |
| CHIC #271 | Mallia | poikilassos | `iki` | 2 |
| CHIC #272 | Mirabelo | ala | `ala` | 1 |
| CHIC #272 | Mirabelo | aleksandros | `ale` | 1 |
| CHIC #272 | Mirabelo | aptara | `ara` | 1 |
| CHIC #272 | Mirabelo | halikarnassos | `ali` | 1 |
| CHIC #272 | Mirabelo | hyakinthos | `yak` | 1 |
| CHIC #272 | Mirabelo | ikaria | `ari` | 1 |
| CHIC #272 | Mirabelo | ikaria | `aria` | 1 |
| CHIC #272 | Mirabelo | ikaria | `ria` | 1 |
| CHIC #272 | Mirabelo | kalumnos | `alu` | 1 |
| CHIC #272 | Mirabelo | muke | `uke` | 1 |
| CHIC #272 | Mirabelo | mukenai | `uke` | 1 |
| CHIC #272 | Mirabelo | olous | `lou` | 1 |
| CHIC #272 | Mirabelo | paros | `aro` | 2 |
| CHIC #272 | Mirabelo | phalasarna | `ala` | 1 |
| CHIC #272 | Mirabelo | praisos | `rai` | 1 |
| CHIC #272 | Mirabelo | prie | `rie` | 1 |
| CHIC #272 | Mirabelo | priene | `rie` | 1 |
| CHIC #272 | Mirabelo | probalinthos | `ali` | 1 |
| CHIC #272 | Mirabelo | salaminos | `ala` | 1 |
| CHIC #273 | Mirabelo | hierapytna | `rap` | 1 |
| CHIC #273 | Mirabelo | hyakinthos | `aki` | 1 |
| CHIC #273 | Mirabelo | kudonia | `udo` | 1 |
| CHIC #273 | Mirabelo | lukia | `uki` | 1 |
| CHIC #273 | Mirabelo | lykabettos | `abe` | 1 |
| CHIC #273 | Mirabelo | muke | `muk` | 1 |
| CHIC #273 | Mirabelo | muke | `muke` | 1 |
| CHIC #273 | Mirabelo | muke | `uke` | 1 |
| CHIC #273 | Mirabelo | mukenai | `muk` | 1 |
| CHIC #273 | Mirabelo | mukenai | `muke` | 1 |
| CHIC #273 | Mirabelo | mukenai | `uke` | 1 |
| CHIC #273 | Mirabelo | zakuntos | `aku` | 1 |
| CHIC #274 | Mirabelo | halikarnassos | `ika` | 1 |
| CHIC #274 | Mirabelo | ida | `ida` | 1 |
| CHIC #274 | Mirabelo | ikaria | `ika` | 1 |
| CHIC #274 | Mirabelo | itanos | `ita` | 1 |
| CHIC #274 | Mirabelo | kuzikos | `iko` | 1 |
| CHIC #274 | Mirabelo | melitos | `ito` | 1 |
| CHIC #274 | Mirabelo | paros | `aro` | 1 |
| CHIC #274 | Mirabelo | poikilassos | `iki` | 1 |
| CHIC #276 | Pinakiano | ala | `ala` | 1 |
| CHIC #276 | Pinakiano | aleksandros | `ale` | 1 |
| CHIC #276 | Pinakiano | aptara | `ara` | 1 |
| CHIC #276 | Pinakiano | dikte | `dik` | 1 |
| CHIC #276 | Pinakiano | halikarnassos | `ali` | 1 |
| CHIC #276 | Pinakiano | hierapytna | `era` | 1 |
| CHIC #276 | Pinakiano | hyakinthos | `aki` | 1 |
| CHIC #276 | Pinakiano | ikaria | `ari` | 1 |
| CHIC #276 | Pinakiano | kalumnos | `alu` | 1 |
| CHIC #276 | Pinakiano | korinthos | `ori` | 1 |
| CHIC #276 | Pinakiano | kuthera | `era` | 1 |
| CHIC #276 | Pinakiano | lukia | `uki` | 1 |
| CHIC #276 | Pinakiano | melitos | `eli` | 1 |
| CHIC #276 | Pinakiano | melos | `elo` | 1 |
| CHIC #276 | Pinakiano | olous | `olo` | 1 |
| CHIC #276 | Pinakiano | olu | `olu` | 1 |
| CHIC #276 | Pinakiano | olunthos | `olu` | 1 |
| CHIC #276 | Pinakiano | paros | `aro` | 1 |
| CHIC #276 | Pinakiano | phalasarna | `ala` | 1 |
| CHIC #276 | Pinakiano | poikilassos | `iki` | 1 |
| CHIC #276 | Pinakiano | poikilassos | `ila` | 1 |
| CHIC #276 | Pinakiano | probalinthos | `ali` | 1 |
| CHIC #276 | Pinakiano | pulos | `ulo` | 1 |
| CHIC #276 | Pinakiano | salaminos | `ala` | 1 |
| CHIC #276 | Pinakiano | thera | `era` | 1 |
| CHIC #276 | Pinakiano | tirintha | `iri` | 1 |
| CHIC #276 | Pinakiano | tiruns | `iru` | 1 |
| CHIC #276 | Pinakiano | tulisos | `uli` | 1 |
| CHIC #276 | Pinakiano | tulissos | `uli` | 1 |
| CHIC #277 | Ziros | halikarnassos | `ika` | 1 |
| CHIC #277 | Ziros | ida | `ida` | 1 |
| CHIC #277 | Ziros | ikaria | `ika` | 1 |
| CHIC #277 | Ziros | itanos | `ita` | 1 |
| CHIC #277 | Ziros | kuzikos | `iko` | 1 |
| CHIC #277 | Ziros | melitos | `ito` | 1 |
| CHIC #277 | Ziros | poikilassos | `iki` | 1 |
| CHIC #279 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #280 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #280 | Mallia | ida | `ida` | 1 |
| CHIC #280 | Mallia | ikaria | `ika` | 1 |
| CHIC #280 | Mallia | itanos | `ita` | 1 |
| CHIC #280 | Mallia | kuzikos | `iko` | 1 |
| CHIC #280 | Mallia | melitos | `ito` | 1 |
| CHIC #280 | Mallia | poikilassos | `iki` | 1 |
| CHIC #281 | Mallia | aleksandros | `lek` | 1 |
| CHIC #281 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #281 | Mallia | halikarnassos | `lik` | 1 |
| CHIC #281 | Mallia | halikarnassos | `lika` | 1 |
| CHIC #281 | Mallia | hierapytna | `era` | 1 |
| CHIC #281 | Mallia | hierapytna | `erap` | 1 |
| CHIC #281 | Mallia | hierapytna | `rap` | 1 |
| CHIC #281 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #281 | Mallia | ida | `ida` | 1 |
| CHIC #281 | Mallia | ikaria | `ika` | 1 |
| CHIC #281 | Mallia | itanos | `ita` | 1 |
| CHIC #281 | Mallia | krete | `ete` | 1 |
| CHIC #281 | Mallia | krete | `ret` | 1 |
| CHIC #281 | Mallia | krete | `rete` | 1 |
| CHIC #281 | Mallia | kudonia | `udo` | 1 |
| CHIC #281 | Mallia | kuthera | `era` | 1 |
| CHIC #281 | Mallia | kuzikos | `iko` | 1 |
| CHIC #281 | Mallia | lab | `lab` | 1 |
| CHIC #281 | Mallia | lebena | `ebe` | 1 |
| CHIC #281 | Mallia | lebena | `leb` | 1 |
| CHIC #281 | Mallia | lebena | `lebe` | 1 |
| CHIC #281 | Mallia | lukia | `luk` | 1 |
| CHIC #281 | Mallia | lukia | `luki` | 1 |
| CHIC #281 | Mallia | lukia | `uki` | 1 |
| CHIC #281 | Mallia | lykabettos | `abe` | 1 |
| CHIC #281 | Mallia | melitos | `eli` | 1 |
| CHIC #281 | Mallia | melitos | `elit` | 1 |
| CHIC #281 | Mallia | melitos | `elito` | 1 |
| CHIC #281 | Mallia | melitos | `ito` | 1 |
| CHIC #281 | Mallia | melitos | `lit` | 1 |
| CHIC #281 | Mallia | melitos | `lito` | 1 |
| CHIC #281 | Mallia | melos | `elo` | 1 |
| CHIC #281 | Mallia | muke | `uke` | 1 |
| CHIC #281 | Mallia | mukenai | `uke` | 1 |
| CHIC #281 | Mallia | poikilassos | `iki` | 1 |
| CHIC #281 | Mallia | probalinthos | `oba` | 1 |
| CHIC #281 | Mallia | probalinthos | `rob` | 1 |
| CHIC #281 | Mallia | probalinthos | `roba` | 1 |
| CHIC #281 | Mallia | tegea | `ege` | 1 |
| CHIC #281 | Mallia | thebai | `eba` | 1 |
| CHIC #281 | Mallia | thera | `era` | 1 |
| CHIC #281 | Mallia | zakuntos | `aku` | 1 |
| CHIC #282 | Pyrgos (Myrtos) | hyakinthos | `yak` | 1 |
| CHIC #282 | Pyrgos (Myrtos) | muke | `uke` | 1 |
| CHIC #282 | Pyrgos (Myrtos) | mukenai | `uke` | 1 |
| CHIC #283 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #283 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #283 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #283 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #283 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #283 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #283 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #283 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #283 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #283 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #284 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #286 | Mallia | aptara | `ara` | 1 |
| CHIC #286 | Mallia | hierapytna | `era` | 1 |
| CHIC #286 | Mallia | kuthera | `era` | 1 |
| CHIC #286 | Mallia | thera | `era` | 1 |
| CHIC #287 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #287 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #287 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #287 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #287 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #287 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #287 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #287 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #287 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #287 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #287 | Crete (unprovenanced) | tegea | `teg` | 1 |
| CHIC #287 | Crete (unprovenanced) | tegea | `tege` | 1 |
| CHIC #287 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #288 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #288 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #288 | Mallia | ida | `ida` | 1 |
| CHIC #288 | Mallia | ikaria | `ika` | 1 |
| CHIC #288 | Mallia | itanos | `ita` | 1 |
| CHIC #288 | Mallia | kuzikos | `iko` | 1 |
| CHIC #288 | Mallia | melitos | `ito` | 1 |
| CHIC #288 | Mallia | muke | `uke` | 1 |
| CHIC #288 | Mallia | mukenai | `uke` | 1 |
| CHIC #288 | Mallia | poikilassos | `iki` | 1 |
| CHIC #289 | Palaikastro | ala | `ala` | 2 |
| CHIC #289 | Palaikastro | aleksandros | `ale` | 2 |
| CHIC #289 | Palaikastro | aptara | `ara` | 2 |
| CHIC #289 | Palaikastro | aptara | `tar` | 2 |
| CHIC #289 | Palaikastro | aptara | `tara` | 2 |
| CHIC #289 | Palaikastro | gor | `gor` | 2 |
| CHIC #289 | Palaikastro | gortyn | `gor` | 2 |
| CHIC #289 | Palaikastro | halikarnassos | `ali` | 2 |
| CHIC #289 | Palaikastro | halikarnassos | `kar` | 2 |
| CHIC #289 | Palaikastro | hierapytna | `era` | 2 |
| CHIC #289 | Palaikastro | ikaria | `ari` | 2 |
| CHIC #289 | Palaikastro | ikaria | `kar` | 2 |
| CHIC #289 | Palaikastro | ikaria | `kari` | 2 |
| CHIC #289 | Palaikastro | kalumnos | `alu` | 2 |
| CHIC #289 | Palaikastro | kalumnos | `kal` | 2 |
| CHIC #289 | Palaikastro | kalumnos | `kalu` | 2 |
| CHIC #289 | Palaikastro | kor | `kor` | 2 |
| CHIC #289 | Palaikastro | korinthos | `kor` | 2 |
| CHIC #289 | Palaikastro | korinthos | `kori` | 2 |
| CHIC #289 | Palaikastro | korinthos | `ori` | 2 |
| CHIC #289 | Palaikastro | krete | `ete` | 1 |
| CHIC #289 | Palaikastro | kuthera | `era` | 2 |
| CHIC #289 | Palaikastro | lebena | `ebe` | 1 |
| CHIC #289 | Palaikastro | melitos | `eli` | 2 |
| CHIC #289 | Palaikastro | melos | `elo` | 2 |
| CHIC #289 | Palaikastro | olous | `olo` | 2 |
| CHIC #289 | Palaikastro | olu | `olu` | 2 |
| CHIC #289 | Palaikastro | olunthos | `olu` | 2 |
| CHIC #289 | Palaikastro | par | `par` | 2 |
| CHIC #289 | Palaikastro | parnassos | `par` | 2 |
| CHIC #289 | Palaikastro | paros | `aro` | 2 |
| CHIC #289 | Palaikastro | paros | `par` | 2 |
| CHIC #289 | Palaikastro | paros | `paro` | 2 |
| CHIC #289 | Palaikastro | per | `per` | 2 |
| CHIC #289 | Palaikastro | pergamos | `per` | 2 |
| CHIC #289 | Palaikastro | phalasarna | `ala` | 2 |
| CHIC #289 | Palaikastro | poikilassos | `ila` | 2 |
| CHIC #289 | Palaikastro | poikilassos | `kil` | 2 |
| CHIC #289 | Palaikastro | poikilassos | `kila` | 2 |
| CHIC #289 | Palaikastro | probalinthos | `ali` | 2 |
| CHIC #289 | Palaikastro | probalinthos | `bal` | 2 |
| CHIC #289 | Palaikastro | probalinthos | `bali` | 2 |
| CHIC #289 | Palaikastro | pulos | `pul` | 2 |
| CHIC #289 | Palaikastro | pulos | `pulo` | 2 |
| CHIC #289 | Palaikastro | pulos | `ulo` | 2 |
| CHIC #289 | Palaikastro | salaminos | `ala` | 2 |
| CHIC #289 | Palaikastro | sparta | `par` | 2 |
| CHIC #289 | Palaikastro | tarra | `tar` | 2 |
| CHIC #289 | Palaikastro | tarsos | `tar` | 2 |
| CHIC #289 | Palaikastro | tegea | `ege` | 1 |
| CHIC #289 | Palaikastro | telmessos | `tel` | 2 |
| CHIC #289 | Palaikastro | ter | `ter` | 2 |
| CHIC #289 | Palaikastro | termessos | `ter` | 2 |
| CHIC #289 | Palaikastro | thebai | `eba` | 1 |
| CHIC #289 | Palaikastro | thera | `era` | 2 |
| CHIC #289 | Palaikastro | tirintha | `iri` | 2 |
| CHIC #289 | Palaikastro | tirintha | `tir` | 2 |
| CHIC #289 | Palaikastro | tirintha | `tiri` | 2 |
| CHIC #289 | Palaikastro | tiruns | `iru` | 2 |
| CHIC #289 | Palaikastro | tiruns | `tir` | 2 |
| CHIC #289 | Palaikastro | tiruns | `tiru` | 2 |
| CHIC #289 | Palaikastro | tul | `tul` | 2 |
| CHIC #289 | Palaikastro | tulisos | `tul` | 2 |
| CHIC #289 | Palaikastro | tulisos | `tuli` | 2 |
| CHIC #289 | Palaikastro | tulisos | `uli` | 2 |
| CHIC #289 | Palaikastro | tulissos | `tul` | 2 |
| CHIC #289 | Palaikastro | tulissos | `tuli` | 2 |
| CHIC #289 | Palaikastro | tulissos | `uli` | 2 |
| CHIC #290 | Sitia | paros | `aro` | 1 |
| CHIC #290 | Sitia | probalinthos | `oba` | 1 |
| CHIC #290 | Sitia | probalinthos | `rob` | 1 |
| CHIC #290 | Sitia | probalinthos | `roba` | 1 |
| CHIC #293 | Adromili | paros | `aro` | 1 |
| CHIC #294 | Crete (unprovenanced) | aptara | `ara` | 1 |
| CHIC #294 | Crete (unprovenanced) | ardettos | `det` | 1 |
| CHIC #294 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #294 | Crete (unprovenanced) | hierapytna | `era` | 2 |
| CHIC #294 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #294 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #294 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #294 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #294 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #294 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #294 | Crete (unprovenanced) | kudonia | `oni` | 1 |
| CHIC #294 | Crete (unprovenanced) | kuthera | `era` | 2 |
| CHIC #294 | Crete (unprovenanced) | kuthera | `kut` | 1 |
| CHIC #294 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #294 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #294 | Crete (unprovenanced) | lykabettos | `bet` | 1 |
| CHIC #294 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #294 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #294 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #294 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #294 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #294 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #294 | Crete (unprovenanced) | thera | `era` | 2 |
| CHIC #294 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #295 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #295 | Crete (unprovenanced) | halikarnassos | `ika` | 2 |
| CHIC #295 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #295 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #295 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #295 | Crete (unprovenanced) | hierapytna | `erap` | 1 |
| CHIC #295 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #295 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #295 | Crete (unprovenanced) | ida | `ida` | 2 |
| CHIC #295 | Crete (unprovenanced) | ikaria | `ika` | 2 |
| CHIC #295 | Crete (unprovenanced) | itanos | `ita` | 2 |
| CHIC #295 | Crete (unprovenanced) | kalumnos | `lum` | 1 |
| CHIC #295 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #295 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #295 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #295 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #295 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #295 | Crete (unprovenanced) | kuzikos | `iko` | 2 |
| CHIC #295 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #295 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #295 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #295 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #295 | Crete (unprovenanced) | lem | `lem` | 1 |
| CHIC #295 | Crete (unprovenanced) | lemnos | `lem` | 1 |
| CHIC #295 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #295 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #295 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #295 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #295 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #295 | Crete (unprovenanced) | melitos | `elit` | 1 |
| CHIC #295 | Crete (unprovenanced) | melitos | `elito` | 1 |
| CHIC #295 | Crete (unprovenanced) | melitos | `ito` | 2 |
| CHIC #295 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #295 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #295 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #295 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #295 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #295 | Crete (unprovenanced) | poikilassos | `iki` | 2 |
| CHIC #295 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #295 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #295 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #295 | Crete (unprovenanced) | salaminos | `lam` | 1 |
| CHIC #295 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #295 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #295 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #295 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #296 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #296 | Crete (unprovenanced) | halikarnassos | `ika` | 2 |
| CHIC #296 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #296 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #296 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #296 | Crete (unprovenanced) | hierapytna | `erap` | 1 |
| CHIC #296 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #296 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #296 | Crete (unprovenanced) | ida | `ida` | 2 |
| CHIC #296 | Crete (unprovenanced) | ikaria | `ika` | 2 |
| CHIC #296 | Crete (unprovenanced) | itanos | `ita` | 2 |
| CHIC #296 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #296 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #296 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #296 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #296 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #296 | Crete (unprovenanced) | kuzikos | `iko` | 2 |
| CHIC #296 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #296 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #296 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #296 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #296 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #296 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #296 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #296 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #296 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #296 | Crete (unprovenanced) | melitos | `elit` | 1 |
| CHIC #296 | Crete (unprovenanced) | melitos | `elito` | 1 |
| CHIC #296 | Crete (unprovenanced) | melitos | `ito` | 2 |
| CHIC #296 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #296 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #296 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #296 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #296 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #296 | Crete (unprovenanced) | poikilassos | `iki` | 2 |
| CHIC #296 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #296 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #296 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #296 | Crete (unprovenanced) | rhytion | `tio` | 1 |
| CHIC #296 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #296 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #296 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #296 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #297 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #297 | Crete (unprovenanced) | ardettos | `det` | 1 |
| CHIC #297 | Crete (unprovenanced) | halikarnassos | `ika` | 2 |
| CHIC #297 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #297 | Crete (unprovenanced) | halikarnassos | `lika` | 1 |
| CHIC #297 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #297 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #297 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #297 | Crete (unprovenanced) | ida | `ida` | 2 |
| CHIC #297 | Crete (unprovenanced) | ikaria | `ika` | 2 |
| CHIC #297 | Crete (unprovenanced) | itanos | `ita` | 2 |
| CHIC #297 | Crete (unprovenanced) | krete | `ete` | 2 |
| CHIC #297 | Crete (unprovenanced) | krete | `ret` | 1 |
| CHIC #297 | Crete (unprovenanced) | krete | `rete` | 1 |
| CHIC #297 | Crete (unprovenanced) | kudonia | `udo` | 1 |
| CHIC #297 | Crete (unprovenanced) | kuthera | `kut` | 1 |
| CHIC #297 | Crete (unprovenanced) | kuzikos | `iko` | 2 |
| CHIC #297 | Crete (unprovenanced) | lab | `lab` | 1 |
| CHIC #297 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #297 | Crete (unprovenanced) | lebena | `leb` | 1 |
| CHIC #297 | Crete (unprovenanced) | lebena | `lebe` | 1 |
| CHIC #297 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #297 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #297 | Crete (unprovenanced) | lukia | `uki` | 1 |
| CHIC #297 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #297 | Crete (unprovenanced) | lykabettos | `bet` | 1 |
| CHIC #297 | Crete (unprovenanced) | melitos | `ito` | 2 |
| CHIC #297 | Crete (unprovenanced) | melitos | `lit` | 1 |
| CHIC #297 | Crete (unprovenanced) | melitos | `lito` | 1 |
| CHIC #297 | Crete (unprovenanced) | muke | `uke` | 2 |
| CHIC #297 | Crete (unprovenanced) | mukenai | `uke` | 2 |
| CHIC #297 | Crete (unprovenanced) | poikilassos | `iki` | 2 |
| CHIC #297 | Crete (unprovenanced) | probalinthos | `oba` | 1 |
| CHIC #297 | Crete (unprovenanced) | probalinthos | `rob` | 1 |
| CHIC #297 | Crete (unprovenanced) | probalinthos | `roba` | 1 |
| CHIC #297 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #297 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #297 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #298 | Crete (unprovenanced) | aptara | `ara` | 2 |
| CHIC #298 | Crete (unprovenanced) | aptara | `tar` | 2 |
| CHIC #298 | Crete (unprovenanced) | aptara | `tara` | 2 |
| CHIC #298 | Crete (unprovenanced) | gor | `gor` | 2 |
| CHIC #298 | Crete (unprovenanced) | gortyn | `gor` | 2 |
| CHIC #298 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #298 | Crete (unprovenanced) | halikarnassos | `kar` | 2 |
| CHIC #298 | Crete (unprovenanced) | hierapytna | `era` | 2 |
| CHIC #298 | Crete (unprovenanced) | hierapytna | `erap` | 1 |
| CHIC #298 | Crete (unprovenanced) | hierapytna | `rap` | 1 |
| CHIC #298 | Crete (unprovenanced) | hyakinthos | `aki` | 1 |
| CHIC #298 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #298 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #298 | Crete (unprovenanced) | ikaria | `kar` | 2 |
| CHIC #298 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #298 | Crete (unprovenanced) | kor | `kor` | 2 |
| CHIC #298 | Crete (unprovenanced) | korinthos | `kor` | 2 |
| CHIC #298 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #298 | Crete (unprovenanced) | kuthera | `era` | 2 |
| CHIC #298 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #298 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #298 | Crete (unprovenanced) | lykabettos | `abe` | 1 |
| CHIC #298 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #298 | Crete (unprovenanced) | par | `par` | 2 |
| CHIC #298 | Crete (unprovenanced) | parnassos | `par` | 2 |
| CHIC #298 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #298 | Crete (unprovenanced) | paros | `par` | 2 |
| CHIC #298 | Crete (unprovenanced) | per | `per` | 2 |
| CHIC #298 | Crete (unprovenanced) | pergamos | `per` | 2 |
| CHIC #298 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #298 | Crete (unprovenanced) | sparta | `par` | 2 |
| CHIC #298 | Crete (unprovenanced) | tarra | `tar` | 2 |
| CHIC #298 | Crete (unprovenanced) | tarsos | `tar` | 2 |
| CHIC #298 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #298 | Crete (unprovenanced) | ter | `ter` | 2 |
| CHIC #298 | Crete (unprovenanced) | termessos | `ter` | 2 |
| CHIC #298 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #298 | Crete (unprovenanced) | thera | `era` | 2 |
| CHIC #298 | Crete (unprovenanced) | tirintha | `tir` | 2 |
| CHIC #298 | Crete (unprovenanced) | tiruns | `tir` | 2 |
| CHIC #298 | Crete (unprovenanced) | zakuntos | `aku` | 1 |
| CHIC #299 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #299 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #299 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #299 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #299 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #299 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #299 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #299 | Crete (unprovenanced) | muke | `uke` | 1 |
| CHIC #299 | Crete (unprovenanced) | mukenai | `uke` | 1 |
| CHIC #299 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #299 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #300 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #301 | Crete (unprovenanced) | halikarnassos | `ika` | 1 |
| CHIC #301 | Crete (unprovenanced) | ida | `ida` | 1 |
| CHIC #301 | Crete (unprovenanced) | ikaria | `ika` | 1 |
| CHIC #301 | Crete (unprovenanced) | itanos | `ita` | 1 |
| CHIC #301 | Crete (unprovenanced) | kuzikos | `iko` | 1 |
| CHIC #301 | Crete (unprovenanced) | melitos | `ito` | 1 |
| CHIC #301 | Crete (unprovenanced) | poikilassos | `iki` | 1 |
| CHIC #302 | Crete (unprovenanced) | aleksandros | `lek` | 1 |
| CHIC #302 | Crete (unprovenanced) | halikarnassos | `lik` | 1 |
| CHIC #302 | Crete (unprovenanced) | hierapytna | `era` | 1 |
| CHIC #302 | Crete (unprovenanced) | hyakinthos | `aki` | 2 |
| CHIC #302 | Crete (unprovenanced) | hyakinthos | `yak` | 1 |
| CHIC #302 | Crete (unprovenanced) | hyakinthos | `yaki` | 1 |
| CHIC #302 | Crete (unprovenanced) | kuthera | `era` | 1 |
| CHIC #302 | Crete (unprovenanced) | lukia | `luk` | 1 |
| CHIC #302 | Crete (unprovenanced) | lukia | `luki` | 1 |
| CHIC #302 | Crete (unprovenanced) | lukia | `uki` | 2 |
| CHIC #302 | Crete (unprovenanced) | melitos | `eli` | 1 |
| CHIC #302 | Crete (unprovenanced) | melos | `elo` | 1 |
| CHIC #302 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #302 | Crete (unprovenanced) | poikilassos | `iki` | 2 |
| CHIC #302 | Crete (unprovenanced) | thera | `era` | 1 |
| CHIC #303 | Crete (unprovenanced) | krete | `ete` | 1 |
| CHIC #303 | Crete (unprovenanced) | lebena | `ebe` | 1 |
| CHIC #303 | Crete (unprovenanced) | poikilassos | `poi` | 1 |
| CHIC #303 | Crete (unprovenanced) | tegea | `ege` | 1 |
| CHIC #303 | Crete (unprovenanced) | thebai | `bai` | 1 |
| CHIC #303 | Crete (unprovenanced) | thebai | `eba` | 1 |
| CHIC #303 | Crete (unprovenanced) | thebai | `ebai` | 1 |
| CHIC #304 | Crete (unprovenanced) | par | `par` | 1 |
| CHIC #304 | Crete (unprovenanced) | parnassos | `par` | 1 |
| CHIC #304 | Crete (unprovenanced) | paros | `aro` | 1 |
| CHIC #304 | Crete (unprovenanced) | paros | `par` | 1 |
| CHIC #304 | Crete (unprovenanced) | paros | `paro` | 1 |
| CHIC #304 | Crete (unprovenanced) | sparta | `par` | 1 |
| CHIC #305 | Lastros | halikarnassos | `ika` | 1 |
| CHIC #305 | Lastros | hyakinthos | `aki` | 1 |
| CHIC #305 | Lastros | ida | `ida` | 1 |
| CHIC #305 | Lastros | ikaria | `ika` | 1 |
| CHIC #305 | Lastros | itanos | `ita` | 1 |
| CHIC #305 | Lastros | kuzikos | `iko` | 1 |
| CHIC #305 | Lastros | lukia | `kia` | 1 |
| CHIC #305 | Lastros | lykabettos | `abe` | 1 |
| CHIC #305 | Lastros | melitos | `ito` | 1 |
| CHIC #305 | Lastros | poikilassos | `iki` | 1 |
| CHIC #305 | Lastros | tegea | `gea` | 1 |
| CHIC #305 | Lastros | zakuntos | `aku` | 1 |
| CHIC #306 | Mallia | ardettos | `det` | 1 |
| CHIC #306 | Mallia | dikte | `dik` | 1 |
| CHIC #306 | Mallia | halikarnassos | `ika` | 1 |
| CHIC #306 | Mallia | hyakinthos | `aki` | 1 |
| CHIC #306 | Mallia | ida | `ida` | 1 |
| CHIC #306 | Mallia | ikaria | `ika` | 1 |
| CHIC #306 | Mallia | itanos | `ita` | 1 |
| CHIC #306 | Mallia | krete | `ete` | 1 |
| CHIC #306 | Mallia | kudonia | `kud` | 1 |
| CHIC #306 | Mallia | kudonia | `kudo` | 1 |
| CHIC #306 | Mallia | kudonia | `udo` | 1 |
| CHIC #306 | Mallia | kuthera | `kut` | 1 |
| CHIC #306 | Mallia | kuzikos | `iko` | 1 |
| CHIC #306 | Mallia | lebena | `ebe` | 1 |
| CHIC #306 | Mallia | lukia | `uki` | 1 |
| CHIC #306 | Mallia | lykabettos | `abe` | 1 |
| CHIC #306 | Mallia | lykabettos | `bet` | 1 |
| CHIC #306 | Mallia | lykabettos | `kab` | 1 |
| CHIC #306 | Mallia | lykabettos | `kabe` | 1 |
| CHIC #306 | Mallia | melitos | `ito` | 1 |
| CHIC #306 | Mallia | muke | `uke` | 1 |
| CHIC #306 | Mallia | mukenai | `uke` | 1 |
| CHIC #306 | Mallia | poikilassos | `iki` | 1 |
| CHIC #306 | Mallia | probalinthos | `oba` | 1 |
| CHIC #306 | Mallia | tegea | `ege` | 1 |
| CHIC #306 | Mallia | tegea | `teg` | 1 |
| CHIC #306 | Mallia | tegea | `tege` | 1 |
| CHIC #306 | Mallia | thebai | `eba` | 1 |
| CHIC #306 | Mallia | zakuntos | `aku` | 1 |
| CHIC #308 | Palaikastro | halikarnassos | `ika` | 1 |
| CHIC #308 | Palaikastro | hyakinthos | `yak` | 1 |
| CHIC #308 | Palaikastro | ida | `ida` | 1 |
| CHIC #308 | Palaikastro | ikaria | `ika` | 1 |
| CHIC #308 | Palaikastro | ikaria | `ria` | 1 |
| CHIC #308 | Palaikastro | itanos | `ita` | 1 |
| CHIC #308 | Palaikastro | kuzikos | `iko` | 1 |
| CHIC #308 | Palaikastro | melitos | `ito` | 1 |
| CHIC #308 | Palaikastro | muke | `uke` | 1 |
| CHIC #308 | Palaikastro | mukenai | `uke` | 1 |
| CHIC #308 | Palaikastro | olous | `lou` | 1 |
| CHIC #308 | Palaikastro | poikilassos | `iki` | 1 |
| CHIC #308 | Palaikastro | praisos | `rai` | 1 |
| CHIC #308 | Palaikastro | prie | `rie` | 1 |
| CHIC #308 | Palaikastro | priene | `rie` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | halikarnassos | `ika` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | hyakinthos | `aki` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | hyakinthos | `yak` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | ida | `ida` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | ikaria | `ika` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | itanos | `ita` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | kuzikos | `iko` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | lykabettos | `abe` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | melitos | `ito` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | muke | `uke` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | mukenai | `uke` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | orchomenos | `men` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | orchomenos | `ome` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | orchomenos | `omen` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | paros | `aro` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | pergamos | `gam` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | poikilassos | `iki` | 1 |
| CHIC #309 | Pyrgos (Myrtos) | zakuntos | `aku` | 1 |
| CHIC #310 | Sitia | aleksandros | `lek` | 1 |
| CHIC #310 | Sitia | halikarnassos | `ika` | 1 |
| CHIC #310 | Sitia | halikarnassos | `lik` | 1 |
| CHIC #310 | Sitia | halikarnassos | `lika` | 1 |
| CHIC #310 | Sitia | hierapytna | `era` | 1 |
| CHIC #310 | Sitia | hierapytna | `erap` | 1 |
| CHIC #310 | Sitia | hierapytna | `rap` | 1 |
| CHIC #310 | Sitia | hyakinthos | `aki` | 2 |
| CHIC #310 | Sitia | hyakinthos | `yak` | 1 |
| CHIC #310 | Sitia | hyakinthos | `yaki` | 1 |
| CHIC #310 | Sitia | ida | `ida` | 1 |
| CHIC #310 | Sitia | ikaria | `ika` | 1 |
| CHIC #310 | Sitia | itanos | `ita` | 1 |
| CHIC #310 | Sitia | krete | `ete` | 1 |
| CHIC #310 | Sitia | krete | `ret` | 1 |
| CHIC #310 | Sitia | krete | `rete` | 1 |
| CHIC #310 | Sitia | kudonia | `udo` | 1 |
| CHIC #310 | Sitia | kuthera | `era` | 1 |
| CHIC #310 | Sitia | kuzikos | `iko` | 1 |
| CHIC #310 | Sitia | lab | `lab` | 1 |
| CHIC #310 | Sitia | lebena | `ebe` | 1 |
| CHIC #310 | Sitia | lebena | `leb` | 1 |
| CHIC #310 | Sitia | lebena | `lebe` | 1 |
| CHIC #310 | Sitia | lukia | `luk` | 1 |
| CHIC #310 | Sitia | lukia | `luki` | 1 |
| CHIC #310 | Sitia | lukia | `uki` | 2 |
| CHIC #310 | Sitia | lykabettos | `abe` | 1 |
| CHIC #310 | Sitia | melitos | `eli` | 1 |
| CHIC #310 | Sitia | melitos | `elit` | 1 |
| CHIC #310 | Sitia | melitos | `elito` | 1 |
| CHIC #310 | Sitia | melitos | `ito` | 1 |
| CHIC #310 | Sitia | melitos | `lit` | 1 |
| CHIC #310 | Sitia | melitos | `lito` | 1 |
| CHIC #310 | Sitia | melos | `elo` | 1 |
| CHIC #310 | Sitia | muke | `uke` | 1 |
| CHIC #310 | Sitia | mukenai | `uke` | 1 |
| CHIC #310 | Sitia | poikilassos | `iki` | 2 |
| CHIC #310 | Sitia | probalinthos | `oba` | 1 |
| CHIC #310 | Sitia | probalinthos | `rob` | 1 |
| CHIC #310 | Sitia | probalinthos | `roba` | 1 |
| CHIC #310 | Sitia | tegea | `ege` | 1 |
| CHIC #310 | Sitia | thebai | `eba` | 1 |
| CHIC #310 | Sitia | thera | `era` | 1 |
| CHIC #310 | Sitia | zakuntos | `aku` | 1 |
| CHIC #311 | Sitia | halikarnassos | `ika` | 1 |
| CHIC #311 | Sitia | ida | `ida` | 1 |
| CHIC #311 | Sitia | ikaria | `ika` | 1 |
| CHIC #311 | Sitia | itanos | `ita` | 1 |
| CHIC #311 | Sitia | kuzikos | `iko` | 1 |
| CHIC #311 | Sitia | melitos | `ito` | 1 |
| CHIC #311 | Sitia | poikilassos | `iki` | 1 |
| CHIC #312 | Xida | hyakinthos | `yak` | 1 |
| CHIC #312 | Xida | muke | `uke` | 1 |
| CHIC #312 | Xida | mukenai | `uke` | 1 |
| CHIC #312 | Xida | paros | `aro` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | ala | `ala` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | aleksandros | `ale` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | aptara | `ara` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | halikarnassos | `ali` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | hierapytna | `era` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | ikaria | `ari` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | kalumnos | `alu` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | korinthos | `ori` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | kuthera | `era` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | melitos | `eli` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | melos | `elo` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | olous | `olo` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | olu | `olu` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | olunthos | `olu` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | paros | `aro` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | phalasarna | `ala` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | poikilassos | `ila` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | probalinthos | `ali` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | pulos | `ulo` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | salaminos | `ala` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | thera | `era` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | tirintha | `iri` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | tiruns | `iru` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | tulisos | `uli` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | tulissos | `uli` | 1 |
| CHIC #314 | Neapolis | ala | `ala` | 2 |
| CHIC #314 | Neapolis | aleksandros | `ale` | 2 |
| CHIC #314 | Neapolis | aptara | `ara` | 2 |
| CHIC #314 | Neapolis | halikarnassos | `ali` | 2 |
| CHIC #314 | Neapolis | halikarnassos | `ika` | 1 |
| CHIC #314 | Neapolis | hierapytna | `era` | 2 |
| CHIC #314 | Neapolis | hyakinthos | `yak` | 1 |
| CHIC #314 | Neapolis | ida | `ida` | 1 |
| CHIC #314 | Neapolis | ikaria | `ari` | 2 |
| CHIC #314 | Neapolis | ikaria | `ika` | 1 |
| CHIC #314 | Neapolis | itanos | `ita` | 1 |
| CHIC #314 | Neapolis | kalumnos | `alu` | 2 |
| CHIC #314 | Neapolis | korinthos | `ori` | 3 |
| CHIC #314 | Neapolis | kuthera | `era` | 2 |
| CHIC #314 | Neapolis | kuzikos | `iko` | 1 |
| CHIC #314 | Neapolis | melitos | `eli` | 2 |
| CHIC #314 | Neapolis | melitos | `ito` | 1 |
| CHIC #314 | Neapolis | melos | `elo` | 2 |
| CHIC #314 | Neapolis | muke | `uke` | 1 |
| CHIC #314 | Neapolis | mukenai | `uke` | 1 |
| CHIC #314 | Neapolis | olous | `olo` | 3 |
| CHIC #314 | Neapolis | olu | `olu` | 3 |
| CHIC #314 | Neapolis | olunthos | `olu` | 3 |
| CHIC #314 | Neapolis | paros | `aro` | 4 |
| CHIC #314 | Neapolis | phalasarna | `ala` | 2 |
| CHIC #314 | Neapolis | poikilassos | `iki` | 1 |
| CHIC #314 | Neapolis | poikilassos | `ila` | 2 |
| CHIC #314 | Neapolis | probalinthos | `ali` | 2 |
| CHIC #314 | Neapolis | pulos | `ulo` | 2 |
| CHIC #314 | Neapolis | salaminos | `ala` | 2 |
| CHIC #314 | Neapolis | thera | `era` | 2 |
| CHIC #314 | Neapolis | tirintha | `iri` | 2 |
| CHIC #314 | Neapolis | tiruns | `iru` | 2 |
| CHIC #314 | Neapolis | tulisos | `uli` | 2 |
| CHIC #314 | Neapolis | tulissos | `uli` | 2 |
| CHIC #316 | Mallia | itanos | `ita` | 1 |
| CHIC #317 | Mallia | ala | `ala` | 1 |
| CHIC #317 | Mallia | aleksandros | `ale` | 1 |
| CHIC #317 | Mallia | aptara | `ara` | 1 |
| CHIC #317 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #317 | Mallia | ikaria | `ari` | 1 |
| CHIC #317 | Mallia | kalumnos | `alu` | 1 |
| CHIC #317 | Mallia | krete | `ret` | 1 |
| CHIC #317 | Mallia | melitos | `lit` | 1 |
| CHIC #317 | Mallia | paros | `aro` | 1 |
| CHIC #317 | Mallia | phalasarna | `ala` | 1 |
| CHIC #317 | Mallia | probalinthos | `ali` | 1 |
| CHIC #317 | Mallia | salaminos | `ala` | 1 |
| CHIC #318 | Mallia | hyakinthos | `yak` | 1 |
| CHIC #318 | Mallia | muke | `uke` | 1 |
| CHIC #318 | Mallia | mukenai | `uke` | 1 |
| CHIC #320 | Mallia | itanos | `ita` | 1 |
| CHIC #321 | Mallia | aptara | `ara` | 1 |
| CHIC #321 | Mallia | aptara | `tar` | 1 |
| CHIC #321 | Mallia | aptara | `tara` | 1 |
| CHIC #321 | Mallia | gor | `gor` | 1 |
| CHIC #321 | Mallia | gortyn | `gor` | 1 |
| CHIC #321 | Mallia | halikarnassos | `kar` | 1 |
| CHIC #321 | Mallia | hierapytna | `era` | 1 |
| CHIC #321 | Mallia | ikaria | `kar` | 1 |
| CHIC #321 | Mallia | kor | `kor` | 1 |
| CHIC #321 | Mallia | korinthos | `kor` | 1 |
| CHIC #321 | Mallia | kuthera | `era` | 1 |
| CHIC #321 | Mallia | par | `par` | 1 |
| CHIC #321 | Mallia | parnassos | `par` | 1 |
| CHIC #321 | Mallia | paros | `par` | 1 |
| CHIC #321 | Mallia | per | `per` | 1 |
| CHIC #321 | Mallia | pergamos | `per` | 1 |
| CHIC #321 | Mallia | sparta | `par` | 1 |
| CHIC #321 | Mallia | tarra | `tar` | 1 |
| CHIC #321 | Mallia | tarsos | `tar` | 1 |
| CHIC #321 | Mallia | ter | `ter` | 1 |
| CHIC #321 | Mallia | termessos | `ter` | 1 |
| CHIC #321 | Mallia | thera | `era` | 1 |
| CHIC #321 | Mallia | tirintha | `tir` | 1 |
| CHIC #321 | Mallia | tiruns | `tir` | 1 |
| CHIC #322 | Mallia | ala | `ala` | 1 |
| CHIC #322 | Mallia | aleksandros | `ale` | 1 |
| CHIC #322 | Mallia | aptara | `ara` | 1 |
| CHIC #322 | Mallia | halikarnassos | `ali` | 1 |
| CHIC #322 | Mallia | hierapytna | `era` | 1 |
| CHIC #322 | Mallia | ikaria | `ari` | 1 |
| CHIC #322 | Mallia | kalumnos | `alu` | 1 |
| CHIC #322 | Mallia | korinthos | `ori` | 1 |
| CHIC #322 | Mallia | kuthera | `era` | 1 |
| CHIC #322 | Mallia | melitos | `eli` | 1 |
| CHIC #322 | Mallia | melos | `elo` | 1 |
| CHIC #322 | Mallia | olous | `olo` | 1 |
| CHIC #322 | Mallia | olu | `olu` | 1 |
| CHIC #322 | Mallia | olunthos | `olu` | 1 |
| CHIC #322 | Mallia | paros | `aro` | 1 |
| CHIC #322 | Mallia | phalasarna | `ala` | 1 |
| CHIC #322 | Mallia | poikilassos | `ila` | 1 |
| CHIC #322 | Mallia | probalinthos | `ali` | 1 |
| CHIC #322 | Mallia | pulos | `ulo` | 1 |
| CHIC #322 | Mallia | salaminos | `ala` | 1 |
| CHIC #322 | Mallia | thera | `era` | 1 |
| CHIC #322 | Mallia | tirintha | `iri` | 1 |
| CHIC #322 | Mallia | tiruns | `iru` | 1 |
| CHIC #322 | Mallia | tulisos | `uli` | 1 |
| CHIC #322 | Mallia | tulissos | `uli` | 1 |
| CHIC #324 | Mallia | aptara | `ara` | 1 |
| CHIC #324 | Mallia | hierapytna | `era` | 2 |
| CHIC #324 | Mallia | kuthera | `era` | 2 |
| CHIC #324 | Mallia | melitos | `eli` | 1 |
| CHIC #324 | Mallia | melos | `elo` | 1 |
| CHIC #324 | Mallia | thera | `era` | 2 |
| CHIC #328 | Mallia | ala | `ala` | 4 |
| CHIC #328 | Mallia | aleksandros | `ale` | 4 |
| CHIC #328 | Mallia | aleksandros | `alek` | 2 |
| CHIC #328 | Mallia | aleksandros | `lek` | 2 |
| CHIC #328 | Mallia | aptara | `ara` | 6 |
| CHIC #328 | Mallia | aptara | `tar` | 1 |
| CHIC #328 | Mallia | aptara | `tara` | 1 |
| CHIC #328 | Mallia | gor | `gor` | 1 |
| CHIC #328 | Mallia | gortyn | `gor` | 1 |
| CHIC #328 | Mallia | halikarnassos | `ali` | 4 |
| CHIC #328 | Mallia | halikarnassos | `alik` | 2 |
| CHIC #328 | Mallia | halikarnassos | `alika` | 2 |
| CHIC #328 | Mallia | halikarnassos | `ika` | 2 |
| CHIC #328 | Mallia | halikarnassos | `ikar` | 1 |
| CHIC #328 | Mallia | halikarnassos | `kar` | 1 |
| CHIC #328 | Mallia | halikarnassos | `lik` | 2 |
| CHIC #328 | Mallia | halikarnassos | `lika` | 2 |
| CHIC #328 | Mallia | halikarnassos | `likar` | 1 |
| CHIC #328 | Mallia | hierapytna | `era` | 5 |
| CHIC #328 | Mallia | hierapytna | `erap` | 2 |
| CHIC #328 | Mallia | hierapytna | `rap` | 2 |
| CHIC #328 | Mallia | hyakinthos | `aki` | 2 |
| CHIC #328 | Mallia | ida | `ida` | 2 |
| CHIC #328 | Mallia | ikaria | `ari` | 4 |
| CHIC #328 | Mallia | ikaria | `ika` | 2 |
| CHIC #328 | Mallia | ikaria | `ikar` | 1 |
| CHIC #328 | Mallia | ikaria | `kar` | 1 |
| CHIC #328 | Mallia | itanos | `ita` | 2 |
| CHIC #328 | Mallia | kalumnos | `alu` | 4 |
| CHIC #328 | Mallia | kor | `kor` | 1 |
| CHIC #328 | Mallia | korinthos | `kor` | 1 |
| CHIC #328 | Mallia | korinthos | `ori` | 3 |
| CHIC #328 | Mallia | krete | `ete` | 2 |
| CHIC #328 | Mallia | krete | `ret` | 2 |
| CHIC #328 | Mallia | krete | `rete` | 2 |
| CHIC #328 | Mallia | kudonia | `udo` | 2 |
| CHIC #328 | Mallia | kuthera | `era` | 5 |
| CHIC #328 | Mallia | kuzikos | `iko` | 2 |
| CHIC #328 | Mallia | lab | `lab` | 2 |
| CHIC #328 | Mallia | lebena | `ebe` | 2 |
| CHIC #328 | Mallia | lebena | `leb` | 2 |
| CHIC #328 | Mallia | lebena | `lebe` | 2 |
| CHIC #328 | Mallia | lukia | `luk` | 2 |
| CHIC #328 | Mallia | lukia | `luki` | 2 |
| CHIC #328 | Mallia | lukia | `uki` | 2 |
| CHIC #328 | Mallia | lykabettos | `abe` | 2 |
| CHIC #328 | Mallia | melitos | `eli` | 3 |
| CHIC #328 | Mallia | melitos | `elit` | 2 |
| CHIC #328 | Mallia | melitos | `elito` | 2 |
| CHIC #328 | Mallia | melitos | `ito` | 2 |
| CHIC #328 | Mallia | melitos | `lit` | 2 |
| CHIC #328 | Mallia | melitos | `lito` | 2 |
| CHIC #328 | Mallia | melos | `elo` | 3 |
| CHIC #328 | Mallia | muke | `uke` | 2 |
| CHIC #328 | Mallia | mukenai | `uke` | 2 |
| CHIC #328 | Mallia | olous | `olo` | 3 |
| CHIC #328 | Mallia | olu | `olu` | 3 |
| CHIC #328 | Mallia | olunthos | `olu` | 3 |
| CHIC #328 | Mallia | par | `par` | 1 |
| CHIC #328 | Mallia | parnassos | `par` | 1 |
| CHIC #328 | Mallia | paros | `aro` | 4 |
| CHIC #328 | Mallia | paros | `par` | 1 |
| CHIC #328 | Mallia | per | `per` | 1 |
| CHIC #328 | Mallia | pergamos | `gam` | 1 |
| CHIC #328 | Mallia | pergamos | `per` | 1 |
| CHIC #328 | Mallia | phalasarna | `ala` | 4 |
| CHIC #328 | Mallia | poikilassos | `iki` | 2 |
| CHIC #328 | Mallia | poikilassos | `ila` | 4 |
| CHIC #328 | Mallia | probalinthos | `ali` | 4 |
| CHIC #328 | Mallia | probalinthos | `oba` | 2 |
| CHIC #328 | Mallia | probalinthos | `rob` | 2 |
| CHIC #328 | Mallia | probalinthos | `roba` | 2 |
| CHIC #328 | Mallia | pulos | `ulo` | 3 |
| CHIC #328 | Mallia | salaminos | `ala` | 4 |
| CHIC #328 | Mallia | sparta | `par` | 1 |
| CHIC #328 | Mallia | tarra | `tar` | 1 |
| CHIC #328 | Mallia | tarsos | `tar` | 1 |
| CHIC #328 | Mallia | tegea | `ege` | 2 |
| CHIC #328 | Mallia | ter | `ter` | 1 |
| CHIC #328 | Mallia | termessos | `ter` | 1 |
| CHIC #328 | Mallia | thebai | `eba` | 2 |
| CHIC #328 | Mallia | thera | `era` | 5 |
| CHIC #328 | Mallia | tirintha | `iri` | 4 |
| CHIC #328 | Mallia | tirintha | `tir` | 1 |
| CHIC #328 | Mallia | tiruns | `iru` | 4 |
| CHIC #328 | Mallia | tiruns | `tir` | 1 |
| CHIC #328 | Mallia | tulisos | `uli` | 3 |
| CHIC #328 | Mallia | tulissos | `uli` | 3 |
| CHIC #328 | Mallia | zakuntos | `aku` | 2 |

### Source C enumeration (item-location consistency, tier-4)

Total source-C match cells: **40**.

| CHIC id | Site | Substring of site | n match positions |
|---|---|---|--:|
| CHIC #070 | Mallia | `lia` | 1 |
| CHIC #086 | Mallia | `lia` | 1 |
| CHIC #174 | Palaikastro | `ika` | 3 |
| CHIC #180 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #225 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #225 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #225 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #244 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #244 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #244 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #248 | Palaikastro | `ika` | 1 |
| CHIC #260 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #260 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #260 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #273 | Mirabelo | `abe` | 1 |
| CHIC #273 | Mirabelo | `rab` | 1 |
| CHIC #273 | Mirabelo | `rabe` | 1 |
| CHIC #276 | Pinakiano | `aki` | 1 |
| CHIC #287 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #289 | Palaikastro | `ala` | 2 |
| CHIC #289 | Palaikastro | `pal` | 2 |
| CHIC #289 | Palaikastro | `pala` | 2 |
| CHIC #294 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #295 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #295 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #295 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #296 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #296 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #296 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #297 | Crete (unprovenanced) | `ete` | 2 |
| CHIC #297 | Crete (unprovenanced) | `ret` | 1 |
| CHIC #297 | Crete (unprovenanced) | `rete` | 1 |
| CHIC #298 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #303 | Crete (unprovenanced) | `ete` | 1 |
| CHIC #308 | Palaikastro | `ika` | 1 |
| CHIC #308 | Palaikastro | `lai` | 1 |
| CHIC #310 | Sitia | `iti` | 1 |
| CHIC #311 | Sitia | `iti` | 1 |
| CHIC #313 | Crete (seal/sealing, mixed sites) | `ali` | 1 |
| CHIC #314 | Neapolis | `oli` | 3 |

## Discipline framing

Per the chic-v6 brief: this is a verification-rate report (mechanical match against external scholarship; NOT specialist judgment). The match criteria are pre-registered above to prevent post-hoc relaxation. Per-tier verification lift is the chic-v5 framework's verification-grade contribution: zero lift means the framework's per-sign extraction does not survive external verification (consistent with the v13 / v22 / v24 internal-vs-external pattern); positive lift is publishable as a reinforcement of the chic-v5 candidate-proposal framework. Either outcome is publishable.

## Determinism

- No RNG. Same (CHIC corpus, anchor pool, leaderboard markdown, scholar entries, toponym pool) → byte-identical artifacts.
- All sortings are deterministic.

## Citations

- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._
- Younger, J. G. (online). _Linear A texts in phonetic transcription._
- Olivier, J.-P. & Godart, L. (1996). _CHIC._
- Beekes, R. S. P. (2010). _Etymological Dictionary of Greek._ (Pre-Greek substrate appendix.)
- Furnée, E. J. (1972). _Die wichtigsten konsonantischen Erscheinungen des Vorgriechischen._
- Salgarella, E. (2020). _Aegean Linear Script(s)._
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
