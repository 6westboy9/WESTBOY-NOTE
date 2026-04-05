#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


TEXT_ELEMENTS_RE = re.compile(r"## Text Elements\s*(.*?)\n%%\n## Drawing", re.S)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
ANCHOR_RE = re.compile(r"\^([A-Za-z0-9_-]+)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 .excalidraw.md 包装和常见异常。")
    parser.add_argument("--drawing-path", required=True, help="目标 .excalidraw.md 路径")
    parser.add_argument("--mode", required=True, choices=["stub", "rendered"], help="校验模式")
    return parser.parse_args()


def extract_units(block: str) -> list[str]:
    units: list[str] = []
    current: list[str] = []
    for raw_line in block.strip().splitlines():
        line = raw_line.rstrip()
        if not line and not current:
            continue
        current.append(line)
        if ANCHOR_RE.search(line):
            units.append("\n".join(current).strip())
            current = []
    if current:
        units.append("\n".join(current).strip())
    return [unit for unit in units if unit]


def normalize_unit(unit: str) -> str:
    return "\n".join(line.rstrip() for line in unit.splitlines()).strip()


def validate(path: Path, mode: str) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    if not FRONTMATTER_RE.search(content):
        errors.append("缺少合法 frontmatter。")

    if "# Excalidraw Data" not in content:
        errors.append("缺少 # Excalidraw Data。")

    if "## Drawing" not in content:
        errors.append("缺少 ## Drawing。")

    if content.count("```compressed-json") != 1:
        errors.append("compressed-json 代码块数量不是 1。")

    if content.count("## Text Elements") != 1:
        errors.append("## Text Elements 段数量不是 1。")

    match = TEXT_ELEMENTS_RE.search(content)
    if not match:
        errors.append("无法正确提取 Text Elements 内容块。")
        return errors

    block = match.group(1).strip()
    if mode == "stub":
        if block:
            errors.append("stub 模式下 Text Elements 应为空。")
        return errors

    units = extract_units(block)
    anchors = []
    for unit in units:
        anchor_match = ANCHOR_RE.search(unit.splitlines()[-1])
        if anchor_match:
            anchors.append(anchor_match.group(1))
    repeated_anchors = [anchor for anchor, count in Counter(anchors).items() if count > 1]
    if repeated_anchors:
        errors.append(f"存在重复锚点，疑似 Text Elements 内容泄露：{', '.join(repeated_anchors)}")

    normalized_units = [normalize_unit(unit) for unit in units]
    duplicates = [text for text, count in Counter(normalized_units).items() if count > 1]
    if duplicates:
        errors.append("存在重复的 Text Elements 单元，疑似内容重复拼接。")

    if '"diagram_type"' in block or '"connectors"' in block or '"blocks"' in block:
        errors.append("Text Elements 区出现了原始规格 JSON 文本。")

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.drawing_path).expanduser().resolve()
    if not path.exists():
        print(f"[ERROR] 未找到文件：{path}", file=sys.stderr)
        return 1
    try:
        errors = validate(path, args.mode)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if errors:
        print(f"[FAIL] {path}")
        for item in errors:
            print(f"- {item}")
        return 2

    print(f"[OK] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
