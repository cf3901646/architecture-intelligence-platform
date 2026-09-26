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
- No new Architecture Knowledge semantics, source families, public MCP tools, generic graph editor, or mandatory new UI.

## 3. I1 — Ready-to-run Quarkus demonstration

**Deliverable:** A documented, reproducible entry point under `examples/quarkus-super-heroes-demo/` (or an equally clear directory) that takes a new developer from checkout to a prepared AIP instance.

A convenience command such as:

```bash
examples/quarkus-super-heroes-demo/run.sh
```

must orchestrate the existing dossier setup rather than require users to manually repeat the I5 qualification runbook. It should check prerequisites, use pinned inputs, start the necessary services/AIP/Neo4j/collector, import the applicable declarations and offline Kubernetes source, exercise the recorded fight-service traffic, wait for readiness based on observable state, and print the local REST/MCP endpoints and next step. Provide a clean stop/reset command.

**Practical adoption:** Document the expected heavy local build (six upstream JVM service images, Maven build, several infrastructure containers, and approximately 10 GB of available disk as in the dossier prerequisite), Docker/Compose, and first-run network/download requirements before the command. The default may reuse *verified* local images or consume prebuilt images only when their immutable digest and provenance are demonstrably tied to the dossier's pinned upstream commit and compatible runtime configuration. `artifacts/compose-images.json` pins the recorded third-party/infrastructure images; it does **not** automatically certify a replaceable prebuilt image for each locally built Quarkus service. Never use upstream rolling `java25-latest` tags as if they represented the pin. Provide a documented `--build-from-source` path; reserve mandatory fresh `--no-cache` builds for qualification, not ordinary user demo starts. If suitable pinned service images cannot be verified, build those services from the pinned source instead.

**Window stability gate:** Use environment `quarkus-i5`. The traffic trigger finishing is not enough to close the window: wait until AIP actually reports all three expected exercised CALLS (`rest-heroes` random, `rest-villains` random, and `rest-narration` POST) as `CONFIRMED`, including delayed narration telemetry. The gate must also assert the *entire* expected `rest-fights` answer: exactly seven per-operation CALLS with the frozen three `CONFIRMED` and four `NOT_OBSERVED_IN_WINDOW` labels, plus its `RESOLVED_CONFIGURED` DEPLOYED_AS binding. An accidental additional hello/image request must fail the demo preparation rather than silently change the story. Only then close and freeze a window enclosing those observations. Fail with actionable diagnostics if the gate cannot be met; never silently release a replay with a changed qualification.

**Stable exploration state:** A closed observation window does *not* freeze the AIP graph snapshot: new OTLP observations can advance the model/evidence snapshot even when the query window stays unchanged. The ready-to-explore demo must therefore stop further ingestion after the required evidence has arrived: finish the scripted traffic, allow the collector to deliver and AIP to commit all required observations, disable/stop the collector's forwarding path, then wait for the AIP revision/snapshot to settle and verify it remains unchanged across two successive read-only checks. Keep AIP/Neo4j and the optional browser/client surfaces running for exploration. The demo must not leave an active traffic generator or ingestion path writing into the demo state. Mark the run *ready* and print the agent prompt only after this stability check succeeds. If someone deliberately restarts collection/reimports or otherwise mutates the graph, the old `snapshot_id` becomes stale: rerun preparation to obtain a new stable context rather than presenting unexplained `get_evidence` refusals. Document that app interactions after freeze are not captured until a new prepared run; do not imply that stopping the collector freezes the running application itself. Subsequent demo answers use this same closed window and stable snapshot.

The demo must capture or expose its actual environment, observation window, **stable snapshot identity**, upstream commit, and AIP build/image identity. `run.sh` must print a **copy/paste-ready agent prompt** with the actual `quarkus-i5` environment and replay-specific UTC `window_start` and `window_end`, and persist the same data in a small run-local context file for later reuse. Example prompts in the documentation must show how to insert the generated values, never hardcode a stale I5 observation window. Two clean replays must produce equivalent semantic findings and qualification labels; dynamically generated snapshot/observation identifiers need not be byte-identical. Do not silently substitute the old synthetic `order-service` fixture for the real Quarkus system. No LLM key or live Kubernetes cluster is needed for the deterministic AIP preparation; building/pulling upstream images may require normal build network access.

**Acceptance:** From a documented clean checkout, the prescribed command results in an inspectable `service:rest-fights` architecture context. Failures explain the prerequisite or step that failed rather than leaving partially prepared state unexplained.

## 4. I2 — Task-driven architecture exploration

**Deliverable:** A short, user-facing walkthrough, grounded in actual REST and MCP answers, starting with the development task rather than an endpoint tour.

Walkthrough sequence:

1. **Before changing rest-fights, what are its direct dependencies?** Show the seven declared CALLS and distinguish the three runtime-CONFIRMED calls from the four NOT_OBSERVED_IN_WINDOW calls. Group by destination service **and operation** (`delivery.via`, method and path): the same destination appears more than once with different qualifications because different operations were exercised. The latter does not imply dead or unused code.
2. **Which evidence supports those claims?** Resolve the returned evidence references within the same stable snapshot, showing declaration sources and the selected observation window. The prepared demo has ingestion stopped to prevent unrelated interaction from invalidating snapshot-bound drill-down; if the graph has nevertheless been deliberately changed, re-query the dependencies to establish a new snapshot and resolve evidence against that snapshot, or reset/replay to recover the frozen story. Never reuse stale evidence references without checking their snapshot.
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

Show real autonomous MCP tool calls and a representative answer that separates source-grounded findings from recommendations for additional inspection. The agent must not create or qualify canonical facts. Supply exact client setup and an explanation that the AIP demo itself needs no model API key, while the chosen agent client may require its own account. The documented prompt must be emitted by the launcher with its real replay window: omission of environment/start/end leads to `NOT_ANSWERED` / `OBSERVATION_CONTEXT_REQUIRED`, so the agent must not guess them. An optional dossier reference can be provided separately to the agent; if it uses that reference, cite it as dossier context rather than tool output.

A short real capture or recording of this **Quarkus-specific** workflow is desirable, but do not make media production the critical path to a runnable demo.

**Acceptance:** A documented client completes the conversation with real AIP tool results and faithful evidence/limitation handling.

## 6. I4 — Entry points and lightweight release

Update the README with an obvious **Quarkus Super Heroes: understand the fight service before changing it** entry point. Link the quick-start, guided questions, and agent walkthrough. Retain a separate link to the minimal synthetic demo; the two demonstrations have different purposes.

Provide one concise demo README with prerequisites, resource/build expectations, run, inspect, agent connection, troubleshooting, and teardown. The existing UI configuration already defaults to `quarkus-i5`; if linking directly to the UI, verify the launched demo uses that config and shows observed results, or omit the UI link. Do not promise observed rows from a default-environment mismatch. Correct stale transport instructions encountered along this path.

Run ordinary CI and targeted integration/contract tests plus a clean demo smoke run against the intended artifact. Smoke checks must assert (a) the exact seven per-operation CALLS with three CONFIRMED and four NOT_OBSERVED_IN_WINDOW, as well as the configured deployment binding, before freezing the window; (b) the ingestion path is stopped and the snapshot stays constant across successive checks and an actual MCP dependencies → evidence drill-down; (c) the generated prompt carries the real environment/start/end; (d) duplicate destinations render per operation; and (e) dossier-only unsupported context remains attributed separately. An optional negative test should mutate a disposable prepared instance, observe snapshot-stale evidence refusal, and demonstrate the documented re-query/reset recovery rather than weaken snapshot fencing. Verify preserved claims, provenance continuity, absence of invented unsupported facts, and no write path through the three MCP tools. Avoid a new qualification framework, duplicate dossiers, excessive completion records, or release-ceremony slices. Publication is an owner decision.

## 7. Definition of done

A new developer can run the documented Quarkus Super Heroes demonstration, ask what they need to know before changing `rest-fights`, inspect dependencies, runtime qualifications, deployment identity and evidence, follow up through a real coding agent, and see unsupported/unresolved boundaries without reconstructing the architecture from source files themselves.

The pre-existing minimal demo still works. No new architecture-answer semantics or MCP tools have been introduced.
