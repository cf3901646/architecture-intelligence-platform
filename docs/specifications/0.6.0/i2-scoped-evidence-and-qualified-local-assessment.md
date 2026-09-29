# AIP v0.6.0 I2 — Scoped Evidence Implementation and Qualified Local Evidence Assessment

**Status:** Draft 0.1 — proposed increment specification; not yet reviewed or accepted. This document prescribes I2 work; it is not an I2 implementation or qualification completion record.  
**Release / increment:** v0.6.0 / I2, Locality-Aware Current State  
**Repository destination (proposed):** `docs/specifications/0.6.0/i2-scoped-evidence-and-qualified-local-assessment.md`  
**Entry baseline inspected:** `main` at `7a949cd3046e91ddd6ea67036b6bf47c241ed037` (PR #311, I1.5 merge).  
**Governing authority:** [Accepted v0.6.0 parent](specification.md), especially §§3–12, 15–16, 33–34; [accepted I1 specification](i1-locality-and-evidence-applicability.md), especially §§4–13, 15–16. This draft does not reopen I1 semantics.  
**Frozen supporting inputs:** [I1 support matrix](i1-locality-support-matrix.md) §§10–15; [scoped-evidence v2 contract](i1-scoped-evidence-v2-contract.md); [independent conformance dossier](i1-conformance-dossier.md) and [`i1-vectors/conformance-expected.json`](i1-vectors/conformance-expected.json); [`i1-vectors/utc-day-window.json`](i1-vectors/utc-day-window.json); [`i1-vectors/v2-evidence-id.json`](i1-vectors/v2-evidence-id.json); [controlled-capture acquisition runbook](i1-capture-acquisition-runbook.md); [I1 completion record](i1-completion-record.md).  
**Normative words:** MUST/SHALL/SHALL NOT have their parent-spec meaning. Text explicitly marked **[I2 proposal — review before implementation]** is not yet a frozen decision.

---

## 1. Purpose and exit outcome

I2 implements the first *internally usable* locality-qualified Current-State path. For an accepted HTTP `CALLS`, AIP retains the original CLIENT event's admitted caller Pod/cluster identity before aggregation, writes separately isolated v2 evidence without changing its original v1 contribution, resolves that Pod at query time through the **selected, time-compatible captured-resource revision**, and produces an independently qualified local assertion with provenance and limitations.

The minimum demonstrable result is two distinct Deployment Workloads, `orders` and `orders-canary`, associated with one canonical caller `service:orders`, whose different, individually attributable CLIENT calls resolve to their respective canonical Operations. On the compatible overlap capture, the matching declared `orders → pricing` Operation is `CONFIRMED` and the independently observed undeclared `orders-canary → legacy-pricing` Operation is `OBSERVED_ONLY`. This establishes **caller** locality, not target placement, exclusivity, a universal dependency or local absence.

I2's deliverable is an internal, deterministic assessment/read model and tests. I3 owns bounded public locality enumeration/comparison, public REST/MCP routes and versioned public response schemas. I4 owns final-candidate independent repeatability/surface qualification; I5 owns the actual pinned controlled reference. A successful I2 rehearsal must not be relabelled as I5 capture evidence.

## 2. Scope and non-goals

**In scope:** original CLIENT carrier across in-batch and cross-batch correlation; exact I1 ingestion guards; isolated v2 key, canonical record and deterministic merge; v1/v2 coexistence; bounded operational transition/refusal reporting; selected-snapshot capture and owner reconciliation; a first-class internal `QualifiedLocalEvidenceAssessment`; the one shared declared/observed qualification owner; conditional unified snapshot fingerprint; deterministic and independently authored conformance tests; early controlled-capture rehearsal and I3 handoff.

**Not in scope:** new Kubernetes/OTel source families, live Kubernetes admission or polling, broad region/tenant/version or messaging locality, Workload-level HTTP coverage, historical snapshot reconstruction, public relation-localities APIs, generic graph/Cypher exposure, inferred target runtime placement, local absence or causal flow, Intent/policy/remediation, an LLM-dependent semantic path, or ADR 0012 compaction/retention enactment. Existing dependency/drift/evidence, Pub/Sub and `DEPLOYED_AS` behavior remain v0.5-compatible.

## 3. Authority and frozen versus proposed decisions

| Area | Already frozen by I1 | Exact implementation decision I2 must record |
|---|---|---|
| CLIENT attribution | Admitted original CLIENT Resource allowlist, exact non-empty string normalization, `client_timestamp = CLIENT.end_time`; I-1–I-5 | Carrier and accepted-fact data model, bounded failure diagnostics, transaction boundary |
| Scoped identity | Ten-field v2 key, sorted-key UTF-8 JSON, full SHA-256 ID, identity/rule versions | Persisted label, indexes, model/schema and query ownership |
| Merge | Fact-timestamp min/max, sum, strongest mode, sorted smallest five trace IDs, absorbing consistency conflicts | Storage-level atomic merge and repeatable seed-fold implementation |
| Legacy isolation | Existing v1 ID, contribution/count/sample/qualification unchanged; no v2 ID in legacy `evidence_ids` or `_EVIDENCE_QUERY` | Explicit storage/read separation and migration/replay transaction model |
| Capture | One selected `CAPTURED_RESOURCE`, exact UID and environment/whole-UTC-day predicates; ordered query phases | Persisted/read-side capture representation, resolution and evidence lineage |
| Assessment | One declared/observed owner; positive only from locally applicable v2; no local `NOT_OBSERVED_IN_WINDOW` | Stable assertion vs snapshot-bound assessment-instance identity, internal projection and types |
| Snapshot | No-v2 byte-identical pin; conditional `scoped_observed_calls_v2` sorted by ID; version 3, one fingerprint | Actual graph-to-state query, independently expected full *after* ID |
| Operations | Report vocabulary and reason boundaries; exact original corpus needed for v2 regeneration | Report bounds/retention/accessibility; retry and replay guarantees; positive evidence cost |

The implementation of these decisions requires an I2 review before the corresponding semantic code is enabled. A semantic disagreement is settled through a reviewed contract amendment, not by rewriting the independent dossier to match application output.

## 4. End-to-end data flow and ownership

```text
OTLP/HTTP protobuf receiver -> decoded RuntimeSpan
 -> existing service/Operation resolution and CLIENT/SERVER correlation
 -> original CLIENT's bounded attribution carrier + accepted v0.5 CALLS fact
 -> existing v1 observation path (unchanged)
 -> I1 ingestion I-1..I-5 -> eligible v2 seed OR ingestion-only refusal
 -> separately persisted caller-Pod-scoped v2 record
 -> stable snapshot fence + selected captured Kubernetes source/revision
 -> ordered phase 1..4 locality applicability and Pod/owner reconciliation
 -> matching source/Service-scoped declaration + shared qualification owner
 -> QualifiedLocalEvidenceAssessment + derivation + limitations
 -> I3 internal handoff (I3 later adds public projection/adapters)
```

`app/architecture_intelligence/service.py` remains the sole semantic owner for the eventual public question. I2 may expose a typed internal entry point consumed by that service; it SHALL NOT introduce a second semantic engine in REST, MCP, SQL/Cypher or an agent. The v2 record describes an attributed event contribution. It does not persist a resolved Workload as an immutable event key: locality is snapshot-dependent and must be assessed at query time.

## 5. Original CLIENT carrier and ingress guards

Extend `app/telemetry/correlation_buffer.py`'s bounded `PendingHttpSpan` (default TTL 60 s and maximum 10,000 entries unchanged) and the associated `app/telemetry/adapter.py` fact path so both arrival orders retain the **original admitted CLIENT** environment, cluster UID, Pod UID, optional namespace/Pod/Deployment/StatefulSet/DaemonSet names and converted CLIENT end timestamp. Do not read these from a SERVER Resource, `peer.service`, unrelated `RuntimeIdentityObservation`, Pod name, `DEPLOYED_AS`, or an inferred matching span. The carrier is transient and shall not itself be persisted.

Only after the existing v0.5 CALLS is accepted, evaluate I1 matrix §14 guards I-1–I-5. Use the receiver-converted aware UTC microsecond instant; for paired calls the accepted fact timestamp (and v1/v2 day and v2 first/last seen) comes from the SERVER, while the CLIENT end timestamp is checked for the same UTC day. For `CLIENT_ONLY`, these timestamps coincide. `SERVER_ONLY` never mints v2. A missing CLIENT identity or known ingress mismatch does **not** change accepted v1 behavior, mint a fabricated identity or refuse the original unscoped relation.

The exact allowlist, exact string matching without trimming/normalization, single CLIENT-internal contradiction `CLIENT_MULTIPLE_WORKLOAD_KINDS`, all simultaneous ingress reasons and primary disposition follow support matrix §§10, 14–15.1. Specific ingress-only reasons remain in operational diagnostics/reporting; do not reconstruct them from v1 in an architecture answer. Preserve v0.5's known size-eviction and receiver duplicate-key behavior as disclosed by I1; do not silently change the existing transport contract.

**Required proof:** in-batch paired, CLIENT-first and SERVER-first cross-batch, CLIENT_ONLY expiry, SERVER_ONLY, field absence/type/value, mismatching environments/days, simultaneous guards and UID conflicts; compare v1 output to the baseline for each case. A size-evicted CLIENT must not be retroactively localized.

## 6. v2 storage, canonical key, merging and coexistence

The persisted v2 key is exactly I1 v2 contract §1's ten fields, with `contract_version=2`, `source_type=OPENTELEMETRY`, `evidence_type=OBSERVED`, `relation_type=CALLS`, exact fact environment/day, canonical caller Service/target **Operation** and original CLIENT cluster/Pod UID. Derive `evidence:otel:calls-scoped:v2:<64 lowercase hex>` from sorted-key, compact, UTF-8 JSON (`ensure_ascii=False`) and full SHA-256. Never use RFC 8785 here. Namespace, Workload, names, source display label, trace/span ID, count, timestamps and capture are **not key inputs**.

**[I2 proposal — review before implementation]** Store the record in a distinct, indexed Neo4j node category (provisional label `ScopedObservedCallV2`) keyed uniquely by `id`; give it a dedicated internal read query. It MUST NOT match the legacy `ObservedEvidence` query or any existing evidence-list endpoint and MUST NOT be attached to the original CALLS relation's `evidence_ids`. Do not enable the v2 read/snapshot code until these negative isolation tests pass. The exact final label/query/index is an I2 freeze decision; the label above is not a public contract.

Persist precisely I1 v2 §3 non-identity fields. Merge `first_seen=min(fact timestamps)`, `last_seen=max`, `observation_count=sum`, strongest `correlation_mode`, distinct sorted first five trace IDs; optional consistency attributes use **absorbing conflict**: once two non-null values disagree, leave the field null and permanently list its name in the sorted conflict set. A known field is not erased by a missing value. Three-seed `A,B,A` and `A,A,B`, seven sample IDs, Pod churn and multiple Workload-kind seeds must yield the independently expected result under all tested input permutations. The baseline v0.5 `merge_runtime_identity_observation` remains unchanged.

Use one explicit persistence/transaction boundary for v1 and eligible v2. A v2 write failure MUST NOT leave an independently committed v1 mutation for an interaction that would have written v2 in that unit, unless I2 first documents and independently tests an equivalent recoverable transaction rule. Ineligible v2 is *normal accepted-v1 processing*, not a graph import failure. Storage/index uniqueness must prevent multiple v2 records with the same ID. Idempotence of *an ingestion unit* must not be confused with an unpromised exactly-once live OTLP transport guarantee.

## 7. Retry, migration and operational reporting — decisions to freeze

**[I2 proposal — review before implementation]** Define one ingestion-unit boundary (the resolved accepted CALLS contribution set for one POST/replay line), fold an interaction once within that unit, and run v1/v2 persistence in one atomic transaction. Clean-state replay of the same pinned original per-interaction corpus reproduces v2 IDs and normalized records; permuting seed order does not alter the normalized v2 result. Replaying already-aggregated historical v1 is *not* authorization to generate v2. A second live POST of identical data is not advertised as exactly once: any counted repeat follows the existing disclosed v1 behavior, with the same event represented no more than once *per ingestion unit* in v2. Record this policy explicitly before merging ingress implementation.

Produce `aip-scoped-evidence-transition-report/1` with I1's exact categories: `LEGACY_UNSCOPED` (**v1 buckets**), `SCOPED_V2_WRITTEN` (**interactions**) and `SCOPED_V2_REFUSED` (**interactions**, one primary reason plus complete sorted reason set). Report both category count units, source identity/revision, environment, UTC day and sanitized diagnostic/normalization rule identity; the report is operational, not a Current-State evidence node and not a snapshot input. Historical v1 remains unscoped. **[I2 proposal — review before implementation]** Keep exact aggregate counters, bound individual diagnostic examples and record truncation/overflow explicitly rather than losing a refusal count; expose the report through the existing authorized operational import/ingest result mechanism, not the public evidence resolver.

**Freeze blocker before coding:** specify what source instance and *actual* source revision identify a live OTLP batch versus a SHA-256-pinned offline replay corpus. Do not invent a captured Kubernetes or architecture source revision for telemetry. Freeze report availability, retention, row/sample cap and retry/error semantics in the first implementation slice; changes to ADR 0012 require their own review.

## 8. Snapshot-bound capture, time and owner resolution

An assessment reads the retained v2 candidate and **one selected canonical snapshot**, including its admitted Kubernetes source contribution and actual capture revision. Do not read the newest graph state outside the revision fence or reconstruct C1 after C2 has replaced it. Reuse the admitted v0.5 Path C Pod UID → captured Pod → ReplicaSet/owner → unique Deployment/StatefulSet/DaemonSet rule; it proves caller Workload locality only for compatible captured evidence. Names, annotations, co-location and a Service `DEPLOYED_AS` do not fill missing per-event attribution.

Apply I1's strict gates, stopping at the earliest terminal phase: (1) whole-day request and supported relation/dimensions, (2) admitted selected `CAPTURED_RESOURCE` versus per-candidate `DECLARED_MANIFEST` refusal, (3) exact environment, v2 `last_seen` and real parseable capturedAt under `ScopedDayWindowV1`, then (4) exact cluster/Pod UID, namespace and owner chain and optional consistency. Sort/distinct reasons and use the fixed within-phase precedence; a later owner conflict cannot override an earlier source-mode/time refusal (L36–L37). Capture time is not continuous Pod-presence evidence. An offset-less but non-empty capturedAt can reach the time-limitation path; an absent required envelope field is rejected at import and never becomes a selected capture.

When selected C2 omits P1, retain P1's v2 evidence and return `UNRESOLVED / LOCALITY_CAPTURE_MISSING_POD`; never reassign its call to P2. A rejected incomplete `CAP-PARTIAL` import leaves the prior accepted C1/CAP-A selected; it cannot be queried as a selected capture (L29). Present CLIENT optional-name disagreement with the capture is query-time `CONFLICT` and does not rewrite v2. Distinguish `AMBIGUOUS` from `CONFLICT`, and a cluster UID contradiction from simple missing Pod, exactly as I1 matrix §15.2.

## 9. Internal Qualified Local Evidence Assessment

Implement a typed result at minimum equivalent to the parent §10 semantic unit:

```text
QualifiedLocalEvidenceAssessment:
  assertion_ref: stable scoped assertion identity
  assessment_instance_ref: snapshot-/rule-bound evaluation identity
  subject_service_id: canonical Service
  assertion: CALLS -> canonical Operation
  context: exact environment + ScopedDayWindowV1
  caller_scope: evidenced cluster UID, namespace and unique Workload ref
  target_runtime_scope: UNKNOWN unless separately evidenced (not part of minimum)
  observation: distinct applicable v2 evidence refs and fact time bounds
  declared_evidence: independently applicable Service/Operation source refs, if any
  selected_capture: source instance + revision + evidence mode + real capturedAt
  derivation: v2 CLIENT attribution; selected Pod/owner chain; declaration match;
              normalization, identity and shared qualification rule IDs/versions
  applicability: I1 disposition + sorted reason codes
  qualification: shared-owner result where positive; otherwise no fabricated status
  coverage: local Workload-level coverage unavailable
  limitations: bounded, evidence-qualified and phase-specific
  snapshot_id / model_revision: the same stable canonical snapshot as the read
```

**[I2 proposal — review before implementation]** Use a pure deterministic internal read-side assessment, without a materialized `LOCAL_ASSESSMENT` graph node. Distinguish a stable **assertion ID**, derived by versioned canonical JSON/hash from canonical caller Service, canonical Operation, exact environment/window and resolved captured Workload identity (cluster UID, namespace, supported kind and UID/ref), from an **assessment instance** tied to the assertion ID, selected canonical snapshot, capture revision and applicable rule versions. Keep v2 Pod evidence IDs as lineage, not as the Workload-assertion key, so multiple actual caller Pods of one Workload can contribute without inventing multiple Workloads. Where applicability does not resolve a unique Workload, return a candidate limitation tied to the v2 attribution and snapshot; do not mint a positive Workload-scoped assertion ID. Freeze exact type names, byte encoding, version strings and expected identity vectors in a reviewed I2 slice. Neither ID is a new public I3 wire contract.

An assessment is Current State only, not Intent. A narrative/Intent-only change must not alter it. Read order, group order, reference order and limitation order must be deterministic. Return enough capture/source identity to reconstruct *why this scope* is applicable; do not synthesize an all-localities fact.

## 10. Shared qualification and local coverage boundary

Reuse `app/qualification/declared_observed.py` as the sole semantic owner of `CONFIRMED`/`OBSERVED_ONLY` logic, applied to **the exact eligible scoped Operation call** and its separately source/Service-scoped declaration. Do not implement a parallel truth table in a new service/read query, and do not pool declared evidence for Operation O1 with observed evidence for O2. With eligible v2 observation and exact applicable declaration: `CONFIRMED`. With eligible v2 and no applicable declaration: `OBSERVED_ONLY`. A declared-only v1/Service relation or unrelated Pod observation mints **no positive local CALLS**.

No admitted minimum input proves Workload-level HTTP coverage. Consequently local `NOT_OBSERVED_IN_WINDOW` is **unreachable** and SHALL NOT be emitted. Where there is no retained eligible v2, answer `INSUFFICIENT_EVIDENCE` using `LOCALITY_NO_ELIGIBLE_LOCAL_OBSERVATION` and `LOCALITY_LOCAL_COVERAGE_UNAVAILABLE`; include `LOCALITY_LEGACY_V1_UNSCOPED` only if legacy-only status is independently established. Never leak an ingestion-only reason into the query, treat an unsupported/unresolved candidate as absence, or change unscoped v0.5 coverage and qualification.

## 11. Conditional canonical snapshot and read consistency

Use `app/architecture_intelligence/repository.py`'s one canonical state/fingerprint mechanism. With **zero** v2 records, preserve `_CANONICALIZATION_VERSION = 3`, identical state bytes, `model_revision`, all v0.5.1 pins and the golden demo snapshot `aip:snapshot:v1:0bfcbdeda363876559bb78f53e432f1a73c368e9fbd4d21c37f8f4335ecdbd5f`. The key `scoped_observed_calls_v2` must be **absent**, not `[]` or `null`. No v2 schema or rules may accidentally perturb the no-v2 semantic-config projection.

With v2 records, add only I1 contract §8's conditionally present state key, ordered by v2 ID, with exactly the frozen fields and `YYYY-MM-DDTHH:MM:SS.ffffffZ` timestamps; keep canonicalization version 3. Hash this *one* state. Do not add a second locality fingerprint or let v2 records appear in the legacy `evidence` array. Snapshot and assessment reads use the existing stability fence; a changed selected capture/owner state changes lineage and unified snapshot even if retained v2 IDs have not changed. I3's later scoped drill-down must resolve against that same snapshot and refuse a mismatched/stale ref rather than silently switch to latest.

**Pre-enablement gates:** (a) independently prove byte-exact no-v2 golden pin against the baseline; (b) produce and freeze an **independently expected full-graph after-`snapshot_id` vector**, not only I1's already-frozen two-record fragment; (c) prove an actual v2-positive current graph yields that value and (d) confirm no v2 ID leaks via any existing v0.5 relation, evidence, dependency or drift read. If an old pin cannot be preserved, stop for the parent-required compatibility amendment; never update a fixture to match an unexpected output.

## 12. Early controlled-capture harness rehearsal

Build the runbook §3 harness (real OTel SDK HTTP client/server instrumentation, two distinct `orders` Deployments sharing one canonical caller Service, `pricing` and `legacy-pricing` providers). Use the Downward API for actual Pod UID and a pinned `kube-system` namespace UID both as CLIENT cluster UID and captured envelope `clusterUid`; no collector-side `k8s.*` enrichment and no synthesized CLIENT spans. Capture C1 with both Pods and C2 after P1 removal, each with real timestamp, source revision and pinned files. Respect stop conditions and non-atomicity disclosure.

Rehearse the runbook's exact offline JSONL → replay Collector HTTP JSON → protobuf exporter → AIP `/v1/traces` path with pinned config, no replay processors/queue/retries. Assert AIP accepts every forwarded protobuf request, one line corresponds to one request, decoded Resource fields remain byte-equal, the source envelopes/digests validate, owner chains resolve uniquely, and both cross-batch arrival orders retain CLIENT identity. Evaluate C1 before selecting C2. Record the rehearsal separately and label it `rehearsal`, **not** the independently recorded I5 qualification fixture. I2's failure to pass any runbook §9 gate blocks I2 exit and I5 acquisition.

## 13. Independent conformance and compatibility evidence

Use the independently authored I1 `conformance-expected.json` (L01–L37, including L17e/L29a–b) as a **read-only oracle**, together with UTC-day (W/M/D/T), v2 key/merge (V/U/MP) and snapshot vectors. For each applicable variant, construct a concrete ingestion/source/capture/assessment test, assert the exact phase, disposition, sorted reasons, identity/ref and prohibited conclusion. Turn abstract Path C `CAP-AMB` and `CAP-CONF` into actual admissible fixture graphs and preserve the distinction between them. Test the L29 invalid-envelope import through the existing validator, not as a fictional selected capture.

Additional integration gates:

| Area | Required evidence |
|---|---|
| Attribution | Same-batch; both cross-batch orders; CLIENT_ONLY and SERVER_ONLY; no name/co-location/DEPLOYED_AS substitution; wrong/absent UID/env/day; retained ingress-only causes |
| Storage | Exact v2 IDs, distinct cluster/Pod/day/Operation; isolated label/read path; single-counted v1 and one seed/interaction; transaction failures; migration reporting |
| Replay | Clean-state corpus replay; all specified v2 permutation/merge vectors; fixed-order repeated clean runs; disclosed live duplicate-POST behavior; source revision and report scope |
| Applicability | All four phases and precedence, capture mode/time, owner ambiguity/conflict, namespace contradiction, Pod churn; rejected-source non-selectability |
| Qualification | O1 `CONFIRMED` vs O2 `OBSERVED_ONLY`; declaration provenance; no cross-Operation pooling; no local negative/coverage promotion |
| Snapshot | No-v2 exact pin, independently expected full after pin, canonical sorting, one revision-fenced snapshot, changed C1/C2 lineage, v2 absent from legacy evidence reads |
| Compatibility | Existing dependency/drift/evidence/Pub/Sub/DEPLOYED_AS semantic and contract regression; full quality, type, imports, security and integration gates |
| Capture | Runbook §9 rehearsal and provenance log; actual I5 capture remains `NOT_RUN` |

Do not assert arbitrary permutation invariance of **legacy v1 sample ordering**: I1 expressly preserves v0.5 first-arrival samples. Prove v2 normalized order independence separately and clean-run byte equality for a **fixed replay order**. I4 will repeat final-candidate qualification, not infer success from I2's development tests.

## 14. Safety, observability and cost

Store only I1-admitted bounded CLIENT metadata, source/rule provenance and at most five trace samples per v2 record; no raw spans, complete OTel Resources, credentials, inferred host/IP identity or arbitrary `k8s.*`. Diagnostics must be sanitized and bounded and never become architecture evidence. Emit operational counts for v1-only versus eligible/refused v2, resolution success/`UNRESOLVED`, cardinality by environment/day/Pod churn, graph size, fingerprint time, read latency, and report overhead. A stress case with many Pod replacements at fixed Workload count must measure these against a no-v2 baseline. Record observed values in the completion record; this draft invents no performance thresholds or successful measurements. Retention/compaction behavior remains unchanged absent a separately accepted ADR.

## 15. I2 slices and exit evidence

| Slice | Bounded delivery | Required exit artifact |
|---|---|---|
| **I2.1 — Decisions and carrier** | Freeze storage, identity/assessment model, transaction/report and replay policy; implement CLIENT carrier and I-1–I-5 without v1 regression | Reviewed decision table, ingress guard tests, both cross-batch arrival orders |
| **I2.2 — Isolated v2 persistence** | v2 canonical ID, seed/merge, isolated storage/index, transaction and transition report | V/U/MP vectors, v1/no-leak regression, deterministic replay and bounded report |
| **I2.3 — Selected-capture applicability** | One snapshot-fenced capture selection, UTC-day phases, owner/UID reconciliation, Pod churn and limitation mapping | Concrete L15–L20/L27/L29/L31/L34–L37 tests, including Path C ambiguous/conflict cases |
| **I2.4 — Qualified assessment** | Stable scoped assertion/assessment identity, applicable declaration via shared qualification owner, typed lineage and limitations | Independent O1/O2 positive tests, declared-only and local-coverage negative tests, same-scope isolation |
| **I2.5 — One snapshot and compatibility** | Conditional v2 canonical-state input; no-v2 and full v2 after ID pins; legacy surface isolation and transaction/replay qualification | Independent full after vector, exact golden-path pin, regression results |
| **I2.6 — Harness, qualification and handoff** | Build/run early rehearsal, complete 65-variant I1 dossier mapping, measure Pod-churn cost, document internal read contract for I3 | Pinned rehearsal log, test matrix, measured bounds, I2 completion record, explicit I3 handoff |

A slice MAY be split or regrouped without moving acceptance criteria. In particular, the capture rehearsal must occur early enough to discover missing CLIENT Resource or replay-format behavior before I5; it cannot be treated as optional polish at the end. Keep PRs focused and record review-driven decisions against the frozen spec.

## 16. Definition of Done, completion record and I3 handoff

I2 is complete only when all of the following are independently supported, not just stated:

1. Original CLIENT identity survives accepted same- and cross-batch CALLS and its ingress guards; v1 semantics do not change when v2 is refused.
2. Every eligible interaction produces the exact isolated v2 ID and order-independent normalized record, with no v2 contamination/double-counting on existing v0.5 surfaces.
3. Retry/replay, transactions, transition-report source identity/revision/bounds/retention and legacy migration have reviewed semantics and executable tests; no unearned exactly-once or historical backfill claim.
4. Against one pinned selected snapshot, I2 resolves applicable caller Pod/cluster to supported Workload through real capture/time/owner proof, with all four query phase gates and C1/C2 churn limitations.
5. Two eligible Workload localities coexist for one canonical caller Service and yield the independently expected Operation-granular `CONFIRMED` and `OBSERVED_ONLY` assessments through the existing qualification owner; no local `NOT_OBSERVED_IN_WINDOW`.
6. The typed first-class assessment has a reviewed stable assertion/instance identity, source/CLIENT/capture/qualification derivation and Current-State-only scope; no materialized assessment is required.
7. Without v2, canonicalization version/state/fingerprint and the published golden path are byte-identical; with v2, a *new independently authored full-graph after pin* proves the conditional single snapshot and stable reads.
8. All I1 L01–L37 variants and vectors have executable implementation-test coverage (the abstract and import-rejected fixtures are made reachable), and v0.5 regression/quality gates pass. State counts, exact HEAD and failed/skipped status; never call an unrun check passed.
9. The two-Workload harness passes the runbook §9 rehearsal and is labelled as such, with digest/provenance/run record; the real I5 capture is not claimed.
10. The completion record reconciles the accepted plan, decisions, deviations, unresolved questions, deferred work, benchmark/cardinality measurements, source versions, test commands and exact merged PR SHAs. Any missing requirement is an explicit blocker or independently approved amendment, never silent deferral.

**Handoff to I3:** provide a pure internal request/result API under the one Architecture Intelligence semantic owner that can enumerate candidate v2/capture-derived localities (I3 sets bounds/continuation), evaluate an optionally selected scope and compare only within one snapshot; supply exact assessment ID/lineage, per-Operation qualification, unqualified candidate/limitation semantics, selected-source/coverage diagnostics and stable evidence lookup hooks. I3 freezes the public Service dependency roll-up, same-snapshot evidence drill-down, REST/negotiated MCP schema/version and final route/tool count. I2's internal interface does not license a public endpoint or a second evidence-resolving hash.

## 17. Items requiring explicit owner review before implementation

The accepted parent and I1 texts do **not** resolve the following I2-level details; their proposed choices above must be reviewed and frozen before corresponding work:

1. Exact persisted v2 graph label/index/read queries, atomic transaction and import/remove scope interaction.
2. Stable scoped assertion ID versus snapshot-bound assessment-instance ID, canonical bytes, version and the negative-candidate identity policy; read-side-only versus materialized assessment.
3. Exact live OTLP ingestion-unit/retry/replay semantics, and whether any transport-dedup change would violate v1 compatibility.
4. A truthful source instance and source revision for live OTLP reporting versus pinned offline replay; report schema, count unit, cap, retention and authorized surface.
5. Independently authored full-graph positive snapshot fixture and assertion ID vectors; no-v2 pin is not negotiable by ordinary fixture updates.
6. Internal I2-to-I3 read/lineage contract and required snapshot fence; I3 remains responsible for public shapes and bounded enumeration.
7. Rehearsal harness image/tool digests and capture provenance; no substitution of synthetic spans for actual CLIENT emission.

**Stop condition:** if any apparently convenient implementation needs to infer an event's Pod from an unrelated observation, change v1 semantics, bypass phase ordering, use a rejected capture, fabricate a Workload-level absence/coverage claim, invent a second snapshot fingerprint, or relax accepted I1 evidence rules, stop and seek a reviewed specification/parent amendment rather than making the independent expectations self-confirming.