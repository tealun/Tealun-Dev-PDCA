# Changelog

本文件记录 Tealun Skills 项目层面的重要变化。单个技能的历史说明可能位于各自目录内。

## Unreleased

- `tasker` 1.9.0、`planner` 2.1.0、`evolver`、`dev-pdca` 1.2.0：吸收外部技能 delivery-no-pseudoblock 的四点（规划见 `docs/88_planning/delivery-gate.md`）。`tasker` 新增 Delivery Gate，适用于每条回复（含只读问答、状态汇报和提问）：在最后一次工具调用之后对整条草稿检查，结尾一句同样受检；回复中已判明的最优下一步在授权和范围内就先做完，不包装成“如需 / 你定 / 回头再说”；只在需要新授权、扩大范围、破坏性风险、工具拿不到的输入或属于用户的取舍时提问，不放宽 M/L 副作用确认；约束性文本去掉以动机为条件的禁止、预埋借口和自拟豁免。`tasker` 验证协议要求 Observation 写出实际看到的内容，单独的“通过”不算观察。`evolver` 写防线、`planner` 写开发指引时套用同一条规则文本检查。`dev-pdca` 会话规则要求每条回复过 Delivery Gate。
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

## 现有技能

- `planner` 2.1.0
- `tasker` 1.9.0
- `auditor` 4.1.0
- `bugfixer` 1.6.1
- `evolver` 当前技能文件未声明版本
- `explainer` 1.0.0
- `dev-pdca` 1.2.0
