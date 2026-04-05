---
name: "obsidian-excalidraw-edu-diagram"
description: "当用户要求在 Obsidian 中生成或修复 Excalidraw 讲解图、把知识点或例题转换为可编辑图解、或把图解嵌入 Markdown 笔记时使用此 Skill。它会标准化生成规格文件、空白 .excalidraw.md、vault 初始化脚本，以及渲染/修复流程，避免直接手写复杂 scene 导致错位、文本泄露或不可编辑。"
---

# Obsidian Excalidraw 讲解图

## 概述

这个 Skill 用来标准化 Obsidian 中的 Excalidraw 讲解图流程。核心原则只有一条：

- 不直接手写复杂 `compressed-json`
- 由 Codex 生成结构化规格 `.diagram.json`
- 由标准空白 `.excalidraw.md` 承载
- 由 vault 内的 Excalidraw 官方脚本在首次打开时原生渲染

这样做的目标是同时保证三件事：

- 图不再因为手拼包装而错位或露出原始 `Text Elements`
- 图生成后仍然可以在 Obsidian 里继续原生新增、删除、调整
- 同一类讲解图可以稳定复用，不必每次重新摸索格式

## 何时使用

当用户出现以下意图时使用本 Skill：

- “把这段知识点画成一张 Excalidraw 讲解图”
- “把例题解析成一张更通俗的图”
- “修复这张 Excalidraw 图的错位、文本泄露、不可新增元素”
- “把讲解图插入 Obsidian 笔记并保持可编辑”
- “在新的 Obsidian vault 里初始化 Excalidraw 讲解图工作流”

不要在这些场景使用本 Skill：

- 用户只是要一张截图或静态图片，不关心继续编辑
- 用户明确要求手绘风格插画，而不是结构化讲解图
- 用户只想修正文案，不需要生成或修复图

## 标准工作流

### 1. 初始化目标 vault

第一次在某个 Obsidian vault 中使用时，先执行：

```bash
python3 scripts/bootstrap_vault.py --vault-path <vault_path>
```

这一步会：

- 检查目标 vault 是否安装了 `obsidian-excalidraw-plugin`
- 写入 `Excalidraw/Scripts/讲解图渲染器.md`
- 写入 `Excalidraw/Scripts/讲解图修复器.md`
- 写入 `Excalidraw/Templates/讲解图空白模板.excalidraw.md`
- 写入 `Excalidraw/CJK Fonts/LXGWWenKaiMono-Regular.ttf`
- 更新 Excalidraw 插件设置，固定脚本目录、模板目录和中文字体配置

### 2. 生成结构化规格

不要直接拼 `.excalidraw.md` 的 `Text Elements` 和 `compressed-json`。

先根据用户需求写结构化规格文件 `.diagram.json`。规格格式见：

- `references/spec_schema.md`

版式坐标和推荐排版见：

- `references/layout_patterns.md`

### 3. 生成空白图文件和规格文件

当规格文件准备好后，执行：

```bash
python3 scripts/create_diagram_package.py \
  --vault-path <vault_path> \
  --drawing-path <drawing_path> \
  --spec-file <spec_file>
```

这个脚本会：

- 在目标位置写入标准空白 `.excalidraw.md`
- 固定 frontmatter
- 固定 `excalidraw-onload-script`
- 复制规格为同名兄弟文件 `<basename>.diagram.json`

### 4. 首次打开时原生渲染

首次在 Obsidian 中打开目标 `.excalidraw.md` 时，`讲解图渲染器.md` 会：

- 读取同名 `.diagram.json`
- 清空当前教学元素
- 按规格创建卡片、说明框、结果框和箭头
- 刷新文本尺寸
- 写入一次性渲染标记，避免后续每次打开都覆盖人工修改

### 5. 嵌入 Markdown 笔记

若用户需要在笔记中插图，使用标准内嵌：

```md
![[相对路径到.excalidraw|1200]]
```

## 新建讲解图

新建时优先使用以下图型：

- `concept-flow`
- `step-flow`
- `timeline`
- `qa-explanation`
- `resource-analysis`
- `address-translation`

新图规格中应优先满足这些约束：

- 画布默认 `1600x900`
- 主题默认 `edu-light`
- 所有块元素都给出明确的 `x/y/width/height`
- 所有连接关系都用块 `id` 建立，不用裸坐标硬连线
- 文本尽量提前分段，避免在渲染时依赖浏览器临场换行

如果没有特别说明，优先使用这些块类型：

- `banner`
- `card`
- `callout`
- `result`
- `table`

## 修复错位或异常文件

先执行：

```bash
python3 scripts/validate_excalidraw_file.py --drawing-path <drawing_path> --mode stub
```

或：

```bash
python3 scripts/validate_excalidraw_file.py --drawing-path <drawing_path> --mode rendered
```

判定逻辑：

- 若是 frontmatter、`## Drawing`、`compressed-json` 结构异常，先修文件包装
- 若包装正常但布局错位、文本溢出、人工误改导致结构紊乱，使用 vault 内 `讲解图修复器.md` 重渲染

常见异常与处理见：

- `references/failure_modes.md`

## 失败处理

如果脚本失败，按下面顺序处理：

1. 确认目标目录是 Obsidian vault，且 `.obsidian/plugins/obsidian-excalidraw-plugin/data.json` 存在
2. 重新执行 `bootstrap_vault.py`
3. 运行 `validate_excalidraw_file.py` 检查包装
4. 在 Obsidian 中手动打开目标图，确认是否触发首次渲染
5. 若图已渲染过但结构损坏，手动执行 `讲解图修复器.md`

如果还是失败，重点检查：

- 中文字体是否已复制到 `Excalidraw/CJK Fonts`
- 插件设置中的 `loadChineseFonts` 是否为 `true`
- `excalidraw-onload-script` 路径是否正确
- 规格文件字段是否满足最小 schema

## 不要做的事

- 不要再直接手写复杂 `compressed-json`
- 不要把教学文案直接塞进 `.excalidraw.md` 的 `## Text Elements` 再手拼锚点
- 不要依赖系统默认中文字体回退
- 不要让 onload 脚本在每次打开时都强制重渲染
- 不要在没有规格文件的情况下直接复制旧图冒充新图

## 参考

- 规格字段说明：`references/spec_schema.md`
- 版式模板：`references/layout_patterns.md`
- 故障排查：`references/failure_modes.md`
