from app.api.openapi_export import OPENAPI_SNAPSHOT_PATH, render_openapi


def test_committed_openapi_snapshot_matches_generated_openapi():
    committed = OPENAPI_SNAPSHOT_PATH.read_text()
    generated = render_openapi()
    assert committed == generated, (
        "schemas/rest/openapi.json is out of date - the REST API changed. If the change is "
        "deliberate, regenerate it with `uv run python -m app.api.openapi_export` and commit it "
        "with the change so the surface diff is reviewed."
    )


def test_openapi_snapshot_regenerates_deterministically():
    assert render_openapi() == render_openapi()
