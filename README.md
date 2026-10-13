# agent-skills

跨项目通用的 Agent Skill 集合，不绑定特定 Agent 工具（Claude Code、Codex 等均可使用）。

每个 skill 自包含、无绝对路径依赖，clone 后即可使用。

## Skill 清单

| Skill | 用途 |
|---|---|
| [`cfm`](cfm/) | 强化「先澄清、后执行」的行为约束：什么必须先问、怎么问、问到什么程度可以动手 |
| [`gpt-image`](gpt-image/) | 用 Codex CLI 的 ChatGPT 订阅能力生成或编辑位图，不需要 API key、不按张计费 |
| [`lark-doc-richtml`](lark-doc-richtml/) | 用飞书文档原生富组件（高亮块、分栏、HTML 块、SVG 画板）排版与增量编辑 |

## 安装

把需要的 skill 目录放到所用 Agent 的 skill 搜索路径下即可（复制或软链均可）。
各 skill 的具体依赖见其 `SKILL.md` 的「依赖」/「依赖与安装」一节。

## 约定

- 每个 skill 独立目录，含 `SKILL.md`（YAML frontmatter 带 `name` / `description`）。
- 脚本一律通过相对路径调用，不使用绝对路径；可变配置走环境变量。
- 新增 skill 请同步更新上表。

## 许可

[MIT](LICENSE)
