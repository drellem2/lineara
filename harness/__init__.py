"""Lineara scoring harness."""

# v0 — initial harness (mg-d5ef): compression_delta_v0 + result.v0 schema.
# v1 — harness v2 (mg-7dd1): adds local_fit_v1 and geographic_genre_fit_v1
#      metrics, extends result.v0 schema with optional diagnostic fields,
#      adds metric to the sweep-runner resume key. local_fit_v0 / v0
#      compression scores produced under v1 are bit-identical to v0.
HARNESS_VERSION = "v1"
INSCRIPTION_BOUNDARY = "INS_BOUNDARY"
