#!/usr/bin/env python3
"""Check that every workflow is a valid ComfyUI API workflow with an output marker.

Run from the repo root:  python scripts/validate_workflows.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = [ROOT / "workflows", ROOT / "examples" / "partner-workflows"]
OUTPUT_MARK = "(output)"


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(ROOT)}: invalid JSON ({exc})"]
    except UnicodeDecodeError as exc:
        return [f"{path.relative_to(ROOT)}: not UTF-8 ({exc})"]

    if not isinstance(data, dict) or not data:
        return [f"{path.relative_to(ROOT)}: expected a non-empty JSON object"]

    if "nodes" in data:
        return [
            f"{path.relative_to(ROOT)}: this looks like a UI workflow; "
            "export with Workflow > Export (API)"
        ]

    has_output = False
    for node_id, node in data.items():
        if not isinstance(node, dict):
            errors.append(f"{path.relative_to(ROOT)}: node {node_id} is not an object")
            continue
        if "class_type" not in node:
            errors.append(f"{path.relative_to(ROOT)}: node {node_id} has no class_type")
        if not isinstance(node.get("inputs", {}), dict):
            errors.append(f"{path.relative_to(ROOT)}: node {node_id} inputs is not an object")
        title = str(node.get("_meta", {}).get("title", ""))
        if OUTPUT_MARK in title.lower():
            has_output = True

    if not has_output:
        errors.append(
            f"{path.relative_to(ROOT)}: no node title contains '(Output)'; "
            "rename the save/preview node"
        )
    return errors


def main() -> int:
    files: list[Path] = []
    for folder in FOLDERS:
        if folder.exists():
            files.extend(sorted(folder.glob("*.json")))

    if not files:
        print("No workflow JSON files found.")
        return 1

    errors: list[str] = []
    for path in files:
        found = check_file(path)
        if found:
            errors.extend(found)
        else:
            try:
                count = len(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                count = "?"
            print(f"OK  {path.relative_to(ROOT)}  ({count} nodes)")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"\nAll {len(files)} workflow files are valid API workflows with an output marker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
