# 讲解图规格 Schema

每张讲解图都对应一个同名兄弟文件：

- `xxx.excalidraw.md`
- `xxx.diagram.json`

## 最小字段

```json
{
  "version": "1.0",
  "diagram_type": "address-translation",
  "title": "分页存储地址变换",
  "theme": "edu-light",
  "canvas": {
    "width": 1600,
    "height": 900
  },
  "blocks": [],
  "connectors": []
}
```

## diagram_type

首版允许值：

- `concept-flow`
- `step-flow`
- `timeline`
- `qa-explanation`
- `resource-analysis`
- `address-translation`

## blocks

每个块至少包含：

```json
{
  "id": "logic",
  "kind": "card",
  "x": 60,
  "y": 220,
  "width": 280,
  "height": 220,
  "title": "逻辑地址",
  "body": "页号 = 4\n页内地址 = 256"
}
```

### kind

首版允许值：

- `banner`
- `card`
- `callout`
- `result`
- `table`

### 可选字段

```json
{
  "subtitle": "可选副标题",
  "color": "#E8F1FF",
  "text_color": "#204A87",
  "stroke_color": "#3B82F6"
}
```

说明：

- `x/y/width/height` 必须由 Codex 预先算好
- `body` 使用换行文本即可，不要求富文本
- `table` 首版也按普通多行文本渲染，不单独画栅格

## connectors

每条连接线至少包含：

```json
{
  "from": "logic",
  "from_side": "right",
  "to": "check",
  "to_side": "left",
  "label": "先检查页号"
}
```

### side

允许值：

- `top`
- `bottom`
- `left`
- `right`

### 可选字段

```json
{
  "color": "#F59E0B"
}
```

## 推荐约束

- `banner` 通常放在顶部横向区域
- `card` 作为主内容块
- `callout` 作为补充说明
- `result` 作为结论块
- `table` 只用于需要对齐的多行文本

## 完整示例

```json
{
  "version": "1.0",
  "diagram_type": "address-translation",
  "title": "分页存储：把逻辑地址拆成页号和页内偏移",
  "theme": "edu-light",
  "canvas": {
    "width": 1600,
    "height": 900
  },
  "blocks": [
    {
      "id": "banner",
      "kind": "banner",
      "x": 40,
      "y": 40,
      "width": 1480,
      "height": 100,
      "title": "先查页号映射到哪个物理块，再把页内偏移原样带过去",
      "body": "页内地址本身就是偏移量，不需要变。"
    },
    {
      "id": "logic",
      "kind": "card",
      "x": 60,
      "y": 220,
      "width": 280,
      "height": 220,
      "title": "逻辑地址",
      "body": "页号 = 4\n页内地址 = 256"
    },
    {
      "id": "check",
      "kind": "callout",
      "x": 420,
      "y": 230,
      "width": 300,
      "height": 200,
      "title": "先检查页号是否合法",
      "body": "若页号 >= 页表长度 L，则地址越界。"
    },
    {
      "id": "ptable",
      "kind": "table",
      "x": 800,
      "y": 190,
      "width": 320,
      "height": 300,
      "title": "页表",
      "body": "0 -> 6\n1 -> 9\n3 -> 11\n4 -> 15\n5 -> 7\n6 -> 18"
    },
    {
      "id": "result",
      "kind": "result",
      "x": 1200,
      "y": 220,
      "width": 300,
      "height": 230,
      "title": "物理地址",
      "body": "物理块号 = 15\n页内地址 = 256\n\n最终结果 = (15, 256)"
    }
  ],
  "connectors": [
    {
      "from": "logic",
      "from_side": "right",
      "to": "check",
      "to_side": "left",
      "label": "先检查页号"
    },
    {
      "from": "check",
      "from_side": "right",
      "to": "ptable",
      "to_side": "left",
      "label": "合法则查页表"
    },
    {
      "from": "ptable",
      "from_side": "right",
      "to": "result",
      "to_side": "left",
      "label": "得到物理块号"
    }
  ]
}
```
