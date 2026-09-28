# AIP v0.6.0 Release Specification — Locality-Aware Current State

**Status:** Draft 0.1 — proposed release contract; decisions in §33 require review before increment implementation  
**Target release:** `v0.6.0`  
**Release theme:** Locality-Aware Current State  
**Entry baseline:** Published and post-release-verified `v0.5.1` (`5719738091baa701d9867726fc89c93fa80bea46`); v0.5.0 provides the underlying discovery and qualification semantics  
**Primary outcome:** AIP can establish which supported architectural relationships hold in explicitly evidenced localities and observation contexts, and deterministically project and compare these local assessments without turning local knowledge into a universal architecture claim.  
**Governing inputs:** [Product Doctrine and Strategic Direction](../../product-doctrine-and-strategic-direction.md), [ROADMAP.md](../../../ROADMAP.md), [v0.5.0 parent specification](../0.5.0/specification.md), [v0.5.1 specification](../0.5.1/specification.md).  
**Source revisions consulted for this draft:** ROADMAP `5082ec45`; Product Doctrine `9c03d53e`; v0.5.0 specification `b4c0163e`; v0.5.1 specification `815fcf0a`. These are source-input identities, not an implementation baseline or release candidate.

---

## 1. Release Promise

`v0.5.0` established broader declared, infrastructure, and observed architecture and bounded Service–Workload identity reconciliation. `v0.5.1` demonstrated the released capabilities through the Quarkus Super Heroes developer workflow without adding semantics. Neither release establishes locality-qualified dependencies or a deterministic projection of local assessments into a broader Current-State view.

`v0.6.0` SHALL make a materially new class of architecture question safely answerable:

> **Where is this dependency established?**  
> **Does this relation differ by supported locality?**

The release SHALL prove:

> **Given a stable Current-State snapshot, applicable evidence, and an explicit observation/locality scope, AIP establishes bounded qualified local evidence assessments and deterministically projects them into a Current-State answer which identifies the included and excluded localities, evidence lineage, qualification, coverage, and limits. An agent can inspect where a relationship is supported without inferring that it holds, or fails to hold, anywhere else.**

The governing semantic path is:

```text
Current-State Evidence
       +
Explicit, evidence-supported locality / observation context
       ↓
Applicable Evidence + Identity Reconciliation
       ↓
Qualified Local Evidence Assessments
       ↓
Deterministic, bounded Current-State Projection
       ↓
Evidence-Qualified Current State
```

The non-negotiable invariants are:

```text
local assessment != universal/global fact
locality != connectivity; WHERE != HOW
co-location != interaction
not observed here != does not happen here
unknown locality != every locality
Service != Kubernetes Service != Workload != Pod
Service version != Service identity
source/capture location != automatically the subject's runtime location
deployment association != location of every runtime call
path through qualified edges != qualified causal end-to-end flow
observed / declared Current State != explicit Architecture Intent
consumer projection != new source of Architecture Knowledge
```

AIP remains advisory and read-only on its public Architecture Intelligence surface. Agents, LLMs, demos, and external context tools never establish or strengthen canonical architectural truth.

## 2. Normative Language

**MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. An example, conceptual type, suggested endpoint, or illustrative field name is not a frozen public wire contract unless explicitly stated as such. The detailed increment specification and versioned schema SHALL freeze concrete names before implementation/fixture authorship; they may not weaken the parent semantics by selecting convenient defaults.

Independent expected results, not output copied from AIP or an agent interpretation, constitute qualification evidence. Tests of implementation alone do not settle ambiguous semantics.

## 3. Entry Conditions and Preserved Baseline

The final candidate SHALL derive from the published `v0.5.1` baseline and retain its supported v0.5.0 Architecture Knowledge semantics:

- one Canonical Model mapping target; source adapters do not write directly to persistence;
- deterministic source inventory, revision, authoritative-removal, atomic import, and replay rules;
- distinct declared, observed, and infrastructure-derived evidence modes;
- bounded identity guards and conflicts, including the established `DEPLOYED_AS` contract;
- one declared-vs-observed qualification owner; non-observation and coverage retain their existing meanings;
- snapshot/revision fencing, evidence resolution, sanitized provenance, deterministic answers, and explicit limitations;
- `ArchitectureIntelligenceService` as the sole semantic owner for public Architecture Knowledge;
- REST and standard negotiated MCP as the supported public adapters, with transport-independent evaluation against the service;
- existing dependency/drift/evidence and Pub/Sub semantics; neither Queue/Topic/Subscription nor Service/Workload distinctions may collapse;
- read-only public Architecture Intelligence and a deterministic, no-LLM-required execution path;
- the released Quarkus demonstration and minimal demonstration remain valid; existing unscoped queries keep their documented v0.5 meanings unless a versioned, reviewed compatibility decision explicitly changes them.

**Important baseline limitation.** A v0.5.1 Service-level `DEPLOYED_AS` resolution is not enough by itself to attribute an individual observed HTTP or messaging interaction to that Workload. The Quarkus demo's frozen 7-second replay and disclosed operator-authored messaging overlay must not be presented as independently establishing two runtime localities, observed Kafka behavior, or a complete application topology. v0.6 qualification needs its own independently authored locality cases.

## 4. Fixed Scope Budget

### 4.1 In scope

`v0.6.0` SHALL deliver:

1. An explicit **locality/context applicability contract** for Current-State evidence, with minimum supported dimensions and refusal rules (§§6–8).
2. A first-class internal **Qualified Local Evidence Assessment** semantic unit, independent of Intent (§§9–12).
3. One bounded, deterministic **Current-State projection** over applicable local assessments, with explicit included/excluded/unknown scope, coverage, qualification, and limitations (§§13–16).
4. A **question-specific locality answer**, suitable for asking where an existing supported relationship holds and comparing evidenced results in selected localities (§§17–19).
5. REST and negotiated-MCP exposure through the single Architecture Intelligence semantic owner, versioned contracts, and same-snapshot evidence drill-down (§§20–23).
6. Independent deterministic positive/negative qualification, v0.5 regression, two real-system boundary checks, a realistic developer walkthrough, and an explicit product-value/pilot disposition (§§20–25).
7. Exact-candidate release qualification, owner-authorized publication if granted, and post-publication artifact verification (§§26–28).

The minimum positive question slice SHALL demonstrate one application dependency relation (`CALLS`) scoped to the **observed caller's independently evidenced runtime locality** and differentiated across two eligible localities. It SHALL also preserve existing `DEPLOYED_AS` placement evidence as placement, not as inferred interaction. Other existing relation kinds may gain locality-aware claims **only** after their evidence, scope and qualification rules are separately specified and tested. They must otherwise remain answerable under their existing v0.5 semantics with their locality-specific limitation explicit.

The minimum locality dimensions SHALL include the existing explicit **environment and observation window** and, for a positive differentiated case, **evidenced cluster identity and namespace/workload scope** through the admitted v0.5 Kubernetes/OTel identity chain. Region, tenant, service version, and other dimensions are candidates only when the selected source/mapping rules actually establish them; they are not universal filters supplied by convention.

### 4.2 Explicitly out of scope

```text
new discovery-source family or live Kubernetes admission
new general-purpose graph/Cypher access or arbitrary graph-neighbourhood API
service-mesh or network-topology discovery
service-to-service communication inferred from Kubernetes placement
causal end-to-end runtime flow or inferred system-level business outcome
fully closed-world absence claims or global dependency completeness
health, readiness, availability or SLO conclusions
explicit Architecture Intent / promises / authority evaluation (v0.7)
Current ↔ Intent assessment or policy/compliance judgment (v0.8)
historical snapshot retention and architecture trajectories
sidecar, DaemonSet, OTel extension or distributed Local Architecture Assessor
migration planning, architecture mutation, approval workflows or remediation
LLM/agent-derived locality, evidence, identity, or qualification
SSTorytime, GT, A2A, GraphRAG or a new agent orchestration framework in the core
```

v0.6 adds a semantic locality capability, not a new placement source or deployment architecture. A future distributed local assessor remains a post-v1.0 hypothesis. New source families such as gRPC/protobuf or Kafka Connect require separate authorization and do not enter v0.6 through the existing adapter seam.

## 5. Increment Contract and Dependency Order

| Increment | Title | Required outcome |
|---|---|---|
| I1 | Locality and Evidence Applicability Contract | Supported scope vocabulary, evidence attribution and refusal semantics are frozen and executable. |
| I2 | Qualified Local Evidence Assessment | AIP independently establishes local Current-State assertions without duplicating or weakening v0.5 qualification. |
| I3 | Bounded Current-State Projection and Public Answers | Users/agents ask the new question deterministically through service, REST and negotiated MCP, with same-snapshot evidence drill-down. |
| I4 | Deterministic Semantic Qualification | Independent positive/negative locality truth tables, cross-context reconciliation, compatibility and repeatability qualify the increment capabilities. |
| I5 | Real-System Qualification and Product Demonstration | Quarkus/Airflow baseline preservation; externally authored locality evidence where real upstream lacks it; useful task-oriented demonstration and bounded pilot disposition. |
| I6 | Release Candidate, Publication and Verification | One exact candidate reaches a recorded `RELEASE_READY_NOT_PUBLISHED` or verified published outcome. |

```text
I1 → I2 → I3 → I4 → I5 → I6
```

I1–I3 MAY be sliced internally, but positive acceptance must be end-to-end and public-question oriented, not merely schema or storage completion. A material semantic ambiguity SHALL stop the affected implementation until resolved by reviewed specification amendment. The parent specification controls the release scope; increment specs may narrow it or freeze deferred details, not silently expand it.

---

# Part I — Locality and Evidence Applicability

## 6. Locality as Supported Applicability, Not a Universal Coordinate

A *locality* is an explicit, bounded scope under which a Current-State assertion may be established. It need not equal one Service, Workload, team, namespace, or graph node; an assessment may span several components where one evidence/rule combination supports that scope. The locality of an **observer/caller**, a **target**, a **source artifact**, and a **claim** are different propositions and SHALL not be silently substituted.

The I1 contract SHALL distinguish:

```text
requested scope             what the caller asked about
source/capture scope        what the source is known to cover
subject runtime scope       where the subject/event is evidenced
claim applicability scope   where that precise assertion is supported
projection selection scope  which supported assessments were included
```

Each scope dimension SHALL be supported by a named admissible evidence/mapping path and a rule version. An omitted, unavailable, contradictory, stale, or unsupported dimension is **unknown/unresolved/unsupported as appropriate**, never wildcard `*`, never inferred from a similar display name, and never a reason to expand the claim to all localities. Exact wire vocabulary for these cases is an I1 freeze decision; their distinct meanings are mandatory now.

### 6.1 Admitted minimum scope

- `environment` and explicit `observation_window`: reuse the existing runtime observation contract and inclusive window-applicability rule where applicable; preserve actual source timestamps and capture identity.
- `cluster identity`: a configured and/or captured identity accepted by the existing source/identity rules; a human-friendly cluster name is not a surrogate for a UID.
- `namespace` and `workload`: only through the resolved, current Kubernetes resource identity and admitted Service/Pod/owner-chain evidence; workload kinds and bounded references remain those already admitted in v0.5.
- `service.version`: optional discriminant only if the specific runtime or declared evidence establishes it and compatible identity/rule logic is defined. A version is not a distinct AIP Service by default.
- Other dimensions (region/tenant etc.): explicit `UNSUPPORTED` or `UNRESOLVED` for a request unless I1 records a supported source, mapping, applicability rule and negative tests. A namespace is not a region or tenant.

The parent SHALL fix the minimum semantic capability; I1 SHALL freeze the actual context type, dimension keys, supported combinations and versioned schema before independent fixtures are written.

## 7. Evidence Attribution and Temporal Compatibility

A positive local claim requires **directly attributable applicable evidence**, not simply a successful relationship query plus a separate Service placement. For the minimum local HTTP `CALLS` case, the observed caller's OTel Resource and the v0.5 Pod-UID → Pod → owner-chain/Workload linkage (including compatible environment/time/captured resource identity) SHALL justify the claimed caller locality. A configured or explicit Service–Workload binding by itself does not assign an individual HTTP event to that Workload. Target locality SHALL be left unknown unless separately evidenced; a caller in namespace A can call a target in namespace B.

The assessment SHALL preserve:

```text
source instance / artifact revision / capture identity
source evidence mode (DECLARED / OBSERVED / INFRASTRUCTURE_DERIVED, etc.)
applicable raw or normalized evidence references (bounded and sanitized)
identity reconciliation and mapping path / rule version
observation environment and window; actual relevant timestamps
supported locality dimensions and any unsupported/missing dimensions
qualification and limitations
```

An offline Kubernetes manifest is declared infrastructure input, not proof that a live resource currently exists. A captured resource is evidence of the capture, not a timeless claim about cluster state. A source-level service declaration SHALL NOT be silently made region-specific merely because a Service has a Workload in a region. Partial or incompatible time context cannot be repaired by nearest-window matching. `NOT_OBSERVED_IN_WINDOW` retains v0.5 coverage semantics and never means verified local absence.

## 8. Source Scope, Identity, and Conflict Rules

I1 SHALL freeze an evidence applicability table per admitted claim kind and dimension before implementation, including at least:

| Evidence or existing fact | What v0.6 may support | What it cannot support alone |
|---|---|---|
| OpenAPI declaration | Service/operation declaration under the source's evidenced scope | Operation observed in a particular runtime Workload |
| OTel HTTP CLIENT observation with resolved Service and admissible scope | Observed direct `CALLS` in that caller's supported runtime scope | Target co-location, causal multi-hop path or source-independent global dependency |
| Kubernetes Workload/Pod capture and owner chain | Captured infrastructure identity and bounded placement scope | An application `CALLS`, `SENDS`, or `PUBLISHES_TO` relationship |
| Existing `DEPLOYED_AS` resolution | Supported Service–Workload association with its exact evidence mode | Attribution of all Service interactions to that Workload |
| Configured mapping | The exact mapped identity association and its versioned provenance | Runtime behavior or live placement beyond the source's own evidence |
| Operator-authored AsyncAPI overlay | Attributable declaration evidence for the admitted messaging claim | Independent upstream or runtime confirmation, or implied Subscription identity |

Where evidence for two scopes differs, assess them separately. A discrepancy in compatible identity/evidence within one scope must be reconciled or reported as conflict; it must not be hidden through specificity ranking, “latest wins”, a global source-trust order, or merging unlike localities. A broader view may describe both different established local states without calling them a contradiction.

A missing scoped source, ambiguous Pod owner, unsupported runtime semantic convention, name-only Workload match, or unproven intersection of contexts SHALL not mint a positive locality-qualified dependency claim. Existing import/inventory authority is preserved; absence from an incomplete discovery scope cannot authorize removal or produce a negative locality conclusion.

## 9. I1 Exit Gates

I1 is complete when:

1. an exact, versioned scope/applicability contract states which locality dimensions, evidence paths and combinations are admitted;
2. positive and negative examples discriminate observer/caller, target, source/capture and claim applicability;
3. scope extraction never broadens a v0.5 refusal or changes a Service identity by name;
4. missing, conflicting, unsupported and temporally incompatible locality evidence have deterministic machine-visible dispositions;
5. the distinction between observation window and future Intent effective interval is explicit in types and documentation;
6. its independently authored examples include a runtime-identity attribution case and a name/co-location-only rejection.

---

# Part II — Qualified Local Evidence Assessment

## 10. Internal Assessment Contract

I2 SHALL implement a first-class semantic unit equivalent to the Product Doctrine's **Qualified Local Evidence Assessment**, independent of storage topology:

```text
QualifiedLocalEvidenceAssessment(
  subject,
  assertion,
  context / supported locality scope,
  observation_window,
  applicable_current_state_evidence,
  source / mapping / identity / qualification rule versions,
  qualification,
  provenance / derivation lineage,
  limitations
)
```

The implementation MAY be a deterministic read-side projection over existing persisted evidence. No new materialized Neo4j label or stored `LOCAL_ASSESSMENT` edge is mandated. Such a choice needs an explicit ownership, expiry, replay, and snapshot decision, not a convenience write.

**No `applicable_intent`, policy result, or migration decision belongs in this unit.** Changing future Intent artifacts while Current-State evidence/context/identity/rules are held fixed SHALL not change the resulting Current State.

An assessment's stable semantic identity SHALL be based on its qualified assertion and evidenced scope using a frozen canonicalization version. Evidence revision, source capture, rule versions, observation window and resulting qualification SHALL be recoverable through its snapshot/assessment lineage. The exact identity relationship (stable assertion ID versus versioned assessment instance) is an I2 freeze decision; it SHALL never let an unchanged display label disguise changed scope or qualification.

## 11. Reuse of v0.5 Qualification and Uncertainty

I2 MUST reuse the existing semantic owner for declared-versus-observed status and coverage. It SHALL NOT implement a parallel `CONFIRMED`/`OBSERVED_ONLY`/`NOT_OBSERVED_IN_WINDOW` formula for local claims. Qualification is computed over **applicable evidence in the requested scope**; evidence from another locality must not improve or downgrade the local qualification through a global union.

Examples to qualify independently:

```text
Locality A: observed caller A CALLS B
Locality B: observed caller A CALLS C

Supported: A→B is established in A; A→C is established in B.
Not supported: A→B is absent in B; A→C is absent in A.
```

Source-derived declaration evidence whose applicability cannot be localized remains a source-scoped declaration, not a manufactured declared-in-every-locality claim. `NOT_OBSERVED_IN_WINDOW` SHALL be accompanied by correct scope-specific coverage and exclusion limits. A locally unsupported/unresolved evidence path must stay visible even if another scope is fully supported.

## 12. I2 Exit Gates

I2 is complete when one pinned-snapshot input yields reproducible local assessments for two evidenced localities, with a complete lineage to source, identity/mapping, observation and qualification rules. Same-locality disagreements remain visible; different supported localities can coexist. Repeating, reordering, reimporting, and source removal follow the pre-existing deterministic lifecycle guarantees. Changing only one locality's applicable evidence cannot silently change another locality's result, other than by an explicitly justified shared identity/rule/snapshot dependency recorded in lineage.

---

# Part III — Deterministic Current-State Projection and Public Answers

## 13. Projection Contract and Completeness

A Current-State projection SHALL be a deterministic selection/reconciliation of applicable **Qualified Local Evidence Assessments** for one explicit snapshot and bounded requested scope. It SHALL preserve:

```text
requested and actually evidenced scopes
included local assessments and their identities
known excluded / incompatible scopes and reasons
unresolved/unsupported inputs and missing dimensions
qualification of every returned architectural claim
source/evidence/provenance and rule lineage
observation context / window
projection completeness and truncation/selection limits
```

“Complete” MUST be defined relative to a specified **evaluated input inventory and requested selection**, not interpreted as proof that the system has no unknown services, dependencies, other localities or unobserved traffic. A scope filter returning no supported claims is not a verified negative architecture assertion.

Projection SHALL NOT strengthen a claim merely by combining it with other locally supported claims. New cross-boundary or system-level architectural claims require their own applicable evidence, temporal/identity compatibility and qualification rule. In particular:

```text
A CALLS B in scope X + B CALLS C in scope Y
    != established causal A→B→C flow in any scope

A and B DEPLOYED_AS Workloads in namespace N
    != A CALLS B
```

## 14. Context Selection and Differentiated-Locality Answer

I3 SHALL provide a **bounded deterministic answer to the new product question**, without requiring an LLM to compare loosely related snapshots. The caller selects a subject and an explicit finite set of supported localities, a common observation window and optional exact relation/target filters. Every selected result is evaluated against the **same frozen snapshot/revision fence**. A bounded discovery of candidate localities MAY be provided only where supported by source inventory and SHALL carry enumeration coverage; unenumerated localities remain outside scope.

The answer SHALL distinguish:

- **established in selected locality**: positive supported claim in the stated scope;
- **not established from applicable evidence**: no positive claim, with qualification and coverage/limitations; not an asserted absence;
- **unknown/unsupported/conflicting locality**: no manufactured result for that scope;
- **differing supported claims**: a comparison of separately established scoped assertions, not an inferred contradiction or assurance of completeness.

The comparison is a deterministic **difference between the supported answers for selected localities**; it is not an assessment against Architecture Intent. Missing or insufficient evidence in one selected locality cannot be reported as a negative contrast to positive evidence in another.

### 14.1 Minimum illustrative fixture

An independently authored source fixture may establish the same declared Service `service:orders` running through two distinct Pod-UID/owner-chain-linked Workload scopes and two admissible OTel client observations:

```text
cluster K1 / namespace n1 / caller workload W1:
  orders CALLS pricing
  -> evidence-qualified, observed in window T

cluster K2 / namespace n2 / caller workload W2:
  orders CALLS legacy-pricing
  -> evidence-qualified, observed in same window T
```

Its output must report both supported relationships at their exact caller localities and state that no absence or exclusivity has been proved in either locality. The fixture MUST NOT use name matching, merely configured Service-level `DEPLOYED_AS`, or synthetic telemetry represented as independent upstream runtime capture. Fixture authorship, semantics and provenance are disclosed.

## 15. Snapshot, Derivation and Stability

All results SHALL be bound to one stable snapshot and deterministic rule/configuration identity, including locality extraction, source capture/revision, accepted identity mappings, qualification and projection versions. Claim/evidence identifiers SHALL be stable under input permutation and idempotent reimport and distinguish genuinely different scoped assertions. A change in applicable source capture, mapping, rule or locality that affects the answer must be reflected in its lineage and snapshot/assessment identity, not silently treated as an unchanged answer.

An evidence request for a claim SHALL resolve under the **same snapshot**; mismatched or unavailable historical dependencies receive the existing explicit refusal/limitation behavior. This release does not introduce historical snapshot retrieval or trajectory storage. Stale-snapshot retry and revision-fence limits follow the existing service contract; neither transport may silently substitute the newest snapshot.

## 16. Existing Dependency, Drift and Deployment Behavior

Existing unscoped dependency/drift/deployment requests keep their v0.5 meaning, including published qualification statuses and existing `DEPLOYED_AS` resolution methods. I3 SHALL not silently relabel a globally requested service-level claim as local, reinterpret deployment as an application dependency, or turn the existing drift endpoint into future Intent-vs-Current assessment. Where new scoped request parameters are admitted, their absence SHALL preserve existing behavior unless a reviewed versioned compatibility change is required and documented.

`DEPLOYED_AS` remains a Service–Workload identity relation; a locality-aware answer MAY cite it as a contributing identity fact, but it SHALL not treat all dependency claims of the Service as workload-specific on that basis alone. Messaging claims stay under their v0.5 source/identity guards and are only locality-qualified if separately admitted by the I1 applicability matrix.

## 17. Public Question-Specific Exposure Proposal

The release requires a bounded, service-owned, deterministic, publicly usable relation-locality projection, not an arbitrary traversal API. **Draft proposal for I3 review:**

```text
ArchitectureIntelligenceService.get_relation_localities(request)
  REST: /api/services/{id}/relation-localities  [illustrative route]
  MCP:  get_relation_localities                 [proposed fourth read-only tool]
```

The proposed tool expresses a materially new architecture question directly rather than forcing the agent to stitch separate dependency answers into a conclusion. It SHALL not become a generic `get_graph`, free-form query, spatial join, or agent-orchestration capability. If I3 can demonstrate the identical bounded question and comparison safely through a compatible extension of the existing three tools, a reviewed parent amendment may retain three instead. **The final tool count, exact route, request and response shapes are open decisions in §33, not presumed implementation facts.** The positive exit contract is not optional: one deterministic relation-locality answer must be available through both public adapters.

Minimum semantic request fields, to be frozen in versioned schemas:

```text
subject: full canonical Service identity
observation context: explicit environment / compatible bounded window
locality selection: finite, exact, validated scopes
relation/target selection: supported bounded filters only
```

Minimum answer semantics:

```text
ArchitectureAnswer: producer / schema / snapshot / outcome / limitations
selected scope and per-scope evaluation status
qualified local claim refs and assessment/claim identity
where each relation is positively established
differing supported results, without implicit negative comparison
coverage/completeness/selection and truncation metadata
source, mapping, qualification and projection lineage
same-snapshot evidence refs
```

The actual supported request/response schema MUST NOT expose a dimension the I1 evidence contract cannot interpret.

## 18. Public Schema and Adapter Parity

I3 SHALL freeze an exposure table **before implementation** mapping each new semantic field/variant to canonical representation (or internal read-model), `ArchitectureIntelligenceService`, REST, negotiated MCP, published JSON Schemas, and evidence resolution. A released public enum/contract change must carry an explicit schema version/migration decision; the v0.5 `schema_version` value `"0.5"` SHALL not be silently reused if the response meaning has changed incompatibly. Build producer version and public schema version remain different concepts.

Equivalent service, REST, and negotiated MCP requests must agree on claims, scopes, qualification, inclusion/exclusion, evidence refs, snapshot and limitations after removing transport envelope differences. All public read calls perform zero graph writes. Tool implementations and REST adapters SHALL not independently reconstruct the locality reasoning. The transport-independent deterministic evaluator calls the semantic service directly.

## 19. I3 Exit Gates

I3 is complete when a coding agent or ordinary HTTP client can ask where a qualified dependency holds in two selected supported localities and receive the same deterministic answer, including meaningful abstentions and snapshot-bound drill-down. An independent MCP client SHALL discover the frozen public tool contract, execute the question, resolve evidence at the same snapshot, and reconnect without change in meaning. The existing three v0.5 tools/REST routes and published v0.5.1 demo SHALL pass compatibility regression. A fourth tool is permitted only if the reviewed I3 specification freezes it and the corresponding qualified public schema.

---

# Part IV — Independent Qualification and User Demonstration

## 20. I4 Frozen Evaluation Method

Before running AIP or deriving expected results from code, I4 SHALL independently author the input/evidence dossier, supported claim inventory, selected localities/windows, expected qualifications, expected exclusions and forbidden claims. Each expected fact SHALL identify the original evidence and the rule that licenses the specific locality attribution. Implementation tests and an LLM-generated expected file are not independent truth.

At a minimum, deterministic scenarios SHALL cover:

| Scenario | Required assertion or refusal |
|---|---|
| Same Service, two distinct caller Workloads, two different observed dependencies | Each positive edge stays in the supported caller locality; comparison shows only differences in established claims. |
| Existing `DEPLOYED_AS` via configured mapping but spans have no admissible Pod UID | Service placement may resolve; workload-local `CALLS` does not. |
| Pod UID + current owner chain + compatible window | Caller-local `CALLS` may qualify where other HTTP identity guards also succeed. |
| Name-only/namespace-only/label-only/co-location-only | No positive runtime locality qualification or interaction. |
| Source declaration applies at Service level without explicit regional binding | No automatic per-region declared assertion. |
| Different known localities with different target edges | Coexist without global conflict or inferred absence in the other locality. |
| Contradictory applicable identity paths within one locality | Explicit conflict, no precedence guess. |
| Missing cluster UID, unsupported region/tenant, wrong namespace, stale capture | Bounded unsupported/unresolved/inapplicable result, no fabricated scope. |
| No observed call in window; partial/none/unknown coverage | v0.5 non-observation semantics and local limits preserved. |
| Snapshot changes between result and evidence drill-down | Explicit refusal or bounded retry, never silent evidence substitution. |
| Source reimport/reorder/inventory disappearance/authorized removal | Deterministic result and existing lifecycle/removal authority preserved. |
| Caller locality evidenced but target locality missing | Do not claim target is local or remote. |
| Two qualified one-hop edges / cross-boundary path | No new causal flow or end-to-end business outcome from traversal alone. |
| Intent-like document or agent-generated narrative is added | No alteration to Current State or its lineage. |
| Existing v0.5.1 Quarkus replay and operator AsyncAPI overlay | No newly inferred runtime locality or Kafka observation. |

I4 SHALL run all qualifying scenarios twice from clean state with byte-identical normalized semantic output and no unexplained nondeterminism. For equivalent requests, semantic mismatches across service/REST/MCP SHALL be zero; no material missing supported claims, no false supported scope, no silent context loss, and no regression in pre-existing qualification. A lower false-claim rate achieved solely by returning every locality unresolved is not success (§27).

## 21. I4 Compatibility and Security Gates

The qualification matrix SHALL include existing v0.5.0/v0.5.1 deterministic evaluation, ingestion/identity/Pub/Sub regression, REST/negotiated MCP interoperability and read-only/security tests. No new transport authorization, persistent distributed assessor, remote reference expansion, broad telemetry payload retention, source-scope widening, or secret capture is permitted by the locality feature. New locality evidence is bounded and sanitized; snapshot and reference identifiers remain opaque on public surfaces.

If performance changes materially because a locality query requires broader snapshot reads, measure against the existing committed read-cost baseline and record resource costs; do not mask a correctness issue with undocumented caching or stronger claims from stale projections. Public answer bounding and determinism outrank maximal graph coverage.

## 22. I5 Real-System Qualification

I5 SHALL revalidate the released, pinned **Quarkus Super Heroes** and **Apache Airflow** v0.5 dossiers on the final v0.6 candidate, preserving independent upstream truth and source-mode labels. Quarkus provides a realistic positive developer story; Airflow remains a materially different system and an important negative/insufficient-evidence case for application dependencies. Their lack of a suitable pair of upstream-proven cross-locality `CALLS` examples is a **coverage gap**, not a license to rewrite either frozen dossier.

To qualify the new two-locality positive path, add a separately disclosed and independently authored **supporting locality fixture or capture** with its own provenance and expected results. If generated telemetry or declared infrastructure is used, label it as a controlled fixture, not a recorded property of the Quarkus upstream application. Prefer extending the released v0.5 Quarkus semantic vocabulary/known services for continuity, but do not substitute invented events for the pinned Quarkus source facts.

Findings SHALL distinguish `CORRECT`, `MISSING_SUPPORTED`, `UNSUPPORTED`, `UNRESOLVED`, `INSUFFICIENT_EVIDENCE`, and genuine semantic defects per the governing validation methodology. No target-specific exception may be introduced solely to pass one demonstration. Re-run both targets and the supporting locality cases on the final candidate after accepted cross-system fixes.

## 23. I5 User Demonstration

Extend (do not destroy) the v0.5.1 Quarkus task-led entry point with a bounded **where-is-this-dependency-established?** walkthrough. The developer first inspects the original published Quarkus answer, then a clearly separated v0.6 locality-capable fixture demonstrates what changes once admissible per-observation caller-locality evidence is available.

The walkthrough SHALL show the actual request and answer for:

1. one positively localized direct relationship with its evidence;
2. the same Service in a second evidenced locality with a different supported dependency;
3. one missing-locality or not-observed case that does **not** imply absence;
4. a Service `DEPLOYED_AS` mapping which does **not** prove that every runtime `CALLS` originated at that Workload;
5. the exact included/excluded locality selection and same-snapshot evidence drill-down.

This is a deterministic, LLM-optional AIP demonstration. An optional real agent conversation illustrates consumption but is not itself qualification evidence. AIP output, source dossier, operator-authored fixture, and agent interpretation SHALL remain separately labelled. Keep setup/teardown simple and do not require a live Kubernetes cluster, Kafka broker, Quarkus build, extra agent harness or model key merely to reproduce the release capability.

## 24. Product Pilot Decision Gate

A release capability is not product-validated solely because semantic tests pass. Before a bounded pilot, freeze representative service-change tasks, expected answers and success/stop thresholds for the initial target user (platform/architecture teams enabling coding agents), comparing with and without AIP under comparable source access. Measure together:

```text
time/engineering effort to establish the correct scoped dependency context
useful supported-answer coverage and justified abstention
false local/global assumptions and misleading absence claims caught
setup, capture, source maintenance, mapping and clarification effort
agent/reviewer ability to preserve scope and evidence in follow-up questions
independently detectable post-change differences versus false alarms
```

If the pilot runs, record `CONTINUE`, `NARROW`, `DEFER`, or `STOP` with reasons. If it has not run by the capability-release decision, record `NOT_RUN` and do not claim that customer outcomes or stable-contract product-value gates have passed. Do not invent numerical success thresholds. A failed gate requires an explicit product/scope disposition and, where material, a roadmap update. Narrowing the accepted contract is preferable to adding an unqualified source or claiming global completeness. Pilot success is a gate to accepting affected capabilities into the later stable contract, not a substitute for v0.6 technical release qualification.

## 25. I4/I5 Exit Evidence

Completion records SHALL cite exact pinned source/fixture revisions, expected facts authored independently, qualification command/results for both clean runs, public schema parity, real-system results, unresolved/unsupported cases, evidence-lineage checks, product-pilot status and disposition if conducted, and any documented scope amendment. A dossier claim unsupported by the source is not repaired by an attractive demo narrative.

---

# Part V — Release, Compatibility and Completion

## 26. Candidate Freeze and Identity

I6 freezes an exact `CANDIDATE_SHA`, package/producer version, committed schema/mapping/rule versions, test and evaluation results, source/fixture pins, expected snapshots and demo outputs. Every qualification assertion SHALL name the exact candidate or immutable artifact it tested. After a change, requalify affected and required end-to-end gates before presenting the candidate as ready. An earlier source checkout, successful PR head, locally rebuilt image, or older tagged RC is not substitutable for the final candidate.

## 27. Pre-Publication Qualification and Decision

The final candidate SHALL pass the release's unit/integration/independent-evaluation suites, both real-system revalidations, supporting locality fixture, clean-state deterministic two-run comparison, public REST/MCP parity and evidence drill-down, v0.5.1 demo regression, golden-path deployment, dependency/container/security/SBOM review, and documentation/source-link checks. Any accepted vulnerability disposition SHALL identify the specific artifact and owner decision; no unresolved release-blocking finding remains.

Technical readiness and publication authority remain distinct. Record a clear `GO`/`NO_GO` technical result against the exact candidate. Only the repository owner authorizes publication. `RELEASE_READY` is not a claim that a final GitHub release or container image was published.

## 28. Publication, Published-Image Golden Path and Closure

If authorized, tag and publish the exact qualified candidate as `v0.6.0`, verify tag/commit identity, published workflow attempt, GHCR digest, anonymous pull, package/build revision, schemas, release notes, full security disposition and published-image golden path. Re-execute a same-snapshot locality answer and evidence drill-down from the published digest, and record its evidence/projection identity. The published image, not a candidate rebuild, is the verification target.

Terminal results are:

```text
RELEASE_READY_NOT_PUBLISHED
  technical qualification passed; owner did not authorize publication; closure records no release claim

SHIPPED_VERIFIED
  owner authorized publication; exact tagged/published artifacts independently verified

NO_GO / POST_RELEASE_FAILED
  release-blocking technical or post-publication verification failure, with explicit disposition
```

The exact files/commands and whether an RC tag is warranted are I6 decisions; v0.5.0's I6 and v0.5.1's lightweight release record are process precedents, not authorization to skip the capability-release qualification specified here.

## 29. Public Surface and Compatibility

`ArchitectureIntelligenceService` SHALL remain the single semantic owner. REST and standard negotiated MCP are public adapters, not alternate sources of architectural truth. The new locality question must be available equivalently on both and validated by a service-direct semantic oracle. Versioned schema changes and migration examples SHALL accompany any added claim/context/limitation shape. Maintain backward compatibility for supported v0.5 requests where feasible; an intentional pre-v1.0 breaking change requires an explicit reviewed decision and migration note, not a silent optional-field widening. Existing generic graph browsing remains outside the Architecture Intelligence correctness path.

## 30. Required Documentation and Evidence

Publish an I1 support matrix (dimension × source/mapping × claim kind); distinction between source, caller and target locality; assessment/projection semantics; reasoned limitations and completeness; REST/MCP request/response examples and schemas; non-observation and temporal compatibility examples; demo setup; deterministic evaluation; real-system findings; version/migration guidance; candidate and publication records. Explain the difference between *supported in selected localities* and *universally true*, and between operator-authored fixtures and independently observed production behavior.

## 31. Release-Level Definition of Done

A user can answer **“Where is this dependency established, and how do supported results differ between these selected localities?”** over one stable snapshot, with independently justified local assessments, explicit locality evidence/qualification, deterministic projection, exclusions/coverage, same-snapshot provenance, and correct refusal where the evidence does not support an answer. The new question works through real REST and negotiated MCP clients, is independently qualified twice from clean state, survives v0.5 regression, and is understandable in a task-led demonstration. Final release claims follow only from the terminal I6 outcome.

Permitted capability claim upon qualification:

> **AIP v0.6.0 establishes supported direct architectural relationships within explicit evidenced localities and observation contexts, and deterministically compares selected qualified local Current-State results without inventing global truths, negative dependencies, intent or causal flows.**

## 32. Relationship to Later Releases

`v0.6.0` produces **Current State only**. `v0.7` may subsequently represent independently attributable Architectural Intent Statements and their authority/lifecycle/scope/effective-time applicability. `v0.8` may then assess Current State against independently applicable Intended Architecture. Neither future path can retroactively become an input into v0.6 Current-State qualification. Historical trajectories, transformation reasoning and distributed local-assessor deployment remain beyond v1.0 unless a later authorized roadmap decision changes that boundary.

## 33. Draft 0.1 Decision Register

The following choices must be frozen in reviewed increment specifications **before** writing corresponding implementation and independent truth fixtures; their constraints are already fixed above.

| Owner | Decision to freeze | Constraint already fixed by this parent |
|---|---|---|
| I1 | Actual `LocalityScope` representation, permitted values/combinations, exact dimension-support/rejection taxonomy; whether region or service version can be positively admitted | Minimum environment/window plus exact evidenced cluster/namespace/Workload slice; missing/unsupported is never wildcard; source/subject/target/claim scopes stay distinct. |
| I1/I2 | Exact attribution rules for OTel HTTP caller observation to Pod/Workload; treatment of capture timestamps and partial scope intersections | No locality from Service-level `DEPLOYED_AS` alone; preserve v0.5 identity and temporal guards. |
| I2 | Stable scoped assertion identity versus versioned local assessment identity; internal read/persist choice and qualification/lineage representation | Deterministic, provenance-linked local assessment; no independent qualification fork, Intent or convenience graph writes. |
| I3 | Public relation-locality route/tool versus equivalent compatible extension; request bounds, optional filters, response field names, schema-version migration | One deterministic question-specific comparison on a single snapshot through service, REST and negotiated MCP; no agent-assembled truth or generic graph tool. |
| I3 | Exact completeness and included/excluded scope fields, scoped limitations and canonical order | Completeness relative to evaluated selected evidence only; no silent exclusion, universal claim or absent-dependency inference. |
| I4 | Independent truth tables, support/coverage thresholds, ordering and normalized two-run comparison artifacts | False supported scope, context loss, snapshot mismatch and cross-surface semantic disagreement are blockers. |
| I5 | Pins and authorship of supporting two-locality input/capture, real-system qualification scope, frozen product pilot metrics/thresholds | Frozen upstream dossiers unchanged; controlled fixture identified as such; both existing real systems revalidated. |
| I6 | Candidate evidence filenames, RC use (if any), actual publication/verification commands and owner decision record | Exact candidate/digest identity, security disposition and distinct unpublished/published terminal outcomes. |

## 34. Draft 0.1 Acceptance Criterion

This draft is ready to split into increment specifications only after review confirms that:

1. it adds a materially new **locality-aware architecture question**, rather than repackaging deployment resolution or source inventory;
2. one exact per-observation locality attribution is demanded for the first positive `CALLS` slice; source-scoped declarations and configured deployment mapping cannot masquerade as observed workload-local interactions;
3. supported local claims can coexist, while unknown/unsupported/partial scopes never imply universal truth or local absence;
4. local assessments and projections preserve existing qualification, source applicability, snapshot, derivation and evidence-reference rules and remain Intent-independent;
5. REST/MCP exposure is bounded, deterministic and owned by one semantic service, with explicit public versioning and a decision on the proposed fourth tool;
6. independent tests and a disclosed supporting locality fixture can prove the new capability without rewriting the v0.5 Quarkus/Airflow source truth; and
7. completion measures a working user question and product value, not just a new internal data type or additional release ceremony.
