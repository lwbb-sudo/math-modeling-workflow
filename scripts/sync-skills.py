#!/usr/bin/env python3
"""Refresh the bundled companion skills from local mathmodel sources."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "bundle" / "skills-manifest.json"

COMMON_EXCLUDES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "处理报告.md",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".temp", ".swp", ".swo"}


def default_builtin_root() -> Path:
    local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return local_app_data / "Programs" / "@mathmodeldesktop" / "resources" / "builtin-skills"


def default_bzd_root() -> Path:
    app_data = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    return app_data / "@mathmodel" / "desktop" / "skills-plugin" / "skills"


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("schema_version") != 1:
        raise ValueError(f"Unsupported manifest schema: {manifest.get('schema_version')!r}")
    return manifest


def should_exclude(relative_path: Path, skill_excludes: list[str]) -> bool:
    parts = relative_path.parts
    if any(part in COMMON_EXCLUDES for part in parts):
        return True
    if relative_path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True

    posix = PurePosixPath(relative_path.as_posix())
    for raw_pattern in skill_excludes:
        pattern = raw_pattern.rstrip("/")
        if not pattern:
            continue
        if posix == PurePosixPath(pattern) or pattern in posix.parts:
            return True
        if posix.match(pattern):
            return True
    return False


def copy_skill(source: Path, target: Path, excludes: list[str], dry_run: bool) -> tuple[int, int]:
    files = 0
    bytes_total = 0
    for current_root, dir_names, file_names in os.walk(source):
        current = Path(current_root)
        relative_root = current.relative_to(source)
        dir_names[:] = [
            name
            for name in dir_names
            if not should_exclude(relative_root / name, excludes)
        ]
        for file_name in file_names:
            relative_file = relative_root / file_name
            if should_exclude(relative_file, excludes):
                continue
            source_file = source / relative_file
            files += 1
            bytes_total += source_file.stat().st_size
            if dry_run:
                continue
            destination_file = target / relative_file
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination_file)
    return files, bytes_total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--builtin-root", type=Path, default=default_builtin_root())
    parser.add_argument("--bzd-root", type=Path, default=default_bzd_root())
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without changing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest.resolve())
    source_roots = {
        "builtin": args.builtin_root.resolve(),
        "bzd-plugin": args.bzd_root.resolve(),
    }

    errors: list[str] = []
    planned: list[tuple[dict, Path, Path]] = []
    expected_names = {entry["name"] for entry in manifest["skills"]}
    if len(expected_names) != len(manifest["skills"]):
        errors.append("Manifest contains duplicate skill names.")

    for skill in manifest["skills"]:
        source_type = skill.get("source_type")
        if source_type not in source_roots:
            errors.append(f"{skill.get('name')}: unknown source_type {source_type!r}")
            continue
        source = source_roots[source_type] / skill["source"]
        target = REPO_ROOT / skill["target"]
        if not source.is_dir():
            errors.append(f"{skill['name']}: source directory not found: {source}")
            continue
        if not (source / "SKILL.md").is_file():
            errors.append(f"{skill['name']}: source has no SKILL.md: {source}")
            continue
        missing_dependencies = sorted(set(skill.get("dependencies", [])) - expected_names)
        if missing_dependencies:
            errors.append(f"{skill['name']}: dependencies absent from manifest: {', '.join(missing_dependencies)}")
        planned.append((skill, source, target))

    if errors:
        print("Cannot sync bundle:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    destination_root = REPO_ROOT / "skills"
    if args.dry_run:
        print("Dry run: no files will be changed.")
    else:
        staging_root = REPO_ROOT / ".skills-staging"
        if staging_root.exists():
            shutil.rmtree(staging_root)
        staging_root.mkdir(parents=True)

    total_files = 0
    total_bytes = 0
    try:
        for skill, source, target in planned:
            effective_target = target if args.dry_run else staging_root / skill["name"]
            file_count, byte_count = copy_skill(
                source,
                effective_target,
                list(skill.get("exclude", [])),
                args.dry_run,
            )
            total_files += file_count
            total_bytes += byte_count
            print(f"{skill['name']}: {file_count} files, {byte_count / (1024 * 1024):.2f} MiB")

        if not args.dry_run:
            for skill, _, _ in planned:
                staged_skill = staging_root / skill["name"]
                if not (staged_skill / "SKILL.md").is_file():
                    raise RuntimeError(f"Staged skill is incomplete: {skill['name']}")
            if destination_root.exists():
                shutil.rmtree(destination_root)
            destination_root.mkdir(parents=True)
            for staged_skill in staging_root.iterdir():
                shutil.move(str(staged_skill), str(destination_root / staged_skill.name))
            shutil.rmtree(staging_root)
    except Exception:
        if not args.dry_run and staging_root.exists():
            shutil.rmtree(staging_root)
        raise

    verb = "Would sync" if args.dry_run else "Synced"
    print(f"{verb} {len(planned)} skills: {total_files} files, {total_bytes / (1024 * 1024):.2f} MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
