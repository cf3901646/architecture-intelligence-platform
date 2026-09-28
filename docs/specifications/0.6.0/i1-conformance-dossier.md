# AIP v0.6.0 I1 — Independent Conformance Dossier (L01–L37)

**Status:** I1 supporting deliverable, slice I1.5. It contains the independently authored expected results for the I1 §13 scenarios. **No AIP implementation of these results exists yet, and none has been run** (I2 implements; I4 qualifies).  
**Release / increment:** `v0.6.0` — Locality-Aware Current State / I1  
**Governing specification:** [I1 — Locality and Evidence Applicability Contract](i1-locality-and-evidence-applicability.md) §13, accepted in PR #283 (merge `aafb03d5735d78b2741a3dc8a2d0336079535ed6`).  
**Expected-result inputs:** [support matrix](i1-locality-support-matrix.md) (§10 allowlist, §12 timestamps, §13 window, §15 dispositions), [v2 evidence contract](i1-scoped-evidence-v2-contract.md), [capture runbook](i1-capture-acquisition-runbook.md).  
**Machine-readable form:** [`i1-vectors/conformance-expected.json`](i1-vectors/conformance-expected.json). The case tables in §3 are rendered from that file, so the two cannot drift apart: the vector test checks that every case heading and variant row matches the JSON.

## 1. Independence and how I2/I4 use this dossier

The results below were authored **by hand from the accepted specification and the I1.1–I1.4 deliverables, before any v0.6 implementation exists**. No AIP output was copied into them (I1 §2, §13). The concrete v2 and v1 IDs are the independently hashed vectors in [`i1-vectors/v2-evidence-id.json`](i1-vectors/v2-evidence-id.json), referenced by name (`V01-base`, `U01-…`).

- `tests/unit/test_v060_i1_contract_vectors.py` checks the dossier's **internal consistency** only. It checks that:
  - L01–L37 are all present and each has variants and prohibited conclusions;
  - every disposition and reason belongs to the frozen vocabulary, with reasons sorted and distinct;
  - each primary disposition follows the §10.1 within-phase precedence of its reasons;
  - `UNSUPPORTED` occurs only in phases 1–2;
  - no ingestion-only code appears in a query answer (§10.2);
  - every vector and capture reference resolves;
  - no case expects a local `NOT_OBSERVED_IN_WINDOW`.

  It is **not** a test of AIP.
- **I2** turns each variant into implementation tests against its code, using these fixtures. A disagreement is resolved by specification decision, never by editing the expected value to match the output (I1 §13; AGENTS.md).
- **I4** re-runs them under input permutation and clean replay on the exact candidate, and checks service/REST/MCP parity. I1 claims none of that.

## 2. Shared fixtures

Unless a variant states otherwise, the request is:
- environment `production`;
- `ScopedDayWindowV1(D, D)` with D = `2026-09-28`;
- relation `CALLS`;
- caller `service:orders`.

The key vectors in `v2-evidence-id.json` already use these values.

| Symbol | Value |
|---|---|
| O1 / O2 / O3 | `operation:pricing:GET:/prices` (owner `service:pricing`) / `operation:legacy-pricing:GET:/prices` (owner `service:legacy-pricing`) / `operation:pricing:GET:/prices/{id}` (owner `service:pricing`) |
| K1 / K2 | Cluster UIDs `7f3c2a10-1b2d-4e5f-8a9b-0c1d2e3f4a5b` / `9e8d7c6b-5a49-4382-b716-a5b4c3d2e1f0` |
| P1 / P2 | Pod UIDs `11111111-aaaa-4bbb-8ccc-000000000001` / `…0002` |
| W1 / W2 | Deployment `shop/orders` / Deployment `shop/orders-canary` |
| `CAP-A` | `CAPTURED_RESOURCE`, `clusterUid` K1, `capturedAt` `2026-09-28T12:00:00Z`, namespace `shop`; P1 → ReplicaSet → W1, P2 → ReplicaSet → W2 (the runbook's overlap capture C1) |
| `CAP-B` | As `CAP-A`, but `capturedAt` `2026-09-28T18:00:00Z` and P1 absent because W1 was deleted (the runbook's C2) |
| `CAP-A-D1` | As `CAP-A`, but `capturedAt` on D+1 |
| `CAP-A-NOTIME` | As `CAP-A`, with `capturedAt` missing or without an offset |
| `CAP-DM` | A `DECLARED_MANIFEST` contribution for `shop` |
| `CAP-AMB` / `CAP-CONF` | Captured, K1, day D. P1 has several admissible Workloads with no contradiction (Path C `AMBIGUOUS`) / contradictory owner paths (Path C `CONFLICT`). |
| `CAP-CONF-D1` | As `CAP-CONF`, with `capturedAt` on D+1 |
| `CAP-PARTIAL` | Captured, K1, day D, completeness not `COMPLETE`; P1 absent |

Result kinds:
- **ingestion:** the matrix §15.1 result, visible only in diagnostics and the transition report.
- **request:** phase-1 preflight.
- **query:** one retained v2 candidate evaluated against one selected capture, with the phase reached.
- **answer:** the generic result when no v2 candidate exists (§15.3). **Every** no-eligible answer carries both `LOCALITY_LOCAL_COVERAGE_UNAVAILABLE` and `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION` (§4 interpretation 1).

## 3. Cases

### L01 — Same v2 key with reordered input fields

I1 §7.1

| Variant | Inputs | Expected |
|---|---|---|
| L01a | V02 fields = V01 fields in reverse order | v2_ids = `["V01-base", "V02-reordered-input"]`<br>v2_ids_equal = `true` |

**Prohibited:** field order changes identity.

### L02 — One caller Service, relation and Operation on one day from two Pod UIDs

I1 §7.1, §7.2

| Variant | Inputs | Expected |
|---|---|---|
| L02a | P1 and P2 each call O1 on day D in environment E, cluster K1 | v2_ids = `["V01-base", "V03-distinct-pod"]`<br>v2_ids_equal = `false`<br>v1_ids = `["U01-v1-for-V01-and-V03"]` |

**Prohibited:** two v1 buckets; a second Workload locality inferred from two Pod keys alone.

### L03 — Same Pod UID text in two cluster UIDs

I1 §7.1

| Variant | Inputs | Expected |
|---|---|---|
| L03a | P1 UID in K1 and in K2 | v2_ids = `["V01-base", "V04-same-pod-uid-other-cluster"]`<br>v2_ids_equal = `false` |

**Prohibited:** cross-cluster alias of Pod identity.

### L04 — Two distinct Deployments behind one caller Service, each Pod calling a different Operation

I1 §2.1, §5.1, §12

| Variant | Inputs | Expected |
|---|---|---|
| L04a | CAP-A selected; V01 (P1 to O1), V06 (P2 to O2) | **query:** `APPLICABLE` [—] · candidate `V01-base` on `CAP-A`, phase 4 → W1<br>**query:** `APPLICABLE` [—] · candidate `V06-other-operation` on `CAP-A`, phase 4 → W2<br>v1_ids = `["U01-v1-for-V01-and-V03", "U02-v1-for-V06"]`<br>provider_services = `{"O1": "service:pricing", "O2": "service:legacy-pricing"}`<br>target_runtime_locality = `"unknown"` |

**Prohibited:** target placement of pricing or legacy-pricing; W1 calls O2 or W2 calls O1; exclusive or global dependency; provider Service inferred from placement.

### L05 — Existing v1-only CALLS plus a separately persisted same-Service Pod identity

I1 §7.2, §10.2

| Variant | Inputs | Expected |
|---|---|---|
| L05a | v1 U01 only; RuntimeIdentityObservation for service:orders/P1 on D; legacy-only status not independently known | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |
| L05b | as a, with the source inventory independently known to be legacy-only | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LEGACY_V1_UNSCOPED`, `LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |

**Prohibited:** positive locality by joining v1 with RuntimeIdentityObservation; Pod locality backfilled into v1.

### L06 — CLIENT lacks Pod UID or cluster UID

I1 §6.2, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L06a | carrier present, k8s.pod.uid missing | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_POD_UID_MISSING`] · v1 unchanged, v2 not written |
| L06b | carrier present, k8s.cluster.uid missing | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_CLUSTER_UID_MISSING`] · v1 unchanged, v2 not written |
| L06c | carrier present, both missing | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_CLUSTER_UID_MISSING`, `LOCALITY_POD_UID_MISSING`] · v1 unchanged, v2 not written |
| L06d | read side after a-c: only U01 exists | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |

**Prohibited:** LOCALITY_CLIENT_IDENTITY_MISSING emitted on account of a missing UID; positive locality; ingestion code in a query answer.

### L07 — Paired CLIENT/SERVER in one batch

I1 §6.1

| Variant | Inputs | Expected |
|---|---|---|
| L07a | T01 timestamps; CLIENT Resource P1/K1/E | **ingestion:** `APPLICABLE` [—] · v1 unchanged, v2 written<br>v2_ids = `["V01-base"]`<br>v2_first_last_seen = `"fact (SERVER) timestamp, vector T01"` |

**Prohibited:** route, method or fact time taken from the CLIENT; caller identity from the SERVER Resource.

### L08 — Cross-batch pairs, CLIENT first and SERVER first

I1 §6.1

| Variant | Inputs | Expected |
|---|---|---|
| L08a | CLIENT in batch 1, SERVER in batch 2 | **ingestion:** `APPLICABLE` [—] · v1 unchanged, v2 written<br>v2_ids = `["V01-base"]` |
| L08b | SERVER in batch 1, CLIENT in batch 2 | **ingestion:** `APPLICABLE` [—] · v1 unchanged, v2 written<br>v2_ids = `["V01-base"]` |

**Prohibited:** loss of CLIENT identity across batches; different v2 record by arrival order; unbounded or raw carrier retention.

### L09 — Qualified CLIENT_ONLY versus SERVER_ONLY

I1 §6.1, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L09a | expired CLIENT becomes a v0.5 CLIENT_ONLY CALLS with its carried P1/K1/E | **ingestion:** `APPLICABLE` [—] · v1 unchanged, v2 written<br>v2_ids = `["V01-base"]`<br>correlation_mode = `"CLIENT_ONLY"` |
| L09b | expired SERVER (SERVER_ONLY) | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_SERVER_ONLY_NO_CLIENT`] · v1 none, v2 not written |

**Prohibited:** caller v2 manufactured from a SERVER span.

### L10 — CLIENT environment differs from the accepted fact environment

I1 §6.2, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L10a | CLIENT environment staging, fact environment production (ingestion) | **ingestion:** `INAPPLICABLE` [`LOCALITY_CLIENT_FACT_ENVIRONMENT_MISMATCH`] · v1 unchanged, v2 not written |
| L10b | read time: V01 (environment production) queried with environment staging | **query:** `INAPPLICABLE` [—] (exact environment mismatch (I1 §10.1 names no code)) · candidate `V01-base` on `CAP-A`, phase 3 |

**Prohibited:** environment alias, case-fold or wildcard; owner identity evaluated after the phase 3 failure.

### L11 — CLIENT and fact timestamps on different UTC days

I1 §6.2, §8

| Variant | Inputs | Expected |
|---|---|---|
| L11a | vector T02 (cross midnight) | **ingestion:** `INAPPLICABLE` [`LOCALITY_CLIENT_FACT_DAY_MISMATCH`] · v1 unchanged, v2 not written<br>v1_bucket_day = `"2026-09-28"` |

**Prohibited:** forced same-day v2 bucket; change to the v1 path.

### L12 — One event with v1 and v2 representations

I1 §7.2

| Variant | Inputs | Expected |
|---|---|---|
| L12a | one paired interaction as in L07 | v1_ids = `["U01-v1-for-V01-and-V03"]`<br>v2_ids = `["V01-base"]`<br>v1_observation_count = `1`<br>legacy_calls_edge_evidence_ids = `["U01-v1-for-V01-and-V03"]`<br>snapshot_evidence_array_contains_v2 = `false` |

**Prohibited:** v2 id in the legacy edge evidence_ids; v0.5 count, coverage or qualification doubled.

### L13 — No v2 in the unchanged golden-path graph

I1 §11.1

| Variant | Inputs | Expected |
|---|---|---|
| L13a | golden-path demo state, no v2 records | snapshot_id = `"no_v2_snapshot_pin"`<br>state_has_scoped_key = `false`<br>canonicalization_version = `3` |

**Prohibited:** empty scoped_observed_calls_v2 key; canonicalization version bump.

### L14 — Valid new v2 records

I1 §11.1

| Variant | Inputs | Expected |
|---|---|---|
| L14a | V01 and V03 records exist | state_has_scoped_key = `true`<br>scoped_fragment = `"snapshot_fragment"`<br>fingerprints = `1`<br>same_snapshot_id_on_all_surfaces = `true` |

**Prohibited:** second locality hash; unrecorded snapshot change.

### L15 — Exact current captured Pod, owner, cluster and time

I1 §9

| Variant | Inputs | Expected |
|---|---|---|
| L15a | CAP-A selected; V01 | **query:** `APPLICABLE` [—] · candidate `V01-base` on `CAP-A`, phase 4 → W1 |

**Prohibited:** Workload from name, label or DEPLOYED_AS.

### L16 — CLIENT cluster UID conflicts with the captured envelope clusterUid

I1 §9, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L16a | V04 (P1 UID, cluster K2); CAP-A contains P1 UID under K1 | **query:** `CONFLICT` [`LOCALITY_CLUSTER_UID_CONFLICT`] · candidate `V04-same-pod-uid-other-cluster` on `CAP-A`, phase 4<br>v2_retained = `true` |

**Prohibited:** positive locality; v2 record rewritten or deleted.

### L17 — DECLARED_MANIFEST, missing capturedAt, incompatible captured day

I1 §8, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L17a | V01; selected contribution is DECLARED_MANIFEST | **query:** `UNSUPPORTED` [`LOCALITY_CAPTURE_MODE_UNSUPPORTED`] · candidate `V01-base` on `CAP-DM`, phase 2 |
| L17b | V01; CAP-A without a parseable capturedAt | **query:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_CAPTURE_TIMESTAMP_MISSING`] · candidate `V01-base` on `CAP-A-NOTIME`, phase 3 |
| L17c | V01; capture as CAP-A but capturedAt on D+1; window D | **query:** `INAPPLICABLE` [`LOCALITY_CAPTURE_TEMPORAL_MISMATCH`] · candidate `V01-base` on `CAP-A-D1`, phase 3 |
| L17d | V01 (last_seen on D); CAP-A-D1 selected; window D+1 | **query:** `INAPPLICABLE` [`LOCALITY_OBSERVATION_TEMPORAL_MISMATCH`] · candidate `V01-base` on `CAP-A-D1`, phase 3 |

**Prohibited:** positive observed caller-Workload locality; substituted or nearest capturedAt.

### L18 — P1 replaced by P2; the later selected snapshot lacks P1

I1 §9

| Variant | Inputs | Expected |
|---|---|---|
| L18a | CAP-B selected; V01 (P1), V03 (P2) | **query:** `UNRESOLVED` [`LOCALITY_CAPTURE_MISSING_POD`] · candidate `V01-base` on `CAP-B`, phase 4<br>**query:** `APPLICABLE` [—] · candidate `V03-distinct-pod` on `CAP-B`, phase 4 → W2<br>v2_retained = `true` |

**Prohibited:** P1's event attributed to P2 or W2; P1's event deleted or reported absent.

### L19 — Multiple admissible owners versus contradictory owner assertions

I1 §9, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L19a | V01; selected capture leaves two admissible Workloads for P1, no contradiction (Path C AMBIGUOUS) | **query:** `AMBIGUOUS` [`LOCALITY_POD_OWNER_AMBIGUOUS`] · candidate `V01-base` on `CAP-AMB`, phase 4 |
| L19b | V01; contradictory owner paths for P1 (Path C CONFLICT) | **query:** `CONFLICT` [`LOCALITY_POD_OWNER_CONFLICT`] · candidate `V01-base` on `CAP-CONF`, phase 4 |

**Prohibited:** specificity or recency guess; AMBIGUOUS collapsed into CONFLICT or UNRESOLVED.

### L20 — Caller local, target locality missing

I1 §4.1, §5

| Variant | Inputs | Expected |
|---|---|---|
| L20a | CAP-A; V01 | **query:** `APPLICABLE` [—] · candidate `V01-base` on `CAP-A`, phase 4 → W1<br>target_runtime_locality = `"unknown"` |

**Prohibited:** pricing placed in namespace shop or cluster K1.

### L21 — Applicable Service-level declaration plus independently observed scoped CALLS

I1 §5

| Variant | Inputs | Expected |
|---|---|---|
| L21a | orders manifest declares the call to pricing O1; CAP-A; V01 | **query:** `APPLICABLE` [—] · candidate `V01-base` on `CAP-A`, phase 4 → W1<br>qualification = `"CONFIRMED"` |

**Prohibited:** declaration treated as Workload-authored or exclusive.

### L22 — Scoped observed CALLS without an applicable declaration

I1 §5

| Variant | Inputs | Expected |
|---|---|---|
| L22a | CAP-A; V06 (O2); no declaration for O2 | **query:** `APPLICABLE` [—] · candidate `V06-other-operation` on `CAP-A`, phase 4 → W2<br>qualification = `"OBSERVED_ONLY"` |
| L22b | as a, plus the O1 declaration | qualification = `"OBSERVED_ONLY"` |

**Prohibited:** O2 confirmed by the declaration of O1.

### L23 — Declared-only relation or Service-level coverage, no scoped call

I1 §5

| Variant | Inputs | Expected |
|---|---|---|
| L23a | O1 declared; v1 coverage exists; no v2 | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |

**Prohibited:** local NOT_OBSERVED_IN_WINDOW; verified local absence; positive Workload-local CALLS.

### L24 — Region, tenant, version or messaging locality requested

I1 §4.2, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L24a | request adds a region, tenant or service-version dimension | **request:** `UNSUPPORTED` [`LOCALITY_UNSUPPORTED_DIMENSION`] · request preflight (phase 1) |
| L24b | request asks for SENDS/PUBLISHES_TO locality | **request:** `UNSUPPORTED` [`LOCALITY_UNSUPPORTED_RELATION`] · request preflight (phase 1) |

**Prohibited:** global or wildcard fallback.

### L25 — Sub-day range, or an event exactly at next-day midnight

I1 §8

| Variant | Inputs | Expected |
|---|---|---|
| L25a | request with date-time bounds inside D | **request:** `UNSUPPORTED` [`LOCALITY_UNSUPPORTED_TEMPORAL_RESOLUTION`] · request preflight (phase 1) |
| L25b | event at 2026-09-29T00:00:00.000000Z; window D | utc_day = `"2026-09-29"`<br>in_window_D = `false`<br>vectors = `["M03-next-midnight-excluded", "D04-midnight-is-next-day"]` |

**Prohibited:** silently widened or narrowed window; change to v0.5 date-time windows.

### L26 — Name-only, co-location or configured Service DEPLOYED_AS, no v2

I1 §5, §6.1

| Variant | Inputs | Expected |
|---|---|---|
| L26a | U01; Deployment orders annotated service:orders; Pod names match orders-*; no v2 | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |

**Prohibited:** per-interaction caller locality inferred.

### L27 — Overlap capture of two Deployments, then an authoritative capture without the old Pod

I1 §9, §12

| Variant | Inputs | Expected |
|---|---|---|
| L27a | CAP-A selected; V01 (P1 to O1), V06 (P2 to O2) | **query:** `APPLICABLE` [—] · candidate `V01-base` on `CAP-A`, phase 4 → W1<br>**query:** `APPLICABLE` [—] · candidate `V06-other-operation` on `CAP-A`, phase 4 → W2<br>workload_localities = `2` |
| L27b | CAP-B selected afterwards | **query:** `UNRESOLVED` [`LOCALITY_CAPTURE_MISSING_POD`] · candidate `V01-base` on `CAP-B`, phase 4<br>**query:** `APPLICABLE` [—] · candidate `V06-other-operation` on `CAP-B`, phase 4 → W2 |

**Prohibited:** two localities claimed from CAP-B; P1 locality reconstructed from an externally kept CAP-A.

### L28 — Many successive Pods at a constant Workload count

I1 §11.5

| Variant | Inputs | Expected |
|---|---|---|
| L28a | n distinct Pods of W1 each call O1 on D | v2_record_count = `"n"`<br>v1_bucket_count = `1`<br>cost_obligation = `"I2/I4 churn measurement (v2 contract §9)"` |

**Prohibited:** compaction or truncation of v2 records.

### L29 — Incomplete inventory or unauthorized source removal

I1 §11.3

| Variant | Inputs | Expected |
|---|---|---|
| L29a | selected capture's inventory incomplete; P1 absent from it | **query:** `UNRESOLVED` [`LOCALITY_CAPTURE_MISSING_POD`] · candidate `V01-base` on `CAP-PARTIAL`, phase 4<br>v2_retained = `true` |

**Prohibited:** local absence inferred; removal authority widened.

### L30 — Intent or agent-narrative changes alone

I1 §4.3

| Variant | Inputs | Expected |
|---|---|---|
| L30a | only narrative or future-Intent text changes | assessment_changed = `false`<br>snapshot_changed = `false` |

**Prohibited:** Intent effective interval used as the observation window; changed evidence or qualification.

### L31 — v2 last_seen on D, capture capturedAt on D+1, request D

I1 §8

| Variant | Inputs | Expected |
|---|---|---|
| L31a | V01; CAP-A-D1; window D | **query:** `INAPPLICABLE` [`LOCALITY_CAPTURE_TEMPORAL_MISMATCH`] · candidate `V01-base` on `CAP-A-D1`, phase 3 |

**Prohibited:** positive locality on D.

### L32 — Two Operations of one provider Service, plus a missing or ambiguous owner

I1 §5.1

| Variant | Inputs | Expected |
|---|---|---|
| L32a | CAP-A; P1 calls O1 (declared) and O3 = operation:pricing:GET:/prices/{id} (undeclared) | per_operation_qualification = `{"O1": "CONFIRMED", "O3": "OBSERVED_ONLY"}`<br>logical_provider = `"service:pricing"`<br>group_evidence = `"sorted union of O1 and O3 references"`<br>group_shape = `"I3"` |
| L32b | an Operation whose canonical owner is missing or ambiguous | provider_dependency_minted = `false` |

**Prohibited:** cross-Operation CONFIRMED; provider Service from a display name.

### L33 — Two ReplicaSets under one Deployment versus two distinct Deployments

I1 §2.1, §12

| Variant | Inputs | Expected |
|---|---|---|
| L33a | P1 and P2 owned by two ReplicaSets of Deployment orders | v2_ids_distinct = `true`<br>workload_localities = `1` |
| L33b | P1 in orders, P2 in orders-canary (CAP-A) | v2_ids_distinct = `true`<br>workload_localities = `2` |

**Prohibited:** ReplicaSet treated as a Workload locality.

### L34 — Query-time namespace contradiction versus CLIENT-internal contradiction

I1 §6.2, §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L34a | CLIENT k8s.namespace.name shop-old passes ingestion; CAP-A has P1 in shop | **ingestion:** `APPLICABLE` [—] · v1 unchanged, v2 written<br>**query:** `CONFLICT` [`LOCALITY_NAMESPACE_CONFLICT`] · candidate `V01-base` on `CAP-A`, phase 4<br>v2_retained = `true` |
| L34b | CLIENT Resource carries both k8s.deployment.name and k8s.statefulset.name | **ingestion:** `CONFLICT` [`LOCALITY_CLIENT_INTERNAL_CONFLICT`] · v1 unchanged, v2 not written |

**Prohibited:** capture compared at ingestion; valid v2 suppressed by a query-time conflict.

### L35 — Ingestion refusals versus read-side v1 abstention, plus valid v2 with Path C owner problems

I1 §10.1, §10.2

| Variant | Inputs | Expected |
|---|---|---|
| L35a | SERVER_ONLY | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_SERVER_ONLY_NO_CLIENT`] · v1 none, v2 not written |
| L35b | no CLIENT carrier (not SERVER_ONLY) | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_CLIENT_IDENTITY_MISSING`] · v1 unchanged, v2 not written |
| L35c | carrier present, Pod UID missing only | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_POD_UID_MISSING`] · v1 unchanged, v2 not written |
| L35d | carrier present, environment and Pod UID missing (matrix §15.1 interpretation) | **ingestion:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_CLIENT_IDENTITY_MISSING`, `LOCALITY_POD_UID_MISSING`] · v1 unchanged, v2 not written |
| L35e | known ingress environment mismatch | **ingestion:** `INAPPLICABLE` [`LOCALITY_CLIENT_FACT_ENVIRONMENT_MISMATCH`] · v1 unchanged, v2 not written |
| L35f | known ingress day mismatch | **ingestion:** `INAPPLICABLE` [`LOCALITY_CLIENT_FACT_DAY_MISMATCH`] · v1 unchanged, v2 not written |
| L35g | CLIENT-internal contradiction plus missing Pod UID | **ingestion:** `CONFLICT` [`LOCALITY_CLIENT_INTERNAL_CONFLICT`, `LOCALITY_POD_UID_MISSING`] · v1 unchanged, v2 not written |
| L35h | read side after any of b-g: only v1 exists | **answer:** `INSUFFICIENT_EVIDENCE` [`LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`, `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`] |
| L35i | valid V01 with Path C ambiguous, then conflicting, owners | **query:** `AMBIGUOUS` [`LOCALITY_POD_OWNER_AMBIGUOUS`] · candidate `V01-base` on `CAP-AMB`, phase 4<br>**query:** `CONFLICT` [`LOCALITY_POD_OWNER_CONFLICT`] · candidate `V01-base` on `CAP-CONF`, phase 4 |

**Prohibited:** specific ingress code in a query answer; every v1 contribution presumed refused; generic carrier-missing code together with a UID-missing code on the UID's account.

### L36 — Day-D observation, day-D+1 capture with a conflicting owner chain, request D

I1 §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L36a | V01; CAP-CONF-D1 (capturedAt D+1, contradictory owners); window D | **query:** `INAPPLICABLE` [`LOCALITY_CAPTURE_TEMPORAL_MISMATCH`] · candidate `V01-base` on `CAP-CONF-D1`, phase 3<br>phase_4_evaluated = `false` |

**Prohibited:** in-scope CONFLICT asserted; owner reasons invented for an unevaluated phase.

### L37 — Candidate has only DECLARED_MANIFEST with contradictory-looking owner data

I1 §10.1

| Variant | Inputs | Expected |
|---|---|---|
| L37a | V01; CAP-DM with contradictory owner references | **query:** `UNSUPPORTED` [`LOCALITY_CAPTURE_MODE_UNSUPPORTED`] · candidate `V01-base` on `CAP-DM`, phase 2<br>phase_4_evaluated = `false` |

**Prohibited:** phase 4 owner assertion; observed locality invented from a manifest.

## 4. Interpretations flagged for review

These interpretations follow from the accepted text but are stated explicitly here, so that review can confirm or redirect them before I2 builds against them:

1. **Coverage code on every no-eligible answer.** No admitted v0.6 input establishes Workload-level coverage (I1 §5), so local coverage is *always* unavailable. Every generic no-eligible answer therefore carries `LOCALITY_LOCAL_COVERAGE_UNAVAILABLE` together with `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION`. I1 §10.2 says "as relevant", and this dossier reads it as always relevant in v0.6.
2. **Environment and UID both missing** (L35d) give both codes. This is carried over from matrix §15.1 as reviewed in PR #308.
3. **Read-time environment mismatch** (L10b) gives `INAPPLICABLE` with no `LOCALITY_*` code, because I1 §10.1 names none and none is minted.
4. **An ingestion result of `APPLICABLE`** (L07–L09, L34a) means only that the interaction passed guards I-1 to I-5 and a v2 seed was written. It is not a locality answer.

## 5. Traceability

| I1 requirement | Where |
|---|---|
| §13: freeze source evidence and expected result for every L01–L37 row, including disposition/reason codes, v1/v2 keys, captured-source context, lineage and prohibited conclusions | §2 fixtures, §3 cases, JSON |
| §13: independently expected, not self-oracled | §1 |
| §16 DoD 4: phase-gated mapping, terminal per-candidate `UNSUPPORTED`, `AMBIGUOUS`, early exits | L17, L19, L31, L35–L37 |
| DoD 5: `CONFIRMED` / `OBSERVED_ONLY`, no local `NOT_OBSERVED_IN_WINDOW` | L21–L23; the consistency test |
| DoD 9: ingestion-only codes stay out of query answers | L06, L35; the consistency test |
| DoD 10: no broadened refusal, no display-name reidentity | L05, L20, L26, L32 |
| DoD 11: observation window ≠ Intent effective interval | L30 |
