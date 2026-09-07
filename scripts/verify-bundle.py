#!/usr/bin/env python3
"""Verify the bundled mathematical-modeling skills and their dependency closure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "bundle" / "skills-manifest.json"
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*([^\s#]+)\s*$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_RESOURCE = re.compile(r"`((?:scripts|references|assets|static)/[^`]+)`")
SKILL_TOKEN = re.compile(r"(?:`|/)((?:bzd-[a-z0-9-]+|mma-[a-z0-9-]+|data-search|metaheuristic-optimization|doctor|nature-figure|mathmodel-figure-templates|paper-diagram|paper-search))(?:`|\b)")
RESOURCE_ARGUMENT_SUFFIX = re.compile(r"\s+(?:--?[a-zA-Z]|<)")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?i)\b[A-Z]:\\Users\\")
EXCLUDED_NAMES = {".git", "__pycache__", ".DS_Store", "Thumbs.db", "desktop.ini", "处理报告.md"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".temp", ".swp", ".swo"}
TEXT_SUFFIXES = {
    "", ".md", ".txt", ".json", ".yaml", ".yml", ".py", ".ps1", ".sh", ".bat",
    ".tex", ".cls", ".cfg", ".bib", ".toml", ".ini", ".csv", ".xml", ".drawio",
}


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def declared_name(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_NAME.search(text)
    return match.group(1).strip() if match else None


def verify_required_assets() -> list[str]:
    required = [
        "skills/mma-paper/assets/template/cumcm/document.tex",
        "skills/mathmodel-figure-templates/scripts/render_template.py",
        "skills/mathmodel-figure-templates/assets/previews",
        "skills/paper-diagram/ATTRIBUTION.md",
        "skills/paper-diagram/assets/icons/tabler/LICENSE",
        "skills/nature-figure/LICENSE.txt",
        "skills/nature-figure/assets",
        "skills/bzd-model-dictionary/assets/model-dictionary.json",
    ]
    return [relative for relative in required if not (REPO_ROOT / relative).exists()]


def verify_bzd_notice() -> list[str]:
    path = REPO_ROOT / "skills" / "bzd-model-dictionary" / "assets" / "model-dictionary.json"
    if not path.is_file():
        return ["BZD model dictionary is missing."]
    text = path.read_text(encoding="utf-8")
    required_phrases = ["BZD数模社", "仅限个人学习", "禁止商用", "版权与传播声明", "资料使用声明"]
    return [f"BZD model dictionary lost required notice phrase: {phrase}" for phrase in required_phrases if phrase not in text]


def normalize_resource_reference(raw: str) -> str | None:
    reference = raw.strip().split("#", 1)[0]
    if not reference or "://" in reference or reference.startswith(("mailto:", "#")):
        return None
    reference = RESOURCE_ARGUMENT_SUFFIX.split(reference, maxsplit=1)[0].strip()
    reference = reference.split(maxsplit=1)[0]
    if "<" in reference or "*" in reference:
        return None
    return reference.rstrip("/.,;:")


def verify_skill_references(skill_name: str, skill_dir: Path, bundled_names: set[str]) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return errors
    text = skill_md.read_text(encoding="utf-8")

    for dependency in sorted(set(SKILL_TOKEN.findall(text))):
        if dependency == skill_name:
            continue
        if dependency not in bundled_names:
            errors.append(f"{skill_name}: explicit skill reference is not bundled: {dependency}")

    raw_resources = set(INLINE_RESOURCE.findall(text))
    raw_resources.update(MARKDOWN_LINK.findall(text))
    for raw_resource in sorted(raw_resources):
        resource = normalize_resource_reference(raw_resource)
        if not resource or not resource.startswith(("scripts/", "references/", "assets/", "static/")):
            continue
        local_resource = skill_dir / resource
        if local_resource.exists():
            continue
        if skill_name == "mma-figure" and resource == "references/figure-catalog.md":
            routed_resource = REPO_ROOT / "skills" / "mathmodel-figure-templates" / resource
            if routed_resource.exists():
                continue
        errors.append(f"{skill_name}: referenced resource is missing: {resource}")
    return errors


def verify_workflow_bodies() -> list[str]:
    skill_lines = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
    if skill_lines and skill_lines[0] == "---":
        end = skill_lines.index("---", 1)
        skill_lines = skill_lines[end + 1:]
    while skill_lines and not skill_lines[0].strip():
        skill_lines.pop(0)

    agents_lines = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8").splitlines()
    try:
        start = agents_lines.index("# Interactive Mathematical Modeling Workflow")
    except ValueError:
        return ["AGENTS.md does not contain the workflow body heading."]
    agents_lines = agents_lines[start:]
    if skill_lines != agents_lines:
        return ["SKILL.md and AGENTS.md workflow bodies differ."]
    return []


def verify_dependency_references(manifest: dict, bundled_names: set[str]) -> list[str]:
    errors: list[str] = []
    expected_dependencies = {
        entry["name"]: set(entry.get("dependencies", []))
        for entry in manifest["skills"]
    }
    expected_dependencies[manifest["root_skill"]] = {entry["name"] for entry in manifest["skills"] if entry["name"] in {
        "bzd-problem-translator", "bzd-problem-restatement", "bzd-problem-analysis-checker",
        "bzd-modeling-ideas", "bzd-model-dictionary", "data-search", "metaheuristic-optimization",
        "mma-figure", "nature-figure", "mathmodel-figure-templates", "paper-diagram", "mma-paper",
        "bzd-model-assumption-checker", "bzd-model-solution-checker", "bzd-abstract-checker",
        "bzd-symbol-notation-checker", "bzd-reference-appendix-checker", "bzd-ai-usage-disclosure",
        "bzd-review-paper", "mma-review", "doctor",
    }}

    for owner, dependencies in expected_dependencies.items():
        missing = sorted(dependencies - bundled_names)
        if missing:
            errors.append(f"{owner}: manifest dependencies are not bundled: {', '.join(missing)}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest.resolve())
    errors: list[str] = []
    warnings: list[str] = []

    manifest_names = [entry["name"] for entry in manifest["skills"]]
    duplicate_manifest = [name for name, count in Counter(manifest_names).items() if count > 1]
    if duplicate_manifest:
        errors.append(f"Duplicate names in manifest: {', '.join(sorted(duplicate_manifest))}")

    bundled_dirs = sorted(path for path in (REPO_ROOT / "skills").iterdir() if path.is_dir()) if (REPO_ROOT / "skills").is_dir() else []
    bundled_dir_names = {path.name for path in bundled_dirs}
    expected_dir_names = set(manifest_names)
    missing_dirs = sorted(expected_dir_names - bundled_dir_names)
    extra_dirs = sorted(bundled_dir_names - expected_dir_names)
    if missing_dirs:
        errors.append(f"Missing bundled skill directories: {', '.join(missing_dirs)}")
    if extra_dirs:
        errors.append(f"Unlisted bundled skill directories: {', '.join(extra_dirs)}")

    declared_names: list[str] = []
    for directory in bundled_dirs:
        skill_md = directory / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{directory.name}: SKILL.md is missing")
            continue
        name = declared_name(skill_md)
        if not name:
            errors.append(f"{directory.name}: SKILL.md has no frontmatter name")
            continue
        declared_names.append(name)
        if name != directory.name:
            errors.append(f"{directory.name}: frontmatter declares name {name!r}")

    root_skill = REPO_ROOT / "SKILL.md"
    root_name = declared_name(root_skill) if root_skill.is_file() else None
    if root_name != manifest.get("root_skill"):
        errors.append(f"Root skill name is {root_name!r}; expected {manifest.get('root_skill')!r}")
    all_declared_names = [name for name in [root_name, *declared_names] if name]
    duplicate_declared = [name for name, count in Counter(all_declared_names).items() if count > 1]
    if duplicate_declared:
        errors.append(f"Duplicate declared skill names: {', '.join(sorted(duplicate_declared))}")

    bundled_names = set(all_declared_names)
    errors.extend(verify_dependency_references(manifest, bundled_names))
    errors.extend(verify_workflow_bodies())
    if root_skill.is_file():
        errors.extend(verify_skill_references(manifest["root_skill"], REPO_ROOT, bundled_names))
    for directory in bundled_dirs:
        errors.extend(verify_skill_references(directory.name, directory, bundled_names))
    missing_assets = verify_required_assets()
    if missing_assets:
        errors.append("Missing required runtime assets: " + ", ".join(missing_assets))
    errors.extend(verify_bzd_notice())

    if (REPO_ROOT / "skills" / "bzd-reference-appendix-checker" / "bzd-reference-appendix-checker").exists():
        errors.append("Duplicated nested bzd-reference-appendix-checker directory is present.")

    inspected_files = 0
    for path in REPO_ROOT.rglob("*"):
        relative = path.relative_to(REPO_ROOT)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if ".git" in relative.parts:
            if path.is_dir() and path.name == ".git":
                errors.append(f"Nested Git directory is present: {relative.as_posix()}")
            continue
        if any(part in EXCLUDED_NAMES for part in relative.parts) or path.suffix.lower() in EXCLUDED_SUFFIXES:
            errors.append(f"Excluded generated file is present: {relative.as_posix()}")
            continue
        if path.is_dir():
            continue
        inspected_files += 1
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path)
        if text is None:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Possible {label} in {relative.as_posix()}")
        if WINDOWS_ABSOLUTE_PATH.search(text):
            errors.append(f"Machine-specific absolute Windows path in {relative.as_posix()}")

    for required_notice in [
        REPO_ROOT / "THIRD_PARTY_NOTICES.md",
        REPO_ROOT / "skills" / "nature-figure" / "LICENSE.txt",
        REPO_ROOT / "skills" / "paper-diagram" / "ATTRIBUTION.md",
    ]:
        if not required_notice.is_file():
            errors.append(f"Required license/notice file is missing: {required_notice.relative_to(REPO_ROOT).as_posix()}")

    print(f"Manifest skills: {len(manifest_names)}")
    print(f"Installed bundle skills including root: {len(all_declared_names)}")
    print(f"Inspected files: {inspected_files}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    if errors:
        print("Verification failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Bundle verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
