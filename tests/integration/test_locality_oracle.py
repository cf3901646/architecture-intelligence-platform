"""v0.6.0 I3.2c: the independent I3 oracle executed against the real service on real Neo4j
(I3 spec §14, §15 I3.2 row; `i3-expected-answer-matrix.md`; decision record D15).

Every `mode: "query"` case of `i3-vectors/expected-answers.json` runs here.
- **Answer cases** must match their complete expected `LocalityAnswer` under the matrix §2 procedure
  (`locality_oracle.matcher`). They must also pass the published 0.6 answer schema and the
  `LocalityAnswer` model.
- **Property cases** run their stated steps, then check every `assert` item. The prose
  `equals_expr` items are decided here, per case, from the generated inputs.

The oracle is read-only. A disagreement is a defect in the implementation, or goes back to the
specification; the expectation is never edited to match (I3 §17 stop condition).

Not executed here:
- the evidence-mode cases (X26-X28, P05) and the legacy-reader isolation case (P06) are I3.3,
  which adds that mode and the adapters;
- the request-validation cases (Q01-Q08) are checked by
  `tests/unit/test_v060_i3_expected_answers.py`.

`test_every_query_case_is_executed` pins the partition, so no case can be skipped silently.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from app.architecture_intelligence.locality_contracts import LocalityAnswer, LocalityQueryRequest
from app.architecture_intelligence.request import (
    ArchitectureDriftRequest,
    EvidenceRequest,
    ObservationContextInput,
    ServiceDependenciesRequest,
)
from app.architecture_intelligence.schema_export import LOCALITY_ANSWER_SCHEMA_PATH
from app.architecture_intelligence.service import ArchitectureIntelligenceService
from app.graph.revision_fence import read_revision
from tests.integration.locality_oracle import world
from tests.integration.locality_oracle.matcher import (
    check_property,
    explain_mismatch,
    match,
    resolve,
    substitute,
)
from tests.integration.test_locality_rehearsal_replay import FIXTURE, PRODUCER

DATABASE = world.DATABASE
ORACLE = json.loads(
    (
        Path(__file__).resolve().parents[2]
        / "docs/specifications/0.6.0/i3-vectors/expected-answers.json"
    ).read_text(encoding="utf-8")
)
CASES = {case["id"]: case for case in ORACLE["cases"]}
ANSWER_SCHEMA = json.loads(LOCALITY_ANSWER_SCHEMA_PATH.read_text(encoding="utf-8"))

QUERY_ANSWER_CASES = sorted(
    case_id
    for case_id, case in CASES.items()
    if case["kind"] == "answer" and case["request"]["mode"] == "query"
)
# The rehearsal cases run together, C2 first, so the C1 cases and P08 (defined right after them)
# share one replay (`world.replay_rehearsal` reuses an unchanged replayed snapshot).
REHEARSAL_ANSWER_CASES = ["X03", "X01", "X02"]
K_ANSWER_CASES = [
    case_id for case_id in QUERY_ANSWER_CASES if case_id not in REHEARSAL_ANSWER_CASES
]
QUERY_PROPERTY_CASES = ["P01", "P02", "P03", "P04", "P07", "P08", "P09"]
# I3.3 adds the evidence mode and the legacy-reader isolation checks (I3 spec §15).
I3_3_CASES = ["P05", "P06", "X26", "X27", "X28"]
REQUEST_CASES = sorted(case_id for case_id, case in CASES.items() if case["kind"] == "request")

K_DAY = "2026-09-28"
K_REQUEST = {
    "mode": "query",
    "subject_service_id": "service:orders",
    "environment": "production",
    "first_day": K_DAY,
    "last_day": K_DAY,
}
K_CLUSTER = "11111111-1111-4111-8111-000000000001"
O1 = "operation:service:pricing:GET:/prices"

needs_rehearsal = pytest.mark.skipif(
    not (FIXTURE / "otlp.jsonl").exists(), reason="the rehearsal fixture is not present"
)


def _service(driver) -> ArchitectureIntelligenceService:
    return ArchitectureIntelligenceService(driver, database=DATABASE, producer=PRODUCER)


def _ask(driver, request: dict) -> dict[str, Any]:
    """One query through the semantic service; the answer must pass both validators."""
    answer = _service(driver).get_service_dependencies_by_locality(
        LocalityQueryRequest.model_validate(request)
    )
    payload = json.loads(answer.model_dump_json())
    LocalityAnswer.model_validate(payload)
    errors = [
        error.message
        for error in jsonschema.Draft202012Validator(ANSWER_SCHEMA).iter_errors(payload)
    ]
    assert errors == [], errors
    return payload


def _identity(uid: str) -> dict:
    return {"cluster_uid": K_CLUSTER, "namespace": "shop", "kind": "Deployment", "uid": uid}


# --- The partition -------------------------------------------------------------------------------


def test_every_query_case_is_executed():
    executed = set(QUERY_ANSWER_CASES) | set(QUERY_PROPERTY_CASES)
    assert executed.isdisjoint(I3_3_CASES)
    assert executed | set(I3_3_CASES) | set(REQUEST_CASES) == set(CASES)
    assert len(QUERY_ANSWER_CASES) == 25 and QUERY_ANSWER_CASES[0] == "X01"
    rehearsal = {c for c in QUERY_ANSWER_CASES if CASES[c]["inputs"]["world"] == "rehearsal"}
    assert rehearsal == set(REHEARSAL_ANSWER_CASES)
    property_cases = {case_id for case_id, case in CASES.items() if case["kind"] == "property"}
    assert property_cases == set(QUERY_PROPERTY_CASES) | {"P05", "P06"}


# --- Answer cases --------------------------------------------------------------------------------


def _assert_answer_matches(driver, tmp_path, case_id: str) -> None:
    case = CASES[case_id]
    prebound = world.build(driver, tmp_path, case["inputs"])

    actual = _ask(driver, substitute(case["request"], prebound))

    expected = case["expected"]
    assert match(expected, actual, prebound) is not None, (
        explain_mismatch(substitute(expected, prebound), actual) or "no injective binding matches",
        json.dumps(actual, indent=1, sort_keys=True),
    )


@needs_rehearsal
@pytest.mark.parametrize("case_id", REHEARSAL_ANSWER_CASES)
def test_the_rehearsal_answer_matches_the_oracle(driver, tmp_path, case_id):
    _assert_answer_matches(driver, tmp_path, case_id)


@needs_rehearsal
def test_p08_a_c1_snapshot_is_refused_after_c2(driver, tmp_path):
    world.replay_rehearsal(driver, "c1")
    request = {
        **K_REQUEST,
        "environment": "locality-capture",
        "first_day": "2026-09-30",
        "last_day": "2026-09-30",
    }
    first = _ask(driver, request)
    world.import_rehearsal_capture(driver, tmp_path, "c2")
    stale = _ask(driver, {**request, "snapshot_id": first["snapshot"]["snapshot_id"]})
    latest = _ask(driver, request)

    _check("P08", {1: first, 3: stale, 4: latest})


@pytest.mark.parametrize("case_id", K_ANSWER_CASES)
def test_the_answer_matches_the_oracle(driver, tmp_path, case_id):
    _assert_answer_matches(driver, tmp_path, case_id)


# --- Property cases ------------------------------------------------------------------------------


def _check(case_id: str, steps: dict[int, Any], custom: dict[str, bool] | None = None) -> None:
    for item in CASES[case_id]["assert"]:
        check_property(item, steps, custom)


def _generated_ids(inputs: dict) -> list[str]:
    return sorted(world.v2_id(v2) for v2 in world.generated_v2(inputs))


def test_p01_s_5_and_500_candidates_read_k_400(driver, tmp_path):
    inputs = CASES["P01"]["inputs"]
    world.build(driver, tmp_path, inputs)

    step = _ask(driver, K_REQUEST)

    path = "cursor(data.inventory.next_cursor).after_id"
    _check("P01", {1: step}, {path: resolve(path, step) == _generated_ids(inputs)[399]})


def _two_pages(driver, request: dict) -> tuple[dict, dict]:
    first = _ask(driver, request)
    cursor = first["data"]["inventory"]["next_cursor"]
    assert cursor is not None
    return first, _ask(driver, {**request, "cursor": cursor})


def test_p02_the_i2_page_boundary_is_walked_on_one_snapshot(driver, tmp_path):
    inputs = CASES["P02"]["inputs"]
    world.build(driver, tmp_path, inputs)

    first, second = _two_pages(driver, K_REQUEST)

    seen = [c["v2_evidence_id"] for page in (first, second) for c in page["data"]["candidates"]]
    _check(
        "P02",
        {1: first, 2: second},
        {
            "union of candidates[*].v2_evidence_id over both pages": sorted(seen)
            == _generated_ids(inputs)
        },
    )


def test_p03_the_workload_cap_splits_a_page_that_i2_did_not_truncate(driver, tmp_path):
    inputs = CASES["P03"]["inputs"]
    world.build(driver, tmp_path, inputs)

    first, second = _two_pages(driver, K_REQUEST)

    seen = [
        locality["workload"]["uid"]
        for page in (first, second)
        for locality in page["data"]["localities"]
    ]
    owners = sorted(pod["owner"]["uid"] for pod in world.generated_pods(inputs))
    _check(
        "P03",
        {1: first, 2: second},
        {"union of localities[*].workload.uid over both pages": sorted(seen) == owners},
    )


def test_p04_a_cursor_for_another_query_or_snapshot_is_refused(driver, tmp_path):
    world.build(driver, tmp_path, CASES["P04"]["inputs"])
    first = _ask(driver, K_REQUEST)
    cursor = first["data"]["inventory"]["next_cursor"]
    assert cursor is not None

    other_query = _ask(driver, {**K_REQUEST, "object_operation_id": O1, "cursor": cursor})
    # Step 3: a graph change - capture B, exactly as the K world defines it (X10's inputs).
    [capture_b] = [c for c in CASES["X10"]["inputs"]["captures"] if c["label"] == "B"]
    world.build_capture(driver, tmp_path, capture_b)
    changed = _ask(driver, {**K_REQUEST, "cursor": cursor})

    _check("P04", {1: first, 2: other_query, 4: changed})


@pytest.mark.parametrize("case_id", CASES["P07"]["inputs"]["inputs_of"])
def test_p07_permuted_import_and_span_order_give_identical_bytes(driver, tmp_path, case_id):
    case = CASES[case_id]
    answers = []
    for reverse in (False, True):
        prebound = world.build(driver, tmp_path / str(reverse), case["inputs"], reverse=reverse)
        answer = _ask(driver, substitute(case["request"], prebound))
        answers.append(json.dumps({**answer, "producer": None}, sort_keys=True))

    _check(
        "P07",
        {},
        {"canonical answer bytes without producer": answers[0] == answers[1]},
    )


def test_p09_the_r5_construction_on_a_partial_inventory_is_unknown(driver, tmp_path):
    world.build(driver, tmp_path, CASES["P09"]["inputs"])

    step = _ask(
        driver,
        {
            **K_REQUEST,
            "compare": [
                _identity("aaaaaaaa-0000-4000-8000-000000000001"),
                _identity("aaaaaaaa-0000-4000-8000-000000000002"),
            ],
        },
    )

    _check("P09", {1: step})


# --- Regressions and isolation (I3 §14 "Regression and isolation"; matrix S15) -----------------


def _graph_state(driver) -> tuple[int, int, int]:
    with driver.session(database=DATABASE) as session:
        nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        relations = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        return read_revision(session), nodes, relations


def _v0_5_answers(driver, snapshot_id: str) -> list[dict]:
    service = _service(driver)
    context = ObservationContextInput(
        environment="production",
        window_start=datetime(2026, 9, 28, tzinfo=UTC),
        window_end=datetime(2026, 9, 28, 23, 59, 59, tzinfo=UTC),
    )
    answers = [
        service.get_service_dependencies(
            ServiceDependenciesRequest(service_id="service:orders", observation_context=context)
        ),
        service.get_architecture_drift(
            ArchitectureDriftRequest(service_id="service:orders", observation_context=context)
        ),
        service.get_evidence(
            EvidenceRequest(evidence_refs=[world.DECLARED_CALLS_EVIDENCE], snapshot_id=snapshot_id)
        ),
    ]
    return [answer.model_dump(mode="json", exclude={"generated_at"}) for answer in answers]


def test_the_locality_query_writes_nothing_and_leaves_v0_5_answers_unchanged(driver, tmp_path):
    case = CASES["X10"]
    prebound = world.build(driver, tmp_path, case["inputs"])
    state = _graph_state(driver)
    snapshot_id = _ask(driver, substitute(case["request"], prebound))["snapshot"]["snapshot_id"]
    before = _v0_5_answers(driver, snapshot_id)

    for case_id in ("X10", "X11", "X14", "X15", "X20", "X24"):
        _ask(driver, substitute(CASES[case_id]["request"], prebound))

    assert _graph_state(driver) == state
    assert _v0_5_answers(driver, snapshot_id) == before


def test_one_snapshot_is_shared_with_the_v0_5_answers_and_no_v2_adds_no_state(driver, tmp_path):
    """No separate fingerprint: the locality answer's snapshot is the canonical one every v0.5
    answer carries. Without v2 (X07), no conditional v2 key enters it (I2 D15.2), so it is the
    snapshot of the same graph without the scoped-evidence operational nodes."""
    prebound = world.build(driver, tmp_path, CASES["X07"]["inputs"])
    answer = _ask(driver, substitute(CASES["X07"]["request"], prebound))
    [dependencies, *_] = _v0_5_answers(driver, answer["snapshot"]["snapshot_id"])
    assert answer["snapshot"] == dependencies["snapshot"]

    with driver.session(database=DATABASE) as session:
        assert session.run("MATCH (v:ScopedObservedCallV2) RETURN count(v) AS c").single()["c"] == 0
        session.run(
            "MATCH (n) WHERE any(label IN labels(n) WHERE label STARTS WITH 'ScopedEvidence') "
            "DETACH DELETE n"
        ).consume()
    assert (
        _ask(driver, substitute(CASES["X07"]["request"], prebound))["snapshot"]
        == (answer["snapshot"])
    )
