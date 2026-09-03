from __future__ import annotations

import ast
import hashlib
import re
import tomllib
import unicodedata
from pathlib import Path

from qwg.v3.v3_2_lock import PACKAGE_VERSION
from qwg.v4 import (
    CANONICALIZATION_PROFILE,
    COMPONENT_ID,
    COMPONENT_ROLE,
    CONTRACT_VERSION,
    KEY_REGISTRY_SCHEMA_VERSION,
    POLICY_VERSION,
    SIGNATURE_BUNDLE_SCHEMA_VERSION,
    VERDICT_SCHEMA_VERSION,
)
from qwg.v4.trust_profile import (
    ALGORITHM_STANDARD_PROFILES,
    OPTIONAL_ALGORITHMS,
    REQUIRED_ALGORITHMS,
    SUPPORTED_ALGORITHMS,
)


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AUTHOR = "DarekDGB"

CONTROLLED_FILES = (
    "pyproject.toml",
    "README.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "docs/qwg/v3/PROOF_PACK.md",
    "docs/qwg/v3/REASON_IDS.md",
    "docs/qwg/v3/RELEASE_STATUS_v3.2.0.md",
    "docs/qwg/v4/CONTRACT.md",
    "docs/qwg/v4/MANIFEST.md",
    "docs/qwg/v4/REAL_CRYPTO_BACKEND.md",
    "docs/qwg/v4/TEST_MATRIX.md",
    "docs/qwg/v4/PROOF_PACK.md",
    "docs/qwg/v4/RELEASE_STATUS_v4.0.0.md",
    "tests/test_v410e1_release_pack_lock.py",
)

REQUIRED_V4_DOCUMENTS = (
    "docs/qwg/v4/CONTRACT.md",
    "docs/qwg/v4/MANIFEST.md",
    "docs/qwg/v4/REAL_CRYPTO_BACKEND.md",
    "docs/qwg/v4/TEST_MATRIX.md",
    "docs/qwg/v4/PROOF_PACK.md",
    "docs/qwg/v4/RELEASE_STATUS_v4.0.0.md",
)

FROZEN_FIXTURES = {
    "tests/fixtures/v4/component_verdict_policy_v1_kat.json": (
        "176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff"
    ),
    "tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json": (
        "b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef"
    ),
}

REAL_OQS_NODES = (
    "tests/test_v48g_real_oqs_mldsa_backend.py::"
    "test_v48g_real_oqs_mldsa65_qwg_backend_round_trip_and_negatives",
    "tests/test_v48h_e_real_oqs_falcon_backend.py::"
    "test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives",
)


def _bytes(relative: str) -> bytes:
    return (ROOT / relative).read_bytes()


def _text(relative: str) -> str:
    return _bytes(relative).decode("utf-8", errors="strict")


def test_v410e1_distribution_author_and_frozen_identities_are_locked() -> None:
    project = tomllib.loads(_text("pyproject.toml"))["project"]

    assert project["version"] == "4.0.0"
    assert project["authors"] == [{"name": EXPECTED_AUTHOR}]
    assert project["description"] == (
        "DGB Quantum Wallet Guard - deterministic Shield v4 wallet-safety "
        "evidence component."
    )

    assert PACKAGE_VERSION == "3.2.0"
    assert COMPONENT_ID == "qwg"
    assert COMPONENT_ROLE == "shield_component_qwg"
    assert CONTRACT_VERSION == 4
    assert VERDICT_SCHEMA_VERSION == "shield.verdict.v2"
    assert CANONICALIZATION_PROFILE == "shield-v4-canon.v1"
    assert POLICY_VERSION == "policy.v1"
    assert SIGNATURE_BUNDLE_SCHEMA_VERSION == "shield.signature_bundle.v1"
    assert KEY_REGISTRY_SCHEMA_VERSION == "shield.key_registry.v1"


def test_v410e1_algorithm_order_profiles_and_role_are_locked() -> None:
    assert REQUIRED_ALGORITHMS == ("classical-ed25519", "ml-dsa")
    assert OPTIONAL_ALGORITHMS == ("fn-dsa",)
    assert SUPPORTED_ALGORITHMS == (
        "classical-ed25519",
        "ml-dsa",
        "fn-dsa",
    )
    assert ALGORITHM_STANDARD_PROFILES == {
        "classical-ed25519": ("rfc8032-ed25519-v1",),
        "ml-dsa": ("fips204-ml-dsa-65-v1",),
        "fn-dsa": ("fips206-draft-falcon1024-v1",),
    }


def test_v410e1_readme_links_complete_release_pack() -> None:
    readme = _text("README.md")
    for relative in REQUIRED_V4_DOCUMENTS:
        assert (ROOT / relative).is_file()
        assert relative in readme

    assert "controlled pre-release; not released and not tagged" in readme
    assert "Candidate tag: `v4.0.0`" in readme


def test_v410e1_frozen_kat_bytes_are_unchanged() -> None:
    proof = _text("docs/qwg/v4/PROOF_PACK.md")
    manifest = _text("docs/qwg/v4/MANIFEST.md")

    for relative, expected in FROZEN_FIXTURES.items():
        actual = hashlib.sha256(_bytes(relative)).hexdigest()
        assert actual == expected
        assert relative in proof or relative in manifest
        assert expected in proof
        assert expected in manifest


def test_v410e1_release_documents_lock_policy_and_authority_boundaries() -> None:
    documents = tuple(_text(relative) for relative in REQUIRED_V4_DOCUMENTS)
    for text in documents:
        normalized = " ".join(text.split())
        assert "classical-ed25519" in normalized
        assert "ml-dsa" in normalized
        assert "fn-dsa" in normalized
        assert "fips206-draft-falcon1024-v1" in normalized
        assert "cannot replace or rescue" in normalized
        assert "not final FIPS 206 proof" in normalized

    combined = " ".join(documents)
    for phrase in (
        "sign or broadcast",
        "consensus",
        "wallet keys",
        "Shield Orchestrator",
        "AdamantineOS remains the final",
    ):
        assert phrase in combined


def test_v410e1_real_oqs_workflow_locks_exact_two_nodes_and_no_skip_guard() -> None:
    workflow = _text(".github/workflows/shield-v4-real-oqs.yml")

    for node in REAL_OQS_NODES:
        path, function = node.split("::", maxsplit=1)
        assert path in workflow
        assert f'--require-testcase "{node}"' in workflow

        tree = ast.parse(_text(path), filename=path)
        function_names = {
            item.name
            for item in tree.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert function in function_names

    assert "--min-tests 2" in workflow
    assert 'SHIELD_V4_REAL_OQS: "1"' in workflow
    assert 'SHIELD_V4_REAL_OQS_FALCON: "1"' in workflow


def test_v410e1_historical_v3_files_are_history_not_pending_tag_instructions() -> None:
    historical = (
        "README.md",
        "CHANGELOG.md",
        "docs/qwg/v3/PROOF_PACK.md",
        "docs/qwg/v3/REASON_IDS.md",
        "docs/qwg/v3/RELEASE_STATUS_v3.2.0.md",
    )
    forbidden = (
        r"do not tag v3\.2\.0",
        r"no v3\.2\.0 tag is allowed",
        r"ready for the `v3\.2\.0`.*only after",
        r"before v3\.2\.0 tagging",
    )

    for relative in historical:
        text = _text(relative)
        assert all(
            re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is None
            for pattern in forbidden
        )


def test_v410e1_release_status_is_candidate_only() -> None:
    status = _text("docs/qwg/v4/RELEASE_STATUS_v4.0.0.md")
    expected = {
        "Status": "CONTROLLED PRE-RELEASE",
        "Release decision": "NOT YET AUTHORIZED",
        "Distribution version": "4.0.0",
        "Candidate tag": "v4.0.0",
        "Tag created": "no",
        "Author attribution": EXPECTED_AUTHOR,
    }

    for field, value in expected.items():
        matches = re.findall(
            rf"^{re.escape(field)}:\s*(.+?)\s*$",
            status,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        assert matches == [value], (field, matches)

    assert "Do not create or move `v4.0.0`" in status


def test_v410e1_controlled_files_are_ascii_strict_utf8_nfc_lf() -> None:
    for relative in CONTROLLED_FILES:
        payload = _bytes(relative)
        text = payload.decode("utf-8", errors="strict")

        assert payload
        assert payload.endswith(b"\n"), relative
        assert not payload.startswith(b"\xef\xbb\xbf"), relative
        assert b"\r" not in payload, relative
        assert b"\x00" not in payload, relative
        assert text.isascii(), relative
        assert text == unicodedata.normalize("NFC", text), relative
        assert EXPECTED_AUTHOR in text, relative


def test_v410e1_coverage_artifacts_are_excluded_from_repository_text_scan() -> None:
    hygiene = _text("tests/test_v49i1_repository_hygiene_lock.py")

    assert 'path.name.startswith(".coverage.")' in hygiene
    assert '".coverage"' in hygiene
