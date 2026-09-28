"""Recomputes the frozen v0.6.0 I1 contract vectors (docs/specifications/0.6.0/i1-vectors/).

The vectors are authored by hand from the I1 support matrix. This module checks them with the
standard library only and deliberately imports nothing from `app/`: it is an independent reference
for the frozen contract, not a test of AIP's implementation (I1 §13, §14).
"""

import hashlib
import json
import re
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "docs" / "specifications" / "0.6.0"
VECTORS = SPEC_DIR / "i1-vectors"

_DAY = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def _load(name: str) -> dict:
    return json.loads((VECTORS / name).read_text(encoding="utf-8"))


def _serialize(value: datetime) -> str:
    utc_value = value.astimezone(UTC)
    return utc_value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc_value.microsecond:06d}Z"


def _parse_day(value: str) -> date | None:
    if not _DAY.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _window(first: str, last: str) -> tuple[datetime, datetime] | None:
    first_day, last_day = _parse_day(first), _parse_day(last)
    if first_day is None or last_day is None or first_day > last_day:
        return None
    start = datetime(first_day.year, first_day.month, first_day.day, tzinfo=UTC)
    # Normalized end: (last_day + 1 day) at midnight UTC minus 1 µs. The offset is summed first so
    # 9999-12-31 (whose next midnight is not representable) does not overflow.
    last_midnight = datetime(last_day.year, last_day.month, last_day.day, tzinfo=UTC)
    end = last_midnight + (timedelta(days=1) - timedelta(microseconds=1))
    return start, end


def _parse_instant(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


DAY_WINDOW = _load("utc-day-window.json")
WINDOWS = {w["id"]: w for w in DAY_WINDOW["windows"]}


@pytest.mark.parametrize("vector", DAY_WINDOW["windows"], ids=lambda v: v["id"])
def test_day_window_normalization(vector: dict) -> None:
    bounds = _window(vector["first_day"], vector["last_day"])
    if not vector["valid"]:
        assert bounds is None
        return
    assert bounds is not None
    assert (_serialize(bounds[0]), _serialize(bounds[1])) == (vector["start"], vector["end"])


@pytest.mark.parametrize("vector", DAY_WINDOW["membership"], ids=lambda v: v["id"])
def test_day_window_membership_is_inclusive(vector: dict) -> None:
    window = WINDOWS[vector["window"]]
    bounds = _window(window["first_day"], window["last_day"])
    instant = _parse_instant(vector["instant"])
    assert bounds is not None and instant is not None
    assert (bounds[0] <= instant <= bounds[1]) is vector["included"]


@pytest.mark.parametrize("vector", DAY_WINDOW["utc_day_assignment"], ids=lambda v: v["id"])
def test_utc_day_assignment(vector: dict) -> None:
    instant = _parse_instant(vector["instant"])
    assert instant is not None
    assert instant.astimezone(UTC).date().isoformat() == vector["utc_day"]


@pytest.mark.parametrize("vector", DAY_WINDOW["capture_instant_parsing"], ids=lambda v: v["id"])
def test_capture_instant_requires_explicit_offset(vector: dict) -> None:
    assert (_parse_instant(vector["value"]) is not None) is vector["parsable"]


def _utc_day(value: str) -> str:
    instant = _parse_instant(value)
    assert instant is not None
    return instant.astimezone(UTC).date().isoformat()


@pytest.mark.parametrize("vector", DAY_WINDOW["timestamp_roles"], ids=lambda v: v["id"])
def test_timestamp_roles(vector: dict) -> None:
    client_day, fact_day = _utc_day(vector["client_timestamp"]), _utc_day(vector["fact_timestamp"])
    # v1 is always bucketed by the accepted fact timestamp; ingestion guard I-4 compares UTC days.
    assert fact_day == vector["v1_bucket_day"]
    assert (client_day == fact_day) is vector["i4_passes"]
    if not vector["i4_passes"]:
        assert vector["reason"] == "LOCALITY_CLIENT_FACT_DAY_MISMATCH"
        assert "v2_bucket_utc_day" not in vector
        return
    # v2 takes its day and first/last_seen from the accepted fact timestamp, never the CLIENT's.
    assert vector["v2_bucket_utc_day"] == fact_day
    fact = _parse_instant(vector["fact_timestamp"])
    assert fact is not None
    assert vector["v2_first_seen"] == vector["v2_last_seen"] == _serialize(fact)


def test_vector_ids_are_unique() -> None:
    ids = [
        v["id"]
        for group in ("windows", "membership", "utc_day_assignment")
        for v in DAY_WINDOW[group]
    ]
    ids += [v["id"] for v in DAY_WINDOW["capture_instant_parsing"]]
    ids += [v["id"] for v in DAY_WINDOW["timestamp_roles"]]
    assert len(ids) == len(set(ids))


def _spec_reason_codes() -> set[str]:
    spec = (SPEC_DIR / "i1-locality-and-evidence-applicability.md").read_text(encoding="utf-8")
    block = spec.split("Internal diagnostic codes", 1)[1].split("```", 2)[1]
    return set(re.findall(r"LOCALITY_[A-Z0-9_]+", block))


def test_support_matrix_uses_only_frozen_reason_codes() -> None:
    frozen = _spec_reason_codes()
    assert len(frozen) == 23
    matrix = (SPEC_DIR / "i1-locality-support-matrix.md").read_text(encoding="utf-8")
    used = set(re.findall(r"LOCALITY_[A-Z0-9_]+", matrix))
    assert used <= frozen, sorted(used - frozen)


# --- I1.3 scoped observed-evidence v2 (i1-scoped-evidence-v2-contract.md) ---

V2 = _load("v2-evidence-id.json")
KEY_VECTORS = {v["id"]: v for v in V2["key_vectors"]}
V2_PREFIX = "evidence:otel:calls-scoped:v2:"
V2_KEY_FIELDS = {
    "contract_version",
    "source_type",
    "evidence_type",
    "relation_type",
    "environment",
    "bucket_utc_day",
    "subject_id",
    "object_id",
    "caller_cluster_uid",
    "caller_pod_uid",
}
V2_ENTRY_FIELDS = V2_KEY_FIELDS | {
    "id",
    "first_seen",
    "last_seen",
    "observation_count",
    "correlation_mode",
    "sample_trace_ids",
    "k8s_namespace_name",
    "k8s_pod_name",
    "k8s_deployment_name",
    "k8s_statefulset_name",
    "k8s_daemonset_name",
    "conflicting_consistency_attributes",
    "key_rule_id",
    "key_rule_version",
    "normalization_rule_id",
    "normalization_rule_version",
}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _v2_id(key: dict) -> str:
    return V2_PREFIX + hashlib.sha256(_canonical(key)).hexdigest()


@pytest.mark.parametrize("vector", V2["key_vectors"], ids=lambda v: v["id"])
def test_v2_key_vector(vector: dict) -> None:
    key = vector["input"]
    assert set(key) == V2_KEY_FIELDS
    assert isinstance(key["contract_version"], int) and key["contract_version"] == 2
    assert _canonical(key) == vector["canonical_bytes_utf8"].encode("utf-8")
    assert hashlib.sha256(_canonical(key)).hexdigest() == vector["sha256"]
    assert _v2_id(key) == vector["evidence_id"]


def test_v2_key_distinctions() -> None:
    ids = {name: v["evidence_id"] for name, v in KEY_VECTORS.items()}
    assert ids["V02-reordered-input"] == ids["V01-base"]  # L01
    assert list(KEY_VECTORS["V02-reordered-input"]["input"]) != list(
        KEY_VECTORS["V01-base"]["input"]
    )
    assert ids["V03-distinct-pod"] != ids["V01-base"]  # L02
    assert ids["V04-same-pod-uid-other-cluster"] != ids["V01-base"]  # L03
    distinct = {k: v for k, v in ids.items() if k != "V02-reordered-input"}
    assert len(set(distinct.values())) == len(distinct)


def test_v2_non_ascii_is_raw_utf8() -> None:
    vector = KEY_VECTORS["V05-non-ascii-environment"]
    assert "ü" in vector["canonical_bytes_utf8"] and "\\u" not in vector["canonical_bytes_utf8"]


@pytest.mark.parametrize("vector", V2["v1_unchanged"], ids=lambda v: v["id"])
def test_v1_id_has_no_pod_or_cluster_component(vector: dict) -> None:
    digest = hashlib.sha256(vector["seed_utf8"].encode("utf-8")).hexdigest()[:12]
    assert digest == vector["sha256_first12"]
    assert (
        vector["evidence_id"]
        == f"evidence:otel:{vector['environment']}:{vector['bucket_day']}:{digest}"
    )
    for name in vector["same_as_v2"]:
        key = KEY_VECTORS[name]["input"]
        seed = f"{key['subject_id']}|{key['relation_type']}|{key['object_id']}"
        assert (key["environment"], key["bucket_utc_day"], seed) == (
            vector["environment"],
            vector["bucket_day"],
            vector["seed_utf8"],
        )


def test_v2_snapshot_fragment() -> None:
    fragment = V2["snapshot_fragment"]
    entries = fragment["entries"]
    assert fragment["state_key"] == "scoped_observed_calls_v2"
    assert entries, "the conditional key is never present with an empty list"
    assert _canonical(entries) == fragment["canonical_bytes_utf8"].encode("utf-8")
    assert hashlib.sha256(_canonical(entries)).hexdigest() == fragment["sha256"]
    assert [e["id"] for e in entries] == sorted(e["id"] for e in entries)
    for entry in entries:
        assert set(entry) == V2_ENTRY_FIELDS
        assert entry["id"] == _v2_id({f: entry[f] for f in V2_KEY_FIELDS})
        assert entry["sample_trace_ids"] == sorted(set(entry["sample_trace_ids"]))[:5]
        conflicts = entry["conflicting_consistency_attributes"]
        assert conflicts == sorted(set(conflicts))
        assert all(entry[name] is None for name in conflicts)
        assert entry["first_seen"] <= entry["last_seen"]


def test_no_v2_snapshot_pin_matches_golden_path() -> None:
    pin = V2["no_v2_snapshot_pin"]
    expected = (ROOT / pin["source"]).read_text(encoding="utf-8")
    assert f'"actual_snapshot_id": "{pin["snapshot_id"]}"' in expected
