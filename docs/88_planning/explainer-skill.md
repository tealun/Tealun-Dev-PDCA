# 规划：新增技能 explainer

状态：已实现并实测（Tiko.day，全局导览 + 新建任务追踪；178 处路径引用全部存在，按 12 处反馈迭代）· 2026-11-02

## 1. 理解卡

- **用户**：用 AI 开发产品、但自己读不懂代码的人。
- **问题**：AI 写出的代码库对他们是黑箱：不知道由哪几块组成、点一个按钮发生了什么、改一处会牵连哪里、AI 刚才那次提交到底改了什么。
- **目标**：一个只读技能，把代码库翻译成不懂代码的人也能看懂、且每句话都能按文件路径核实的说明，存进 `docs/explainer/`，可以增量更新。
- **非目标**：不修改代码、配置或其他文档；不判定缺陷、不给严重性评级（那是 auditor）；不诊断报错（那是 bugfixer）；不做规划决策（那是 planner）。

## 2. 契约

- `done_definition`：`explainer/` 目录（SKILL.md、references/、templates/、agents/openai.yaml）与现有五个技能格式一致；接入插件清单、套件包、README（中英）、指令片段、CHANGELOG；套件包重建并通过 `--check`；在 Tiko.day 上产出全局导览和一个核心功能追踪，并据结果迭代技能至少一轮。
- `validation_method`：`python3 scripts/build_suite.py --check`；`claude plugin validate .`；frontmatter YAML 解析与长度检查；Tiko.day 产出中抽查结论的文件路径都存在、行号指向对应代码；读回所有改动文件。
- `fail_condition`：职责与现有技能重叠且无法用边界写清；套件包超出 WorkBuddy 已知限制；实测产出里出现无法用路径核实的结论。

## 3. 决策

| # | 决策 | 理由 |
|---|---|---|
| D1 | 技能名 `explainer`，版本 1.0.0，目录结构 `SKILL.md` + `references/` + `templates/` + `agents/openai.yaml` | 与现有技能一致；`templates/` 只有一层，打包时可按现有规则摊平 |
| D2 | SKILL.md 与 references 用英文写，frontmatter 描述中英混合触发词；templates 用中文 | 与现有技能写法一致；模板是产出骨架，产出默认中文 |
| D3 | 唯一可写范围是目标项目的 `docs/explainer/`；绝不改代码、配置、其他文档，不提交、不推送（除非用户明确要求） | “只读”指对代码只读；说明文档是它唯一的产物 |
| D4 | 每个结论必须带 `路径` 或 `路径:行号`；没追到的写“未找到/未核实”，不补推测 | 用户要求“不能凭空推测”；让不懂代码的人也能把结论交给别人核实 |
| D5 | 敏感区域固定五类：密钥与凭证、支付、用户数据、数据库结构、登录与权限；只写位置和变量名，绝不写出密钥的值 | 用户点名前四类；登录与权限是这四类的守门处，一并标出 |
| D6 | 产出目录：`README.md`（索引与基线）、`project-map.md`、`glossary.md`、`sensitive-areas.md`、`flows/<功能>.md`、`impact/<日期>-<主题>.md`、`changes/<日期>-<短提交号>.md` | 导览、术语、敏感区是“地图”，长期维护；追踪、影响、变更是按次生成的单页 |
| D7 | 增量更新以 git 提交号为基线：每页头部记录基线提交；更新时只看基线以来的差异，只改受影响的段落，并更新基线；无 git 时用日期加文件清单 | 支持增量而不是每次重写，且能证明“这页对应哪个版本的代码” |
| D8 | “改动影响”只给牵连范围和改动难度（低/中/高，按引用数量、是否碰敏感区、有无测试判定），不给缺陷结论；“读懂变更”发现可疑点只列为“建议交给 auditor/bugfixer 确认” | 与 auditor（有证据的缺陷与严重性）、bugfixer（症状诊断）划清边界 |
| D9 | 衔接写在 explainer 自己的描述和套件包会话规则里，不改其他五个技能 | 范围最小；其他技能的行为与版本不受影响 |
| D10 | 在 PDCA 中定位为“看懂”辅助环节，贯穿各阶段：tasker/bugfixer 动手前帮用户理解要改的地方；功能完成或审计之后刷新项目地图 | 它不属于 P/D/C/A 任何一格，硬塞会误导 |
| D11 | Mermaid：每张图不超过约 15 个节点，节点用白话命名，对应路径放在图下的表里；含特殊字符的标签加引号 | 图要给不懂代码的人看，路径堆在图里不可读 |
| D12 | 套件包 dev-pdca 升到 1.1.0，`SKILLS` 加入 explainer，入口描述和路由加入 explainer；仍守 WorkBuddy 限制（`description_zh` ≤500，当前 459，需压缩其他文字腾出空间） | 套件包必须与源码同步，CI 会检查 |

## 4. 假设

- A1：目标用户能在 Agent 里看到渲染后的 Markdown 和 Mermaid（GitHub、多数 IDE 预览可渲染）。不能渲染时图仍是可读的文本。
- A2：目标项目多数在 git 里；无 git 时退化为按日期记录。

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：Tiko.day 实测产出的每条结论路径都存在 | 脚本抽取产出里的路径逐个 `test -e`，行号抽查 | 实测阶段 |
| V2：加入 explainer 后套件包仍满足 WorkBuddy 限制 | `build_suite.py --check` 输出 | 接入阶段 |
| V3：插件清单有效 | `claude plugin validate .` | 接入阶段 |

## 6. 职责边界（与现有技能）

| 技能 | 它做 | explainer 不做 |
|---|---|---|
| planner | 决定要做什么、写权威规划文档 | 不做决策；`docs/explainer/` 是派生说明，代码与权威文档优先 |
| tasker | 改文件和状态，给证据 | 不改代码；只写 `docs/explainer/` |
| bugfixer | 复现症状、证明原因、修复 | 不诊断报错；看到症状就转 bugfixer |
| auditor | 有证据的缺陷、严重性、发布风险 | 不出缺陷结论或严重性；疑点转 auditor |
| evolver | 把验证过的教训固化为防线和台账 | 不写演进台账 |

## 7. 交付切片

1. 规划（本文）→ auditor 审计本文 → 修正。
2. 写 `explainer/`：SKILL.md、references（读码方法、白话写作与图、增量更新）、templates（7 个）、agents/openai.yaml。
3. 接入：`.claude-plugin/marketplace.json`、`scripts/build_suite.py`、`suite/dev-pdca/SKILL.md`、`README.md`、`README.en.md`、`docs/agent-instructions-snippet.md`、`AGENTS.md`、`.github/ISSUE_TEMPLATE/skill_improvement.md`、`CHANGELOG.md`；重建 `dev-pdca.zip`。同步脚本按 `*/SKILL.md` 自动发现技能，无需改。
4. 实测：开发只在本仓库进行；Tiko.day 只作为只读样本，不在其仓库写入任何文件。实测产出（按 `docs/explainer/` 结构）写到会话 scratchpad 供用户查看；按发现迭代本仓库里的技能。
5. 发布前 auditor；周期结束 evolver。

就绪结论：Ready for implementation。
