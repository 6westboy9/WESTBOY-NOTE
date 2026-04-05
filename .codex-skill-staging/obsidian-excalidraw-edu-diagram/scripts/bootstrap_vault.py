#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


PLUGIN_SETTINGS_REL = Path(".obsidian/plugins/obsidian-excalidraw-plugin/data.json")
SCRIPT_DIR_REL = Path("Excalidraw/Scripts")
TEMPLATE_DIR_REL = Path("Excalidraw/Templates")
FONT_DIR_REL = Path("Excalidraw/CJK Fonts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化 Obsidian vault 的 Excalidraw 讲解图工作流。")
    parser.add_argument("--vault-path", required=True, help="目标 Obsidian vault 路径")
    return parser.parse_args()


def require_vault(vault_path: Path) -> Path:
    settings_path = vault_path / PLUGIN_SETTINGS_REL
    if not settings_path.exists():
        raise FileNotFoundError(
            f"未找到 Excalidraw 插件设置文件：{settings_path}\n"
            "请先在目标 vault 中安装并启用 obsidian-excalidraw-plugin。"
        )
    return settings_path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def copy_asset(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def update_settings(settings_path: Path) -> dict:
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    data["scriptFolderPath"] = str(SCRIPT_DIR_REL).replace("\\", "/")
    data["templateFilePath"] = str(TEMPLATE_DIR_REL / "讲解图空白模板.excalidraw.md").replace("\\", "/")
    data["loadChineseFonts"] = True
    data["fontAssetsPath"] = str(FONT_DIR_REL).replace("\\", "/")
    data["experimentalEnableFourthFont"] = True
    data["experimantalFourthFont"] = str(FONT_DIR_REL / "LXGWWenKaiMono-Regular.ttf").replace("\\", "/")
    settings_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def bootstrap(vault_path: Path) -> None:
    settings_path = require_vault(vault_path)
    root = skill_root()

    copy_asset(
        root / "assets/vault_scripts/讲解图渲染器.md",
        vault_path / SCRIPT_DIR_REL / "讲解图渲染器.md",
    )
    copy_asset(
        root / "assets/vault_scripts/讲解图修复器.md",
        vault_path / SCRIPT_DIR_REL / "讲解图修复器.md",
    )
    copy_asset(
        root / "assets/templates/讲解图空白模板.excalidraw.md",
        vault_path / TEMPLATE_DIR_REL / "讲解图空白模板.excalidraw.md",
    )
    copy_asset(
        root / "assets/fonts/LXGWWenKaiMono-Regular.ttf",
        vault_path / FONT_DIR_REL / "LXGWWenKaiMono-Regular.ttf",
    )

    update_settings(settings_path)


def main() -> int:
    args = parse_args()
    vault_path = Path(args.vault_path).expanduser().resolve()
    try:
        bootstrap(vault_path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    print(f"[OK] 已初始化 vault: {vault_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
