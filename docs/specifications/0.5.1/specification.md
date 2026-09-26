# AIP v0.5.1 — Realistic Architecture Demo: Quarkus Super Heroes

**Status:** Proposed  
**Target:** `v0.5.1`  
**Baseline:** Published `v0.5.0`  
**Scope authority:** [ROADMAP.md — v0.5.1](../../../ROADMAP.md)

## 1. Release promise

> A user and their coding agent can obtain and inspect architecture context for a concrete Quarkus development task without reconstructing that context themselves.

The centerpiece of v0.5.1 is a **ready-to-run Quarkus Super Heroes demo**, based on the final v0.5.0 I5 dossier and qualified evidence. This is an experience/replay release, not a new Architecture Knowledge capability or a general UI project.

The hero task is: **“Before changing the fight service, help me understand what it depends on, which interactions were observed, how its deployment is identified, and what evidence and limitations I should inspect.”**

## 2. Baseline and constraints

- Reuse `docs/real-world-validation/v0.5.0/quarkus-super-heroes/` and final-candidate evidence under `docs/real-world-validation/v0.5.0/final-candidate/quarkus-super-heroes/`; do not rewrite the frozen dossier or its historical records.
- Use the dossier's pinned upstream Quarkus Super Heroes commit `8ea03377bfe7a89c49e1ccc0e501bf5fafbc2cce`. Preserve the distinctions between upstream-supplied, upstream-derived, operator-configured, and independently observed evidence.
- Reuse the four OpenAPI declarations, fight-service architecture manifest, identity bindings, offline namespaced Kubernetes evidence, and supported runtime observation path. The upstream-unmodified Kubernetes bundle remains a deliberate rejected/negative input, not a healthy demo source.
- The services run in Docker Compose; the Kubernetes bundle is an **offline declared manifest**, not evidence that the Compose services are running in a cluster. WHERE something is does not establish HOW it interacts.
- The final I5 qualification established **45/45 supported facts** (35 PROVIDES, 7 CALLS, 3 DEPLOYED_AS), zero incorrect supported facts. Of the seven CALLS, three exercised calls are CONFIRMED and four unexercised calls NOT_OBSERVED_IN_WINDOW. The three deployment bindings are RESOLVED_CONFIGURED. The demo may demonstrate these qualified outcomes but must get its displayed answers from the running AIP instance.
- Unsupported gRPC, Kafka `fights`, and legacy `messaging.operation` must stay unsupported. Do not invent a Kafka Topic/Queue/Subscription claim or a dependency for a name-only deployment candidate.
- **Source-of-truth boundary:** the v0.5.0 public `rest-fights` dependency answer is `ANSWERED` with `limitations: []` and contains only seven supported CALLS plus one DEPLOYED_AS. It does **not** identify the unsupported gRPC locations call or Kafka `fights` publication. Those are documented by the independently authored frozen dossier/upstream evidence, **not by AIP's public answer**. The demo must label their origin explicitly, must not add them to an AIP-results panel, and must not imply `limitations: []` means the whole application's dependencies are known. Dossier finding F4 provides a narrower AIP hint: `service:grpc-locations` is OBSERVED_ONLY and relation-less, which does not qualify a rest-fights → grpc-locations relation.
- Keep `examples/runtime-demo/` and its existing minimal demonstration intact.
- No new Architecture Knowledge semantics, source families, public MCP tools, generic graph editor, or mandatory new UI. Rebuilding, running, or documenting a full live Quarkus Super Heroes environment is out of scope for v0.5.1; the frozen I5 dossier is reused solely as provenance and input for the lightweight replay.

## 3. I1 — Lightweight, ready-to-run Quarkus demo

**Deliverable:** A simple replay of the already-qualified Quarkus Super Heroes evidence. The normal demo is **not** a repeat of the I5 qualification run and does not start the real multi-service application.

Target entry point:

```bash
examples/quarkus-super-heroes-demo/run.sh
```

Default flow:

1. Start **AIP + Neo4j** using the existing local Compose pattern; reuse existing infrastructure rather than create a new orchestration framework.
2. Import the frozen four OpenAPI declarations, `rest-fights` manifest, identity bindings, and the positive offline namespaced Kubernetes bundle from the v0.5.0 dossier. Keep the intentionally rejected upstream-unmodified bundle out of the healthy path.
3. Replay a small, committed **timestamp-frozen OTLP fixture** representing the three exercised qualified HTTP calls. If the dossier does not contain reusable raw OTLP bytes, construct the smallest transparent, independently checked transcription from its frozen observations, document that provenance, and check its resulting supported facts against the final I5 expectations. Do not present reconstructed bytes as the original live capture and do not manufacture unsupported gRPC/Kafka claims.
4. Stop replay/ingestion after it completes; retain AIP and Neo4j for read-only user/agent exploration. Query the actual `rest-fights` dependencies answer once as a simple readiness check: the seven per-operation CALLS have three `CONFIRMED` and four `NOT_OBSERVED_IN_WINDOW` labels, and the `DEPLOYED_AS` binding is `RESOLVED_CONFIGURED`. Fail visibly rather than publish a misleading demo if that shape differs.
5. Print the local AIP/MCP URLs and a copy/paste-ready agent prompt containing the fixture's `quarkus-i5` environment and actual closed UTC window. Save this context in a small run-local text/JSON file. Include a `--down` or similarly simple cleanup command.

**Keep the implementation small:** Prefer a Compose file or override, a short shell launcher, the fixture, and one README. Reuse existing import/OTLP/test helpers. No generalized demo engine, dynamic observation-window discovery, revision-stability polling subsystem, image-provenance pipeline, duplicate dossier, or elaborate test harness. A single actual dependency→evidence smoke read after ingestion has stopped is enough to catch an unusable snapshot-bound walkthrough.

The default replay needs Docker/Compose and the existing AIP dependencies; it does **not** require compiling Quarkus, Maven, Kafka, application databases, six application images, a live Kubernetes cluster, an LLM key, or upstream network access beyond obtaining the AIP image/dependencies. Document ordinary disk/download requirements for this lightweight path; do not advertise the I5 live-run 10 GB requirement as the default demo requirement.

**Snapshot handling:** Fixed input timestamps make the demonstration window stable, but the graph snapshot can still advance if someone imports or ingests new data. The launcher finishes ingestion before announcing readiness and does not leave a background producer running. The walkthrough explains that deliberate mutations require a fresh dependencies read and evidence resolution at the new snapshot, or a simple `--down` and rerun. Do not add a new snapshot-freeze feature.

**Acceptance:** A user runs one command, gets a real AIP answer about `service:rest-fights` with the expected qualifications and deployment binding, and can resolve its evidence through MCP. The previous minimal synthetic demo remains unchanged.

## 4. I2 — Task-driven architecture exploration

**Deliverable:** A short, user-facing walkthrough, grounded in actual REST and MCP answers, starting with the development task rather than an endpoint tour.

Walkthrough sequence:

1. **Before changing rest-fights, what are its direct dependencies?** Show the seven declared CALLS and distinguish the three runtime-CONFIRMED calls from the four NOT_OBSERVED_IN_WINDOW calls. Group by destination service **and operation** (`delivery.via`, method and path): the same destination appears more than once with different qualifications because different operations were exercised. The latter does not imply dead or unused code.
2. **Which evidence supports those claims?** Resolve the returned evidence references within the same stable snapshot, showing declaration sources and the selected observation window. The default replay has finished ingestion before exploration. If someone deliberately mutates the graph, re-query dependencies and resolve evidence at the new snapshot, or reset/replay. Never reuse stale evidence references without checking their snapshot.
3. **Where is the fight service deployed?** Use the existing MCP `get_service_dependencies` response: its DEPLOYED_AS claim already includes the `rest-fights` Workload target and RESOLVED_CONFIGURED reconciliation. Show configured identity evidence, and separately label the dossier's declared-manifest/offline context. Do not require REST for the agent's core workflow or claim live cluster deployment or co-location-based interaction.
4. **What remains uncertain before I edit the service?** Add a visibly separated **“Additional context from the frozen dossier (not AIP's dependency answer)”** section: the known upstream gRPC locations interaction and Kafka `fights` publish are outside AIP's currently supported answer space. Cite the dossier/upstream evidence directly; they are developer investigation leads, not AIP-qualified dependency claims and not AIP `limitations` entries. If showing the F4 `service:grpc-locations` OBSERVED_ONLY entity, say explicitly that AIP cannot qualify its relation to `rest-fights`. Explain any intentionally unresolved/unmapped deployment identities without guessing.
5. **What follows from this?** Let a developer inspect `rest-heroes`, `rest-villains`, or `rest-narration` as natural follow-ups while distinguishing AIP-established architecture facts from the agent's suggested investigation steps.

Use shipped REST routes and the **standard negotiated MCP** transport. The public tool surface remains exactly `get_service_dependencies`, `get_architecture_drift`, and `get_evidence`. Do not use the retired direct MCP envelope. The demonstration agent obtains the deployment binding from the MCP dependencies answer; REST may be offered as an optional independent inspection path, not a required fourth agent capability.

The walkthrough should show the meaningful output and provenance rather than dumping unannotated JSON. Visually and textually separate **live AIP result**, **frozen dossier/upstream context**, and **agent-suggested follow-up**. Do not attribute dossier-only context to AIP, and do not silently merge unsupported interactions into the returned `claims` or `limitations`. Lightweight formatting/helpers are fine, but they must not implement independent semantics or fake answers.

**Acceptance:** A reader can perform the end-to-end fight-service investigation and follow every supported conclusion to its evidence, while seeing the unsupported/unresolved limits.

## 5. I3 — Real coding-agent walkthrough and discovery

**Deliverable:** One reproducible example conversation with an existing coding-agent client (Codex CLI or Claude Code) connected to the running Quarkus AIP demo.

Suggested prompt:

> Before changing `rest-fights`, query AIP for `service:rest-fights` in environment `<ENVIRONMENT_FROM_RUN_SH>` from `<WINDOW_START_FROM_RUN_SH>` to `<WINDOW_END_FROM_RUN_SH>`. Use `get_service_dependencies`, `get_architecture_drift`, and `get_evidence`; the dependencies answer also supplies the deployment binding. Resolve evidence at the same snapshot. If a snapshot-stale response appears after someone mutates the prepared demo, re-query architecture answers and resolve evidence at the new snapshot (or reset/replay for the frozen demo); never guess or ignore the refusal. Group dependency claims by target **and operation**, showing their separate qualifications. Distinguish facts returned by AIP from developer follow-ups. The frozen dossier independently records a gRPC locations interaction and Kafka `fights` publication outside the supported AIP answer; do not report these as AIP claims or AIP limitations, and do not assume the empty limitations list proves complete application coverage. Do not guess unresolved identity.

Show real autonomous MCP tool calls and a representative answer that separates source-grounded findings from recommendations for additional inspection. The agent must not create or qualify canonical facts. Supply exact client setup and an explanation that the AIP demo itself needs no model API key, while the chosen agent client may require its own account. The documented prompt must be emitted by the launcher with the frozen fixture's actual window: omission of environment/start/end leads to `NOT_ANSWERED` / `OBSERVATION_CONTEXT_REQUIRED`, so the agent must not guess them. An optional dossier reference can be provided separately to the agent; if it uses that reference, cite it as dossier context rather than tool output.

A short real capture or recording of this **Quarkus-specific** workflow is desirable, but do not make media production the critical path to a runnable demo.

**Acceptance:** A documented client completes the conversation with real AIP tool results and faithful evidence/limitation handling.

## 6. I4 — Entry points and lightweight release

Update the README with an obvious **Quarkus Super Heroes: understand the fight service before changing it** entry point. Link the quick-start, guided questions, and agent walkthrough. Retain a separate link to the minimal synthetic demo; the two demonstrations have different purposes.

Provide one concise demo README with lightweight replay prerequisites, run, inspect, agent connection, troubleshooting, and teardown; no full live-Quarkus startup or capture walkthrough belongs to v0.5.1. The existing UI configuration already defaults to `quarkus-i5`; if linking directly to the UI, verify the launched demo uses that config and shows observed results, or omit the UI link. Do not promise observed rows from a default-environment mismatch. Correct stale transport instructions encountered along this path.

Run ordinary CI and one clean lightweight replay smoke test: assert the seven per-operation labels and configured deployment binding, verify the generated prompt's fixture environment/window, and make one real snapshot-consistent MCP dependencies → evidence drill-down. The walkthrough must visibly separate AIP findings from dossier-only unsupported context. Reuse existing test helpers; do not reconstruct the full I5 qualification matrix. Avoid a new qualification framework, duplicate dossiers, excessive completion records, or release-ceremony slices. Publication is an owner decision.

## 7. Definition of done

A new developer can run the documented Quarkus Super Heroes demonstration, ask what they need to know before changing `rest-fights`, inspect dependencies, runtime qualifications, deployment identity and evidence, follow up through a real coding agent, and see unsupported/unresolved boundaries without reconstructing the architecture from source files themselves.

The pre-existing minimal demo still works. No new architecture-answer semantics or MCP tools have been introduced.
