#!/usr/bin/env python3
"""Verify that the repository is internally consistent and reproducible."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# WorkforMe fork: only the Claude package is built and verified (CHANGES.md CH-01).
VERSIONED_MANIFESTS = (
    Path("platform/claude/plugin.json"),
    Path("claude/.claude-plugin/plugin.json"),
)
MARKETPLACE_TARGETS = {
    Path(".claude-plugin/marketplace.json"): Path("claude"),
}


class VerificationError(RuntimeError):
    pass


def run(command: list[str], cwd: Path, *, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if result.returncode != 0:
        detail = (result.stdout or "") + (result.stderr or "")
        raise VerificationError(
            f"command failed ({' '.join(command)})" + (f"\n{detail.strip()}" if detail.strip() else "")
        )
    return (result.stdout or "").strip()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"JSON root must be an object: {path}")
    return value


def changelog_version(root: Path) -> str:
    match = re.search(r"^##\s+v([^\s(]+)", (root / "CHANGELOG.md").read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise VerificationError("CHANGELOG.md has no version heading")
    return match.group(1)


def manifest_versions(root: Path) -> dict[Path, str]:
    versions: dict[Path, str] = {}
    for relative in VERSIONED_MANIFESTS:
        path = root / relative
        if not path.is_file():
            raise VerificationError(f"missing versioned manifest: {relative}")
        data = load_json(path)
        version = data.get("version")
        if not isinstance(version, str) or not version.strip():
            raise VerificationError(f"missing version: {path.relative_to(root)}")
        versions[path.relative_to(root)] = version
    return versions


def validate_json_files(root: Path) -> None:
    candidates = set(root.glob("**/plugin.json")) | set(root.glob("**/marketplace.json"))
    for path in sorted(candidates):
        load_json(path)
    print(f"OK JSON manifests ({len(candidates)})")


def validate_versions(root: Path, tag: str | None) -> None:
    versions = manifest_versions(root)
    unique = set(versions.values())
    if len(unique) != 1:
        detail = "\n".join(f"  {path}: {version}" for path, version in versions.items())
        raise VerificationError(f"manifest version mismatch:\n{detail}")
    version = unique.pop()
    changelog = changelog_version(root)
    if version != changelog:
        raise VerificationError(f"manifest version {version} != CHANGELOG version {changelog}")
    if tag is not None:
        if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
            raise VerificationError(f"release tag must be vX.Y.Z: {tag}")
        if tag != f"v{version}":
            raise VerificationError(f"tag {tag} != manifest version v{version}")
    print(f"OK version {version}" + (f" and tag {tag}" if tag else ""))


def marketplace_source(entry: dict) -> str | None:
    source = entry.get("source")
    if isinstance(source, str):
        return source
    if isinstance(source, dict) and source.get("source") == "local":
        value = source.get("path")
        return value if isinstance(value, str) else None
    return None


def validate_marketplaces(root: Path) -> None:
    versions = set(manifest_versions(root).values())
    if len(versions) != 1:
        raise VerificationError("manifest versions must match before marketplace validation")
    version = versions.pop()
    for manifest, expected_target in MARKETPLACE_TARGETS.items():
        data = load_json(root / manifest)
        plugins = data.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
            raise VerificationError(f"expected one plugin entry: {manifest}")
        entry = plugins[0]
        if entry.get("name") != "dryforge-docs":  # WorkforMe fork (CHANGES.md CH-02)
            raise VerificationError(f"unexpected plugin name: {manifest}")
        entry_version = entry.get("version")
        if entry_version is not None and entry_version != version:
            raise VerificationError(f"marketplace version {entry_version} != manifest version {version}: {manifest}")
        source = marketplace_source(entry)
        normalized = source.removeprefix("./") if source else None
        if normalized != expected_target.as_posix():
            raise VerificationError(f"unexpected marketplace source {source!r}: {manifest}")
        target = (root / normalized).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_dir():
            raise VerificationError(f"marketplace source is not a package directory: {manifest}")
    print(f"OK marketplace targets ({len(MARKETPLACE_TARGETS)})")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise VerificationError(f"missing YAML frontmatter: {path}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z0-9-]+):(?:\s*(.*))?$", line)
        if field:
            values[field.group(1)] = (field.group(2) or "").strip()
    return values



def validate_claude_package(root: Path) -> None:
    """Claude counterpart of the removed per-platform package checks (CHANGES.md CH-01)."""
    source_skills = root / "src/skills"
    generated_skills = root / "claude/skills"
    source_names = sorted(path.name for path in source_skills.iterdir() if path.is_dir())
    generated_names = sorted(path.name for path in generated_skills.iterdir() if path.is_dir()) \
        if generated_skills.is_dir() else []
    if not source_names or generated_names != source_names:
        raise VerificationError("Claude skills do not match src/skills")
    for name in source_names:
        skill_file = generated_skills / name / "SKILL.md"
        values = frontmatter(skill_file)
        if values.get("name") != name:
            raise VerificationError(f"Claude skill name does not match directory: {name}")
        if not values.get("description"):
            raise VerificationError(f"Claude skill description is missing: {name}")
        if values.get("disable-model-invocation") != "true":
            raise VerificationError(f"Claude skill is not manual-only: {name}")
        if not values.get("allowed-tools"):
            raise VerificationError(f"Claude skill has no allowed-tools: {name}")
        # Everything except the injected frontmatter lines must equal the source byte-for-byte.
        injected = re.compile(r"^(disable-model-invocation|allowed-tools):.*\n", re.MULTILINE)
        if injected.sub("", skill_file.read_text(encoding="utf-8")) != \
                (source_skills / name / "SKILL.md").read_text(encoding="utf-8"):
            raise VerificationError(f"Claude SKILL.md differs from src beyond frontmatter: {name}")
    source_refs = {
        path.relative_to(source_skills): path.read_bytes()
        for path in source_skills.rglob("*")
        if path.is_file() and path.name not in {".DS_Store", "SKILL.md"}
    }
    generated_refs = {
        path.relative_to(generated_skills): path.read_bytes()
        for path in generated_skills.rglob("*")
        if path.is_file() and path.name not in {".DS_Store", "SKILL.md"}
    }
    if source_refs != generated_refs:
        raise VerificationError("Claude skill references do not match src/skills")
    print(f"OK Claude package ({len(source_names)} skills)")


def git_status(root: Path) -> str:
    top = Path(run(["git", "rev-parse", "--show-toplevel"], root, capture=True)).resolve()
    relative = root.resolve().relative_to(top)
    pathspec = "." if relative == Path(".") else relative.as_posix()
    return run(["git", "status", "--porcelain", "--untracked-files=all", "--", pathspec], top, capture=True)


def validate_reproducible_build(root: Path) -> None:
    before = git_status(root)
    if before:
        raise VerificationError(f"verification requires a clean tree:\n{before}")
    run(["bash", "-n", "build/build.sh"], root)
    run(["bash", "build/build.sh"], root)
    after = git_status(root)
    if after:
        raise VerificationError(f"generated outputs are stale or uncommitted:\n{after}")
    print("OK reproducible build")



def validate_licenses(root: Path) -> None:
    canonical = (root / "LICENSE").read_bytes()
    if b"Apache License" not in canonical or b"Version 2.0, January 2004" not in canonical:
        raise VerificationError("LICENSE is not the Apache License 2.0 text")
    copies = sorted(path for path in root.rglob("LICENSE") if ".git" not in path.parts)
    for path in copies:
        if path.read_bytes() != canonical:
            raise VerificationError(f"LICENSE differs from the root LICENSE: {path.relative_to(root)}")
    print(f"OK license copies ({len(copies)})")


def verify(root: Path, tag: str | None = None) -> None:
    required = [
        "CHANGELOG.md",
        "build/build.sh",
        "src/skills",
        "platform/claude/plugin.json",
        ".claude-plugin/marketplace.json",
        "LICENSE",
    ]
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        raise VerificationError(f"missing required paths: {', '.join(missing)}")
    validate_json_files(root)
    validate_versions(root, tag)
    validate_marketplaces(root)
    validate_claude_package(root)
    validate_licenses(root)
    validate_reproducible_build(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tag", help="Validate a release tag such as v1.2.0")
    args = parser.parse_args()
    try:
        verify(args.root.resolve(), args.tag)
    except (VerificationError, OSError, ValueError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
