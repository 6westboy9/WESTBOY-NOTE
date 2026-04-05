#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BLANK_DRAWING_B64 = "N4IgLgngDgpiBcIYA8DGBDANgSwCYCd0B3EAGhADcZ8BnbAewDsEAmcm+gV31TkQAswYKDXgB6MQHNsYfpwBGAOlT0AtmIBeNCtlQbs6RmPry6uA4wC0KDDgLFLUTJ2lH8MTDHQ0YNMWHRJMRZFFhCABjIkT1UYRjAaBABtAF1ydCgoAGUAsD5QSXw8LOwNPkZOTExyHRgiACF0VABrQq5GXABhekx6fAQQAGIAM1GxkABfCaA=="
REQUIRED_TOP_LEVEL_KEYS = {"version", "diagram_type", "title", "theme", "canvas", "blocks", "connectors"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成讲解图的空白 Excalidraw 文件和兄弟规格文件。")
    parser.add_argument("--vault-path", required=True, help="目标 Obsidian vault 路径")
    parser.add_argument("--drawing-path", required=True, help="目标 .excalidraw.md 路径，可相对 vault 或绝对路径")
    parser.add_argument("--spec-file", required=True, help="源规格文件路径")
    return parser.parse_args()


def resolve_in_vault(vault_path: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (vault_path / candidate).resolve()


def ensure_inside_vault(vault_path: Path, target: Path) -> None:
    try:
        target.relative_to(vault_path)
    except ValueError as exc:
        raise ValueError(f"目标路径必须位于 vault 内：{target}") from exc


def load_and_validate_spec(spec_path: Path) -> dict:
    if not spec_path.exists():
        raise FileNotFoundError(f"未找到规格文件：{spec_path}")
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - data.keys())
    if missing:
        raise ValueError(f"规格文件缺少字段：{', '.join(missing)}")
    if not isinstance(data["blocks"], list) or not isinstance(data["connectors"], list):
        raise ValueError("规格文件中的 blocks/connectors 必须是数组。")
    return data


def build_excalidraw_stub() -> str:
    return (
        "---\n"
        "excalidraw-plugin: parsed\n"
        "tags: [excalidraw]\n"
        'excalidraw-onload-script: "Excalidraw/Scripts/讲解图渲染器.md"\n'
        "---\n"
        "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== "
        "You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. "
        "For more info check in plugin settings under 'Saving'\n\n"
        "# Excalidraw Data\n\n"
        "## Text Elements\n"
        "%%\n"
        "## Drawing\n"
        "```compressed-json\n"
        f"{BLANK_DRAWING_B64}\n"
        "```\n"
        "%%\n"
    )


def main() -> int:
    args = parse_args()
    vault_path = Path(args.vault_path).expanduser().resolve()
    drawing_path = resolve_in_vault(vault_path, args.drawing_path)
    spec_path = Path(args.spec_file).expanduser().resolve()

    try:
        ensure_inside_vault(vault_path, drawing_path)
        spec = load_and_validate_spec(spec_path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    sibling_spec_path = drawing_path.with_suffix("").with_suffix(".diagram.json")
    marker_path = drawing_path.with_suffix("").with_suffix(".diagram.rendered")

    drawing_path.parent.mkdir(parents=True, exist_ok=True)
    drawing_path.write_text(build_excalidraw_stub(), encoding="utf-8")
    sibling_spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if marker_path.exists():
        marker_path.unlink()

    print(f"[OK] 已生成 Excalidraw 文件：{drawing_path}")
    print(f"[OK] 已生成规格文件：{sibling_spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
