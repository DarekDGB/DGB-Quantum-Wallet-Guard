from __future__ import annotations

import re
import tomllib
import unicodedata
from pathlib import Path

ALLOWED_ATTRIBUTION = "DarekDGB"
STALE_PATHS = (
    "/".join(("examples", "dormant_" + "key_sweep_scenario.py")),
    "/".join(("tests", "test_dormant_" + "key_sweep.py")),
)

_GENERATED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "venv",
    }
)
_GENERATED_FILE_NAMES = frozenset({".coverage", "coverage.xml"})
_ATTRIBUTION_LINE = re.compile(
    r"^(?:author(?:\s+attribution)?|co-author|maintainer|"
    r"(?:ai\s+)?(?:engineering\s+)?assistant|created\s+by|developed\s+by|written\s+by)"
    r"\s*:\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
_STRUCTURED_ATTRIBUTION_LINE = re.compile(
    r"""^["'](?:author|author_attribution|maintainer)["']\s*:\s*"""
    r"""["'](?P<value>[^"']+)["']\s*,?\s*$""",
    re.IGNORECASE,
)
_COPYRIGHT_LINE = re.compile(
    r"^copyright\s+(?:\(c\)|\N{COPYRIGHT SIGN})\s+\d{4}(?:-\d{4})?"
    r"(?:\s+(?P<value>.+?))?\s*$",
    re.IGNORECASE,
)


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "pyproject.toml").is_file() and (candidate / "src" / "qwg").is_dir():
            return candidate
    raise AssertionError("repository root not found")


def _is_generated(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return (
        path.name in _GENERATED_FILE_NAMES
        or path.suffix in {".pyc", ".pyo"}
        or any(part in _GENERATED_DIRECTORY_NAMES for part in relative.parts)
        or any(part.endswith(".egg-info") for part in relative.parts)
    )


def _repository_files() -> list[Path]:
    root = _repo_root()
    return sorted(
        path for path in root.rglob("*") if path.is_file() and not _is_generated(path, root)
    )


def _display(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _text_files() -> list[tuple[Path, str]]:
    return [(path, path.read_bytes().decode("utf-8")) for path in _repository_files()]


def _known_mojibake_markers() -> tuple[str, ...]:
    codepoint_sequences = (
        (0x00C2,),
        (0x00C3,),
        (0x00E2, 0x0153),
        (0x00E2, 0x20AC),
        (0x00EF, 0x00BB, 0x00BF),
        (0x00F0, 0x0178),
    )
    return tuple(
        "".join(chr(codepoint) for codepoint in sequence) for sequence in codepoint_sequences
    )


def _plain_metadata_line(line: str) -> str:
    return line.strip().replace("*", "").replace("`", "")


def test_approved_stale_sweep_files_are_absent() -> None:
    root = _repo_root()
    present = [relative for relative in STALE_PATHS if (root / relative).exists()]
    assert present == [], f"approved stale paths remain: {present}"


def test_repository_text_is_strict_utf8_nfc_and_mojibake_free() -> None:
    failures: list[str] = []
    markers = _known_mojibake_markers()

    for path in _repository_files():
        raw = path.read_bytes()
        relative = _display(path)
        if raw.startswith(bytes((0xEF, 0xBB, 0xBF))):
            failures.append(f"{relative}: UTF-8 BOM")
        if bytes((0,)) in raw:
            failures.append(f"{relative}: NUL byte")
        if bytes((13,)) in raw:
            failures.append(f"{relative}: CR byte")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            failures.append(f"{relative}: invalid UTF-8 at byte {exc.start}")
            continue
        if text != unicodedata.normalize("NFC", text):
            failures.append(f"{relative}: text is not NFC-normalized")
        if chr(0xFFFD) in text:
            failures.append(f"{relative}: replacement character")
        if any(0x80 <= ord(character) <= 0x9F for character in text):
            failures.append(f"{relative}: C1 control character")
        if any(marker in text for marker in markers):
            failures.append(f"{relative}: known mojibake marker")

    assert failures == [], "repository text hygiene failures:\n" + "\n".join(failures)


def test_repository_author_attribution_is_darekdgb_only() -> None:
    failures: list[str] = []
    declarations = 0
    noncanonical_name = "An" + "gel"
    noncanonical_name_pattern = re.compile(
        rf"(?<!\w){re.escape(noncanonical_name)}(?!\w)", re.IGNORECASE
    )
    noncanonical_handle = "@" + "Darek" + "_" + "DGB"

    for path, text in _text_files():
        for line_number, line in enumerate(text.splitlines(), start=1):
            if (
                noncanonical_name_pattern.search(line) is not None
                or noncanonical_handle.casefold() in line.casefold()
            ):
                failures.append(f"{_display(path)}:{line_number}: non-canonical attribution token")
                continue
            plain = _plain_metadata_line(line)
            match = _ATTRIBUTION_LINE.fullmatch(plain)
            if match is None:
                match = _STRUCTURED_ATTRIBUTION_LINE.fullmatch(plain)
            if match is not None:
                declarations += 1
                if match.group("value").strip() != ALLOWED_ATTRIBUTION:
                    failures.append(f"{_display(path)}:{line_number}: non-canonical attribution")
                continue
            copyright_match = _COPYRIGHT_LINE.fullmatch(plain)
            if copyright_match is not None and copyright_match.group("value") is not None:
                declarations += 1
                if copyright_match.group("value").strip() != ALLOWED_ATTRIBUTION:
                    failures.append(
                        f"{_display(path)}:{line_number}: non-canonical copyright owner"
                    )

    project = tomllib.loads((_repo_root() / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    package_authors = project.get("authors", [])
    declarations += len(package_authors)
    if not package_authors or any(
        author.get("name") != ALLOWED_ATTRIBUTION for author in package_authors
    ):
        failures.append(
            "pyproject.toml: project authors must contain only the canonical attribution"
        )

    assert declarations > 0, "no author attribution declarations found"
    assert failures == [], "author attribution lock failures:\n" + "\n".join(failures)


def test_stale_repository_identity_is_absent() -> None:
    stale_identity = "-".join(("DigiByte", "Quantum", "Wallet", "Guard"))
    findings: list[str] = []

    for path, text in _text_files():
        for line_number, line in enumerate(text.splitlines(), start=1):
            if stale_identity in line:
                findings.append(f"{_display(path)}:{line_number}")

    assert findings == [], "stale repository identity remains:\n" + "\n".join(findings)


def test_python_requirement_metadata_is_locked() -> None:
    project = tomllib.loads((_repo_root() / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    assert project.get("requires-python") == ">=3.11"


def test_retired_sweep_api_implementation_claims_are_absent() -> None:
    retired_tokens = ("QWG" + "Engine", "process_" + "sweep_event", *STALE_PATHS)
    findings: list[str] = []

    for path, text in _text_files():
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(token in line for token in retired_tokens):
                findings.append(f"{_display(path)}:{line_number}")

    assert findings == [], "retired implementation claims remain:\n" + "\n".join(findings)
