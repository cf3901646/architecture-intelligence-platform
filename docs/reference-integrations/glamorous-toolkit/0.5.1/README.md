# AIP × Glamorous Toolkit — v0.5.1 Quarkus integration

**AIP release:** v0.5.1 (public schema `"0.5"`)  
**GT baseline:** fresh official [GT 1.1.601](https://github.com/feenkcom/gtoolkit/releases/tag/v1.1.601), bundling gt4llm v0.7.304  
**Status:** integration workspace; preserve the separately [validated v0.4.2 PoCs](../0.4.2/README.md) as historical evidence. Do not treat their PASS results as a new v0.5.1 agent/client requalification.

## Starting point

The reproducible evidence source is the published [Quarkus Super Heroes replay](../../../../examples/quarkus-super-heroes-demo/README.md) and its [Q1–Q8 walkthrough](../../../../examples/quarkus-super-heroes-demo/walkthrough.md). It starts no live Quarkus system. AIP exposes exactly three read-only [MCP tools](../../../mcp.md) at `http://127.0.0.1:8000/mcp`.

Query `service:rest-fights` with environment `quarkus-i5` and window `2026-09-25T13:06:47Z` to `2026-09-25T13:06:54Z`. The clean replay contains seven operation-level HTTP claims (three confirmed, four not observed in this window), a configured `DEPLOYED_AS`, and an operator-authored AsyncAPI `PUBLISHES_TO` Topic `fights` claim with unresolved subscription identity. Preserve the complete answer, limitations, both evidence-ref roles and its returned snapshot.

## Reuse rather than rebuild

1. Retain the existing local `GtAipMcpClient` + `GtAipArchitectureAnswer` query/Inspector layer after its independent connection checks.
2. Selectively reuse the historical [PoC 2 evidence models](../0.4.2/poc-2-evidence-exploration.md), [PoC 3 agentic investigation](../0.4.2/poc-3-agentic-architecture-exploration.md), and [PoC 4 bounded ephemeral micro-tools](../0.4.2/poc-4-dynamic-moldable-tools.md). The historical [Architecture Explorer installer](../0.4.2/architecture-explorer-install.st) expects AIP-specific classes to exist; it is not a standalone loader.
3. In the new launcher replace `GtAipMcpStructuredFunctionTool toolsForClient: mcpClient` with upstream `mcpClient llmFunctionTools`. The local adapter is no longer required because [gt4llm PR #12](https://github.com/feenkcom/gt4llm/pull/12) was merged and is included in GT 1.1.601. Do not override bundled gt4llm classes.
4. Replace the old OrderService standing context and hardcoded ephemeral rows with Quarkus-specific questions. Preserve the original grounded, snapshot-bound evidence lookup and developer-controlled promotion boundaries.
5. Support `DIRECT_DEPENDENCY` and `DEPLOYED_AS` as distinct claim variants. Never infer deployment identity from matching names, Kafka Subscription identity from consumer groups, or an unused operation from `NOT_OBSERVED_IN_WINDOW`.

## Verification gates

- **MCP:** actual GT client negotiation succeeds; the public three tools and complete nested input schemas are visible; `structuredContent` is retained.
- **Inspectors:** nine claims are retained (7 HTTP / 1 messaging / 1 deployment), `PARTIAL` and `UNRESOLVED_IDENTITY` remain visible; evidence is resolved at the originating snapshot.
- **Agent-first:** agent chooses MCP tools and chains evidence without inventing explanations or supported facts.
- **Object-first:** developer selects the MCP-backed GT object, stores it in the existing chat object storage and uses `GtLTools gtObjectsExecution` for navigation.
- **Ephemeral:** an agent can instantiate/populate the existing `GtAipEphemeralMicroTool` with actual Quarkus claim lineage, but does not compile methods or permanently change classes.

Record each v0.5.1 gate only after running it in this image. Add any finished source export, runbook or test evidence **here**, not under `0.4.2/`.
