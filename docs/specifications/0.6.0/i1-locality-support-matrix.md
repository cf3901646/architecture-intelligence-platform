# AIP v0.6.0 I1 — Locality Support Matrix

**Status:** I1 supporting deliverable, slice I1.1 (baseline inventory, role vocabulary and applicability matrix). Contract freeze artifact under review; it claims no implementation and no executed conformance.  
**Release / increment:** `v0.6.0` — Locality-Aware Current State / I1  
**Governing specification:** [I1 — Locality and Evidence Applicability Contract](i1-locality-and-evidence-applicability.md) (accepted, [PR #283](https://github.com/michaelegner/architecture-intelligence-platform/pull/283), merge `aafb03d5735d78b2741a3dc8a2d0336079535ed6`), under the [accepted v0.6.0 parent](specification.md) (PR #278, merge `be26edcd133edc8576a85d301be33b836335c41b`).  
**Code baseline inspected:** `main` at `77479c107ddc719e465cf6827c4bedd18afea8bd`. Every `file:line` reference below is to that commit.  
**Internal contract identifier:** `locality-contract/1` (I1 §4.1). This identifies the internal semantic contract, not the future public I3 JSON schema version.

This document restates **no new semantics**. It freezes, in tabular and reviewable form, what the accepted I1 specification already decides, and records the verified current code baseline those decisions build on. Where this document and the I1 specification appear to disagree, the I1 specification wins and this document is defective. Later I1 slices extend this document (I1.2: CLIENT field allowlist, UTC-day window normalization and the phase-gated disposition table) or add sibling deliverables (I1.3 v2 evidence contract, I1.4 capture runbook, I1.5 conformance dossier and completion record).

---

## 1. Baseline inventory (I1 §2, slice I1.1)

The table verifies each I1 §2 baseline claim against the code and adds the facts I2 must not overlook. "Consequence" is the constraint that follows from the accepted I1 contract; it is not an additional rule.

| # | Mechanism (at `77479c1`) | Verified current behaviour | Consequence under the accepted I1 contract |
|---|---|---|---|
| B1 | [`app/canonical/ids.py`](../../../app/canonical/ids.py):39 `observed_evidence_id` | ID is `evidence:otel:{environment}:{YYYY-MM-DD}:{h}` where `h` is the first **12** hex characters of SHA-256 over the UTF-8 string `subject_id\|relation_type\|object_id`. No Pod, cluster, trace or span component. | **The v1 attribution gap:** a v1 bucket cannot distinguish caller Pods or clusters. v1 stays byte-unchanged; caller attribution requires the separate v2 identity (I1 §7). |
| B2 | [`app/telemetry/correlation_buffer.py`](../../../app/telemetry/correlation_buffer.py):9 `PendingHttpSpan` | Fields: `trace_id, span_id, parent_span_id, span_kind, service_name, service_namespace, service_version, environment, method, route, target_identity, timestamp`. **No `k8s_*` or cluster field.** | I2 must extend the transient carrier with the admitted CLIENT identity (I1 §6.1). Without that, cross-batch pairs cannot produce v2. |
| B3 | `HttpCorrelationConfig`, [`app/settings.py`](../../../app/settings.py):57; buffer `sweep_expired`/eviction, `correlation_buffer.py`:78–94 | TTL defaults to 60 s, measured from **wall-clock insertion time**. The size bound defaults to 10 000. TTL-expired spans are returned by `sweep_expired()`. Size-evicted spans are only counted in `evictions` and otherwise **dropped silently**. | The existing TTL and size bounds are preserved (I1 §6.1). A size-evicted CLIENT yields neither v1 nor v2 today; this contract does not change that. |
| B4 | [`app/telemetry/adapter.py`](../../../app/telemetry/adapter.py):234 `correlate_http_call_observations` | Pairing: SERVER is keyed `(trace_id, parent_span_id)` and CLIENT `(trace_id, span_id)`, in batch and across batches (`offer_server` at `correlation_buffer.py`:96, `offer_client` at :115). An expired CLIENT can become a `CLIENT_ONLY` fact (`adapter.py`:393). An expired SERVER **always** becomes `UnresolvedObservation(missing_caller_identity)` (`adapter.py`:402–426). | `SERVER_ONLY` produces no CALLS fact today, so it can produce neither v1 CALLS nor v2 (I1 §6.1, L09). `CLIENT_ONLY` may become v2 only if its CLIENT identity survives (I1 §6.1). |
| B5 | `adapter.py`:256–262 (docstring) and :311–314 | On the paired path (in-batch and cross-batch), environment, method, route and fact timestamp (`server.end_time`) all come from the **SERVER** span. The CLIENT supplies only `source_service_version`. **The CLIENT environment is never compared with the SERVER/fact environment.** | Preserve the SERVER-sourced route/method/timestamp (I1 §2, §6.1). Ingestion guard (3) (CLIENT environment == accepted fact environment, I1 §6.2) is a **new, v2-only** check and does not alter v1 acceptance. |
| B6 | [`app/telemetry/otlp_receiver.py`](../../../app/telemetry/otlp_receiver.py):46 `_resource_identity` | The only Resource reader. It reads exactly `service.name`, `service.namespace`, `service.version`, `service.instance.id`, `deployment.environment.name`, `k8s.pod.uid`, `k8s.pod.name`, `k8s.namespace.name`, `k8s.cluster.uid`, `k8s.deployment.name`, `k8s.statefulset.name`, `k8s.daemonset.name`. | All CLIENT fields the I1 contract needs are already read by the receiver; nothing wider may be admitted (I1 §6.2(5), §11.4). The exact allowlist is frozen in slice I1.2. |
| B7 | `otlp_receiver.py`:66 `_to_datetime`; [`app/telemetry/model.py`](../../../app/telemetry/model.py):69 `day_bucket` | Span times are `datetime.fromtimestamp(unix_nano / 1e9, tz=UTC)`, which gives microsecond precision after float conversion. `day_bucket` truncates to a calendar day in the timestamp's own `tzinfo`; it is UTC in practice because the receiver emits UTC. | The event-instant precision and UTC-day assignment are frozen in slice I1.2 (I1 §8). |
| B8 | [`app/telemetry/runtime_identity.py`](../../../app/telemetry/runtime_identity.py); `RuntimeIdentityObservation`, [`app/provenance/model.py`](../../../app/provenance/model.py):71 | A per-Service/Pod/day observation, derived from **any** span with `service.name`, `k8s.pod.uid` and environment. It is independent of any individual relationship. | It is **Path C input only**. It never attributes a CALLS to a Pod (I1 §2, §5; L05, L26). |
| B9 | [`app/architecture_intelligence/deployment_projection.py`](../../../app/architecture_intelligence/deployment_projection.py):677 `_observation_context_limitation` | In order: missing environment gives `DEPLOYMENT_EVIDENCE_INCOMPLETE`; environment mismatch gives `DEPLOYMENT_ENVIRONMENT_MISMATCH`; `window_start <= last_seen <= window_end` is inclusive; then `window_start <= capturedAt <= window_end` is inclusive, and an unparseable or missing `capturedAt` gives `DEPLOYMENT_TEMPORAL_MISMATCH`. | I1 §8 reuses this **exact inclusive predicate**, fed with the v2 bucket's own `last_seen` and the matching Pod capture's `capturedAt`. v0.5 Path C itself is unchanged. |
| B10 | `deployment_projection.py`:628 `_consistency_attributes_agree`, :658 | Cluster UID is checked only here, as `obs.k8s_cluster_uid is not None and obs.k8s_cluster_uid != pod.cluster_uid`. A **missing** observation cluster UID counts as agreement. | This lenient v0.5 rule is **not** the v2 rule. v2 requires a non-empty CLIENT `k8s.cluster.uid` at ingestion (I1 §6.2(2)) and exact equality with the envelope `clusterUid` at query time (I1 §4.2, §9; L16). v0.5 behaviour is unchanged. |
| B11 | `DeploymentResolutionStatus`, [`app/architecture_intelligence/contracts.py`](../../../app/architecture_intelligence/contracts.py):598 | `RESOLVED_EXPLICIT`, `RESOLVED_CONFIGURED`, `RESOLVED_OBSERVED`, `CONFLICT`, `AMBIGUOUS`, `UNRESOLVED`. | The locality dispositions preserve the distinct Path C meanings of `AMBIGUOUS` and `CONFLICT` (I1 §9, §10.1; L19). |
| B12 | [`app/sources/kubernetes_envelope.py`](../../../app/sources/kubernetes_envelope.py):206–216; [`app/sources/kubernetes_mapping.py`](../../../app/sources/kubernetes_mapping.py):44; [`app/sources/kubernetes_owner_chain.py`](../../../app/sources/kubernetes_owner_chain.py):186 | `metadata.capturedAt` is **envelope-wide**; there is no per-resource capture time. `source.clusterUid` and `source.mode` ∈ {`DECLARED_MANIFEST`, `CAPTURED_RESOURCE`}. Supported Workload kinds are Deployment, StatefulSet and DaemonSet. Owner chains are Pod→ReplicaSet→Deployment, Pod→StatefulSet and Pod→DaemonSet. | `capturedAt` is the capture's time, not continuous Pod presence (I1 §8–9). One Deployment rolling across two ReplicaSets is **one** Workload (I1 §2.1, §12; L33). |
| B13 | [`app/qualification/declared_observed.py`](../../../app/qualification/declared_observed.py):25–27, :58 | The statuses are `CONFIRMED`, `OBSERVED_ONLY` and `NOT_OBSERVED_IN_WINDOW`. Observed matching requires exact environment and an inclusive `last_seen` window. Declared evidence ignores environment and window. | This remains the single qualification owner (ADR 0010). Local `NOT_OBSERVED_IN_WINDOW` is unreachable and forbidden (I1 §5). |
| B14 | [`app/architecture_intelligence/repository.py`](../../../app/architecture_intelligence/repository.py):53, :344; [`examples/release-golden-path/expected.json`](../../../examples/release-golden-path/expected.json):45 | `_CANONICALIZATION_VERSION = 3`. The snapshot ID is `aip:snapshot:v1:` plus the full SHA-256 of sorted-key canonical JSON of the state. The frozen golden pin is `aip:snapshot:v1:0bfcbdeda363876559bb78f53e432f1a73c368e9fbd4d21c37f8f4335ecdbd5f`. | With no v2 records, the bytes, the version and this pin must stay identical (I1 §11.1; L13). The conditional v2 contribution is frozen in slice I1.3. |

---

## 2. Role vocabulary (I1 §4.1)

The six roles are **independent even when their values coincide**. No role's value may be copied into another role without its own admissible evidence path.

| Role (contract name) | Answers | Admissible source | Must never be derived from |
|---|---|---|---|
| `RequestedScope` | What the caller asked about: question, environment, whole-UTC-day window, optional later I3 locality selection | The request | Evidence. A request is not evidence. |
| `SourceCaptureScope` | What a source is known to cover: source instance/revision, admitted inventory, evidence mode, `capturedAt` | The source's accepted inventory and envelope | Timeless presence. A capture is not continuous state. |
| `CallerRuntimeScope` | Where the caller side of **one individual** accepted CALLS ran (cluster UID, Pod UID, then, after query-time resolution, namespace and Workload) | The actual CLIENT span's Resource, carried with that interaction | Same-Service Pod co-occurrence, SERVER Resource, `DEPLOYED_AS`, display names |
| `TargetRuntimeScope` | Where the target ran | Only separately evidenced target runtime placement | The caller's scope, or the logical Operation owner. **Unknown by default** (L20). |
| `ClaimApplicabilityScope` | Where the precise assertion is supported | The derivation of that assertion from its inputs and rule | Anything broader than its inputs |
| `ProjectionSelectionScope` | Which candidate localities a later I3 answer evaluated, included or excluded | The I3 projection | Source evidence. Filtering is not evidence. |

## 3. Internal contract types (I1 §4.3)

The field sets below are frozen as **internal** types of `locality-contract/1`. They are not public API, storage labels or the I3 wire schema. The `V1` suffix versions *the type*, not the v1 observed-evidence generation (I1 §2.1).

| Type | Fields (I1 §4.3) | Semantic boundary |
|---|---|---|
| `LocalityDayContextV1` | `environment`, `first_utc_day`, `last_utc_day` (inclusive date range), `requested_dimensions` (admitted only), `selected_snapshot_ref` | An **observed Current-State evidence window** (§6 below). |
| `CallerAttributionV1` | `subject_service_id`, `relation_type` = `CALLS`, `object_operation_id`, `accepted_fact_environment`, `accepted_fact_timestamp`, `client_environment`, `client_timestamp`, `client_cluster_uid`, `client_pod_uid`, `optional_consistency` (admitted allowlist), `normalization_rule` (ID and version) | Retained at **ingestion**, independently of any Workload resolution. It establishes Pod attribution, not Workload locality. |
| `ResolvedCallerLocalityV1` | `attribution_ref`, `selected_snapshot_ref`, `capture_source_revision`, `captured_at`, `cluster_uid`, `namespace`, `workload_ref`, `disposition`, `reasons` (sorted, distinct) | Computed at **query time** against the one selected snapshot. It is never written back into the v2 event identity. |

---

## 4. Evidence × claim-kind applicability matrix (I1 §5, parent §8)

This is the **minimum** matrix. Any claim kind or evidence not listed is not admitted in v0.6 and needs separately reviewed scope, rules and independent tests.

| Evidence | Nature | May support | Cannot support alone | Conformance |
|---|---|---|---|---|
| Accepted OpenAPI Service/Operation declaration | DECLARED | A source- and Service-scoped declared Operation. It may match an **independently observed** local CALLS through the shared qualification owner. | That an event executed in a particular Workload; a region-local declaration; a Workload-authored or Workload-exclusive declaration | L21, L22, L23 |
| Resolved OTel HTTP CLIENT span with actual bounded Resource | OBSERVED | Per-interaction caller **Pod and cluster** identity | A unique owner Workload, or target placement, without captured evidence | L06, L07, L15 |
| Correlated OTel HTTP SERVER span | OBSERVED | The existing resolved provider method, route and fact timestamp | Caller locality from the SERVER Resource | L07, L09 |
| Existing v1 daily CALLS evidence | OBSERVED | The existing Service-level observed relation, coverage and counts | Retrospective Pod or Workload attribution by a Service/time join | L05, L12 |
| `RuntimeIdentityObservation` | OBSERVED | Its own Path C Service/Pod/`DEPLOYED_AS` inputs | Proof that a particular CALLS originated from that Pod | L05, L26 |
| Isolated v2 scoped CALLS record | OBSERVED | A caller-Pod/cluster-specific observed contribution | Positive Workload locality without a compatible capture in the query snapshot | L02, L15, L18 |
| Unique `CAPTURED_RESOURCE` Pod/owner chain | INFRASTRUCTURE capture | The exact captured resource and owner/Workload identity at `capturedAt` | A CALLS edge; timeless Pod presence; an observed action inferred from placement | L15, L18, L27 |
| `DECLARED_MANIFEST` Kubernetes contribution | DECLARED infrastructure | Its own declared infrastructure identity (v0.5 semantics) | Any observed caller-Workload locality: per candidate `UNSUPPORTED` / `LOCALITY_CAPTURE_MODE_UNSUPPORTED` | L17, L37 |
| Configured or explicit `DEPLOYED_AS` | CONFIGURED / DECLARED | Its own source-qualified Service–Workload association | The location of all of that Service's interactions | L26 |
| Operator-authored AsyncAPI overlay | DECLARED | A source-attributable declared messaging claim under v0.5 | Observed Kafka behaviour or local messaging qualification (`UNSUPPORTED` in this slice) | L24 |

### 4.1 Qualification boundary (I1 §5)

| Inputs for one caller-local CALLS against one exact Operation | Shared qualification owner result | Forbidden |
|---|---|---|
| Matching accepted Service/Operation declaration **and** an applicable scoped observed CALLS | `CONFIRMED` | Treating the declaration as Workload-authored or Workload-exclusive |
| Applicable scoped observed CALLS, no matching declaration (or a declaration for a different Service or Operation) | `OBSERVED_ONLY` | Confirming from the wrong Service or Operation (L22) |
| Declaration only, or Service-level coverage only, no applicable scoped CALLS | No positive Workload-local CALLS; `INSUFFICIENT_EVIDENCE` with `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION` / `LOCALITY_LOCAL_COVERAGE_UNAVAILABLE` | Local `NOT_OBSERVED_IN_WINDOW`, which is unreachable because no Workload-level coverage source is admitted (L23) |

Unscoped v0.5 qualification, coverage and `NOT_OBSERVED_IN_WINDOW` semantics are unchanged.

---

## 5. Locality dimension support matrix (I1 §4.2, parent §6.1)

| Dimension | Status in `locality-contract/1` | Only admissible source | Missing or unavailable value | Requested but not admitted |
|---|---|---|---|---|
| `environment` | **Admitted, required** | Accepted fact `deployment.environment.name`; the CLIENT value must be exactly equal at ingestion | No v2 (ingestion); `INSUFFICIENT_EVIDENCE` | — |
| Whole UTC-day window | **Admitted, required** | The request's inclusive date range. Normalization is frozen in slice I1.2. | — | Sub-day or partial-day: `UNSUPPORTED` / `LOCALITY_UNSUPPORTED_TEMPORAL_RESOLUTION` |
| Caller cluster UID | **Admitted, required, exact** | Actual CLIENT `k8s.cluster.uid`, which must equal the captured envelope `clusterUid` | `INSUFFICIENT_EVIDENCE` / `LOCALITY_CLUSTER_UID_MISSING` | — |
| Caller Pod UID | **Admitted as attribution identity only** | Actual CLIENT `k8s.pod.uid` | `INSUFFICIENT_EVIDENCE` / `LOCALITY_POD_UID_MISSING` | — |
| Caller namespace | **Admitted, derived at query time** | The captured Pod/owner-chain namespace in the selected snapshot. The CLIENT `k8s.namespace.name` is a consistency check only. | `UNRESOLVED` | — |
| Caller Workload | **Admitted, derived at query time** | A unique supported captured owner chain (Deployment, StatefulSet, DaemonSet) in the selected snapshot | `UNRESOLVED` / `AMBIGUOUS` / `CONFLICT` per I1 §9–10 | — |
| Target runtime locality | **Not established by this contract** | Separately evidenced target placement only; none is admitted in the minimum slice | Unknown (L20) | — |
| Region | **Unsupported** | — | — | `UNSUPPORTED` / `LOCALITY_UNSUPPORTED_DIMENSION` |
| Tenant | **Unsupported** | — | — | `UNSUPPORTED` / `LOCALITY_UNSUPPORTED_DIMENSION` |
| Service-version locality | **Unsupported** (`service.version` never mints a canonical Service) | — | — | `UNSUPPORTED` / `LOCALITY_UNSUPPORTED_DIMENSION` |
| Messaging locality (SENDS / PUBLISHES_TO / …) | **Unsupported** | — | — | `UNSUPPORTED` / `LOCALITY_UNSUPPORTED_RELATION` |

Admitted relation: HTTP `CALLS` (caller Service → provider **Operation**) only. Other v0.5 relations keep their existing query semantics; only the new relation-locality surface reports them as unsupported for locality qualification.

**No wildcard.** An omitted, missing, contradictory, stale or unsupported dimension is reported with its disposition. It is never `*`, never inferred from a similar display name, a label, namespace proximity or co-location, and never a reason to widen the claim to all localities (parent §6; I1 §4.2).

**Two Workloads in one cluster and namespace are two localities** if and only if their captured owner chains independently establish two distinct supported Workload objects. Two ReplicaSets of one Deployment are one Workload (L33).

---

## 6. No-inference matrix (DoD 2 and 10; parent gates 3 and 6)

Each row is an inference the contract forbids, together with the conformance case that must prove it stays forbidden.

| Attempted basis for assigning an individual CALLS to a caller Pod or Workload | Result | Case |
|---|---|---|
| Same-Service `RuntimeIdentityObservation` joined to a v1 bucket by Service/time | No attribution: unscoped v1 only, no backfill | L05 |
| Pod or Workload **name** match, labels, namespace proximity, co-location | No attribution | L26 |
| Configured or explicit Service-level `DEPLOYED_AS` | No attribution | L26 |
| SERVER Resource, `peer.service`, tracing parentage alone | No caller identity | L09, §6.1 |
| Legacy v1 aggregate without replayable original per-interaction input | `INSUFFICIENT_EVIDENCE` / `LOCALITY_LEGACY_V1_UNSCOPED` (only where legacy-only status is independently known) | L05, L35 |
| Replacement Pod P2 for an event from P1 | Never reattached: P1's Workload becomes `UNRESOLVED` when P1 leaves the selected capture | L18, L27 |
| Nearest timestamp, skew allowance, implicit timezone, substituted `capturedAt` | Not admitted | L17, L31 |
| Latest, friendliest or most specific of several owner candidates | Not admitted: `AMBIGUOUS` or `CONFLICT` retained | L19 |
| Display-name matching of a canonical Service or Operation owner | Never rewrites Service identity or Operation ownership | L32 |
| Extracting a narrower scope from an existing v0.5 refusal | Never converts a refusal into positive locality | §10.2 |

## 7. Operation → provider Service projection constraints (I1 §5.1; handoff to I3)

I1 fixes **constraints only**. The exact public roll-up shape is an I3 freeze.

1. The observed relation is `caller Service --CALLS--> provider Operation`. The v2 `object_id` is the canonical **Operation ID**.
2. Each eligible local CALLS is qualified against its **exact** Operation through the existing qualification owner.
3. The logical provider Service is the Operation's **unique canonical owning Service** from accepted source/identity state. It is never taken from a display name or an inferred deployed target.
4. Grouping key for a later Service dependency: *(caller Service, resolved caller Workload locality, provider Service, selected observation context/snapshot)*. Evidence and claim references are the deduplicated, sorted **union** of the qualifying per-Operation references, and each Operation-level status and provenance is retained.
5. When Operation ownership is missing or ambiguous, no provider Service dependency is minted.
6. No `CONFIRMED` is produced by pooling a declaration of one Operation with an observation of another.
7. No global, absent, exclusive or target-runtime-locality claim is derived from a group.

**Handed to I3:** response shape, bounded Operation membership and evidence union, canonical ordering, group-level qualification presentation, the incomplete or ambiguous-owner disposition, and distinct-Operation/same-provider and missing-owner acceptance scenarios (L32).

## 8. Observation window versus Intent effective interval (I1 §4.3; parent gate 5; DoD 11)

| | Current-State observation window | Future (v0.7) Intent effective interval |
|---|---|---|
| Type | `LocalityDayContextV1.first_utc_day` / `last_utc_day` (and the I1.2 `ScopedDayWindowV1`) | A different type on a different semantic timeline (not defined in v0.6) |
| Meaning | The days in which **actual observed evidence** is considered | When an intended architecture is meant to hold |
| Enters Current-State qualification | Yes, as the observation-context bound | **Never.** It cannot substitute for the observation window and cannot change evidence or qualification (L30). |

Documentation, examples and later types must not use one term for the other.

---

## 9. Traceability of this slice

| I1 requirement | Section here |
|---|---|
| §14 slice I1.1: baseline code/source inventory and v1 attribution gap | §1 (B1–B14) |
| §4.1 roles, `locality-contract/1` | §2 |
| §4.3 internal types | §3 |
| §5 / parent §8 claim-kind × evidence matrix; qualification boundary | §4, §4.1 |
| §4.2 / parent §6.1 dimensions, unsupported set, no wildcard | §5 |
| DoD 2 and 10 no-inference (parent gates 3 and 6) | §6 |
| §5.1 Operation → provider Service constraints | §7 |
| §4.3 / DoD 11 observation window vs Intent | §8 |

Deferred to later I1 slices: the CLIENT allowlist and exact comparison rules, the UTC-day normalization and golden vectors, and the §10.1 phase-gate table (I1.2); the v2 key, vectors and snapshot contract (I1.3); the capture runbook (I1.4); and the independent L01–L37 expected dossier and completion record (I1.5).
