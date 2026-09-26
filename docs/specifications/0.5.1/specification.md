# AIP v0.5.1 — User Demonstration & Developer Experience

**Status:** Proposed  
**Target release:** v0.5.1  
**Baseline:** Published v0.5.0  
**Theme:** Show, Don't Tell  
**Priority:** User experience over implementation ceremony

## 1. Release Goal

AIP v0.5.1 makes the existing Architecture Intelligence capabilities accessible through a compelling, reproducible demonstration.

The release must answer one question:

**Can a new user understand what AIP does, experience its value, and explore the evidence behind its conclusions without first understanding its internal architecture?**

v0.5.0 established broader evidence-qualified Current State discovery. v0.5.1 turns that foundation into something users can experience.

The release adds no new architecture intelligence dimension, Canonical Model family, or public MCP tool.

Its principal deliverable is a coherent demonstration covering dependency discovery, architecture drift, Kubernetes deployment identity, Pub/Sub semantics, evidence provenance, and explicit uncertainty.

## 2. User Experience

### 2.1 Target audience

The demonstration targets three audiences:

- Software architects exploring the Current State of a distributed system.
- Developers investigating dependencies and undocumented runtime behavior.
- Developers using AI coding agents that need trustworthy architecture context.

A user should not need to understand Neo4j, the internal Canonical Model, the qualification pipeline, or the source adapter architecture before experiencing AIP.

### 2.2 Primary user journey

The demonstration follows an architecture investigation rather than presenting a collection of API endpoints.

The user starts with a question:

**What does my order service actually depend on, and can I trust that information?**

AIP presents its dependencies, their qualifications, and their evidence.

The user discovers that:

1. ProductService is declared and observed.
2. LegacyPricingService is observed but undocumented.
3. A declared messaging dependency was not observed in the selected window.
4. Kubernetes evidence identifies a deployment workload.
5. An alternative identity scenario produces a conflict that AIP refuses to resolve by guessing.
6. Evidence can be inspected to understand why each conclusion was reached.

A second journey demonstrates the distinction between Queue, Topic, and Subscription without conflating infrastructure and application relationships.

The demonstration must make clear that AIP does not simply generate an architecture diagram. It produces architecture claims qualified by evidence.

## 3. I1 — A Usable Demonstration

**Goal:** Make it easy for a new user to run and explore AIP.

### 3.1 One-command startup

Provide a single, documented command that prepares and launches the demonstration.

Target interaction:

```bash
./demo/run.sh
```

The command should:

- start the required services;
- import the existing deterministic demonstration fixtures;
- ingest the frozen runtime observations;
- verify that the demonstration is ready;
- print the local browser URL;
- make cleanup straightforward.

No LLM API key, external cloud account, Kubernetes cluster, or live broker is required.

Reuse the v0.5.0 golden-path fixtures and existing runtime demonstration wherever possible. Do not introduce a second, independently maintained semantic fixture universe.

Existing demonstration and golden-path infrastructure may be reorganized or wrapped if that improves usability.

### 3.2 Interactive architecture exploration

Provide a browser-based demonstration.

The preferred solution is to extend AIP's existing lightweight web UI rather than build a new frontend framework or separate application.

The demonstration should expose four connected perspectives:

**Architecture Overview**

Display the services and their relevant dependencies in a readable architecture graph or equivalent interactive visualization.

Support selection of a service and navigation to its details.

Use visually distinguishable categories for declared, observed, and deployment relationships. Do not collapse these into generic edges.

**Service Detail**

For a selected service, display:

- direct dependencies;
- declared-versus-observed qualification;
- observation context;
- deployment associations;
- unresolved cases and limitations.

Show the actual supported claims, not a separately reconstructed architecture model.

**Evidence Inspector**

Selecting a claim reveals its evidence and provenance.

Show the source type, source locator, relevant evidence references, and observation context where applicable.

Evidence reads must remain bound to the originating snapshot.

A user should be able to follow a supported claim to the evidence behind it without manually copying identifiers into another tool.

**Uncertainty and Conflicts**

Provide clear presentations for:

- `OBSERVED_ONLY`;
- `NOT_OBSERVED_IN_WINDOW`;
- `CONFLICT`;
- `AMBIGUOUS`;
- `UNRESOLVED`;
- `UNSUPPORTED`, where applicable.

These must retain their distinct meanings.

An unresolved identity must never silently become a guessed relationship.

### 3.3 Guided demonstration scenarios

Provide three selectable demonstration scenarios.

| Scenario | What the user learns |
|---|---|
| Architecture Drift | Declared and observed architecture can disagree. |
| Deployment Identity | Kubernetes evidence can establish deployment identity, but not application dependencies. |
| Messaging Semantics | Topics, Subscriptions, and Queues have distinct meanings. |

The deployment demonstration should explicitly include an identity conflict.

Users should be able to switch scenarios without editing YAML files or manually invoking import endpoints.

Each scenario has a short explanation of what to inspect and why the result matters.

### 3.4 I1 acceptance

I1 is complete when:

- a new user can start the demo from a clean checkout using the documented command;
- the browser presents the supported architecture claims;
- clicking a claim exposes its evidence;
- all three scenarios are accessible;
- limitations and unresolved cases remain visible;
- the demonstration runs entirely locally;
- existing architecture semantics are unchanged.

The result must be tested against real AIP API responses. Hardcoded UI conclusions or fabricated evidence are prohibited.

## 4. I2 — Demonstrate AIP as Architecture Context for Agents

**Goal:** Demonstrate how a coding agent benefits from AIP without becoming an architecture authority.

### 4.1 Agent workflow

Provide a working example using one mainstream MCP-capable coding agent.

Codex CLI or Claude Code is sufficient as the primary demonstration client.

The demo should show an agent answering:

> Investigate OrderService using AIP. Identify its direct dependencies, explain any architecture drift, resolve the evidence behind your findings, and distinguish supported conclusions from limitations. Do not infer relationships that AIP cannot establish.

The agent should autonomously use the existing three read-only MCP tools:

- `get_service_dependencies`
- `get_architecture_drift`
- `get_evidence`

The workflow must use standard negotiated MCP as shipped in v0.5.0, not the retired direct envelope.

### 4.2 Demonstrate the value, not the protocol

The example should emphasize the difference between a plausible architecture explanation and an evidence-qualified answer.

The agent's response should clearly distinguish:

- what is declared;
- what is observed;
- what is confirmed;
- what is not observed in the selected window;
- what AIP cannot establish;
- which evidence supports each statement.

An agent must not transform an AIP limitation into a confident architecture assertion.

### 4.3 Capture a short walkthrough

Produce a short demonstration video or animated walkthrough showing the actual agent interaction.

Suggested sequence:

1. Developer asks an architecture question.
2. Agent invokes AIP.
3. AIP returns qualified findings.
4. Agent resolves the supporting evidence.
5. Developer receives an actionable, evidence-backed explanation.

Target duration: approximately 90–120 seconds.

Record actual tool interactions. Do not present simulated output as a live demonstration.

### 4.4 I2 acceptance

- At least one supported coding-agent client completes the workflow.
- MCP tool discovery and calls work against the v0.5.1 demonstration.
- Evidence resolution remains snapshot-consistent.
- The agent communicates unresolved and unsupported findings accurately.
- The complete workflow is reproducible through documented instructions.

Additional clients may be checked opportunistically, but recreating a comprehensive four-client qualification matrix is not a release requirement.

## 5. I3 — Documentation, Presentation & Release

**Goal:** Make the demonstration the primary entry point to the project.

### 5.1 README redesign

The README should lead with what a user can accomplish, not an explanation of AIP's internal components.

Suggested opening:

> **Understand your architecture from evidence, not assumptions.**
>
> AIP reconciles declared APIs, runtime observations, messaging contracts, and deployment information into evidence-qualified architecture context for developers and coding agents.

Immediately follow this with:

- a screenshot or short animation of the demonstration;
- the one-command Quick Start;
- three representative architecture questions;
- a link to the guided walkthrough.

Update outdated examples and transport references to match v0.5.0's actual public contract.

The README should remain concise. Detailed internals belong in the existing technical documentation.

### 5.2 Demo documentation

Provide one focused walkthrough:

`demo/README.md`

It should explain how to start, explore, connect an agent, and stop the demonstration.

Document the expected findings, particularly LegacyPricingService, deployment identity conflict, and Pub/Sub distinctions.

Describe limitations explicitly without overwhelming the introductory experience.

### 5.3 Presentation assets

Create reusable material for sharing AIP:

- one overview screenshot showing the interactive architecture;
- one screenshot showing a finding and its evidence;
- one short video demonstrating the end-to-end experience.

These should be suitable for the GitHub README, external project discussions, and a LinkedIn demonstration.

The existing video assets and rendering infrastructure should be reused where practical.

### 5.4 Release

Use normal CI, integration tests, deterministic evaluation, and a clean demonstration run.

Release qualification is limited to verifying that the documented experience works against the intended v0.5.1 artifact and that existing architecture semantics remain intact.

No new evaluation methodology, extensive completion records, or multi-stage release qualification framework is required.

Publication remains an explicit owner decision.

## 6. Non-Goals

The following are excluded from v0.5.1:

- new discovery source families;
- gRPC/protobuf support;
- live Kubernetes access;
- live broker discovery;
- locality-qualified architecture claims;
- Architecture Intent and Assessment;
- additional MCP tools;
- LLM-based architecture inference;
- a general-purpose graph editor;
- user accounts, authentication, or hosted SaaS deployment;
- a comprehensive frontend redesign;
- mandatory GT/Moldable Development integration;
- new release governance infrastructure.

AIP's deterministic, evidence-qualified semantic core remains the authority.

The demonstration must not introduce an alternative architecture reasoning engine in the presentation layer.

## 7. Delivery Plan

Three implementation increments are sufficient.

| Increment | Deliverable | Demonstration value |
|---|---|---|
| I1 | One-command demo and interactive architecture exploration | Users can experience AIP directly. |
| I2 | Working coding-agent demonstration | Developers see how AIP improves agent architecture context. |
| I3 | README, walkthrough, presentation assets, release | New users can discover and reproduce the experience. |

Each increment should produce something that can actually be demonstrated.

Prefer a small number of coherent PRs over artificially subdividing work into ceremonial slices.

## 8. Definition of Done

v0.5.1 is complete when a new user can:

1. Clone AIP and launch the demonstration with one command.
2. See an architecture overview with meaningful relationship distinctions.
3. Investigate an undocumented runtime dependency.
4. Inspect the evidence supporting a claim.
5. Understand why AIP refuses to resolve a conflicting deployment identity.
6. Explore the existing messaging semantics.
7. Connect a coding agent and receive an evidence-backed architecture explanation.

All seven interactions must work against actual AIP behavior.

The fundamental release criterion is simple:

**AIP's value should be visible through using the product, not through reading its specification.**