# Quarkus Super Heroes demo: input provenance

The demo reuses the frozen v0.5.0 I5 dossier
([`docs/real-world-validation/v0.5.0/quarkus-super-heroes/`](../../docs/real-world-validation/v0.5.0/quarkus-super-heroes/),
upstream pin `8ea03377bfe7a89c49e1ccc0e501bf5fafbc2cce`) and adds two demo-owned inputs. Neither is
upstream-supplied, and neither is qualification evidence.

| Input | Kind | Origin |
|---|---|---|
| Dossier `runtime/declarations/` (4 OpenAPI, the `rest-fights` manifest, identity bindings), `runtime/k8s/namespaced/`, `runtime/mapping.yaml` | Dossier inputs, mounted unmodified | See the dossier's `profile.md` |
| [`overlay/`](overlay/) | **Operator-authored** AsyncAPI declaration | This demo |
| [`otlp.json`](otlp.json) | **Transcription** of observed evidence | The final-candidate evidence records |

## `overlay/`: operator-authored AsyncAPI for Kafka `fights`

Quarkus Super Heroes ships no AsyncAPI, so the dossier records Kafka `fights` as unsupported. The
overlay declares what the upstream code does, as a team would:

- `rest-fights` publishes to topic `fights`: `@Channel("fights") MutinyEmitter` at
  `rest-fights/.../FightService.java:64`, `mp.messaging.outgoing.fights.topic=fights`.
- `event-statistics` consumes it: `@Incoming` at `event-statistics/.../SuperStats.java:59`.
- The `Fight` payload is transcribed from `rest-fights/src/main/avro/fight.avsc`.

(Citations as recorded in the dossier's `ground-truth.md`, "Kafka `fights`".)

Under the existing v0.5.0 I4 rules, the accepted overlay gives AIP **declaration evidence** for
`rest-fights` `PUBLISHES_TO` Topic `fights`. It gives no upstream provenance and no runtime
confirmation: the real producer spans carry only the legacy `messaging.operation` key, which stays
unsupported, and none are replayed. The consumer side deliberately has no
`x-aip-subscription-name`, because a Kafka consumer group is never a Subscription. AIP therefore
omits it (`SUBSCRIPTION_IDENTITY_MISSING`) and names no consumer.

## `otlp.json`: transcribed runtime observation

The dossier keeps no raw OTLP bytes. `otlp.json` is transcribed from the three `OBSERVED` evidence
records in
[`final-candidate/quarkus-super-heroes/artifacts/public-surfaces/evidence_service_rest-fights_batch_0.rest.json`](../../docs/real-world-validation/v0.5.0/final-candidate/quarkus-super-heroes/artifacts/public-surfaces/evidence_service_rest-fights_batch_0.rest.json):
one `CLIENT_SERVER` call each from `rest-fights` to `GET /api/villains/random`,
`GET /api/heroes/random` and `POST /api/narration`, with `service.version` `1.0`, environment
`quarkus-i5` and each server span ending at the record's `first_seen`. Span names, ids and the few
milliseconds of span duration are authored. It is not the original capture, and it contains no gRPC
or Kafka spans.
