"""Lineara scoring harness."""

# v0 — initial harness (mg-d5ef): compression_delta_v0 + result.v0 schema.
# v1 — harness v2 (mg-7dd1): adds local_fit_v1 and geographic_genre_fit_v1
#      metrics, extends result.v0 schema with optional diagnostic fields,
#      adds metric to the sweep-runner resume key. local_fit_v0 / v0
#      compression scores produced under v1 are bit-identical to v0.
# v7 — harness v7 (mg-ddee): adds sign_prediction_perplexity_v0 (corpus-derived
#      phoneme cluster model + cluster-bigram corpus side metric) and
#      paired-difference scoring (substrate − matched control) as the
#      primary view. v1 metrics are unchanged; existing rows remain valid.
HARNESS_VERSION = "v7"
INSCRIPTION_BOUNDARY = "INS_BOUNDARY"
