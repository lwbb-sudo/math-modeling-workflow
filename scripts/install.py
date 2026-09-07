#!/usr/bin/env python3
"""Install the workflow and all bundled companion skills into a skill root."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "bundle" / "skills-manifest.json"
ROOT_SKILL_NAME = "math-modeling-workflow"
ROOT_SKILL_FILES = ("SKILL.md",)
ROOT_SKILL_DIRS: tuple[str, ...] = ()
SKIP_NAMES = {".git", "__pycache__", ".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".swp", ".swo"}


def default_target() -> Path:
    configured = os.environ.get("CLAUDE_SKILLS_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".claude" / "skills"


def load_skill_names() -> list[str]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    names = [ROOT_SKILL_NAME, *(skill["name"] for skill in manifest["skills"])]
    if len(names) != len(set(names)):
        raise ValueError("Bundle contains duplicate skill names.")
    return names


def ignore_bundle_files(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        path = Path(directory) / name
        if name in SKIP_NAMES or path.suffix.lower() in SKIP_SUFFIXES:
            ignored.add(name)
    return ignored


def copy_root_skill(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for file_name in ROOT_SKILL_FILES:
        shutil.copy2(REPO_ROOT / file_name, destination / file_name)
    for directory_name in ROOT_SKILL_DIRS:
        shutil.copytree(REPO_ROOT / directory_name, destination / directory_name)


def source_for(skill_name: str) -> Path | None:
    if skill_name == ROOT_SKILL_NAME:
        return None
    return REPO_ROOT / "skills" / skill_name


def validate_bundle(skill_names: list[str]) -> None:
    missing: list[str] = []
    if not (REPO_ROOT / "SKILL.md").is_file():
        missing.append(f"{ROOT_SKILL_NAME}: root SKILL.md")
    for name in skill_names[1:]:
        source = source_for(name)
        if source is None or not (source / "SKILL.md").is_file():
            missing.append(f"{name}: {source}")
    if missing:
        raise FileNotFoundError("Bundle is incomplete:\n  - " + "\n  - ".join(missing))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=default_target(), help="Parent directory that contains skill folders.")
    parser.add_argument("--force", action="store_true", help="Replace existing skills after listing all conflicts.")
    parser.add_argument("--dry-run", action="store_true", help="Print the install plan without changing files.")
    parser.add_argument("--list", action="store_true", help="List bundled skills and exit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_names = load_skill_names()
    validate_bundle(skill_names)

    if args.list:
        for name in skill_names:
            print(name)
        return 0

    target = args.target.expanduser().resolve()
    conflicts = [name for name in skill_names if (target / name).exists()]

    print(f"Target: {target}")
    print(f"Skills: {len(skill_names)}")
    if conflicts:
        print("Conflicts:")
        for name in conflicts:
            print(f"  - {target / name}")
        if not args.force:
            print("Nothing changed. Re-run with --force to replace these skills.", file=sys.stderr)
            return 2

    for name in skill_names:
        action = "replace" if name in conflicts else "install"
        print(f"  {action}: {name}")

    if args.dry_run:
        print("Dry run complete; no files changed.")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix="math-modeling-workflow-install-", dir=target.parent))
    backup_parent = Path(tempfile.mkdtemp(prefix="math-modeling-workflow-backup-", dir=target.parent))
    installed: list[Path] = []
    backups: list[tuple[Path, Path]] = []

    try:
        staged_target = staging_parent / "skills"
        staged_target.mkdir()
        for name in skill_names:
            staged_skill = staged_target / name
            source = source_for(name)
            if source is None:
                copy_root_skill(staged_skill)
            else:
                shutil.copytree(source, staged_skill, ignore=ignore_bundle_files)
            if not (staged_skill / "SKILL.md").is_file():
                raise RuntimeError(f"Staged skill has no SKILL.md: {name}")

        for name in conflicts:
            original = target / name
            backup = backup_parent / name
            shutil.move(str(original), str(backup))
            backups.append((original, backup))

        for name in skill_names:
            destination = target / name
            shutil.move(str(staged_target / name), str(destination))
            installed.append(destination)
    except Exception:
        for destination in reversed(installed):
            if destination.exists():
                shutil.rmtree(destination)
        for original, backup in reversed(backups):
            if backup.exists():
                shutil.move(str(backup), str(original))
        raise
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)
        shutil.rmtree(backup_parent, ignore_errors=True)

    print(f"Installed {len(skill_names)} skills into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
