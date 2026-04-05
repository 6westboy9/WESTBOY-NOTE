# 常见故障与处理

## 1. 图下方露出原始 Text Elements

现象：

- 上半部分能看到图
- 下半部分又露出一大段原始文本

原因：

- `.excalidraw.md` 包装被手工拼坏
- `Text Elements` 内容重复写入
- `## Drawing` 或 `compressed-json` 段落不规范

处理：

1. 运行 `validate_excalidraw_file.py`
2. 若包装异常，重新生成空白 `.excalidraw.md`
3. 保留 `.diagram.json`
4. 再次通过渲染器重建图

## 2. 中文文本错位、换行漂移

原因：

- 没有固定中文字体
- 依赖系统字体回退
- 手写坐标时正文过长

处理：

1. 重新执行 `bootstrap_vault.py`
2. 检查 `loadChineseFonts=true`
3. 检查 `Excalidraw/CJK Fonts/LXGWWenKaiMono-Regular.ttf` 是否存在
4. 缩短单块正文，显式换行

## 3. 图可以改删，但不能新增元素

原因：

- 文件虽然能被插件识别，但不是插件原生稳定写出的包装
- 手工修改 scene 后留下边界问题

处理：

1. 不再直接手写复杂 scene
2. 重建为“空白图 + 规格文件 + 首次渲染”模式
3. 若已渲染完成但结构异常，运行 `讲解图修复器.md`

## 4. 每次打开都被重新渲染

原因：

- onload 渲染脚本没有一次性标记

处理：

- 本 Skill 的渲染器会写入 `<basename>.diagram.rendered`
- 若此标记存在，首次渲染脚本会直接退出

## 5. 手动修过图后还想恢复结构

处理：

- 手动执行 `Excalidraw/Scripts/讲解图修复器.md`
- 修复器会读取同名 `.diagram.json` 重新渲染

注意：

- 修复器是破坏性重建
- 会清空当前教学元素并重画，不应在保留局部手工排版的前提下执行
