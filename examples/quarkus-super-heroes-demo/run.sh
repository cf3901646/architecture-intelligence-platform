#!/usr/bin/env bash
# v0.5.1 Quarkus Super Heroes demo (spec §4): one command, a replay of already-qualified evidence.
#
#   examples/quarkus-super-heroes-demo/run.sh          start, import, replay, check, print prompt
#   examples/quarkus-super-heroes-demo/run.sh --down   stop and delete the demo's data
#
# Needs only docker (with Compose) and curl. See README.md and PROVENANCE.md.
set -euo pipefail

DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$DEMO_DIR/../.." && pwd)"
# Run-local state lives outside examples/, which the v0.5.0 release golden path pins file by file.
RUN_DIR="$REPO_ROOT/.aip-qsh-demo"
AIP_URL="http://localhost:8000"
COLLECTOR_URL="http://localhost:4318"
ENVIRONMENT="quarkus-i5"
WINDOW_START="2026-09-25T13:06:47Z"
WINDOW_END="2026-09-25T13:06:54Z"

compose() {
  docker compose -p aip-qsh-demo --project-directory "$REPO_ROOT" \
    -f "$DEMO_DIR/docker-compose.yml" --env-file /dev/null "$@"
}

fail() {
  echo "error: $*" >&2
  exit 1
}

if [[ "${1:-}" == "--down" ]]; then
  QSH_DEMO_NEO4J_PASSWORD=unused compose down -v --remove-orphans
  rm -rf "$RUN_DIR"
  echo "Demo stopped and its data deleted."
  exit 0
fi
[[ $# -eq 0 ]] || { echo "usage: $0 [--down]" >&2; exit 2; }

for tool in docker curl; do
  command -v "$tool" >/dev/null || fail "'$tool' is required"
done
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

mkdir -p "$RUN_DIR"
if [[ ! -s "$RUN_DIR/neo4j-password" ]]; then
  (umask 077 && head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n' >"$RUN_DIR/neo4j-password")
fi
QSH_DEMO_NEO4J_PASSWORD="$(cat "$RUN_DIR/neo4j-password")"
export QSH_DEMO_NEO4J_PASSWORD

if [[ -n "$(compose ps -q 2>/dev/null)" ]]; then
  fail "the demo is already running; use '$0 --down' first for a fresh replay"
fi
for port in 8000 4318; do
  if (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
    fail "port $port is in use (the minimal demo also uses 8000); stop it first"
  fi
done

echo "==> Starting AIP, Neo4j and the OpenTelemetry Collector (first run builds the AIP image)"
compose up -d --build --wait

echo "==> Importing the frozen dossier declarations, Kubernetes manifest and messaging overlay"
curl -sS --fail-with-body -X POST "$AIP_URL/api/import" -o "$RUN_DIR/import.json" \
  || fail "import failed: $(cat "$RUN_DIR/import.json" 2>/dev/null)"

fence() {
  compose exec -T architecture-intelligence python examples/runtime-demo/read_revision_fence.py --json \
    | tr -dc '0-9'
}

echo "==> Replaying the frozen OpenTelemetry observation window"
before="$(fence)"
curl -sS --fail-with-body -X POST "$COLLECTOR_URL/v1/traces" -H 'content-type: application/json' \
  --data-binary "@$DEMO_DIR/otlp.json" >/dev/null || fail "the collector rejected otlp.json"
last=""
for _ in $(seq 1 30); do
  sleep 3
  current="$(fence)"
  if [[ -n "$current" && "$current" != "$before" && "$current" == "$last" ]]; then
    break
  fi
  last="$current"
done
[[ -n "$current" && "$current" != "$before" && "$current" == "$last" ]] \
  || fail "the replayed observations were not ingested within 90s"

echo "==> Checking the rest-fights answer against the frozen evidence"
compose exec -T architecture-intelligence python qsh/check_ready.py <"$RUN_DIR/import.json" \
  >"$RUN_DIR/dependencies.json" || { cat "$RUN_DIR/dependencies.json" >&2; exit 1; }

cat >"$RUN_DIR/context.json" <<JSON
{
  "mcp_url": "$AIP_URL/mcp",
  "service_id": "service:rest-fights",
  "observation_context": {
    "environment": "$ENVIRONMENT",
    "window_start": "$WINDOW_START",
    "window_end": "$WINDOW_END"
  }
}
JSON

cat >"$RUN_DIR/prompt.txt" <<PROMPT
We need to change the image-narration behavior in rest-fights. Before touching the code, use the
AIP MCP server to establish its dependencies, deployment context, observed behavior, supporting
evidence and unresolved integration boundaries.

Query service:rest-fights with environment "$ENVIRONMENT", window_start "$WINDOW_START" and
window_end "$WINDOW_END". Use get_service_dependencies, get_architecture_drift and get_evidence,
and resolve evidence at the snapshot the answer returned. Group dependencies by target and
operation. Keep facts returned by AIP apart from your own suggestions, and do not guess
unresolved identities. The answer's limitations list what AIP knows it could not resolve; they do
not mean every other dependency of the application is known.
PROMPT

cat <<DONE

Quarkus Super Heroes demo is ready (a replay; nothing is ingesting any more).

  MCP server:  $AIP_URL/mcp   (standard negotiated MCP, no API key needed)
  REST:        $AIP_URL/api/services/service:rest-fights/dependencies?environment=$ENVIRONMENT&from=$WINDOW_START&to=$WINDOW_END
  Window:      $ENVIRONMENT, $WINDOW_START to $WINDOW_END

Agent prompt (also in $RUN_DIR/prompt.txt):

$(sed 's/^/  /' "$RUN_DIR/prompt.txt")

Stop and delete the demo's data with: $0 --down
DONE
