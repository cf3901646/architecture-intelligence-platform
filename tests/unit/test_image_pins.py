"""Every container image outside `docs/` is pinned by digest, so a dev stack, test run, demo or
release build can't silently change underneath us when an upstream tag moves.

`docs/` is excluded because its compose files are historical real-world-validation evidence with
their own frozen conventions. Dependabot bumps the Dockerfile and compose pins; the testcontainers
Neo4j literals aren't visible to it, so they must match `docker-compose.yml`'s pin - a Dependabot
bump of that pin fails here until the literals follow.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_DIGEST_PINNED = re.compile(r"^[^\s@]+:[^\s@]+@sha256:[0-9a-f]{64}$")
_COMPOSE_IMAGE = re.compile(r"^\s*image:\s*(\S+)\s*$", re.MULTILINE)
_DOCKERFILE_IMAGE = re.compile(r"^\s*(?:FROM\s+(\S+)|COPY\s+--from=(\S+)\s)", re.MULTILINE)
_NEO4J_CONTAINER = re.compile(r'Neo4jContainer\(\s*"([^"]+)"')


def _tracked(pattern: str) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--", pattern],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        REPO_ROOT / line
        for line in result.stdout.splitlines()
        if line and not line.startswith("docs/")
    ]


def _image_refs() -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for pattern in ("*docker-compose*.yml", "*docker-compose*.yaml"):
        for path in _tracked(pattern):
            for image in _COMPOSE_IMAGE.findall(path.read_text()):
                # An image supplied by the caller (e.g. the golden path's released image) is pinned
                # by that caller, not here.
                if not image.startswith("${"):
                    refs.append((str(path.relative_to(REPO_ROOT)), image))
    for path in _tracked("*Dockerfile*"):
        for base, copy_from in _DOCKERFILE_IMAGE.findall(path.read_text()):
            refs.append((str(path.relative_to(REPO_ROOT)), base or copy_from))
    for path in _tracked("*.py"):
        for image in _NEO4J_CONTAINER.findall(path.read_text()):
            refs.append((str(path.relative_to(REPO_ROOT)), image))
    return refs


def _dev_compose_neo4j_ref() -> str:
    images = _COMPOSE_IMAGE.findall((REPO_ROOT / "docker-compose.yml").read_text())
    [neo4j_ref] = [image for image in images if image.startswith("neo4j:")]
    return neo4j_ref


def test_image_references_are_found():
    sources = {source for source, _ in _image_refs()}
    assert {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.demo.yml",
        "examples/runtime-demo/Dockerfile",
        "tests/integration/conftest.py",
    } <= sources


@pytest.mark.parametrize(("source", "image"), _image_refs())
def test_image_is_pinned_by_digest(source, image):
    assert _DIGEST_PINNED.match(image), f"{source}: {image} is not pinned by digest"


def test_testcontainers_neo4j_matches_the_dev_compose_pin():
    expected = _dev_compose_neo4j_ref()
    for path in _tracked("*.py"):
        for image in _NEO4J_CONTAINER.findall(path.read_text()):
            assert image == expected, f"{path.relative_to(REPO_ROOT)}: {image} != {expected}"
    demo_images = _COMPOSE_IMAGE.findall((REPO_ROOT / "docker-compose.demo.yml").read_text())
    assert expected in demo_images
