# Quickstart

这份指南面向第一次安装 Tealun Skills 的用户。目标是：先安全预览，再同步到你的本机 Agent 工具。

只用 Claude Code 的话，可以不用同步脚本，直接走插件市场，在会话里输入：

```text
/plugin marketplace add tealun/Tealun-Skills
/plugin install tealun-skills@tealun-skills
```

新建会话后技能即可使用，手动调用时写 `/tealun-skills:tasker` 这样的形式。下面的步骤是同步脚本的用法。两种方式在 Claude Code 里不要同时用，否则每个技能会出现两份。

用 WorkBuddy 等只能上传单个技能压缩包的平台，运行 `python3 scripts/build_suite.py` 生成套件包 `dist/dev-pdca-<版本>.zip` 后上传，详见 README 的「方式三」。

装好后，记得把技能触发条件写进项目指令，见 [docs/agent-instructions-snippet.md](docs/agent-instructions-snippet.md)。

## 1. 准备

你需要至少安装一种兼容 Agent Skills 的工具，例如 Codex、Claude Code、Cursor、Gemini、Kimi 或 OpenCode。

如果你不确定本机有没有可同步目标，先运行目标检测。

## 2. 查看会安装到哪里

Windows：

```powershell
.\sync-skills.ps1 --list-targets
```

macOS / Linux：

```bash
./sync-skills.sh --list-targets
```

如果没有检测到目标，请先打开或配置你的 Agent CLI，让它创建自己的配置目录。

## 3. 先 dry run

dry run 只显示将要复制到哪里，不会写入文件。

Windows：

```powershell
$env:DRY_RUN = '1'
.\sync-skills.ps1
Remove-Item Env:\DRY_RUN
```

macOS / Linux：

```bash
DRY_RUN=1 ./sync-skills.sh
```

## 4. 同步全部技能

Windows：

```powershell
.\sync-skills.ps1
```

macOS / Linux：

```bash
./sync-skills.sh
```

## 5. 只同步指定技能

Windows：

```powershell
.\sync-skills.ps1 tasker planner
```

macOS / Linux：

```bash
./sync-skills.sh tasker planner
```

## 6. WSL 用户

在 WSL 中运行 `sync-skills.sh` 时，默认会委托给 Windows 侧的 PowerShell 脚本，避免误写到 WSL 的 Linux home。

如需显式同步 WSL 环境：

```bash
./sync-skills.sh --target-env wsl
```

如需同时同步 Windows 与 WSL：

```bash
./sync-skills.sh --target-env all
```

## 7. 验证是否生效

重新打开你的 Agent CLI 或新建会话，然后尝试：

```text
用 tasker 执行一个小任务，并告诉我验证结果。
```

如果 Agent 能识别 `tasker` 的工作流，说明技能已加载。

## 常见问题

### 没有检测到目标怎么办？

先确认你的工具已经安装并运行过一次。部分工具只有在首次运行后才会创建配置目录。

### 同步后还是没生效怎么办？

关闭当前 Agent 会话并重新打开。很多工具只会在新会话启动时加载技能目录。

### 可以手动复制吗？

可以。把任意技能目录完整复制到目标工具的 `skills` 目录即可，例如把 `tasker/` 复制为 `~/.agents/skills/tasker/`。目录内的 `SKILL.md` 必须保留。
