# AIP v0.6.0 I1 — Controlled Two-Workload Capture: Acquisition Runbook

**Status:** I1 supporting deliverable, slice I1.4. This is the acquisition **plan** for the real controlled reference that I5 must qualify. I1 claims no capture has been executed. The I2 rehearsal (§9) and the I5 acquisition (§§4–8) are future work, and their status is `NOT_RUN`.  
**Release / increment:** `v0.6.0` — Locality-Aware Current State / I1  
**Governing specification:** [I1 — Locality and Evidence Applicability Contract](i1-locality-and-evidence-applicability.md) §12 (with §§8–9, 13, 16 DoD 7 and 16.1 gate 8), accepted in [PR #283](https://github.com/michaelegner/architecture-intelligence-platform/pull/283) (merge `aafb03d5735d78b2741a3dc8a2d0336079535ed6`); [parent](specification.md) §§9 (gate 8), 22 and 33 (I5 row).  
**Builds on:** [support matrix](i1-locality-support-matrix.md) §§10–15 (CLIENT allowlist, timestamps, window, dispositions) and the [v2 evidence contract](i1-scoped-evidence-v2-contract.md).  
**Precedent reused:** the v0.5 I2 independent capture, [`tests/fixtures/kubernetes/i2-independent-capture/PROVENANCE.md`](../../../tests/fixtures/kubernetes/i2-independent-capture/PROVENANCE.md). It uses a throwaway `kind` cluster, `kubectl get -o yaml`, the `kube-system` Namespace UID as `clusterUid` (`clusterIdentityEvidenceRef: kube-system-namespace-uid`), and a `CAPTURED_RESOURCE` envelope with SHA-256-pinned files.

---

## 1. Ownership (I1 §12; DoD 7)

| Role | Named person | Responsibility |
|---|---|---|
| **Acquisition owner** | **Michael Egner** (owner decision recorded in I1 planning, 2026-09-28) | Executes or approves the I5 acquisition, signs off the run record, and holds the stop decision |
| Expected-answer author | Michael Egner | Authors the §7 expected answers **after** the capture and **before** any AIP evaluation of it |
| I2 rehearsal executor | The I2 implementer, with the owner reviewing | Runs §9 before I5 |

The owner is named, so this is **not** an I1 blocker.

## 2. Scenario to acquire (I1 §12)

```text
kind cluster K (one cluster; clusterUid = kube-system Namespace UID)
namespace aip-locality

Deployment "orders"         (W1)  1 replica, Pod P1  CLIENT: GET http://pricing/prices
Deployment "orders-canary"  (W2)  1 replica, Pod P2  CLIENT: GET http://legacy-pricing/prices
Deployment "pricing"              SERVER  GET /prices   (provider of Operation O1)
Deployment "legacy-pricing"       SERVER  GET /prices   (provider of Operation O2)

Both orders Deployments: same image, same service.name=orders -> one canonical caller service:orders
```

| Requirement | Rule |
|---|---|
| Two distinct Workloads | `orders` and `orders-canary` are **two separate Deployment objects**. One Deployment rolled from ReplicaSet R1 to R2 is **invalid** as the positive two-locality fixture: it resolves to one Workload (I1 §2.1, §12; L33). |
| One caller Service | Both set `service.name=orders` and resolve to the one canonical `service:orders` from its accepted declaration. Both Deployments may carry the annotation `architecture-intelligence.io/service-id: "service:orders"`. That association is **not** used to attribute any call (L26). |
| Operations | `pricing` and `legacy-pricing` are each declared by an accepted OpenAPI source with `GET /prices`, giving canonical O1 = `operation:pricing:GET:/prices` and O2 = `operation:legacy-pricing:GET:/prices`. The runbook records the exact accepted IDs from the import report, and never from display names (I1 §5.1). |
| Declared relation | The `orders` architecture manifest declares a call to `pricing` only. The expected results are then `CONFIRMED` for (W1, O1) and `OBSERVED_ONLY` for (W2, O2) (I1 §5; L21, L22). |
| Target locality | Nothing in this scenario evidences where `pricing` or `legacy-pricing` ran. The expected target locality is unknown (L20). |

## 3. Authentic CLIENT Resource: emission and collection (I1 §6, §12)

The capture must contain **actual** CLIENT spans from real HTTP calls made by the real `orders` processes. Synthesized spans do not qualify, including spans from `examples/runtime-demo/traffic_generator.py` and anything else that fabricates CLIENT/SERVER pairs. Such spans may appear only as labelled synthetic fixtures (§8(c)).

| Item | Frozen method |
|---|---|
| Instrumentation | The OpenTelemetry SDK's standard HTTP **client** instrumentation in `orders` and HTTP **server** instrumentation in both providers. Span kinds, `http.request.method`, `http.route` (SERVER) and `peer.service` (CLIENT, needed for the v0.5 `CLIENT_ONLY` target identity) come from the SDK and its semantic conventions. |
| `k8s.pod.uid` | Kubernetes Downward API: env `POD_UID` from `fieldRef: metadata.uid`, injected into `OTEL_RESOURCE_ATTRIBUTES` as `k8s.pod.uid=$(POD_UID)`. The value is API-server-assigned. |
| `k8s.namespace.name`, `k8s.pod.name` | Downward API `metadata.namespace` and `metadata.name`, both optional consistency fields |
| `k8s.deployment.name` | A literal per Deployment (`orders` or `orders-canary`), optional consistency. It must equal the captured owner Deployment, or phase 4 correctly reports `CONFLICT`. |
| `k8s.cluster.uid` | The `kube-system` Namespace UID, read once with `kubectl get namespace kube-system -o jsonpath='{.metadata.uid}'` and injected as a literal env value at apply time. Its provenance is the same command that produces the envelope's `clusterUid`, recorded in the run record. The value must be byte-equal to the envelope `clusterUid` (I1 §4.2, §12; L16). |
| `deployment.environment.name` | A literal `locality-capture` on every workload, matching the AIP observation-context environment |
| Collector (recording) | The OpenTelemetry Collector **contrib** distribution, image pinned by digest, because the `file` exporter is contrib-only. It has an OTLP receiver and a `file` exporter with `format: json`, which writes one OTLP-JSON `TracesData` object (`resourceSpans`, the same shape as an OTLP/HTTP JSON `ExportTraceServiceRequest`) per line. There is no `k8sattributes` or `resource` processor, so the Resource is exactly what the SDK emitted. A `batch` processor is allowed because it preserves each `ResourceSpans`' Resource; the recorded lines are then the batch boundaries. **`otlp.jsonl` is not AIP input.** AIP's `/v1/traces` accepts only `application/x-protobuf` (`app/api/telemetry.py`:19) and `decode_export_request` parses protobuf bytes. The recording reaches AIP only through the §6 replay Collector. |
| Forbidden sources | Collector-side enrichment of `k8s.*`; any value derived from Pod names, labels or IP association; any hand edit of the recorded file |

## 4. Run procedure (for I5, rehearsed by I2 in §9)

The run must start and finish within **one UTC day**, beginning at or after `01:00Z` and completing all captures by `22:00Z`. The contract does not need this margin; it keeps the evidence away from midnight so the run cannot exercise the cross-day refusal (L11) by accident.

```bash
# 0. Pins (record every output in RUN-RECORD.md)
kind version; kubectl version; docker version --format '{{.Server.Version}}'
# node image and collector image pinned by digest, as in the v0.5 I2 precedent

# 1. Throwaway cluster and cluster identity
kind create cluster --name aip-locality-capture --image kindest/node:<pinned>@sha256:<digest>
kubectl wait --for=condition=Ready node --all --timeout=120s
CLUSTER_UID=$(kubectl get namespace kube-system -o jsonpath='{.metadata.uid}')   # -> clusterUid

# 2. Build and load images: orders (one image for both Deployments), pricing, legacy-pricing.
#    Record each image digest.

# 3. Namespace, Collector (file exporter volume), providers
kubectl create namespace aip-locality
kubectl apply -f collector.yaml -f pricing.yaml -f legacy-pricing.yaml

# 4. Both caller Workloads at once (the overlap), CLUSTER_UID substituted into the manifests
kubectl apply -f orders.yaml -f orders-canary.yaml
kubectl -n aip-locality rollout status deployment/orders deployment/orders-canary --timeout=180s

# 5. Traffic: each orders Pod makes its real calls for >= 5 minutes. Record the start and end UTC times.

# 6. Capture C1 (overlap: P1 and P2 both Running)
kubectl get namespace aip-locality -o yaml > c1-ns.yaml
kubectl -n aip-locality get deployment,replicaset,pod,service,ingress -o yaml > c1-rest.yaml
date -u +%Y-%m-%dT%H:%M:%SZ            # -> C1 metadata.capturedAt

# 7. Promotion: delete Deployment "orders" and wait until P1 is gone. Continue canary traffic 2 minutes.
kubectl -n aip-locality delete deployment orders --wait=true
kubectl -n aip-locality wait --for=delete pod/<P1-name> --timeout=120s

# 8. Capture C2 (post-promotion: P1 absent), same commands, and record C2 capturedAt.

# 9. Stop traffic, flush the Collector, copy out the OTLP JSON-lines file.

# 10. Teardown
kind delete cluster --name aip-locality-capture
```

Envelopes C1 and C2 each follow the v0.5 `KubernetesSourceSnapshot` form in the I2 precedent:
- `source.mode: CAPTURED_RESOURCE`, `clusterUid: $CLUSTER_UID`, `clusterIdentityEvidenceRef: kube-system-namespace-uid`;
- `scope.namespaces: [aip-locality]` and the fixed `resourceTypes`;
- `completeness.status: COMPLETE` with a self-declared authority, disclosed as such;
- a distinct `metadata.revision` and the real `capturedAt`;
- `files[].sha256` pins.

**Temporal atomicity.** Each capture is taken with separate `kubectl get` calls and is not atomic. The run record discloses this, as the precedent does.

**Stop conditions.** Abort and restart the run if any of these holds:
- P1 and P2 are not both `Running` at C1;
- either Pod was replaced during the traffic window (its UID changed);
- any CLIENT Resource lacks `k8s.pod.uid`, `k8s.cluster.uid` or the environment;
- any CLIENT `k8s.cluster.uid` differs from `$CLUSTER_UID`;
- C1 or C2 falls on a different UTC day from the traffic;
- anyone edits a recorded artifact.

## 5. Artifacts and pins

Proposed location, which I5 may rename: `tests/fixtures/locality/two-workload-capture/`, laid out like the I2 precedent.

| Artifact | Content | Pin |
|---|---|---|
| `otlp.jsonl` | The recording Collector's file-exporter output, unmodified: one OTLP-JSON request per line | SHA-256 |
| `replay/collector-replay.yaml`, `replay/replay.py` | The §6 replay Collector configuration and the line-by-line replay driver | SHA-256; Collector image digest in `RUN-RECORD.md` |
| `c1/envelope.yaml`, `c1/resources.yaml` | Overlap capture | SHA-256 in `envelope.yaml` `files[]` and in `SHA256SUMS` |
| `c2/envelope.yaml`, `c2/resources.yaml` | Post-promotion capture | same |
| `declarations/` | `orders` architecture manifest; `pricing` and `legacy-pricing` OpenAPI | SHA-256 |
| `manifests/` | Every applied manifest, with `CLUSTER_UID` substituted as applied | SHA-256 |
| `harness/` | App and Collector source or config, image digests | Git revision and digests |
| `RUN-RECORD.md` | Pins from step 0, `CLUSTER_UID` and its command, P1/P2 UIDs and names, W1/W2 Deployment UIDs, traffic window, C1/C2 `capturedAt` and revisions, atomicity disclosure, the accepted canonical Operation IDs from the import report, stop-condition checklist | — |
| `expected.md` | §7 expected answers, authored before evaluation | SHA-256, and the commit that lands it precedes any evaluation output |
| `SHA256SUMS` | All of the above | — |

## 6. Clean offline replay (I1 §12; parent §22)

No live cluster is needed after acquisition, and AIP gains no live Kubernetes admission (I1 §12). Replay into a **clean** AIP state:
1. Import the declarations.
2. Import C1, or for the post-promotion checks C2, as the selected Kubernetes source. Each is a snapshot contribution, not a historical store, so selecting C2 replaces C1 (I1 §9).
3. Replay the traffic through the **pinned replay path**, which is the only supported wire path:

   ```text
   otlp.jsonl --(one line = one request, in file order)--> POST /v1/traces, Content-Type: application/json
       --> replay Collector OTLP/HTTP receiver (:4318)
       --> otlphttp exporter, OTLP protobuf, Content-Type: application/x-protobuf
       --> AIP /v1/traces
   ```

   `replay/collector-replay.yaml` must:
   - use the same Collector image as `docker-compose.demo.yml`, pinned by digest;
   - have `receivers: otlp` with `protocols.http` only;
   - have **no processors**: no `batch`, which would merge or split recorded requests, and no attribute or resource processors;
   - have one exporter `otlphttp/aip` with `encoding: proto`, `compression: none` (AIP does not negotiate `Content-Encoding`, as in the demo config), `sending_queue.enabled: false` and `retry_on_failure.enabled: false`.

   Without a queue each received request is forwarded synchronously, one to one. With retries off, a failed export stops the replay instead of silently re-sending: a repeated POST can double-count v1, the disclosed gap in v2 contract §7.

   `replay/replay.py` posts each line in order, requires HTTP 200 from the Collector for each, and waits for AIP's revision to settle before the next line. This is the golden-path pattern (`examples/release-golden-path/golden_path.py` `_post_otlp` and `_wait_for_revision_to_settle`). It aborts on the first non-200 response.

Two clean runs must produce identical normalized results (I1 §13; I4 repeats this for the final candidate).

**Order matters for L27.** Evaluate the positive two-locality question while C1 is the selected capture, **before** importing C2 (I1 §9). An externally kept C1 file does not make P1's Workload resolvable again once C2 is selected.

## 7. Expected answers to author before evaluation (template)

Fill in the concrete IDs from `RUN-RECORD.md` and commit `expected.md` **before** the first AIP evaluation of the capture. Query: environment `locality-capture`, one whole-UTC-day window for the run day, caller `service:orders`.

| # | Selected capture | Candidate | Expected disposition / result | Cases |
|---|---|---|---|---|
| E1 | C1 | (P1 → W1 `orders`) CALLS O1 | `APPLICABLE`; the shared owner gives `CONFIRMED` (declared orders→pricing plus scoped observed) | L04, L15, L21, L27 |
| E2 | C1 | (P2 → W2 `orders-canary`) CALLS O2 | `APPLICABLE`; `OBSERVED_ONLY` (no declaration for legacy-pricing) | L04, L22, L27 |
| E3 | C1 | Enumerated caller localities | Exactly two Workload localities, W1 and W2, one cluster and namespace. No claim that W1 calls O2 or that W2 calls O1, no target placement, no absence. | L04, L20, L27, L33 |
| E4 | C2 | P1's v2 records | Retained, still attributed to P1; Workload `UNRESOLVED` / `LOCALITY_CAPTURE_MISSING_POD`; never reattached to P2 or to W2 | L18, L27 |
| E5 | C2 | P2's v2 records | Still `APPLICABLE` at W2 when C2's `capturedAt` is on the window day | L27 |
| E6 | Either | v1 | One v1 bucket per (orders, Operation, day), with counts unchanged by v2 | L02, L12 |
| E7 | Either | Snapshot | The `snapshot_id` differs between C1-selected and C2-selected states, and both carry the conditional `scoped_observed_calls_v2` key | L14 |

The concrete v2 IDs in `expected.md` are computed from the recorded UIDs with the frozen v2 key rule (v2 contract §2), using the standalone vector tooling, never AIP output.

## 8. Artifact labelling (I1 §12)

Every artifact and report states exactly one of:
- **(a) Actual independently recorded controlled reference:** the §5 artifacts from the I5 run.
- **(b) Independently authored expected answers:** `expected.md`.
- **(c) Synthetic negative-test fixture:** any hand-built input, e.g. conflicting cluster UID, `DECLARED_MANIFEST`, or missing `capturedAt` variants derived for L16/L17/L37. Such fixtures never replace (a).
- **(d) Frozen upstream dossiers:** Quarkus/Airflow, unchanged and not rewritten for locality.
- **(e) Future external product pilot:** none here.

A controlled `kind` run is not a production observation and not a pilot.

## 9. I2 rehearsal gate (before I5)

I2 builds the §3 harness and runs §4 once as a **rehearsal**. Rehearsal artifacts are labelled `rehearsal`, are not I5 evidence, and are not committed as the reference. The rehearsal passes when all of the following hold:
1. Every recorded CLIENT Resource carries a non-empty `k8s.pod.uid` equal to the Pod's API UID, a `k8s.cluster.uid` byte-equal to `$CLUSTER_UID`, and `deployment.environment.name=locality-capture`.
2. **The replay wire path works as pinned.** Each `otlp.jsonl` line is accepted by the replay Collector (HTTP 200), and the forwarded **protobuf** request is accepted by AIP `/v1/traces` (HTTP 200, no Collector export error). The number of requests AIP receives equals the number of lines, so batch boundaries are preserved and nothing is merged, split or retried; check this with the Collector's exporter request metrics or an AIP request log. The Resource attributes AIP decodes (`service.name`, `deployment.environment.name`, `k8s.pod.uid`, `k8s.cluster.uid`, `k8s.namespace.name`, `k8s.pod.name`, `k8s.deployment.name`) equal the recorded line's values byte-for-byte. C1 and C2 validate as `KubernetesSourceSnapshot` envelopes with matching `files[]` digests. The runbook does **not** claim that raw `otlp.jsonl` decodes with AIP's protobuf decoder.
3. P1 and P2 resolve through the unmodified owner-chain module to Deployments `orders` and `orders-canary` respectively, with distinct Deployment UIDs.
4. Once I2's carrier exists, CLIENT identity is retained for both in-batch and cross-batch arrival orders in the replay (I1 §6.1; L07, L08).
5. Every §4 stop condition is checked and recorded.

A rehearsal failure is an I2 blocker, not an I5 surprise.

## 10. Traceability

| Requirement | Section |
|---|---|
| I1 §12: named owner, or the pending owner as an I1 blocker | §1 |
| §12: two distinct Deployments, one canonical caller Service, exact Operation IDs and owners | §2 |
| §12: authentic CLIENT Resource emission and collection; cluster identity provenance | §3 |
| §12: overlap capture before replacement; later post-promotion capture; `capturedAt`; environment mapping; teardown | §4 |
| §12: source revisions and SHA-256 pins | §5 |
| §12: clean offline replay, with no live admission in AIP; pinned JSON → Collector → protobuf wire path | §6, §9 gate 2 |
| §12: expected results authored before evaluation | §7 |
| §12: labels (a)–(e) | §8 |
| §12: I2 early rehearsal; parent §9 gate 8 (executable plan before I2) | §9 |
| DoD 7; parent gate 8 (Pod UID, CLIENT `k8s.cluster.uid`, capture `clusterUid`, `capturedAt`, ownership, replay pins) | §§1–9 |
