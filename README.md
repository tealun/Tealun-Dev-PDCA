# Tealun Dev PDCA

中文 | [English](README.en.md)

让 AI Agent 少一点"我以为我做了"，多一点"我证明我做到了"。

Tealun Dev PDCA 用 PDCA（计划、执行、检查、改进）的方法组织 AI 辅助开发：5 个技能各管一个环节，彼此衔接成一个闭环；另有一个只读的 `explainer`，把 AI 写的代码翻译成不懂代码的人也能看懂的说明。它可以同步到本机 Agent 工具，可以作为 Claude Code 插件安装，也可以打成一个套件包（`dev-pdca`）上传到只支持单个技能的平台。它面向已经在用 Codex、Claude Code、Cursor、Gemini、Kimi、OpenCode 或共享 `.agents/skills` 目录的用户：你不用换工具，只是给代理加上几套更稳的工作方式。

## 先解决这些问题

如果你用 AI Agent 做项目，大概率遇到过这些时刻：

- 让它改文件，它说完成了，结果没有写入、没有回读、没有验证。
- 让它做规划，它很快写了一堆文档，但需求、架构和验收标准还是散的。
- 让它审计代码，它只挑风格问题，真正的安全、数据、部署风险没有证据。
- 让它修 bug，它没复现就改，改完以后你还得自己判断是不是碰巧好了。
- 一个问题这次聊明白了，下个会话又从头犯。
- AI 写了一大堆代码，你看不懂它由哪几块组成，也不知道改一处会牵连哪里。

这些问题的共同点是缺了一个环节：没想清楚就动手，做完不检查，检查出问题不追根，修好了不沉淀。所以这个仓库按 PDCA 把开发拆成 5 个技能，再配一个帮你看懂代码的 `explainer`。

## PDCA 开发闭环

| 环节 | 技能 | 做什么 |
| --- | --- | --- |
| Plan 计划 | `planner` | 写代码之前，把需求、架构、验收标准和阶段门槛定下来 |
| Do 执行 | `tasker` | 每次改动先定完成标准和可执行的检查，做完给出证据 |
| Check 检查 | `auditor` | 合并、发布前或按需审计，只报告有证据的问题 |
| Check → 修复 | `bugfixer` | 检查失败或出现症状时，复现、证明原因、最小修复、补回归测试 |
| Act 改进 | `evolver` | 把验证过的经验变成测试、规则、台账，作为下一轮计划的输入 |
| 看懂（贯穿各环节） | `explainer` | 只读：用白话、类比和 Mermaid 图讲清项目结构、功能流程、改动影响和每次提交，每条结论附文件路径，存进 `docs/explainer/` 并增量更新 |

技能之间会自动衔接：执行中检查失败，`tasker` 转交 `bugfixer`，修好后回到执行；改动涉及安全或部署时，先交给 `auditor`；同一个周期里第二次被纠正、以及周期结束时，`evolver` 各检查一次有没有值得固化的经验，有就提议落盘，喂给下一轮 `planner`。`explainer` 不占 PDCA 的某一格：`tasker` 或 `bugfixer` 动手之前，先用它看懂要改的地方；功能完成或审计之后，用它刷新项目地图。单个技能也能用，整套装上才是完整的闭环。

技能的重点不是让 Agent 多说，而是让它少猜、少跳步，并把每个环节的结果变成可检查的证据。

## 快速开始

四种安装方式都是一次装齐整套，按平台选一种即可：

- 用 Claude Code：推荐走插件市场，两条命令装好，以后一条命令更新。
- 用 claude.ai（网页、桌面端）：从 Release 下载插件包，上传即可安装。
- 用 Codex、Cursor、Gemini、Kimi、OpenCode 或共享 `.agents/skills` 目录：用同步脚本。
- 用 WorkBuddy 等只能上传单个技能压缩包的平台：用套件包 `dev-pdca`。

前两种方式下，6 个技能独立安装，各自按描述自动触发，冷启动时触发最精准。套件包把 6 个技能放进一个技能里，由入口统一分派，联动规则在整个会话里生效。

Claude Code 里不要两种方式都装，否则同一个技能会出现两份（`tasker` 和 `dev-pdca:tasker`）。同步脚本只要检测到 Claude 也会写入 `~/.claude/skills`，已经用插件安装的话，跑完脚本后可以删掉 `~/.claude/skills` 下这六个目录。

### 方式一：Claude Code 插件市场

在 Claude Code 会话里输入：

```text
/plugin marketplace add tealun/tealun-dev-pdca
/plugin install dev-pdca@tealun
```

也可以在终端里执行同样的操作：

```bash
claude plugin marketplace add tealun/tealun-dev-pdca
claude plugin install dev-pdca@tealun
```

装好后新建会话，六个技能都会加载。插件里的技能名带前缀，手动调用时写 `/dev-pdca:tasker`、`/dev-pdca:bugfixer` 这样的形式；自动触发不受影响。

更新：`/plugin marketplace update tealun`。也可以在 `/plugin` 的 Marketplaces 里给这个市场打开自动更新。

### claude.ai 一键安装

1. 打开 [最新 Release](https://github.com/tealun/tealun-dev-pdca/releases/latest)，下载 `tealun-dev-pdca-<版本>.zip`。同一个包也以 `.plugin` 为后缀附上，内容完全相同。
2. 在 claude.ai 打开 Customize > Plugins > Add > Upload plugin，上传这个 zip。

同一个工具里只保留一种安装方式，否则技能会出现两份。如果之前单独上传过 planner、tasker、bugfixer、auditor、evolver 这五个技能，先在技能设置里删掉它们，再装插件。插件发布新版本后，重新下载并上传。

### 方式二：同步脚本

把仓库里的技能同步到本机 Agent 工具的 `skills` 目录。建议先查看会写入哪些目标，再 dry run 预览一次，确认无误后正式同步。

#### Windows

```powershell
git clone https://github.com/tealun/tealun-dev-pdca.git
cd tealun-dev-pdca
.\sync-skills.ps1 --list-targets
$env:DRY_RUN = '1'
.\sync-skills.ps1
Remove-Item Env:\DRY_RUN
.\sync-skills.ps1
```

#### macOS / Linux

```bash
git clone https://github.com/tealun/tealun-dev-pdca.git
cd tealun-dev-pdca
bash ./sync-skills.sh --list-targets
DRY_RUN=1 bash ./sync-skills.sh
bash ./sync-skills.sh
```

#### 只同步指定技能

如果你只想安装某几个技能，把技能名放到命令末尾：

```powershell
.\sync-skills.ps1 tasker planner
```

macOS / Linux：

```bash
bash ./sync-skills.sh tasker planner
```

安装后，重新打开你的 Agent CLI 或新建会话，让工具重新加载技能目录。

### 方式三：套件包 dev-pdca

直接下载仓库根目录的 [`dev-pdca.zip`](dev-pdca.zip)，在平台的技能导入或上传入口选择它即可。它包含入口技能和全部 6 个子技能，与仓库里的技能源码保持同步（每次推送由 CI 校验）。

如果平台要求 `SKILL.md` 直接位于压缩包根目录，在仓库里运行 `python3 scripts/build_suite.py`（需要 Python 3，无第三方依赖），上传生成的 `dist/dev-pdca-<版本>-flat.zip`。

装好后不用记技能名，直接说要做的事：

```text
做一次审计，重点看部署风险
修复这个 500 报错，先复现再改
帮我梳理 M0 计划
```

也可以点名：`/dev-pdca 审计 当前项目`、`/dev-pdca bugfixer 这个报错`。只输入 `/dev-pdca` 会列出整套技能。

## 让 Agent 真的调用技能

装好技能不等于 Agent 会用。项目指令里如果没写什么时候该用哪个技能，Agent 往往按自己的习惯干活，技能装了一整个开发周期也可能一次都不被调用。解决办法是在项目的 `CLAUDE.md` 或 `AGENTS.md` 里写明触发条件。

把下面这段复制进你项目的指令文件：

```markdown
## 配套技能：要调用，不要只“照着精神做”

本项目使用 Tealun Dev PDCA（planner、tasker、bugfixer、auditor、evolver、explainer）。触发条件满足时，通过技能工具调用对应技能（或读取它的 SKILL.md 并按步骤执行）；只按“大意”去做不算调用。每个会话的第一条回复，先说明这六个技能里哪些可用；缺哪个就直说。

- **planner：任何规划意图，不论大小。** 功能、页面、URL 或站点结构调整、数据或 schema 变更、重构、发布、路线图、文档体系或流程。在写代码或内容之前调用，先把决定写进对应文档。
- **tasker：任何对文件或状态的改动。** 动手前写清完成定义和一个可执行的检查；收尾时给出证据（命令输出、截图），不要只给描述。只读的问答不需要。
- **bugfixer：用户说有问题或“还是不对”、截图里能看到缺陷、或者某个检查失败时。** 先复现或直接观察，证明原因，只修这个原因，再验证最初的症状已经消失。
- **auditor：推送安全、部署、URL 参数或共享状态相关的改动之前，发布之前，以及任何审计请求。**
- **evolver：用户报告的问题修好并验证之后、同一周期内第二次被纠正之后、以及每个工作周期结束时。** 把经验和对应的防线记到 `docs/98_evolution/evolution-ledger.md`。
- **explainer：用户看不懂要改的地方，或想知道项目由哪几块组成、某个按钮点了之后发生什么、改一处会牵连哪里、AI 刚才改了什么时。** 只读，不改代码；白话说明写进 `docs/explainer/`，每条结论附文件路径。tasker 或 bugfixer 动手前先用它确认要改的地方；功能完成或审计之后用它刷新项目地图。
```

英文版片段、各工具的指令文件名，以及在云端会话里技能缺失时怎样把技能固定版本放进项目，见 [docs/agent-instructions-snippet.md](docs/agent-instructions-snippet.md)。

## 安装后怎么用

进入你的项目目录，重新打开 Agent CLI 或新建会话。在 Codex 这类支持 slash command 的工具里，直接输入：

```text
/tasker 检查当前项目 README 是否有断链，并给出验证结果。
/auditor 审计当前项目，优先看 README、安装脚本和文档一致性。
/bugfixer 修复这个 500 报错，先复现再改。
/planner 梳理这个项目的 M0/M1 计划，先找架构风险。
/evolver 把这次已验证的修复经验落到项目规则和演进台账。
/explainer 给我做一次全局导览，再追踪一下点“保存”之后发生了什么。
```

不支持 slash command 的工具，把 `/tasker` 换成“用 tasker”这类自然语言即可。

如果技能已加载，Agent 会按对应技能的工作流执行。比如 `tasker` 会说明任务范围、验证方法、执行证据和最终结论，而不是只给一句"看起来没问题"。

### 自动触发

很多 Agent 会根据每个技能 `SKILL.md` 里的 `description` 自动选择技能。你不一定要手动输入 `/tasker`：

- 说“帮我把这个任务做完，并给出验证结果”时，通常会触发 `tasker`。
- 说“审计这个项目”“做一次代码 review”“检查安全和部署风险”时，通常会触发 `auditor`。
- 贴出报错、500、回归问题，或者说“还是不对”“先复现再修”时，通常会触发 `bugfixer`。
- 说“需求梳理”“技术方案”“M0/M1 计划”“项目规划”时，通常会触发 `planner`。
- 说“固化经验”“防止复发”“落到规则/台账/复盘”时，通常会触发 `evolver`。
- 说“给我讲讲这个项目”“这个按钮点了之后发生什么”“改这里会影响哪里”“AI 刚才改了什么”时，通常会触发 `explainer`。

如果 Agent 没选中，直接用 slash command 强制指定即可。在长期项目里，更可靠的做法是按上面「让 Agent 真的调用技能」把触发条件写进项目指令。

更完整的安装和排障步骤见 [QUICKSTART.md](QUICKSTART.md)。

## 该用哪个技能

| 你的场景 | 推荐技能 | 它会帮你守住什么 |
| --- | --- | --- |
| 项目刚开始，需求、架构、里程碑还不清楚 | `planner` | 把决策、假设、待验证项和阶段门槛写清楚，减少边做边猜 |
| 你要 Agent 改代码、补文档、跑检查 | `tasker` | 每个完成声明都要有产物和验证，避免"说做了但没做" |
| 合并、发布或交付前想查风险 | `auditor` | 只报告有证据的问题，并区分严重性、置信度和验证缺口 |
| 已经有报错、回归、异常表现 | `bugfixer` | 先复现和定位，再做最小修复，修好后补回归测试，避免靠经验猜 bug |
| 同类问题反复出现，想把教训留住 | `evolver` | 把已验证经验变成规则、检查、台账或下一轮计划输入 |
| 看不懂 AI 写的代码，改之前想先弄明白 | `explainer` | 只读不改代码；每条结论附文件路径，敏感区域（密钥、支付、用户数据、数据库结构）单独标出 |

## 安装到哪里

同步脚本会检测本机已经安装或配置过的兼容工具，把技能复制到对应的 `skills` 目录。当前覆盖：

- Claude
- Codex
- Cursor
- Gemini
- Kimi
- Kimi Desktop（Windows）
- OpenCode
- Shared agents (`~/.agents/skills`)

脚本采用覆盖式复制：仓库里的技能内容会同步到目标目录；目标目录里仅本地存在的元数据文件通常会保留。同步前先跑 `DRY_RUN=1`，可以看到将要写入的位置。

## 更新技能

插件市场安装的，在 Claude Code 里运行 `/plugin marketplace update tealun`。

同步脚本安装的，拉取最新内容后重新运行同步脚本即可。

macOS / Linux：

```bash
git pull
bash ./sync-skills.sh
```

Windows：

```powershell
git pull
.\sync-skills.ps1
```

## 项目结构

```text
.
├── .claude-plugin/   # Claude Code 插件市场清单（marketplace.json）
├── auditor/          # 证据驱动的项目审计技能
├── bugfixer/         # 面向具体症状的修复技能
├── evolver/          # 把经验固化为长期防线的复盘技能
├── explainer/        # 把代码翻译成白话说明的只读技能
├── planner/          # 项目前期规划技能
├── tasker/           # 通用任务执行纪律技能
├── suite/dev-pdca/   # 套件包入口：PDCA 分派规则
├── scripts/          # build_suite.py：构建 dev-pdca 套件包
├── dev-pdca.zip      # 套件包成品，供 WorkBuddy 等单技能平台上传
├── docs/             # 指令片段、本仓库的演进台账
├── sync-skills.ps1   # Windows 同步脚本
└── sync-skills.sh    # macOS / Linux / WSL 同步脚本
```

## 遇到问题

先看三件事：

1. 你的 Agent 工具是否支持目录型 `SKILL.md` 技能包。
2. `--list-targets` 是否能找到目标目录。
3. 同步后是否重新打开了 Agent CLI 或新建会话。

更多排查方式见 [SUPPORT.md](SUPPORT.md)。想贡献改进可以看 [CONTRIBUTING.md](CONTRIBUTING.md)。安全相关问题请按 [SECURITY.md](SECURITY.md) 处理。

## 许可证

本项目使用 MIT License，详见 [LICENSE](LICENSE)。
