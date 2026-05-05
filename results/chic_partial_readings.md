# CHIC partial readings under paleographic anchor inheritance (chic-v2; mg-362d)

Partial readings of every CHIC inscription in `corpora/cretan_hieroglyphic/all.jsonl`, with each syllabographic sign position replaced by its anchor's Linear B carryover phonetic value (where the anchor pool covers the sign), or left as `#NNN` (where it does not). Built by `scripts/build_chic_anchors.py` from `pools/cretan_hieroglyphic_anchors.yaml`.

## Rendering convention

- Anchored clean reading: emit phonetic value (e.g. `ra`).
- Anchored uncertain reading: emit `[?:value]`.
- Unanchored clean reading: emit `#NNN`.
- Unanchored uncertain reading: emit `[?:#NNN]`.
- DIV: emit `/`.
- Illegible: emit `[?]`.
- Ideogram (chic-v1 sign_class=ideogram): emit `IDEO:#NNN`.

**Anchor coverage rate** = anchored syllabographic positions / total syllabographic positions (per chic-v1's classification). Ideogram, ambiguous, DIV, and illegible tokens are excluded from both numerator and denominator. An inscription with zero syllabographic positions reports coverage = 0.0 and is leaderboard-ineligible by convention.

## Corpus rollup

- Inscriptions: **302**
- With ≥1 syllabographic position: **288**
- With ≥1 anchored position: **263**
- Total syllabographic sign positions: **1420**
- Total anchored positions: **864**
- Corpus-wide anchor coverage: **0.6085** (864/1420)
- Anchor pool size: **20** (3 tier-1, 17 tier-2)

## Per-inscription partial readings

| CHIC id | Site | Support | n_syll | n_anch | coverage | partial reading |
|---|---|---|--:|--:|--:|---|
| CHIC #001 | Knossos | crescent | 4 | 3 | 0.7500 | `[?:me] #034 ro ra` |
| CHIC #002 | Knossos | crescent | 5 | 2 | 0.4000 | `[?:pa] #056 #068 / [?:#050] a / [?]` |
| CHIC #003 | Knossos | nodulus | 11 | 8 | 0.7273 | `a mu / #009 ma pa #020 / je a / #050 a wa` |
| CHIC #004 | Knossos | crescent | 3 | 2 | 0.6667 | `ke i #059` |
| CHIC #005 | Knossos | crescent | 2 | 1 | 0.5000 | `[?:#047] ke [?]` |
| CHIC #006 | Knossos | crescent | 0 | 0 | 0.0000 | `IDEO:#154` |
| CHIC #007 | Knossos | crescent | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #008 | Knossos | crescent | 3 | 2 | 0.6667 | `ti i #032 [?]` |
| CHIC #009 | Knossos | crescent | 2 | 0 | 0.0000 | `[?:#065] #063` |
| CHIC #010 | Knossos | crescent | 1 | 1 | 1.0000 | `i` |
| CHIC #011 | Knossos | crescent | 3 | 3 | 1.0000 | `de de / [?:ti] / [?]` |
| CHIC #012 | Knossos | crescent | 2 | 2 | 1.0000 | `[?] / ti de [?]` |
| CHIC #013 | Knossos | crescent | 4 | 1 | 0.2500 | `#062 #011 #056 / ki [?]` |
| CHIC #014 | Knossos | crescent | 1 | 1 | 1.0000 | `[?] [?:i] [?]` |
| CHIC #015 | Knossos | crescent | 2 | 0 | 0.0000 | `#011 #056 [?]` |
| CHIC #016 | Knossos | crescent | 2 | 1 | 0.5000 | `de #056` |
| CHIC #017 | Knossos | crescent | 3 | 2 | 0.6667 | `IDEO:#153 / #059 mu ro` |
| CHIC #018 | Knossos | crescent | 7 | 2 | 0.2857 | `#009 #056 te / #020 #047 / ki #005` |
| CHIC #019 | Knossos | crescent | 2 | 1 | 0.5000 | `[?] / [?:ta] [?:#046] / [?]` |
| CHIC #020 | Knossos | crescent | 1 | 0 | 0.0000 | `[?] [?:#078] / [?]` |
| CHIC #021 | Knossos | crescent | 4 | 2 | 0.5000 | `i #017 de #034 / IDEO:#153` |
| CHIC #022 | Knossos | crescent | 4 | 3 | 0.7500 | `#055 ra de [?] / [?] [?:ro]` |
| CHIC #023 | Knossos | crescent | 3 | 1 | 0.3333 | `wa [?:#045] #029` |
| CHIC #024 | Knossos | crescent | 2 | 0 | 0.0000 | `#011 #056 / IDEO:#153` |
| CHIC #025 | Knossos | crescent | 2 | 1 | 0.5000 | `[?] i #011 / [?]` |
| CHIC #026 | Knossos | crescent | 2 | 1 | 0.5000 | `#011 ke / IDEO:#153` |
| CHIC #027 | Knossos | crescent | 9 | 5 | 0.5556 | `wa ni #011 / ke #067 #032 / je ta #034 [?]` |
| CHIC #028 | Knossos | crescent | 5 | 3 | 0.6000 | `#072 / [?] / [?] / [?:#062] ke te / [?:ni] / [?]` |
| CHIC #029 | Knossos | crescent | 5 | 3 | 0.6000 | `[?:wa] / [?:#060] [?:ra] / [?:ke] #055` |
| CHIC #030 | Knossos | medallion | 3 | 1 | 0.3333 | `[?:#068] [?:#046] [?:ke] / [?]` |
| CHIC #031 | Knossos | medallion | 4 | 1 | 0.2500 | `#034 de #056 #052` |
| CHIC #032 | Knossos | medallion | 8 | 4 | 0.5000 | `#056 #047 ro / #050 a / je #047 te` |
| CHIC #033 | Knossos | medallion | 3 | 2 | 0.6667 | `[?:#050] ke i / [?] / [?] [?]` |
| CHIC #034 | Knossos | medallion | 5 | 4 | 0.8000 | `mu te pa / [?] / [?] / #072 de / NUM:10` |
| CHIC #035 | Knossos | medallion | 2 | 2 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| CHIC #036 | Knossos | medallion | 4 | 3 | 0.7500 | `#023 [?:te] ke je / NUM:100` |
| CHIC #037 | Knossos | medallion | 5 | 3 | 0.6000 | `wa mu te / #017 #039 / NUM:100` |
| CHIC #038 | Knossos | medallion | 9 | 7 | 0.7778 | `ke ma #029 / je pa de / je #069 ra / NUM:110` |
| CHIC #039 | Knossos | medallion | 11 | 4 | 0.3636 | `#056 [?:#023] / #043 ra / #020 ma / wa #017 / je #023 [?:#051] / NUM:120` |
| CHIC #040 | Knossos | medallion | 10 | 6 | 0.6000 | `ke ra te / #072 #039 / ki de / NUM:2 / #068 ro / [?:#004]` |
| CHIC #041 | Knossos | medallion | 6 | 1 | 0.1667 | `#069 #047 ni / NUM:1 / NUM:2 / #085 #011 #001 / NUM:32` |
| CHIC #042 | Knossos | medallion | 7 | 3 | 0.4286 | `#037 #011 #029 / #043 ra / NUM:100 / ki de / NUM:634 / NUM:243` |
| CHIC #043 | Knossos | medallion | 11 | 4 | 0.3636 | `#007 ja #006 #023 / [?] / ta ja / #024 #050 / ra #047 #047 / NUM:32` |
| CHIC #044 | Knossos | medallion | 3 | 2 | 0.6667 | `[?:i] ja #068 / IDEO:#153 / NUM:200` |
| CHIC #045 | Knossos | medallion | 3 | 1 | 0.3333 | `#011 ma #034 / IDEO:#174 / NUM:1` |
| CHIC #046 | Knossos | medallion | 3 | 2 | 0.6667 | `de [?:ke] #023 / IDEO:#166 / NUM:100` |
| CHIC #047 | Knossos | medallion | 5 | 4 | 0.8000 | `me me ma / #089 ki / IDEO:#156 / NUM:441` |
| CHIC #048 | Knossos | bar | 0 | 0 | 0.0000 | `IDEO:#164 / NUM:2 / IDEO:#165 / NUM:2 / IDEO:#165 / NUM:2 / [?] / IDEO:#164 / NUM:2 / [?]` |
| CHIC #049 | Knossos | bar | 23 | 10 | 0.4348 | `[?:#046] #063 / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [?] / ki de / NUM:40 / je #023 / NUM:20 / ki de / NUM:300 / #027 / [?:#005] NUM:50 / #034 #056 / NUM:6400 / ke #040 te / NUM:1300 [?] / ti #040 #004 / NUM:550 [?] / [?] / #088 #003 / [?] / [?] / NUM:1 [?:#006] NUM:0` |
| CHIC #051 | Knossos | bar | 1 | 0 | 0.0000 | `[?] #051 / NUM:450 / [?] / NUM:20 [?] / [?] / NUM:6` |
| CHIC #052 | Knossos | bar | 10 | 7 | 0.7000 | `[?:te] / NUM:60 / #063 #047 te ro / NUM:40 / [?] / je ke te / NUM:290 / [?] / NUM:50 / NUM:50 / NUM:70 / [?:#029] ra / NUM:710` |
| CHIC #053 | Knossos | bar | 14 | 7 | 0.5000 | `[?] / ti de ni #003 / [?] #058 ro #056 / [?] / IDEO:#160 / NUM:170 / IDEO:#176 / NUM:160 / [?] / a je [?:pa] #074 #075 / [?] / [?:IDEO:#160] / [?:IDEO:#110] / [?] / [?] / IDEO:#176 / NUM:170 [?] / #058 [?:#002] / NUM:22` |
| CHIC #054 | Knossos | bar | 10 | 9 | 0.9000 | `[?:wa] te / [?] / NUM:110 / je pa de / NUM:170 / [?] / NUM:160 / NUM:150 / NUM:50 / [?:#029] de / NUM:450 / ra ro ke / NUM:60` |
| CHIC #055 | Knossos | bar | 5 | 2 | 0.4000 | `[?:#033] #018 ra [?] / [?:ra] #058 [?] / [?] / NUM:10` |
| CHIC #056 | Knossos | bar | 17 | 16 | 0.9412 | `ra ro ke / ki de / NUM:85 / NUM:800 / NUM:540 / NUM:44 / NUM:44 / wa je ra / NUM:800 / ki de / NUM:83 / #026 te / wa je i / NUM:483 / ki de / NUM:46` |
| CHIC #057 | Knossos | bar | 13 | 4 | 0.3077 | `wa #029 #032 #011 / NUM:10 / #079 #032 pa / NUM:20 / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50` |
| CHIC #058 | Knossos | bar | 22 | 10 | 0.4545 | `wa mu te / NUM:640 / #047 ra ro / NUM:80 / #078 #032 #034 / NUM:50 / [?:ja] ra #005 / NUM:60 / #034 [?:#002] / NUM:20 / ti i #002 / NUM:90 / #078 #032 ra [?:#023] [?:#045] / NUM:30` |
| CHIC #059 | Knossos | bar | 35 | 22 | 0.6286 | `ti de de / ki #005 / NUM:40 [?] / i #071 #066 ra / NUM:400 [?] / #060 [?:pa] / ti #029 #002 / [?:pa] [?] / [?] / [?:#001] NUM:30 / [?] / NUM:2300 [?] / [?] / [?:IDEO:#300] / [?] / [?:ro] #021 te / ki de [?] / #072 de / NUM:11 / ki de / [?:#006] / ke #036 [?] / [?] / [?] / ti de #007 wa [?] / [?:#056] ra te / NUM:11 / [?]` |
| CHIC #060 | Knossos | bar | 7 | 5 | 0.7143 | `ti de ni #003 [?] / [?:#009] mu te [?]` |
| CHIC #061 | Knossos | bar | 23 | 10 | 0.4348 | `[?:#023] #032 / NUM:1 / wa #056 ro / NUM:1 / [?] #034 #056 / NUM:1 / #037 #011 #029 / NUM:1 / [?] / [?] / [?] / ra ke [?:#009] / NUM:1 / [?:ke] de / [?:#001] / #034 #056 / ke de / NUM:1 / #056 ra ra / NUM:12` |
| CHIC #062 | Knossos | bar | 14 | 12 | 0.8571 | `[?:mu] te / wa #034 de / [?] / [?:#001] NUM:40 / [?] mu te / [?] / NUM:30 / [?:wa] mu te / [?] / NUM:540 / [?:wa] mu te` |
| CHIC #063 | Knossos | bar | 13 | 10 | 0.7692 | `[?:#006] je ke / NUM:105 [?] / [?:ni] #006 / NUM:3 / ki de [?] / [?:je] me / NUM:20 [?] / [?] / [?] / [?:de] te / NUM:20 [?] / [?:me] #006 [?]` |
| CHIC #064 | Knossos | bar | 1 | 0 | 0.0000 | `NUM:2030 [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / NUM:110 [?:#002] / [?]` |
| CHIC #065 | Knossos | bar | 14 | 5 | 0.3571 | `#072 de #071 #050 #005 #063 / NUM:1 / #047 me / NUM:1 / ke ro / NUM:1 / NUM:42 / IDEO:#161 / IDEO:#161 / NUM:300 / [?:IDEO:#152] / NUM:1 / IDEO:#156 / NUM:2 / IDEO:#180 / NUM:32 / IDEO:#152 / NUM:1 / #033 #047 / IDEO:#178 / #072 de / NUM:1 / IDEO:#158 / IDEO:#167 / IDEO:#155` |
| CHIC #066 | Knossos | bar | 2 | 0 | 0.0000 | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:#005] #063 / NUM:1 / [?:IDEO:#182] / NUM:12 / IDEO:#161` |
| CHIC #067 | Knossos | bar | 3 | 2 | 0.6667 | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 / NUM:1 / [?:IDEO:#152] / NUM:1 / ke ro / NUM:1 / [?]` |
| CHIC #068 | Knossos | tablet | 0 | 0 | 0.0000 | `[?:IDEO:#156] / NUM:10 / [?:IDEO:#151] / NUM:5 / IDEO:#175 / [?:IDEO:#153] / NUM:15 / [?:IDEO:#154] / NUM:8` |
| CHIC #069 | Knossos | tablet | 3 | 3 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| CHIC #070 | Mallia | cone | 4 | 1 | 0.2500 | `wa #034 [?:#007] #040` |
| CHIC #071 | Mallia | cone | 4 | 2 | 0.5000 | `#022 #056 ra te` |
| CHIC #072 | Mallia | medallion | 2 | 1 | 0.5000 | `#011 i / NUM:29` |
| CHIC #073 | Mallia | medallion | 3 | 1 | 0.3333 | `#027 #034 ra` |
| CHIC #074 | Mallia | medallion | 4 | 3 | 0.7500 | `wa ra #060 ki` |
| CHIC #075 | Mallia | medallion | 2 | 0 | 0.0000 | `#060 #009` |
| CHIC #076 | Mallia | medallion | 3 | 1 | 0.3333 | `#008 #056 pa` |
| CHIC #077 | Mallia | medallion | 3 | 1 | 0.3333 | `[?:ro] #055 #081` |
| CHIC #078 | Mallia | medallion | 3 | 1 | 0.3333 | `#083 [?:#047] ke [?]` |
| CHIC #079 | Mallia | medallion | 3 | 1 | 0.3333 | `#068 [?:ma] #015` |
| CHIC #080 | Mallia | medallion | 3 | 1 | 0.3333 | `#012 [?:ro] #082` |
| CHIC #081 | Mallia | medallion | 2 | 2 | 1.0000 | `ti ra` |
| CHIC #082 | Mallia | medallion | 3 | 2 | 0.6667 | `#020 a ni` |
| CHIC #083 | Mallia | medallion | 2 | 0 | 0.0000 | `#030 #034` |
| CHIC #084 | Mallia | medallion | 1 | 1 | 1.0000 | `[?] a [?]` |
| CHIC #085 | Mallia | lame | 2 | 1 | 0.5000 | `#068 te` |
| CHIC #086 | Mallia | lame | 2 | 1 | 0.5000 | `#068 [?:a] [?]` |
| CHIC #087 | Mallia | lame | 2 | 0 | 0.0000 | `#064 #096 [?]` |
| CHIC #088 | Mallia | lame | 2 | 2 | 1.0000 | `[?:ro] ni` |
| CHIC #089 | Mallia | lame | 10 | 4 | 0.4000 | `ki de #023 / #034 ni #084 / #051 #051 #051 ni` |
| CHIC #090 | Mallia | lame | 4 | 2 | 0.5000 | `a i #007 #051 / NUM:0` |
| CHIC #091 | Mallia | lame | 6 | 4 | 0.6667 | `wa pa #009 [?] / ra ro #034 [?]` |
| CHIC #092 | Mallia | lame | 4 | 2 | 0.5000 | `[?:te] #080 #032 [?] / [?] / [?:me] [?]` |
| CHIC #093 | Mallia | lame | 0 | 0 | 0.0000 | `[?] / [?]` |
| CHIC #097 | Mallia | crescent | 3 | 2 | 0.6667 | `NUM:2 / #040 ra i` |
| CHIC #098 | Mallia | medallion | 4 | 2 | 0.5000 | `[?:#072] i #007 a` |
| CHIC #103 | Mallia | medallion | 4 | 2 | 0.5000 | `[?:ra] #055 je [?:#056] [?] / [?:IDEO:#163] [?]` |
| CHIC #104 | Mallia | medallion | 3 | 0 | 0.0000 | `#032 #009 #056 / IDEO:#168 / NUM:100` |
| CHIC #105 | Mallia | lame | 4 | 3 | 0.7500 | `[?] a i / [?] pa #035 / NUM:210` |
| CHIC #106 | Mallia | lame | 2 | 2 | 1.0000 | `[?:pa] de` |
| CHIC #107 | Mallia | lame | 1 | 0 | 0.0000 | `[?] #020` |
| CHIC #108 | Mallia | lame | 0 | 0 | 0.0000 | `IDEO:#169 / NUM:5 / [?] / [?] / NUM:6` |
| CHIC #109 | Mallia | lame | 5 | 2 | 0.4000 | `ke #034 / #003 [?] / #036 ke [?]` |
| CHIC #110 | Mallia | lame | 3 | 1 | 0.3333 | `ki #040 [?] / [?:#085] / [?]` |
| CHIC #111 | Mallia | bar | 2 | 0 | 0.0000 | `[?] / [?] / [?:#060] / [?] / [?] [?] / [?] / [?:#040] / [?]` |
| CHIC #113 | Mallia | bar | 27 | 15 | 0.5556 | `[?:#047] #002 te / de i [?] / #050 ra ke / NUM:10 / NUM:57 [?] / [?] #056 ma / NUM:20 / to #090 / #012 #050 / wa de a a [?] / [?:#040] pa / je #023 wa #063 #060 / #008 ra [?]` |
| CHIC #115 | Mallia | bar | 5 | 2 | 0.4000 | `[?:#035] me #034 / [?] pa #060 / [?] / [?]` |
| CHIC #116 | Mallia | bar | 0 | 0 | 0.0000 | `[?] / [?] / [?]` |
| CHIC #117 | Mallia | bar | 4 | 0 | 0.0000 | `[?:#055] [?:#020] [?] / [?:#011] [?:#040] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?]` |
| CHIC #118 | Mallia | bar | 4 | 2 | 0.5000 | `#056 ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM:1 / [?] / [?] / [?:IDEO:#153] / NUM:1 / #040 je / IDEO:#177 / NUM:1 / IDEO:#173 / NUM:2 / IDEO:#155 / NUM:4 / IDEO:#156 / NUM:20 / IDEO:#179 / NUM:240 / IDEO:#161 / NUM:1 / IDEO:#162 / NUM:1` |
| CHIC #120 | Mallia | tablet | 0 | 0 | 0.0000 | `[?] / NUM:100 / [?] / [?] / NUM:300` |
| CHIC #121 | Mallia | bar | 1 | 1 | 1.0000 | `NUM:41 [?] / [?:pa] [?]` |
| CHIC #123 | Knossos | crescent | 2 | 1 | 0.5000 | `ke #058` |
| CHIC #124 | Knossos | crescent | 3 | 0 | 0.0000 | `#040 #029 #029` |
| CHIC #125 | Knossos | sealing | 4 | 1 | 0.2500 | `wa #052 [?:#034] #045 / NUM:0` |
| CHIC #126 | Mallia | nodulus | 5 | 0 | 0.0000 | `#036 #047 #009 #056 #062` |
| CHIC #127 | Mallia | nodulus | 2 | 0 | 0.0000 | `#062 #040` |
| CHIC #128 | Mallia | nodulus | 3 | 1 | 0.3333 | `[?:#008] me #017 / NUM:0` |
| CHIC #129 | Mallia | nodulus | 3 | 2 | 0.6667 | `wa #040 de / NUM:0` |
| CHIC #130 | Mallia | nodulus | 3 | 2 | 0.6667 | `#052 mu [?:i] / NUM:0` |
| CHIC #131 | Mallia | nodulus | 2 | 1 | 0.5000 | `#036 ke` |
| CHIC #133 | Pyrgos (Myrtos) | vase | 3 | 3 | 1.0000 | `ra ti ni / NUM:0` |
| CHIC #134 | Knossos | sealing | 2 | 2 | 1.0000 | `wa ke` |
| CHIC #135 | Samothrace | roundel | 2 | 2 | 1.0000 | `wa ke` |
| CHIC #136 | Samothrace | roundel | 2 | 2 | 1.0000 | `wa ke` |
| CHIC #137 | Samothrace | nodulus | 2 | 2 | 1.0000 | `wa ke` |
| CHIC #138 | Zakros | sealing | 2 | 1 | 0.5000 | `ki #005` |
| CHIC #140 | Knossos | crescent | 3 | 2 | 0.6667 | `ki pa #005` |
| CHIC #141 | Knossos | crescent | 2 | 1 | 0.5000 | `#063 ro` |
| CHIC #142 | Knossos | crescent | 3 | 0 | 0.0000 | `#018 #039 #005 / NUM:0` |
| CHIC #143 | Knossos | crescent | 1 | 1 | 1.0000 | `wa` |
| CHIC #144 | Knossos | crescent | 2 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #145 | Knossos | crescent | 2 | 1 | 0.5000 | `ki #005` |
| CHIC #148 | Mallia | nodulus | 3 | 2 | 0.6667 | `#011 i a` |
| CHIC #149 | Mallia | sealing | 3 | 2 | 0.6667 | `ro #021 te` |
| CHIC #150 | Mallia | sealing | 2 | 2 | 1.0000 | `ki de` |
| CHIC #151 | Phaistos | sealing | 2 | 2 | 1.0000 | `wa me` |
| CHIC #152 | Zakros | sealing | 2 | 2 | 1.0000 | `mu ki` |
| CHIC #153 | Zakros | sealing | 1 | 1 | 1.0000 | `mu [?]` |
| CHIC #154 | Mallia | sealing | 2 | 2 | 1.0000 | `wa i` |
| CHIC #155 | Haghia Triada | sealing | 2 | 2 | 1.0000 | `mu ja` |
| CHIC #157 | Knossos | crescent | 2 | 2 | 1.0000 | `ki de` |
| CHIC #158 | Knossos | crescent | 2 | 1 | 0.5000 | `ki #005` |
| CHIC #159 | Knossos | crescent | 2 | 2 | 1.0000 | `[?:ki] de` |
| CHIC #160 | Knossos | crescent | 3 | 2 | 0.6667 | `[?:ti] #020 ni` |
| CHIC #161 | Knossos | crescent | 2 | 2 | 1.0000 | `ki de` |
| CHIC #162 | Knossos | crescent | 3 | 3 | 1.0000 | `i ja ro` |
| CHIC #163 | Knossos | crescent | 3 | 3 | 1.0000 | `wa ra i` |
| CHIC #165 | Knossos | crescent | 2 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #166 | Knossos | crescent | 3 | 1 | 0.3333 | `#056 #047 ro` |
| CHIC #167 | Knossos | crescent | 3 | 3 | 1.0000 | `de ra ra` |
| CHIC #168 | Knossos | crescent | 2 | 2 | 1.0000 | `wa ra [?]` |
| CHIC #169 | Knossos | sealing | 3 | 3 | 1.0000 | `i ja ro` |
| CHIC #170 | Knossos | sealing | 2 | 2 | 1.0000 | `ki de` |
| CHIC #171 | Mallia | nodulus | 2 | 0 | 0.0000 | `#062 #040` |
| CHIC #172 | Mallia | crescent | 3 | 3 | 1.0000 | `ja ke ti` |
| CHIC #173 | Mallia | sealing | 3 | 1 | 0.3333 | `je #034 #056` |
| CHIC #174 | Palaikastro | sealing | 5 | 2 | 0.4000 | `ki #005 / ki #065 #005` |
| CHIC #175 | Pyrgos (Myrtos) | potsherd | 2 | 2 | 1.0000 | `[?:wa] ke [?] [?]` |
| CHIC #177 | Knossos | nodulus | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #178 | Knossos | sealing | 3 | 2 | 0.6667 | `[?:wa] [?:de] [?:#050] [?] / NUM:0` |
| CHIC #179 | Knossos | sealing | 3 | 3 | 1.0000 | `wa ke / ke [?]` |
| CHIC #180 | Crete (unprovenanced) | seal | 4 | 2 | 0.5000 | `ki de #050 #056 / NUM:0` |
| CHIC #181 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `i ja` |
| CHIC #182 | Crete (unprovenanced) | seal | 4 | 1 | 0.2500 | `#056 ta #029 #011 / NUM:0` |
| CHIC #183 | Crete (unprovenanced) | seal | 3 | 2 | 0.6667 | `i ra #011` |
| CHIC #184 | Crete (unprovenanced) | seal | 3 | 3 | 1.0000 | `ki pa ra` |
| CHIC #186 | Kalo Horio | seal | 4 | 3 | 0.7500 | `ti te de #047 / NUM:0` |
| CHIC #187 | Mallia | seal | 2 | 1 | 0.5000 | `me #008` |
| CHIC #188 | Mallia | seal | 2 | 2 | 1.0000 | `ki [?:de]` |
| CHIC #189 | Mallia | seal | 2 | 2 | 1.0000 | `[?:wa] mu [?]` |
| CHIC #191 | Mochlos | seal | 2 | 0 | 0.0000 | `#036 #040 / NUM:49 [?]` |
| CHIC #193 | Ziros | seal | 3 | 2 | 0.6667 | `a ke #056 / NUM:0` |
| CHIC #194 | Crete (unprovenanced) | seal | 2 | 1 | 0.5000 | `ki #005` |
| CHIC #195 | Crete (unprovenanced) | seal | 3 | 3 | 1.0000 | `i ja ro` |
| CHIC #196 | Gortys | seal | 2 | 2 | 1.0000 | `ke te` |
| CHIC #197 | Mallia | seal | 3 | 2 | 0.6667 | `ro #021 te` |
| CHIC #198 | Mirabelo | seal | 2 | 2 | 1.0000 | `ra to` |
| CHIC #199 | Mallia | seal | 0 | 0 | 0.0000 | `NUM:70 [?]` |
| CHIC #200 | Mallia | seal | 5 | 3 | 0.6000 | `#029 ni #056 i [?:ma]` |
| CHIC #201 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `wa ke` |
| CHIC #202 | Arkhanes | seal | 5 | 3 | 0.6000 | `wa ke / ke [?:#095] #052` |
| CHIC #203 | Knossos | seal | 5 | 3 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #204 | Mallia | seal | 3 | 1 | 0.3333 | `i #034 [?:#066]` |
| CHIC #205 | Crete (unprovenanced) | seal | 5 | 3 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #207 | Mallia | seal | 4 | 4 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| CHIC #208 | Avdou | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #209 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `[?:ki] de` |
| CHIC #210 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #211 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #212 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `i ja` |
| CHIC #213 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #214 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `i ja` |
| CHIC #215 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #216 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #217 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #218 | Crete (unprovenanced) | seal | 3 | 3 | 1.0000 | `i ja ro` |
| CHIC #219 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #220 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #221 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #223 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #224 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `[?:wa] i` |
| CHIC #225 | Crete (unprovenanced) | seal | 3 | 0 | 0.0000 | `#068 #009 #011` |
| CHIC #226 | Lasithi | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #227 | Lithines | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #229 | Mallia | seal | 2 | 1 | 0.5000 | `#036 ke` |
| CHIC #231 | Mallia | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #232 | Mallia | seal | 1 | 1 | 1.0000 | `[?:de]` |
| CHIC #233 | Mallia | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #234 | Mallia | seal | 2 | 0 | 0.0000 | `#017 #050` |
| CHIC #235 | Mallia | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #236 | Mallia | seal | 3 | 1 | 0.3333 | `#012 ra #048` |
| CHIC #237 | Mirabelo | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #238 | Mochlos | seal | 3 | 1 | 0.3333 | `je #034 #056` |
| CHIC #239 | Praisos | seal | 3 | 2 | 0.6667 | `i [?:ja] [?:#034]` |
| CHIC #240 | Sitia | seal | 2 | 2 | 1.0000 | `NUM:1 / ki de` |
| CHIC #241 | Sitia | seal | 2 | 0 | 0.0000 | `[?:#094] [?:#036]` |
| CHIC #242 | Crete (unprovenanced) | seal | 5 | 3 | 0.6000 | `#056 #059 / i ja ro` |
| CHIC #243 | Crete (unprovenanced) | seal | 5 | 3 | 0.6000 | `#006 je ke / NUM:0 / je #023` |
| CHIC #244 | Crete (unprovenanced) | seal | 5 | 3 | 0.6000 | `ki de / je #034 #056` |
| CHIC #245 | Crete (unprovenanced) | seal | 3 | 1 | 0.3333 | `de [?] / #029 #014 [?]` |
| CHIC #246 | Kritsa | seal | 4 | 2 | 0.5000 | `ki #005 / #006 ni` |
| CHIC #247 | Mallia | seal | 4 | 3 | 0.7500 | `ki de / ki #005` |
| CHIC #248 | Palaikastro | seal | 6 | 4 | 0.6667 | `i ja ro / je #034 #056` |
| CHIC #249 | Sitia | seal | 4 | 4 | 1.0000 | `i ja / ki de` |
| CHIC #250 | Zakros | seal | 5 | 4 | 0.8000 | `ki #005 / i ja ro` |
| CHIC #251 | Arkhanes | seal | 7 | 4 | 0.5714 | `ke [?:#095] [?:#052] / wa ke / [?:#094] [?:i]` |
| CHIC #252 | Arkhanes | seal | 6 | 3 | 0.5000 | `ke #095 #052 / wa ke / [?:#062]` |
| CHIC #253 | Crete (unprovenanced) | seal | 6 | 5 | 0.8333 | `i ja / ki de / ki #005` |
| CHIC #254 | Crete (unprovenanced) | seal | 5 | 3 | 0.6000 | `ki #005 / #036 ke ro / [?]` |
| CHIC #255 | Crete (unprovenanced) | seal | 11 | 6 | 0.5455 | `ki #036 #018 / ti de wa ro #056 #036 / #046 ki` |
| CHIC #256 | Crete (unprovenanced) | seal | 3 | 2 | 0.6667 | `i #043 de / NUM:0` |
| CHIC #257 | Crete (unprovenanced) | seal | 8 | 6 | 0.7500 | `i ja ro / #036 ke ro / #046 ki` |
| CHIC #258 | Crete (unprovenanced) | seal | 7 | 6 | 0.8571 | `i ja / #036 ke ro / ki de` |
| CHIC #259 | Crete (unprovenanced) | seal | 4 | 3 | 0.7500 | `ki de / ki #005` |
| CHIC #260 | Crete (unprovenanced) | seal | 7 | 5 | 0.7143 | `ki de / i ja / je #034 #056` |
| CHIC #261 | Crete (unprovenanced) | seal | 7 | 6 | 0.8571 | `ki #005 / i ja ro / ki de` |
| CHIC #262 | Crete (unprovenanced) | seal | 9 | 7 | 0.7778 | `#036 ke ke ro / i ja ro / ki #005` |
| CHIC #263 | Crete (unprovenanced) | seal | 7 | 5 | 0.7143 | `#036 [?:ke] / i ja ro / ki #005` |
| CHIC #264 | Heraklion | seal | 7 | 4 | 0.5714 | `pa #050 / #004 / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki #005` |
| CHIC #265 | Kasteli | seal | 6 | 3 | 0.5000 | `i ja / #043 #009 / [?] / #036 ke` |
| CHIC #266 | Kordakia | seal | 7 | 6 | 0.8571 | `ki #005 / ki ta de / ki de` |
| CHIC #267 | Kydonia | seal | 7 | 4 | 0.5714 | `mu ja mu / #036 ke / #050 #011` |
| CHIC #268 | Lakonia | seal | 6 | 4 | 0.6667 | `NUM:70 / ki #005 / i ja / NUM:70 / #006 ra` |
| CHIC #269 | Lasithi | seal | 7 | 6 | 0.8571 | `i ja ro [?] / de [?:de] [?] / [?:#046] ki` |
| CHIC #270 | Lasithi | seal | 8 | 8 | 1.0000 | `ra i / ki de / i ro ja te` |
| CHIC #271 | Mallia | seal | 10 | 4 | 0.4000 | `#012 a [?:#062] #018 / ni [?:ro] #011 / #060 ki #056` |
| CHIC #272 | Mirabelo | seal | 10 | 6 | 0.6000 | `i ja ro / #036 ke ro / [?] / [?:#068] ja #011 #020` |
| CHIC #273 | Mirabelo | seal | 9 | 5 | 0.5556 | `mu #005 #050 / ke ro te / ra #005 #050` |
| CHIC #274 | Mirabelo | seal | 7 | 6 | 0.8571 | `ki de / ki #005 / i ja ro` |
| CHIC #276 | Pinakiano | seal | 8 | 5 | 0.6250 | `wa i / ro #006 #034 / #005 ki de` |
| CHIC #277 | Ziros | seal | 7 | 6 | 0.8571 | `ki #005 / ke ke pa / ki de` |
| CHIC #278 | Crete (unprovenanced) | seal | 2 | 2 | 1.0000 | `ki de` |
| CHIC #279 | Crete (unprovenanced) | seal | 3 | 3 | 1.0000 | `i ja ro` |
| CHIC #280 | Mallia | seal | 3 | 2 | 0.6667 | `wa ti #005` |
| CHIC #281 | Mallia | seal | 3 | 1 | 0.3333 | `je #034 [?:#056]` |
| CHIC #282 | Pyrgos (Myrtos) | seal | 3 | 1 | 0.3333 | `#008 [?:ke] [?:#036]` |
| CHIC #283 | Crete (unprovenanced) | seal | 7 | 4 | 0.5714 | `ki #005 / ki de / #056 pa #058` |
| CHIC #284 | Crete (unprovenanced) | seal | 5 | 5 | 1.0000 | `ki de / i ja ro` |
| CHIC #285 | Crete (unprovenanced) | seal | 3 | 2 | 0.6667 | `#029 / [?:ki] [?:de] [?]` |
| CHIC #286 | Mallia | seal | 4 | 3 | 0.7500 | `i ja / #047 ra` |
| CHIC #287 | Crete (unprovenanced) | seal | 7 | 5 | 0.7143 | `ki de / ra te #069 / ki #005` |
| CHIC #288 | Mallia | seal | 6 | 4 | 0.6667 | `i ja / ki #005 / #036 ke` |
| CHIC #289 | Palaikastro | seal | 7 | 2 | 0.2857 | `[?] [?:#056] #011 / [?] ke #056 #034 [?] / [?] [?] / [?:#034] ja [?]` |
| CHIC #290 | Sitia | seal | 8 | 5 | 0.6250 | `ki de / #051 ro #005 / ma a #033` |
| CHIC #291 | Crete (unprovenanced) | seal | 0 | 0 | 0.0000 | `IDEO:#157` |
| CHIC #293 | Adromili | seal | 10 | 10 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| CHIC #294 | Crete (unprovenanced) | seal | 27 | 18 | 0.6667 | `ta de [?] #040 [?] / #059 je [?:#014] ni ke #047 ra ke ke ki #050 ke ti #056 / #056 [?:te] [?:ma] / ta ta / ke je [?] #034 [?] a #056` |
| CHIC #295 | Crete (unprovenanced) | seal | 11 | 6 | 0.5455 | `ki de / #029 ma de / je #034 [?:#056] / ki #005 / #080` |
| CHIC #296 | Crete (unprovenanced) | seal | 11 | 6 | 0.5455 | `ti #007 #018 / me i #039 / ki de / je #034 #056` |
| CHIC #297 | Crete (unprovenanced) | seal | 13 | 7 | 0.5385 | `#050 ke / i #008 / #036 ja / #011 #056 / ki de / ki #005 te` |
| CHIC #298 | Crete (unprovenanced) | seal | 15 | 11 | 0.7333 | `#056 ra #040 / ra te ke #045 ra / i ja ro / ki #005 / ki de` |
| CHIC #299 | Crete (unprovenanced) | seal | 9 | 7 | 0.7778 | `ki de / ki #005 / #036 ke / i ja ro` |
| CHIC #300 | Crete (unprovenanced) | seal | 10 | 6 | 0.6000 | `ki de / i ja ro / ki #036 #018 / #014 #050` |
| CHIC #301 | Crete (unprovenanced) | seal | 9 | 6 | 0.6667 | `ki de / ki #005 / #018 #046 / wa ke ro` |
| CHIC #302 | Crete (unprovenanced) | seal | 12 | 7 | 0.5833 | `je #034 ki de / #046 ki / #006 #062 #012 / i ja ro` |
| CHIC #303 | Crete (unprovenanced) | seal | 12 | 9 | 0.7500 | `#062 #020 ti / wa mu te / [?:ke] #039 [?:i] ro / ki de` |
| CHIC #304 | Crete (unprovenanced) | seal | 9 | 5 | 0.5556 | `#039 pa / #036 pa / #011 [?:ja] / #076 pa ro` |
| CHIC #305 | Lastros | seal | 8 | 5 | 0.6250 | `wa #066 a #062 / ki de / ki #005 / IDEO:#181 / IDEO:#180` |
| CHIC #306 | Mallia | seal | 12 | 3 | 0.2500 | `#052 #050 mu / #036 i [?:#076] / #039 #056 [?:#014] / je #018 #050` |
| CHIC #308 | Palaikastro | seal | 9 | 5 | 0.5556 | `#036 ke ro / #034 #007 / ki de / IDEO:#174 / ki #005` |
| CHIC #309 | Pyrgos (Myrtos) | seal | 12 | 9 | 0.7500 | `ki #005 / wa #040 me ni / i ja ro / #036 ke ro` |
| CHIC #310 | Sitia | seal | 9 | 4 | 0.4444 | `je #034 #056 / #017 #050 / NUM:1 / #046 ki / wa i` |
| CHIC #311 | Sitia | seal | 6 | 5 | 0.8333 | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:#005] / [?:ki] [?:de]` |
| CHIC #312 | Xida | seal | 11 | 8 | 0.7273 | `i ja ro / #036 ke ro / #047 de [?:pa] / #076 pa` |
| CHIC #313 | Crete (seal/sealing, mixed sites) | seal | 5 | 3 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #314 | Neapolis | seal | 24 | 12 | 0.5000 | `#050 ro #034 / ki de / #050 #007 #018 / #046 IDEO:#168 ki / i ja ro / #036 ke ro / ki de / [?:#018] #043 / #018 #043 / ki #005` |
| CHIC #315 | Arkhanes | seal | 0 | 0 | 0.0000 | `IDEO:#181 / IDEO:#134` |
| CHIC #316 | Mallia | chamaizi_vase | 4 | 3 | 0.7500 | `de ni #006 ta` |
| CHIC #317 | Mallia | pithos | 7 | 4 | 0.5714 | `wa je [?:ja] #034 ti [?:#093] [?:#065]` |
| CHIC #318 | Mallia | unknown | 3 | 2 | 0.6667 | `[?:#051] ke ke` |
| CHIC #319 | Mallia | pithos | 4 | 1 | 0.2500 | `[?:#088] #087 ra #027` |
| CHIC #320 | Mallia | vase | 3 | 2 | 0.6667 | `ni #059 ta / [?]` |
| CHIC #321 | Mallia | potsherd | 2 | 1 | 0.5000 | `[?:#056] ra` |
| CHIC #322 | Mallia | chamaizi_vase | 2 | 0 | 0.0000 | `#008 #068` |
| CHIC #323 | Mallia | pithos | 0 | 0 | 0.0000 | `NUM:6 [?]` |
| CHIC #324 | Mallia | chamaizi_vase | 4 | 2 | 0.5000 | `je #023 ra #018` |
| CHIC #325 | Mallia | chamaizi_vase | 0 | 0 | 0.0000 | `NUM:28 [?]` |
| CHIC #326 | Mallia | chamaizi_vase | 1 | 1 | 1.0000 | `[?] me` |
| CHIC #327 | Mallia | chamaizi_vase | 3 | 2 | 0.6667 | `de ni #006 / NUM:57` |
| CHIC #328 | Mallia | offering_table | 16 | 7 | 0.4375 | `[?:#062] #034 #002 #056 ra ta ke #051 ra #094 #034 #056 ma de i #029` |
| CHIC #329 | Mallia | chamaizi_vase | 2 | 2 | 1.0000 | `de wa` |
| CHIC #330 | Mallia | potsherd | 2 | 0 | 0.0000 | `[?:#029] #064 [?]` |
| CHIC #331 | Prodromos | chamaizi_vase | 2 | 1 | 0.5000 | `wa #091` |
