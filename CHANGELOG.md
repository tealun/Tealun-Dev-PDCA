# Changelog

本文件记录 Tealun Skills 项目层面的重要变化。单个技能的历史说明可能位于各自目录内。

## Unreleased

- `dev-pdca.zip` 不再提交进仓库（规划见 `docs/88_planning/suite-zip-out-20261105.md`）。原因：仓库根目录同时是 Claude 插件文件夹，官方提交清单写明，插件文件夹里的 `.zip` 会转人工审核。现在 `build_suite.py` 把包输出到 `dist/dev-pdca.zip`；`--check` 改为校验并在内存里构建，不再与仓库里提交的成品比对；`release.yml` 构建后把它附到 Release 上，附件名不变。WorkBuddy 用户改从 `releases/latest/download/dev-pdca.zip` 下载。包内容不变：重新构建出的包与 v1.0.1 Release 上的附件 sha256 一致（50365d88…）。
- `tasker` 1.12.0、`bugfixer` 1.7.0、`dev-pdca` 1.5.0：遵守率监测与第三批修正（规划见 `docs/88_planning/compliance-monitoring-20261104.md`）。`bugfixer` 正文定义什么算“还是不对”：交付的行为坏了，或者没做到已约定的结果；改措辞、标点、风格、命名、在已确认目标内换文件、改范围，属于需求修正，由 `tasker` 退回 clarify 或 plan 重做，不转 bugfixer。`tasker` 的 Post-Error Restraint Gate 只针对仓库或项目选错；只有确实还剩事情时才写下一步，没有就写“下一步：无”，不再为了凑格式编一个可选步骤。`check_ledger.py` 同时检查 `compliance-log.md` 的行格式和取值；新增 `tests/test_scripts.py`（15 个 unittest，覆盖台账追加、台账与遵守率检查、套件打包校验）并接入 CI。新增每周定时独立审计，读取云端会话记录按 G1–G5 打分，结果以 PR 提交。按全新 agent 第二次试跑的反馈：快速通道里用户给出的文本一律原样写入，格式惯例只管用户没指定的部分（之前惯例会自作主张加句号）；挪动一行算作必须一起改的两个文件；没有远端时 `<repo>` 写目录名；收尾的三行里，下一步只在确实还剩事情时才写；改换文件属于范围纠正，撤掉错改的那处是新契约的一部分，用户已经给过的细化要求带到新文件。`bugfixer` 观察到约定结果其实已经在位时，停下报告并交回，不改任何东西；用户说法前后矛盾时，引用两次原话请用户确认以哪次为准。`evolver` 1.2.1：描述和正文对第二次纠正检查点的说法统一；只完成一步、整体目标还没完成的回复不算收尾。
- `tasker` 1.12.0、`evolver` 1.2.0、`planner` 2.3.0、`dev-pdca` 1.4.0：评审遗留项（规划见 `docs/88_planning/review-followup-2-20261104.md`）。`tasker` 新增小改动快速通道：用户已说清具体改什么、只涉及一个文件（或必须一起改的两个文件）、不碰共享契约/配置/安装/发布/凭据/生产、可直接回退时，用一行写出契约和检查，用户的指令即算确认，收尾给检查的实际输出；条件不再满足或检查失败就回到完整的 M 级流程。Code Commenting Gate 和提交/推送收口移到 `references/`，按条件加载。`INTRO.md` 和 `RELEASE_*.md` 移到 `docs/releases/tasker/`，不再随技能安装。`evolver` 去掉会话中途的静默追踪，没有显式调用时只在第二次被接受的纠正之后和周期收尾时各做一次 advisory 检查；`append_evolution_ledger.py` 在非 Git 目录下退回使用 `--root`，不再抛异常；台账里 `Corrected`/`Guarded` 的行算未闭合，后续拿到证据时原地升级，`planner` 遇到相关的未闭合行要转成 To Verify。`build_suite.py` 校验六个子技能的 frontmatter 字段集合一致、description 不超过 1024、version 为 x.y.z（字段取舍：保留 Claude Code 扩展字段和顶层 `version`，原因见规划 F7）。
- `tasker` 1.12.0、`bugfixer` 1.6.2、`planner` 2.2.0、`evolver` 1.1.0、`dev-pdca` 1.3.0：落实 2026-11-04 专家评审的五项改进（规划见 `docs/88_planning/review-followup-20261104.md`）。`tasker` 的触发描述收窄为“执行对文件或状态的改动”，删去调试、评审、规划、分析等越界词，并写明失败、评审、规划、读代码、复盘分别交给哪个技能。转入 bugfixer 的兜底阈值只在 `bugfixer` 正文定义一处：去掉 “roughly”，把“一轮诊断交换”定义成可计数的单位；`tasker` 正文和 `dev-pdca` 会话规则改为引用这一处，两份描述不再写这条阈值。`planner` 规划第一步先读演进台账，把相关的 `Next Planning Input` 写进 Decisions 或 To Verify，交接时列出用到的条目，补上 PDCA 从 Act 回到 Plan 的入口。`evolver` 补上 `argument-hint`、`user-invocable`、`disable-model-invocation` 字段，描述里加入“复盘、总结经验、吸取教训、下次别再犯”等日常说法。新增 `docs/98_evolution/compliance-log.md`，每个周期结束时按 5 道 Gate 记录规则有没有被遵守，满 10 个周期后统计遵守率；`AGENTS.md` 写入这条要求。
- `tasker` 1.12.0、`planner` 2.1.0、`evolver` 1.0.0（首次声明版本）、`dev-pdca` 1.2.0：吸收外部技能 delivery-no-pseudoblock 的四点（规划见 `docs/88_planning/delivery-gate.md`）。`tasker` 新增 Delivery Gate，适用于每条回复（含只读问答、状态汇报和提问）：在最后一次工具调用之后对整条草稿检查，结尾一句同样受检；回复中已判明的最优下一步在授权和范围内就先做完，不包装成“如需 / 你定 / 回头再说”；只在需要新授权、扩大范围、破坏性风险、工具拿不到的输入或属于用户的取舍时提问，不放宽 M/L 副作用确认；约束性文本去掉以动机为条件的禁止、预埋借口和自拟豁免。`tasker` 验证协议要求 Observation 写出实际看到的内容，单独的“通过”不算观察。`evolver` 写防线、`planner` 写开发指引时套用同一条规则文本检查。`dev-pdca` 会话规则要求每条回复过 Delivery Gate。
- 新增 `scripts/check_ledger.py` 并接入 CI：演进台账编号必须唯一、格式正确、每行 8 列，防止并行分支各自追加同一编号后被合并进 main。
- `dev-pdca` 1.0.2：WorkBuddy 审核以“zip 内含 6 个 SKILL.md，属多 skill 包”驳回。打包时子技能入口改名为 `<名称>/<名称>.md` 并去掉 frontmatter，入口技能按新路径查找子技能；`build_suite.py` 校验包内只有根目录一个 `SKILL.md`、其他 `.md` 不带技能 frontmatter、文件无 UTF-8 BOM。新增 `docs/workbuddy-rules.md`，逐条列出 WorkBuddy 已知规则、来源和对应的本地检查。
- 新增只读技能 `explainer` 1.0.0：面向用 AI 开发、但不读代码的人，把代码库翻译成白话说明。四种模式：全局导览、功能追踪、改动影响、读懂变更；默认中文，术语附白话解释并汇总成术语表，用 Mermaid 画模块关系与流程，每条结论标注文件路径，密钥、支付、用户数据、数据库结构、登录与权限单独标出。产出写入目标项目的 `docs/explainer/`，按基线提交增量更新；绝不修改代码，疑点转交 auditor / bugfixer。规划见 `docs/88_planning/explainer-skill.md`。发布前用全新 agent 在真实项目上试跑一次，按反馈补齐：多模式请求按顺序执行、同一功能多入口时说明选择、公开配置与机密分开、行号必须取自当时的搜索输出、长链路分段、Mermaid 时序图规模上限、配置项引用格式、项目需保持不动时的产出位置。
- `AGENTS.md` 新增硬规则：新增或大改技能后、发布前，用只拿到 `SKILL.md` 的全新 agent 在真实项目上试跑；样本项目只读。
- `dev-pdca` 1.1.0：加入 `explainer` 子技能的路由与会话规则（tasker / bugfixer 动手前可先用它看懂要改的地方，功能完成或审计后可刷新项目地图）；入口描述同步更新并仍满足 WorkBuddy 长度限制。插件清单、README（中英）、指令片段、`AGENTS.md` 与 issue 模板同步加入 `explainer`。
- `tasker` 1.8.4、`bugfixer` 1.6.1、`dev-pdca` 1.0.1：CI 失败、外部平台上传/发布/审核被拒明确列为转入 bugfixer 的触发信号（描述与正文同步）；`tasker` 的 Acceptance Gate 要求交付给外部系统时，先收集其验收规则并尽量写成本地检查，不再靠逐次被拒来发现规则。
- 新增仓库根目录 `AGENTS.md` 与 `CLAUDE.md`：本仓库自己的工作也按触发条件调用这五个技能，并写入发布前先查清平台规则、改技能后重建套件包等仓库规则。
- `dev-pdca` 示例按 WorkBuddy 上限减为每种语言 3 条（规划、修复、复盘），新增 `category: developer`；`build_suite.py` 一并校验 WorkBuddy 已知限制：`name` 格式、`display_name_en` ≤ 60、`description_zh` ≤ 500、`description_en` ≤ 1000、示例 1–3 条。
- `dev-pdca` 补充 `examples_zh` / `examples_en`（WorkBuddy「试试这样问我」示例，各 5 条，覆盖五个子技能，按实际使用场景改写）和 `author`；`build_suite.py` 校验示例字段存在。
- `description_en` 压缩到 WorkBuddy 上限 1000 字符以内；`build_suite.py` 校验 `description_zh` / `description_en` 不超过 1000 字符。
- `dev-pdca` 的 `description_zh` / `description_en` 改写为完整的能力介绍：逐个说明五个子技能各自守住什么，以及它们之间如何自动接力。
- `dev-pdca` 入口补充 WorkBuddy 上架必填的 frontmatter：`display_name`、`display_name_en`、`description_zh`、`description_en`；`build_suite.py` 校验这四项。
- `dev-pdca` 套件包改为最多三层目录（`dev-pdca/<子技能>/<文件>`），以满足 WorkBuddy 的层级限制：子技能的 `references/`、`scripts/` 文件在打包时移到子技能目录下，文中引用路径同步改写；不再打包 Codex 专用的 `agents/` 元数据。仓库内技能源码结构不变。
- 新增套件包 `dev-pdca` 1.0.0（`suite/dev-pdca/SKILL.md`）：一个入口技能按 PDCA 分派到 5 个子技能，面向 WorkBuddy 等只能上传单个技能的平台。子技能文件按 `./<name>/SKILL.md`、`../<name>/SKILL.md` 顺序解析，套件包与仓库/插件两种目录结构都能用；原本分散在各技能描述里的自动转交条件，集中为会话级规则。
- 新增 `scripts/build_suite.py`：校验入口描述长度、版本号和子技能完整性，生成仓库根目录的 `dev-pdca.zip`（可直接下载上传）和 `dist/` 下的 `-flat.zip`。构建结果逐字节可复现，`--check` 用来发现成品与源码不一致。
- 新增 CI `.github/workflows/suite-package.yml`：每次推送校验 `dev-pdca.zip` 与技能源码一致。
- README（中英文）与插件清单改为以 PDCA 开发闭环介绍技能分工与衔接，并增加套件包安装方式。
- 新增面向开源用户的项目 README。
- 新增快速开始、支持、贡献、行为准则、安全策略和许可证文件。
- 明确技能集合、安装方式、兼容工具和反馈路径。
- `bugfixer` 增加生成物新鲜度/版本失效检查，以及部署进程找不到 CLI 二进制时的环境差异排查规则。
- `tasker` 增加提交/推送收口校验：区分用户改动与任务文件、回读本地提交，并用远端分支 SHA 验证推送结果；多阶段任务在阶段边界 checkpoint，清理仅限明确生成物。
- `bugfixer` 1.6.0：原症状验证消失后，项目有测试框架时要补一条不带修复就会失败的自动化回归测试（没有测试框架时补最接近的可执行检查）；条件允许时临时撤掉修复做一次变异检查，证明这条测试真的能拦住问题。没有可用框架时写明原因并作为未防护缺口报告。
- 新增 `docs/agent-instructions-snippet.md`：可直接粘贴到项目 `CLAUDE.md` / `AGENTS.md` 的中英文技能触发片段，以及在云端会话里把技能固定版本放进项目的做法。
- 新增 Claude Code 插件市场清单 `.claude-plugin/marketplace.json`：`/plugin marketplace add tealun/Tealun-Skills` 后 `/plugin install tealun-skills@tealun-skills` 即可安装五个技能。技能目录位置不变，同步脚本照常可用。
- README 增加插件安装方式、「让 Agent 真的调用技能」指令片段；新增英文版 `README.en.md`，两份 README 顶部互相链接。

## tealun-dev-pdca 1.0.1（2026-11-05）

品牌更名：Tealun Skills 改名为 Tealun Dev PDCA。六个技能的名称和行为都不变。

- 插件名改为 `dev-pdca`，上架名称为 Tealun Dev PDCA；手动调用改为 `/dev-pdca:tasker` 这样的形式。
- 插件市场名改为 `tealun`。在 Claude Code 里安装：`/plugin marketplace add tealun/tealun-dev-pdca`，然后 `/plugin install dev-pdca@tealun`。
- 仓库改名为 `tealun/tealun-dev-pdca`，旧地址会自动跳转。下载文件改名为 `tealun-dev-pdca-<版本>.zip` / `.plugin`。
- **从 1.0.0 升级**：插件名变了，不会自动更新。在 Claude Code 里先卸载 `tealun-skills@tealun-skills`、移除旧市场，再按上面的命令安装；在 claude.ai 上删除旧插件，再上传新的 zip。
- 每个技能的 `SKILL.md` 末尾加了一行出处（作者、仓库、MIT）。LICENSE 的版权人改为 Tealun。套件包 `dev-pdca` 升到 1.5.1，内容只多了这行出处。规划见 `docs/88_planning/rename-dev-pdca-20261105.md`。

## tealun-skills 1.0.0（2026-11-04）

首个插件版本：仓库本身是一个合规的 Claude 插件，发布由推送 `v<版本>` tag 触发，CI 自动生成 GitHub Release。

- 包含六个技能：`planner` 2.3.0、`tasker` 1.12.0、`bugfixer` 1.7.0、`auditor` 4.1.0、`evolver` 1.2.1、`explainer` 1.0.0。
- 安装：在 claude.ai 打开 Customize > Plugins > Add > Upload plugin，上传 Release 里的 `tealun-skills-1.0.0.zip`（同一内容另附 `tealun-skills-1.0.0.plugin`）；在 Claude Code 里用 `/plugin marketplace add tealun/Tealun-Skills` 安装。同一个工具里只保留一种安装方式；从早先单独上传的技能升级时，先删掉旧的五个。
- 新增 `.claude-plugin/plugin.json`，插件版本只在这一处记录。新增 `scripts/build_plugin.py`：校验插件清单、技能引用的文件、插件目录的提交规则，以及“技能改了就要升版本”，再可复现地打包。新增 `.github/workflows/release.yml`。新增 `docs/claude-directory-rules.md`。规划见 `docs/88_planning/plugin-release-20261104.md`。

## 现有技能

- 插件 `dev-pdca` 1.0.1（Tealun Dev PDCA；六个技能的组合版本，见 `.claude-plugin/plugin.json`）
- `planner` 2.3.0
- `tasker` 1.12.0
- `auditor` 4.1.0
- `bugfixer` 1.7.0
- `evolver` 1.2.1
- `explainer` 1.0.0
- `dev-pdca` 1.5.1
