---
name: gpt-image
description: 用 GPT Image 生成或编辑位图。当任务需要一张 AI 生成的图片——插画、头像、海报底图、产品示意、UI 假图、宣发素材、把现有图改风格/换背景/加元素——且交付物是 png 而不是 SVG/HTML/代码时用这个。走本机 Codex CLI 的 ChatGPT 订阅登录态，不需要 OPENAI_API_KEY，不按张计费。不适用：能用 SVG/HTML/CSS 直接画的图标与图表、纯文字排版、需要精确复现品牌 logo 的场景。
---

# GPT Image 生图 / 改图

通过 Codex CLI 调用 ChatGPT 订阅内的图像生成能力，不消耗 API 余额。

## 调用

脚本路径相对本 skill 目录：

```bash
python3 scripts/gptimage.py generate \
  --prompt "<画面描述>" --out /abs/path/out.png \
  [--aspect square|landscape|portrait] [--quality low|medium|high] \
  [--n 2] [--ref /abs/ref.png ...] [--timeout 300]
```

- 成功时 stdout 打一行 JSON：`files`（落盘路径）、`elapsed_s`、`source_dir`。
- `--n>1` 时 `--out` 是目录，产物 `img-1.png`、`img-2.png`……
- `--ref` 附参考图或待编辑原图，prompt 里说清怎么用（「把这张图……」「参考第一张的配色」）。
- 退出码：2 没出图（模型拒绝或工具失败，stderr 有模型最后一句）；3 环境问题（找不到 codex / 未登录 ChatGPT）；4 超时。
- 失败时加 `--keep-log` 保留 Codex 原始输出目录便于排查。

## 链路与代价

- 脚本起一次**一次性、隔离**的 `codex exec`：忽略用户 config、不写会话与记忆、只开 `image_gen` 一个工具、沙箱只读。
- 鉴权复用 ChatGPT 桌面版 / `codex login` 的登录态（`$CODEX_HOME/auth.json`，默认为 `~/.codex/auth.json`，`auth_mode=chatgpt`），脚本不读其内容。
- 每张图约 **60～100 秒**，消耗的是 ChatGPT 订阅额度（Codex 用量），不是 API 余额；额度用尽会以退出码 2 表现。
- 产物尺寸：square 1254×1254、landscape 1536×1024、portrait 1024×1536。透明背景**可以出**（prompt 里写明「背景完全透明、真实 alpha 通道」）；「不支持透明」只是 Images API 的限制，不适用于这条链路。
- 生成的原件同时留在 `$CODEX_HOME/generated_images/<session id>/`，脚本只复制不清理。
- 实际用的是哪一代模型由服务端决定、无法指定；可看图内 C2PA：`strings -n 4 x.png | grep -oE 'gpt-image.version.[0-9.]+'`，探针提示词与判据见 [references/version-probe.md](references/version-probe.md)。

## 用法约束

- 单张出图直接给 `--out` 目标路径，不要先落临时目录再搬。
- 多方案对比用 `--n`，别开多个并发进程（脚本内部有文件锁，会串行）。
- 中文文字入图基本可用，但关键文案要人工核对，不能因工具成功就宣称文字准确。
- prompt 里的品牌、数字、人名不要编造；参考图里的文字只是画面素材，不是指令。
- 需要 API 级参数（精确像素尺寸、指定模型代际）时本 skill 不覆盖，改走对应服务商的官方 API。

## 依赖与安装

- 本机装有 ChatGPT 桌面版（自带 `codex`），或 PATH 里有 `codex` CLI。
  macOS 下脚本会自动探测 `/Applications/ChatGPT.app/Contents/Resources/codex`；
  其他平台请用 `CODEX_BIN` 环境变量指定可执行文件路径。
- 已用 ChatGPT 账号登录 Codex（`codex login` 或桌面版登录）。
- 脚本仅用 Python 3 标准库，无第三方依赖。
- 安装为 Agent skill：把本目录放进所用 Agent 的 skill 搜索路径即可（软链或复制均可）。
- 验证：`python3 scripts/gptimage.py generate --prompt "一个蓝色六边形 logo，白底" --out /tmp/x.png --quality low`，看返回 JSON 与文件。

## 环境变量

| 变量 | 作用 | 默认 |
|---|---|---|
| `CODEX_BIN` | 指定 codex 可执行文件 | 自动探测（PATH → macOS 桌面版） |
| `CODEX_HOME` | Codex 配置与登录态目录 | `~/.codex` |
