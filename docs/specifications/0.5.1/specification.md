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
- Keep `examples/runtime-demo/` and its existing minimal demonstration intact.
- No new Architecture Knowledge semantics, source families, public MCP tools, generic graph editor, or mandatory new UI.

## 3. I1 — Ready-to-run Quarkus demonstration

**Deliverable:** A documented, reproducible entry point under `examples/quarkus-super-heroes-demo/` (or an equally clear directory) that takes a new developer from checkout to a prepared AIP instance.

A convenience command such as:

```bash
examples/quarkus-super-heroes-demo/run.sh
```

must orchestrate the existing dossier setup rather than require users to manually repeat the I5 qualification runbook. It should check prerequisites, use pinned inputs, start the necessary services/AIP/Neo4j/collector, import the applicable declarations and offline Kubernetes source, exercise the recorded fight-service traffic, wait for readiness based on observable state, and print the local REST/MCP endpoints and next step. Provide a clean stop/reset command.

The demo must capture or expose its actual environment, observation window, snapshot identity, upstream commit, and AIP build/image identity. Two clean replays must produce equivalent semantic findings and qualification labels; dynamically generated snapshot/observation identifiers need not be byte-identical. Do not silently substitute the old synthetic `order-service` fixture for the real Quarkus system. No LLM key or live Kubernetes cluster is needed for the deterministic AIP preparation; building/pulling upstream images may require normal build network access.

**Acceptance:** From a documented clean checkout, the prescribed command results in an inspectable `service:rest-fights` architecture context. Failures explain the prerequisite or step that failed rather than leaving partially prepared state unexplained.

## 4. I2 — Task-driven architecture exploration

**Deliverable:** A short, user-facing walkthrough, grounded in actual REST and MCP answers, starting with the development task rather than an endpoint tour.

Walkthrough sequence:

1. **Before changing rest-fights, what are its direct dependencies?** Show the seven declared CALLS and distinguish the three runtime-CONFIRMED calls from the four NOT_OBSERVED_IN_WINDOW calls. The latter does not imply dead or unused code.
2. **Which evidence supports those claims?** Resolve the returned evidence references within the same snapshot, showing declaration sources and the selected observation window.
3. **Where is the fight service deployed?** Show its RESOLVED_CONFIGURED DEPLOYED_AS binding, configured identity evidence, and the declared-manifest/offline limitation. Do not claim live cluster deployment or co-location-based interaction.
4. **What remains uncertain before I edit the service?** Make gRPC and Kafka `fights` support boundaries explicit; note intentionally unresolved/unmapped deployment identities without guessing.
5. **What follows from this?** Let a developer inspect `rest-heroes`, `rest-villains`, or `rest-narration` as natural follow-ups while distinguishing AIP-established architecture facts from the agent's suggested investigation steps.

Use shipped REST routes and the **standard negotiated MCP** transport. The public tool surface remains exactly `get_service_dependencies`, `get_architecture_drift`, and `get_evidence`. Do not use the retired direct MCP envelope. Deployment answers can be obtained via the existing REST deployment endpoint or the existing supported dependency answer as appropriate.

The walkthrough should show the meaningful output and provenance rather than dumping unannotated JSON. Lightweight formatting/helpers are fine, but they must not implement independent semantics or fake answers.

**Acceptance:** A reader can perform the end-to-end fight-service investigation and follow every supported conclusion to its evidence, while seeing the unsupported/unresolved limits.

## 5. I3 — Real coding-agent walkthrough and discovery

**Deliverable:** One reproducible example conversation with an existing coding-agent client (Codex CLI or Claude Code) connected to the running Quarkus AIP demo.

Suggested prompt:

> Before changing `rest-fights`, use AIP to establish its direct dependencies, declared-versus-observed qualification, and deployment bindings. Resolve the evidence behind relevant findings using the same snapshot. Tell me which architecture facts are supported and what I still need to investigate. Do not infer unsupported Kafka or gRPC interactions or guess unresolved identity.

Show real autonomous MCP tool calls and a representative answer that separates source-grounded findings from recommendations for additional inspection. The agent must not create or qualify canonical facts. Supply exact client setup and an explanation that the AIP demo itself needs no model API key, while the chosen agent client may require its own account.

A short real capture or recording of this **Quarkus-specific** workflow is desirable, but do not make media production the critical path to a runnable demo.

**Acceptance:** A documented client completes the conversation with real AIP tool results and faithful evidence/limitation handling.

## 6. I4 — Entry points and lightweight release

Update the README with an obvious **Quarkus Super Heroes: understand the fight service before changing it** entry point. Link the quick-start, guided questions, and agent walkthrough. Retain a separate link to the minimal synthetic demo; the two demonstrations have different purposes.

Provide one concise demo README with prerequisites, run, inspect, agent connection, troubleshooting, and teardown. Correct stale transport instructions encountered along this path.

Run ordinary CI and targeted integration/contract tests plus a clean demo smoke run against the intended artifact. Verify preserved claims, provenance continuity, absence of invented unsupported facts, and no write path through the three MCP tools. Avoid a new qualification framework, duplicate dossiers, excessive completion records, or release-ceremony slices. Publication is an owner decision.

## 7. Definition of done

A new developer can run the documented Quarkus Super Heroes demonstration, ask what they need to know before changing `rest-fights`, inspect dependencies, runtime qualifications, deployment identity and evidence, follow up through a real coding agent, and see unsupported/unresolved boundaries without reconstructing the architecture from source files themselves.

The pre-existing minimal demo still works. No new architecture-answer semantics or MCP tools have been introduced.
