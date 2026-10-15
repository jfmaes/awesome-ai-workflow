from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ultimate-agentic-workflow" / "artifact-manifest.json"
FIXED_FAILURE = "invalid_source_manifest"
EXPECTED_MANIFEST = {
    "schemaVersion": 1,
    "owner": "awesome-ai-workflow",
    "exports": [
        {
            "exportName": "ultimate-agentic-workflow",
            "exportRootRelativePath": "ultimate-agentic-workflow",
            "harnesses": ["claude", "codex"],
        },
        {
            "exportName": "evaluate-tech",
            "exportRootRelativePath": (
                "ultimate-agentic-workflow/assets/claude/skills/evaluate-tech"
            ),
            "harnesses": ["claude", "codex"],
        },
        {
            "exportName": "deep-research",
            "exportRootRelativePath": (
                "ultimate-agentic-workflow/assets/codex/skills/deep-research"
            ),
            "harnesses": ["codex"],
        },
    ],
}

_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", re.ASCII)
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_URL_FORM = re.compile(r"(?:^|/)[A-Za-z][A-Za-z0-9+.-]*:", re.ASCII)
_KNOWN_CREDENTIAL = re.compile(
    r"(?:^|[/._-])(?:"
    r"sk-(?:proj-)?[A-Za-z0-9_-]{16,}|"
    r"sk_(?:live|test)_[A-Za-z0-9_-]{12,}|"
    r"github_pat_[A-Za-z0-9_]{16,}|"
    r"gh[pousr]_[A-Za-z0-9]{20,}|"
    r"glpat-[A-Za-z0-9_-]{12,}|"
    r"xox[baprs]-[A-Za-z0-9-]{16,}|"
    r"AIza[A-Za-z0-9_-]{12,}|"
    r"(?:AKIA|ASIA)[0-9A-Z]{16}|"
    r"eyJ[A-Za-z0-9_-]{12,}"
    r")(?:$|[/._-])",
    re.ASCII | re.IGNORECASE,
)
_CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?:^|[/._-])(?:api[-_]?key|access[-_]?token|auth[-_]?token|token|secret|"
    r"password|authorization|bearer|credential)\s*[:=]\s*[\"']?"
    r"[^/\s\"']{8,}[\"']?(?:$|/)",
    re.ASCII | re.IGNORECASE,
)
_PORTABLE_SEGMENT = re.compile(r"^[A-Za-z0-9._-]+$", re.ASCII)
_WINDOWS_DEVICE = re.compile(
    r"^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$",
    re.ASCII | re.IGNORECASE,
)
_FORBIDDEN_SEGMENTS = {".git", ".cache", "__pycache__", "node_modules"}
_FORBIDDEN_FINAL_SEGMENTS = {
    "installed_plugins.json",
    "known_marketplaces.json",
    "marketplace.json",
}


class _InvalidManifest(Exception):
    pass


def _invalid() -> None:
    raise _InvalidManifest


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _invalid()
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    _invalid()


def _credential_shaped(value: str) -> bool:
    return (
        _KNOWN_CREDENTIAL.search(value) is not None
        or _CREDENTIAL_ASSIGNMENT.search(value) is not None
    )


def _utf8_length(value: str) -> int:
    return len(value.encode("utf-8", errors="strict"))


def _safe_identifier(value: object) -> bool:
    return (
        type(value) is str
        and _IDENTIFIER.fullmatch(value) is not None
        and _utf8_length(value) <= 128
        and not _credential_shaped(value)
    )


def _safe_relative_posix_path(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        if (
            _utf8_length(value) > 512
            or value.startswith("/")
            or "\\" in value
            or _CONTROL.search(value) is not None
            or _URL_FORM.search(value) is not None
            or "://" in value
            or _credential_shaped(value)
        ):
            return False
        segments = value.split("/")
        return (
            len(segments) <= 32
            and all(
                segment not in ("", ".", "..") and _utf8_length(segment) <= 128
                for segment in segments
            )
        )
    except UnicodeError:
        return False


def _validate_manifest(value: object) -> dict[str, Any]:
    if type(value) is not dict or set(value) != {"schemaVersion", "owner", "exports"}:
        _invalid()
    manifest = value
    schema_version = manifest["schemaVersion"]
    if (
        type(schema_version) not in (int, float)
        or schema_version != 1
        or manifest["owner"] != "awesome-ai-workflow"
        or not _safe_identifier(manifest["owner"])
        or type(manifest["exports"]) is not list
        or len(manifest["exports"]) > 4_096
    ):
        _invalid()

    export_names: set[str] = set()
    for declaration in manifest["exports"]:
        if type(declaration) is not dict or set(declaration) != {
            "exportName",
            "exportRootRelativePath",
            "harnesses",
        }:
            _invalid()
        export_name = declaration["exportName"]
        harnesses = declaration["harnesses"]
        if (
            not _safe_identifier(export_name)
            or export_name in export_names
            or not _safe_relative_posix_path(declaration["exportRootRelativePath"])
            or type(harnesses) is not list
            or not 1 <= len(harnesses) <= 2
            or any(type(harness) is not str or harness not in {"claude", "codex"} for harness in harnesses)
            or len(set(harnesses)) != len(harnesses)
        ):
            _invalid()
        export_names.add(export_name)
    return manifest


def _parse_artifact_manifest(source: bytes) -> dict[str, Any]:
    try:
        if type(source) is not bytes or len(source) > 256 * 1024:
            _invalid()
        if source.startswith(b"\xef\xbb\xbf"):
            _invalid()
        value = json.loads(
            source.decode("utf-8", errors="strict"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        return _validate_manifest(value)
    except Exception:
        raise ValueError(FIXED_FAILURE) from None


def _json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _assert_invalid(
    source: bytes,
    capsys: pytest.CaptureFixture[str],
    canary: str | None = None,
) -> None:
    with pytest.raises(ValueError) as caught:
        _parse_artifact_manifest(source)
    assert str(caught.value) == FIXED_FAILURE
    captured = capsys.readouterr()
    if canary:
        assert canary not in str(caught.value)
        assert canary not in captured.out
        assert canary not in captured.err


@dataclass(frozen=True)
class _GitRecord:
    path: bytes
    mode: str
    object_type: str
    object_id: str
    content: bytes


def _git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def _git_tree_records(root: str) -> list[_GitRecord]:
    assert _git("cat-file", "-t", f"HEAD:{root}") == b"tree\n"
    listing = _git("ls-tree", "-r", "-z", f"HEAD:{root}")
    records: list[_GitRecord] = []
    for raw_record in listing.rstrip(b"\0").split(b"\0"):
        header, path = raw_record.split(b"\t", 1)
        mode_bytes, type_bytes, object_id_bytes = header.split(b" ", 2)
        object_type = type_bytes.decode("ascii")
        object_id = object_id_bytes.decode("ascii")
        content = _git("cat-file", "blob", object_id) if object_type == "blob" else b""
        records.append(
            _GitRecord(
                path=path,
                mode=mode_bytes.decode("ascii"),
                object_type=object_type,
                object_id=object_id,
                content=content,
            )
        )
    return records


def _portable_record_path(path: bytes) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    if not 1 <= len(path) <= 512:
        _invalid()
    text = path.decode("utf-8", errors="strict")
    if text.startswith("/") or "\\" in text or ":" in text or _credential_shaped(text):
        _invalid()
    segments = tuple(text.split("/"))
    if len(segments) > 32:
        _invalid()
    for segment in segments:
        if (
            not segment
            or segment in (".", "..")
            or _utf8_length(segment) > 128
            or segment.endswith((".", " "))
            or _PORTABLE_SEGMENT.fullmatch(segment) is None
            or _WINDOWS_DEVICE.fullmatch(segment.split(".", 1)[0]) is not None
        ):
            _invalid()
    folded = tuple(
        "".join(chr(ord(character) + 32) if "A" <= character <= "Z" else character for character in segment)
        for segment in segments
    )
    return text, segments, folded


def _validate_record_paths(records: list[_GitRecord]) -> list[tuple[str, tuple[str, ...], tuple[str, ...]]]:
    paths = [_portable_record_path(record.path) for record in records]
    exact_leaves: set[str] = set()
    folded_leaves: set[str] = set()
    directory_spellings: dict[str, str] = {}
    for text, segments, folded_segments in paths:
        folded_leaf = "/".join(folded_segments)
        if text in exact_leaves or folded_leaf in folded_leaves:
            _invalid()
        exact_leaves.add(text)
        folded_leaves.add(folded_leaf)
        for length in range(1, len(segments)):
            exact_prefix = "/".join(segments[:length])
            folded_prefix = "/".join(folded_segments[:length])
            previous = directory_spellings.get(folded_prefix)
            if previous is not None and previous != exact_prefix:
                _invalid()
            directory_spellings[folded_prefix] = exact_prefix
    for _text, _segments, folded_segments in paths:
        if any("/".join(folded_segments[:length]) in folded_leaves for length in range(1, len(folded_segments))):
            _invalid()
    return paths


def _validate_direct_export_tree(
    export_name: str,
    records: list[_GitRecord],
) -> list[_GitRecord]:
    try:
        if type(records) is not list or not records or len(records) > 16_384:
            _invalid()
        if any(
            type(record) is not _GitRecord
            or record.object_type != "blob"
            or record.mode not in {"100644", "100755"}
            or len(record.content) > 16 * 1024 * 1024
            for record in records
        ):
            _invalid()
        if sum(len(record.content) for record in records) > 256 * 1024 * 1024:
            _invalid()
        paths = _validate_record_paths(records)
        for record, (text, segments, _folded) in zip(records, paths, strict=True):
            if any(segment in _FORBIDDEN_SEGMENTS for segment in segments):
                _invalid()
            if segments[-1] in _FORBIDDEN_FINAL_SEGMENTS:
                _invalid()
            if ".claude-plugin" in segments and not (
                export_name == "ultimate-agentic-workflow"
                and text == ".claude-plugin/plugin.json"
                and record.mode == "100644"
            ):
                _invalid()
        return records
    except Exception:
        raise ValueError(FIXED_FAILURE) from None


def _capability_export_tree_v1_digest(
    export_name: str,
    records: list[_GitRecord],
) -> str:
    validated = _validate_direct_export_tree(export_name, records)
    digest = hashlib.sha256()
    digest.update(b"capability-export-tree-v1\0")
    digest.update(struct.pack(">I", len(validated)))
    for record in sorted(validated, key=lambda item: item.path):
        blob_digest = hashlib.sha256()
        blob_digest.update(b"capability-export-blob-v1\0")
        blob_digest.update(struct.pack(">Q", len(record.content)))
        blob_digest.update(record.content)
        digest.update(b"\x01")
        digest.update(b"\x00" if record.mode == "100644" else b"\x01")
        digest.update(struct.pack(">I", len(record.path)))
        digest.update(record.path)
        digest.update(struct.pack(">Q", len(record.content)))
        digest.update(blob_digest.digest())
    return digest.hexdigest()


def _synthetic_record(path: str, *, mode: str = "100644") -> _GitRecord:
    return _GitRecord(
        path=path.encode("utf-8"),
        mode=mode,
        object_type="blob",
        object_id="0" * 40,
        content=b"inert-test-byte",
    )


def test_manifest_bytes_and_exact_declaration() -> None:
    assert MANIFEST.is_file(), "artifact manifest is missing"
    source = MANIFEST.read_bytes()

    assert not source.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in source
    assert source.endswith(b"\n") and not source.endswith(b"\n\n")
    manifest = _parse_artifact_manifest(source)
    assert manifest == EXPECTED_MANIFEST
    assert list(manifest) == ["schemaVersion", "owner", "exports"]
    assert all(
        list(declaration) == ["exportName", "exportRootRelativePath", "harnesses"]
        for declaration in manifest["exports"]
    )
    assert len({row["exportName"] for row in manifest["exports"]}) == 3
    assert all(len(set(row["harnesses"])) == len(row["harnesses"]) for row in manifest["exports"])


def test_strict_json_rejects_bom_invalid_utf8_constants_and_duplicate_decoded_keys(
    capsys: pytest.CaptureFixture[str],
) -> None:
    valid = _json_bytes(EXPECTED_MANIFEST)
    duplicate_root = valid.replace(
        b'"schemaVersion":1',
        b'"schemaVersion":1,"\\u0073chemaVersion":1',
        1,
    )
    duplicate_row = valid.replace(
        b'"exportName":"ultimate-agentic-workflow"',
        b'"exportName":"ultimate-agentic-workflow","\\u0065xportName":"duplicate"',
        1,
    )
    for source in [
        b"\xef\xbb\xbf" + valid,
        b"\xff" + valid,
        valid.replace(b'"schemaVersion":1', b'"schemaVersion":NaN', 1),
        duplicate_root,
        duplicate_row,
    ]:
        _assert_invalid(source, capsys)


def test_rejects_duplicate_identities_wrong_literals_and_unknown_keys(
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidates: list[dict[str, Any]] = []

    duplicate_export = copy.deepcopy(EXPECTED_MANIFEST)
    duplicate_export["exports"].append(copy.deepcopy(duplicate_export["exports"][0]))
    candidates.append(duplicate_export)

    duplicate_harness = copy.deepcopy(EXPECTED_MANIFEST)
    duplicate_harness["exports"][0]["harnesses"] = ["claude", "claude"]
    candidates.append(duplicate_harness)

    wrong_owner = copy.deepcopy(EXPECTED_MANIFEST)
    wrong_owner["owner"] = "other-owner"
    candidates.append(wrong_owner)

    wrong_version = copy.deepcopy(EXPECTED_MANIFEST)
    wrong_version["schemaVersion"] = 2
    candidates.append(wrong_version)

    unknown_root = copy.deepcopy(EXPECTED_MANIFEST)
    unknown_root["unknown"] = True
    candidates.append(unknown_root)

    unknown_row = copy.deepcopy(EXPECTED_MANIFEST)
    unknown_row["exports"][0]["unknown"] = True
    candidates.append(unknown_row)

    for candidate in candidates:
        _assert_invalid(_json_bytes(candidate), capsys)


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "",
        "/absolute/private/root",
        "skills\\windows",
        "skills/control\x01byte",
        "../escape",
        "skills/./nested",
        "https://example.test/export",
        f"skills/sk-proj-{'A' * 32}",
    ],
)
def test_rejects_unsafe_export_roots(
    unsafe_path: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    candidate = copy.deepcopy(EXPECTED_MANIFEST)
    candidate["exports"][0]["exportRootRelativePath"] = unsafe_path
    _assert_invalid(_json_bytes(candidate), capsys, unsafe_path or None)


@pytest.mark.parametrize(
    "field",
    ["command", "env", "timestamp", "backup", "sourceContent"],
)
def test_rejects_injected_sensitive_fields_without_leaking(
    field: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    canary = f"SENTINEL_PRIVATE_{field.upper()}"
    candidate = copy.deepcopy(EXPECTED_MANIFEST)
    candidate["exports"][0][field] = canary
    _assert_invalid(_json_bytes(candidate), capsys, canary)


def test_declared_roots_are_nonempty_tracked_git_trees_and_digest_covered() -> None:
    digests: list[str] = []
    for declaration in EXPECTED_MANIFEST["exports"]:
        records = _git_tree_records(declaration["exportRootRelativePath"])
        assert records
        assert all(record.mode not in {"120000", "160000"} for record in records)
        assert all(record.object_type == "blob" for record in records)
        assert _validate_direct_export_tree(declaration["exportName"], records) == records
        digest = _capability_export_tree_v1_digest(declaration["exportName"], records)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        digests.append(digest)
    assert len(set(digests)) == len(digests) == 3


def test_inert_plugin_marker_is_tracked_and_changes_the_direct_export_digest() -> None:
    records = _git_tree_records("ultimate-agentic-workflow")
    markers = [record for record in records if record.path == b".claude-plugin/plugin.json"]
    assert len(markers) == 1
    assert markers[0].mode == "100644"

    full_digest = _capability_export_tree_v1_digest("ultimate-agentic-workflow", records)
    without_marker = _capability_export_tree_v1_digest(
        "ultimate-agentic-workflow",
        [record for record in records if record not in markers],
    )
    assert full_digest != without_marker

    with pytest.raises(ValueError, match=f"^{FIXED_FAILURE}$"):
        _validate_direct_export_tree(
            "ultimate-agentic-workflow",
            [*records, _synthetic_record(".claude-plugin/extra.json")],
        )


@pytest.mark.parametrize(
    ("export_name", "path", "mode"),
    [
        ("ultimate-agentic-workflow", ".git/config", "100644"),
        ("ultimate-agentic-workflow", "docs/.cache/state", "100644"),
        ("ultimate-agentic-workflow", "pkg/__pycache__/cache.pyc", "100644"),
        ("ultimate-agentic-workflow", "vendor/node_modules/pkg/index.js", "100644"),
        ("ultimate-agentic-workflow", "installed_plugins.json", "100644"),
        ("ultimate-agentic-workflow", "registry/known_marketplaces.json", "100644"),
        ("ultimate-agentic-workflow", "plugins/marketplace.json", "100644"),
        ("ultimate-agentic-workflow", ".claude-plugin/extra.json", "100644"),
        ("ultimate-agentic-workflow", "nested/.claude-plugin/plugin.json", "100644"),
        ("evaluate-tech", ".claude-plugin/plugin.json", "100644"),
        ("ultimate-agentic-workflow", ".claude-plugin/plugin.json", "100755"),
        (
            "ultimate-agentic-workflow",
            "plugins/cache/vendor/.claude-plugin/plugin.json",
            "100644",
        ),
    ],
)
def test_direct_export_policy_rejects_closed_manager_and_cache_paths(
    export_name: str,
    path: str,
    mode: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValueError) as caught:
        _validate_direct_export_tree(export_name, [_synthetic_record(path, mode=mode)])
    assert str(caught.value) == FIXED_FAILURE
    captured = capsys.readouterr()
    assert path not in str(caught.value)
    assert path not in captured.out
    assert path not in captured.err


def test_direct_export_policy_matches_only_exact_closed_names() -> None:
    near_misses = [
        _synthetic_record("docs/.cacheable/readme.md"),
        _synthetic_record("registry/marketplace.json.md"),
        _synthetic_record("vendor/node_modules.txt"),
        _synthetic_record("metadata/.claude-plugin-info/plugin.json"),
    ]
    assert _validate_direct_export_tree("ultimate-agentic-workflow", near_misses) == near_misses
