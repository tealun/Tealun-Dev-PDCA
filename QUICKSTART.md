# Quickstart

这份指南面向第一次安装 Tealun Dev PDCA 的用户。按你用的工具选一种方式；同一个工具里只用一种，否则每个技能会出现两份。

## Claude Code

在会话里输入：

```text
/plugin marketplace add tealun/claude-plugins
/plugin install dev-pdca@tealun
```

新建会话后技能即可使用；手动调用写 `/dev-pdca:tasker` 这样的形式。更新：`/plugin marketplace update tealun`。

## claude.ai（网页、桌面端）

从 [最新 Release](https://github.com/tealun/tealun-dev-pdca/releases/latest) 下载 `tealun-dev-pdca-<版本>.zip`，在 claude.ai 打开 Customize > Plugins > Add > Upload plugin 上传。

## Codex、Cursor、Gemini、Kimi、OpenCode 等

从 [最新 Release](https://github.com/tealun/tealun-dev-pdca/releases/latest) 下载 `tealun-dev-pdca-<版本>.zip` 并解压，把 `skills/` 下需要的技能文件夹复制到工具的技能目录（例如 `~/.codex/skills`、`~/.cursor/skills`、`~/.gemini/skills` 或共享的 `~/.agents/skills`），然后重新打开工具或新建会话。

## WorkBuddy 等只能上传单个技能的平台

从 [最新 Release](https://github.com/tealun/tealun-dev-pdca/releases/latest/download/dev-pdca.zip) 下载 `dev-pdca.zip` 上传，详见 README 的「方式三」。

## 装好之后

把技能触发条件写进项目指令，见 [docs/agent-instructions-snippet.md](docs/agent-instructions-snippet.md)。遇到问题看 [SUPPORT.md](SUPPORT.md)。
