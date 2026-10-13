---
name: lark-doc-richtml
description: 用飞书文档的原生富组件排一篇文章——高亮块、分栏 grid、HTML 块（可直接写前端页面）、SVG 数据图画板、带语义底色的表格，以及在已有文档上增量插入这些组件时的编排与踩坑。写飞书文档、给文档加图表/卡片/分栏、把数据做成图、在已有飞书文档上补组件时使用。只讲组件语法与编排；文档结构、文风与创建流程以 lark-doc 为准，整篇定稿版的封面/语音/配图流程以 lark-doc-showcase 为准。
---

# 飞书原生富组件编排

按内容的信息关系选组件，而不是按版面好看选。组件的准确语法、创建与更新流程以 `lark-doc` skill 为准（`references/lark-doc-xml.md`、`lark-doc-xml-extended-blocks.md`、`lark-doc-update.md`）；本 skill 只补「选哪个组件、怎么写、哪里会踩坑」。

本 skill 通过 `lark-cli` 操作飞书文档，命令写法见下；`<skill-dir>` 指本 skill 的目录，脚本按相对路径调用即可。

## 组件选型

按真实信息关系对照，不要为了版面丰富硬套组件：

| 信息关系 | 组件 | 标签 |
|-|-|-|
| 同组字段的精确比较或映射 | 表格 | `<table>` |
| 两组以上简短并列信息横向阅读 | 分栏 | `<grid>` + `<column>` |
| 单个关键提醒、口径说明、限制 | 高亮块 | `<callout>` |
| 复杂版式图表、信息卡、可复用的前端片段 | HTML 块 | `<html5-block>` |
| 幅度、区间、分布、趋势 | SVG 画板 | `<whiteboard type="svg">` |
| 流程、依赖、因果、时序、拓扑 | 画板（mermaid/svg） | `<whiteboard>` |
| 简单并列、步骤、连续论述 | 列表或段落 | `<ul>` / `<p>` |

同一篇文档内同类关系复用同类组件。去掉后不影响读者任务的装饰性组件，不加。

## 各组件要点

### 高亮块 callout

```xml
<callout emoji="📌" background-color="light-blue"><p>内容</p></callout>
```

- **子块只能放** `p`、`ol`、`ul`、`checkbox`，以及行内标签。放 `table`、`img`、`pre`、`hr`、`grid`、`whiteboard` 会失败。
- 图片要与 callout **并列放进同一个 grid 列**，不能塞进 callout 里。
- 背景色用 `light-*`；强提醒才用 `medium-*`，彩色文字只强调短语。

### 分栏 grid

```xml
<grid><column width-ratio="0.5"><p>左</p></column><column width-ratio="0.5"><p>右</p></column></grid>
```

- 各列 `width-ratio` **之和必须为 1**。四列用 0.25，三列用 1/3，两列 0.5。
- 每列可放 `p`、`callout`、`img`、`whiteboard` 等块级标签。
- 常见用法：KPI 指标卡（4 列 callout）、结论分组（2×2 彩色 callout）、图配文。

### HTML 块 html5-block

把完整单文件 HTML 存成 `.html`，XML 写 `<html5-block path="@./widget.html"/>`。

**必须的 head 声明**（缺了会渲染异常）：

```html
<meta name="use-iframe" content="true">
<meta name="html-box-height-mode" content="auto">
<meta name="description" content="内容摘要，会导出为 alt">
```

- `html-box-height-mode`：正文需完整展开用 `auto`（普通文档流，根容器不要设固定高度或 `overflow:hidden`）；需单屏滚动/切页用 `viewport`（配 `100vh`）。
- 文档可用宽度约 **820px**，根容器用 `width:100%; max-width:100%; box-sizing:border-box`。
- **HTML 总长上限 500KB**，不要内联大图、Base64、字体、长 JSON。
- **静态渲染**：飞书文档里的 HTML 块不执行交互脚本，点击、悬浮、动画都不会响应。数字是硬编码的，不随数据更新。要交互得换载体。
- 做成 KPI 卡、迷你条形图、信息仪表板这类「HTML 更精细而 SVG 太笨重」的场景最合适。

### SVG 数据图画板

```xml
<whiteboard type="svg" path="@./chart.svg"></whiteboard>
```

- 路径**相对 lark-cli 运行的 CWD**，不是草稿目录。`@./draft_xxx/chart.svg` 而非 `@./chart.svg`（后者会报 `cannot read file`）。
- SVG 必须自包含：有 `<svg>` 根与 `viewBox`，不引用外部图片、脚本、远程资源。
- 画板是**可编辑的**，创建时返回 `block_token`，之后可在飞书里直接改。
- 导出核对：`lark-cli whiteboard +export --whiteboard-token <token> --output-type preview --output ./wb.jpg`（扩展名必须是 `.jpg`）。
- 图要能独立读懂：标轴、单位、分母、时点；图里带关键数字；图下方给一句文字结论，视觉不作为唯一证据。

## emoji 回退（高频坑）

飞书只认常见单码位 emoji。**带变体符号的会被强制替换成 💡**，实测会回退的包括：`⚠️` `⚔️` `⏱️` `↔️` `🕹️` `⚖️` `🗓️` `🧩` `🧭` `🚩`，以及所有彩色方块类 `🟦🟩🟧🟪`。

写法：**只用单码位、无变体选择符的**，例如 `📌` `📈` `🔎` `👥` `✅` `⏳` `🏆` `❗` `🎯`。

- 写入前：`python3 scripts/check_emoji.py draft.xml`
- 写入后：`python3 scripts/check_emoji.py --doc <token>`，`fallback_bulb` 必须为 0（除非本来就用了 💡）。
- 回退发生在**写入时**，写进去就已经是 💡。所以事后 `str_replace` 搜 `🟦` 是搜不到的——必须按 callout 的 `block_id` 整块 `block_replace` 才能改。

## 在已有文档上增量插入

改已有文档走 `block_insert_after`，不要 `overwrite`（会清空图片、评论、他人替换过的配图）。

流程：
1. `docs +fetch --doc <token> --scope outline --max-depth 2 --detail with-ids` 拿到各章节标题的 `block_id`。
2. 按「插在哪个标题之后」逐处 `block_insert_after --block-id <标题id> --content "<新组件>"`。
3. 每轮写完 **block ID 全部变化**，下一步基于最新 fetch，不要沿用旧 ID。

会失败的两处：
- **`block_replace` 换标签类型会失败**。callout 直接换成 grid 报 `degrade_code=1010 Nesting still failed`。层级不兼容时拆成更小的操作：改单个 callout 就用 `block_replace --block-id <callout的id>` 换成另一个单 callout（不嵌套 grid）。
- **`str_replace` 找不到字符**说明该内容存进文档时已被改写（如 emoji 回退）。改用 `block_replace` 按 ID 换。

**表格列宽**用 `<colgroup><col width="120"/></colgroup>` 紧跟 `<table>`。表头 `background-color="light-gray"`，合计行用 `medium-gray`，需强调的行用 `light-orange` 等，避免整表铺色。

## 写作纪律（与内容层的关系）

组件不改变内容判断。结论先行、不写开篇前言、章节标题用名词短语、单位统一、不用比喻——这些遵循使用方自己的文风规则，本 skill 只管呈现。数据图的数字必须与正文逐字一致，不从图里引入新数字。

## 交付前核对

1. `docs +script --command parse --content "@./<draft>"` 通过（`data.assessment.status == passed`）。
2. `check_emoji.py --doc <token>`，`fallback_bulb` 为 0。
3. 回读统计组件数：`python3 scripts/count_blocks.py --doc <token>`，确认 grid / callout / html5-block / whiteboard / table 数量符合计划。
4. 关键数字与正文对照一遍。

## 依赖

- `lark-cli`：飞书命令行工具。
- 官方 `lark-doc` skill：本 skill 依赖它提供 XML 语法与文档读写流程。
- Python 3 标准库（脚本无第三方依赖）。
