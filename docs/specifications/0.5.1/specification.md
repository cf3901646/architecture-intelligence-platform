# AIP v0.5.1 — Realistic Architecture Demo: Quarkus Super Heroes

**Status:** Proposed  
**Target:** `v0.5.1`  
**Baseline:** Published `v0.5.0`  
**Scope authority:** [ROADMAP.md — v0.5.1](../../../ROADMAP.md)

## 1. Promise and task

> A user and their coding agent can obtain and inspect architecture context for a concrete Quarkus development task without reconstructing that context themselves.

v0.5.1 is a lightweight, ready-to-run demo over the already-qualified Quarkus Super Heroes (QSH) evidence, driven by one development task:

> **"Add the narration image to the fight result: `rest-fights` should also call `POST /api/narration/image`. What do I need to know before changing it?"**

## 2. Constraints

- Reuse the frozen v0.5.0 I5 dossier (`docs/real-world-validation/v0.5.0/quarkus-super-heroes/`, upstream pin `8ea03377bfe7a89c49e1ccc0e501bf5fafbc2cce`) as input and provenance, without modifying it. Do not start the live Quarkus stack.
- No new Architecture Knowledge semantics, source families or MCP tools. The tools remain exactly `get_service_dependencies`, `get_architecture_drift` and `get_evidence`, over standard negotiated MCP. Keep `examples/runtime-demo/` unchanged.
- The v0.5.0 `rest-fights` dependency answer has `limitations: []`. That does not mean the application's dependencies are completely known. The gRPC `grpc-locations` call is **dossier context**, never an AIP claim or AIP limitation, and is labelled as such.
- **Messaging overlay.** QSH ships no AsyncAPI, so the dossier correctly records Kafka `fights` as unsupported. The demo adds a small, disclosed **operator-authored** AsyncAPI overlay (§4). A `fights` Topic may exist only because of that overlay, and it is never presented as upstream or qualified evidence. Kafka *runtime observation* stays unsupported (legacy `messaging.operation` key), and a consumer group is never a Subscription.

## 3. Why Quarkus Super Heroes

QSH has upstream-supplied OpenAPI, native OTLP export, Kubernetes manifests and an independently qualified dossier (45/45 supported facts). Airflow, the other qualified system, has no `CALLS` and stays validation-only. Other candidates were checked and are not better fits:
- `piomin/sample-message-driven-microservices` has no OpenAPI and no AsyncAPI, and too few services to need AIP;
- `mudigal-technologies/microservices-sample` is unmaintained and uses Swagger 2.0;
- `dotnet/eShop` uses OpenAPI 3.1.1 (not accepted) and legacy messaging span keys.

None of them ships AsyncAPI. On any system, messaging needs a declaration that the team writes, and the overlay demonstrates exactly that.

## 4. I1 — One-command demo

Entry point: `examples/quarkus-super-heroes-demo/run.sh` (and `run.sh --down`).

1. Start AIP and Neo4j with the existing Compose pattern.
2. Import the dossier inputs: the four OpenAPI declarations, the `rest-fights` manifest, the identity bindings, the `k8s/namespaced` bundle and `mapping.yaml`.
3. Import the overlay. It consists of two AsyncAPI `2.6.0` files in the style of `tests/fixtures/pubsub/kafka/declarations/`:
   - `rest-fights` publishes `fights`;
   - `event-statistics` subscribes;
   - both use `x-aip-destination-kind: topic` and a shared `x-aip-broker-id`, and neither has an `x-aip-subscription-name`.

   A short `PROVENANCE.md` cites the upstream producer/consumer code and the `Fight` Avro schema that the message is taken from.
4. Replay a small, timestamp-frozen OTLP fixture for the three exercised HTTP calls, with its provenance noted. Nothing keeps running afterwards.
5. Read the actual `rest-fights` dependencies answer once and fail visibly unless it has:
   - seven `CALLS`: three `CONFIRMED` and four `NOT_OBSERVED_IN_WINDOW`;
   - `DEPLOYED_AS` `RESOLVED_CONFIGURED`;
   - `PUBLISHES_TO` `Topic:fights`, present and not `CONFIRMED`.

   Record the overlay's exact answer shape on the first real run and pin it in the smoke test. If it contradicts the I4 rules in [`docs/ingestion.md`](../../ingestion.md), stop and report.
6. Print the MCP URL and a ready-to-copy agent prompt containing the fixture's environment and window.

The demo needs only Docker/Compose: no Maven, Kafka, application databases, cluster or LLM key. Keep it to a Compose file or override, a short launcher, the inputs and one README. If someone mutates the graph, re-query or rerun, because evidence is snapshot-bound.

## 5. I2 — Question ladder and agent conversation

The walkthrough follows the task. Each answer comes from a live AIP call, and the walkthrough keeps **AIP result**, **dossier context** and **agent suggestion** visibly apart.

| # | Question | Must show | Must not claim |
|---|---|---|---|
| Q1 | What does `rest-fights` depend on? | The seven `CALLS`, grouped by target **and operation** | That `limitations: []` means complete coverage |
| Q2 | What actually ran? | Three `CONFIRMED` and four `NOT_OBSERVED_IN_WINDOW` claims, plus the window | That a call that was not observed is unused |
| Q3 | Why do you believe it calls `GET /api/heroes/random`? | Declared and observed evidence, resolved at the same snapshot | Evidence from another snapshot |
| Q4 | Where does it run? | `RESOLVED_CONFIGURED` through the configured mapping, taken from the MCP dependencies answer | That deployment creates dependencies, or that it is live in a cluster |
| Q5 | And `rest-narration`? There is a Deployment with the same name. | Not resolved: a matching name never resolves an identity | A resolution by name |
| Q6 | What is declared but was not exercised? | The drift answer, which includes `POST /api/narration/image` | Undeclared traffic |
| Q7 | Does it publish events, and who consumes them? | `PUBLISHES_TO` `Topic:fights`, declared by the operator overlay; the subscriber unknown (`SUBSCRIPTION_IDENTITY_MISSING`); runtime unable to confirm | A `CONFIRMED` publish, or `event-statistics` as a Subscription |
| Q8 | What should I watch out for? | The image operation was never exercised; the narration deployment is unresolved; the gRPC `locations` call is dossier context | That the change is safe |

**Agent conversation.** Record one real conversation with Codex CLI or Claude Code, using the printed prompt. Check each answer against three things:
1. it is grounded in evidence ids;
2. it makes no claim from the "must not claim" column;
3. it states the limits.

The conversation is an example, not qualification evidence. The AIP demo needs no model API key; the agent client may need its own account.

## 6. I3 — Entry point and release

- Add a README entry point: **Quarkus Super Heroes: understand the fight service before changing it**. Keep the minimal demo linked separately.
- Add one demo README covering prerequisites, running, the question ladder, agent setup and teardown.
- Add one smoke test that asserts the §4 step 5 shape and runs one MCP dependencies → evidence drill-down at the same snapshot. Plus normal CI.
- Publication is an owner decision.

## 7. Done

A new developer runs one command and asks what they need to know before changing `rest-fights`. They see its dependencies, runtime qualifications, deployment identity, event publication and evidence, and they can follow up through a real coding agent. Unsupported and unresolved boundaries, and the operator-authored overlay, are clearly labelled throughout. The minimal demo still works, and no new semantics or MCP tools have been added.
